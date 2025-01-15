import asyncio
import math
import ctypes
from ctypes.wintypes import HANDLE, MSG, BOOL, LPMSG, HWND, UINT, LPARAM, DWORD, LPHANDLE
from typing import Callable
from _overlapped import INVALID_HANDLE_VALUE, GetQueuedCompletionStatus
from _winapi import INFINITE, CloseHandle

WAIT_OBJECT_0 = 0
WAIT_IO_COMPLETION = 192
WAIT_TIMEOUT = 258
WAIT_FAILED = 4294967295
MWMO_ALERTABLE = 2
MWMO_INPUTAVAILABLE = 4
PM_REMOVE = 1
QS_ALLINPUT = 1279
WS_OVERLAPPED = 0
WM_QUIT = 18

LRESULT = LPARAM

def _winfn(lib, name, *args):
    fun = getattr(lib, name)
    globals()[name] = ctypes.WINFUNCTYPE(*args)(fun)

_user32 = ctypes.WinDLL("USER32")
_winfn(_user32, 'PeekMessageW', BOOL, LPMSG, HWND, UINT, UINT, UINT)
_winfn(_user32, 'TranslateMessage', BOOL, LPMSG)
_winfn(_user32, 'DispatchMessageW', LRESULT, LPMSG)
_winfn(_user32, 'MsgWaitForMultipleObjectsEx', DWORD,
       DWORD, LPHANDLE, DWORD, DWORD, DWORD)

class MsgIocpProactor(asyncio.IocpProactor):
    def __init__(self):
        super().__init__()
        self._msg = MSG()
        self._handles = (HANDLE * 1)()
        self._handles[0] = self._iocp
        self._counter = 0
        self.pre_message_hook: Callable[[MSG], bool] | None = None
        self.post_message_hook: Callable[[MSG], None] | None = None

    def _poll(self, timeout=None):
        if timeout is None:
            ms = INFINITE
        elif timeout < 0:
            raise ValueError("negative timeout")
        else:
            # MsgWaitForMultipleObjectsEx() has a resolution of 1 millisecond,
            # round away from zero to wait *at least* timeout seconds.
            ms = math.ceil(timeout * 1e3)
            if ms >= INFINITE:
                raise ValueError("timeout too big")

        while True:
            status = None
            rv = MsgWaitForMultipleObjectsEx(
                1, self._handles, ms, QS_ALLINPUT, MWMO_ALERTABLE | MWMO_INPUTAVAILABLE)
            self._counter += 1
            if rv == WAIT_OBJECT_0 or rv == WAIT_IO_COMPLETION:
                status = GetQueuedCompletionStatus(self._iocp, ms)
            elif rv == WAIT_OBJECT_0 + 1:
                while rc := PeekMessageW(self._msg, 0, 0, 0, PM_REMOVE):
                    if not self.pre_message_hook or not self.pre_message_hook(
                            self._msg):
                        TranslateMessage(self._msg)
                        DispatchMessageW(self._msg)
                        if self.post_message_hook:
                            self.post_message_hook(self._msg)
                        if self._msg.message == WM_QUIT:
                            asyncio.get_event_loop().stop()
            # elif rv == WAIT_TIMEOUT:
            #     logger.debug("MsgWaitForMultipleObjectsEx WAIT_TIMEOUT")
            # elif rv == WAIT_FAILED:
            #     logger.debug("MsgWaitForMultipleObjectsEx WAIT_FAILED")
            # else:
            #     logger.debug(f"MsgWaitForMultipleObjectsEx returned {rv}")

            if status is None:
                break

            err, transferred, key, address = status
            try:
                f, ov, obj, callback = self._cache.pop(address)
            except KeyError:
                if self._loop.get_debug():
                    self._loop.call_exception_handler({
                        'message': ('GetQueuedCompletionStatus() returned an '
                                    'unexpected event'),
                        'status': ('err=%s transferred=%s key=%#x address=%#x'
                                   % (err, transferred, key, address)),
                    })

                # key is either zero, or it is used to return a pipe
                # handle which should be closed to avoid a leak.
                if key not in (0, INVALID_HANDLE_VALUE):
                    CloseHandle(key)
                continue

            if obj in self._stopped_serving:
                f.cancel()
            # Don't call the callback if _register() already read the result or
            # if the overlapped has been cancelled
            elif not f.done():
                try:
                    value = callback(transferred, key, ov)
                except OSError as e:
                    f.set_exception(e)
                    self._results.append(f)
                else:
                    f.set_result(value)
                    self._results.append(f)
                finally:
                    f = None

        # Remove unregistered futures
        for ov in self._unregistered:
            self._cache.pop(ov.address, None)
        self._unregistered.clear()

class MsgProactorEventLoop(asyncio.ProactorEventLoop):
    def __init__(self):
        super().__init__(MsgIocpProactor())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop()
        self.close()

def run_loop(coro, forever=False):
    '''
    run coroutine and enter infinite loop if forever is True.
    '''
    with MsgProactorEventLoop() as loop:
        asyncio.set_event_loop(loop)
        if coro:
            loop.run_until_complete(coro)
        if forever:
            loop.run_forever()
