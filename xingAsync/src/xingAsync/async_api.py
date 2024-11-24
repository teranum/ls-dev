import ctypes
from datetime import datetime
import os
import win32gui, win32api

from xingAsync.native import XING_MSG

class XingApi:
    real_domain = b"api.ls-sec.co.kr"
    simul_domain = b"demo.ls-sec.co.kr";
    XM_MSG_BASE: int = 1024

    def __init__(self, xing_folder: str = "C:\\LS_SEC\\xingAPI"):
        self.xing_folder = xing_folder
        full_path = os.path.join(xing_folder, "xingAPI.dll")

        try:
            self._module = ctypes.WinDLL(full_path)
        except :
            self._module = None

        # create window handle
        class_name = 'XingApiClientClass-' + str(datetime.now())
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._window_proc
        wc.lpszClassName = class_name
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        self._hwnd = win32gui.CreateWindow(class_atom, class_name, 0, 100, 100, 100, 100, 0, 0, wc.hInstance, None)

        self._server_connected = False
        self._user_logined = False
        self._is_simulation = False
        self._accounts = list()

        self.last_message = str()

        pass

    #properties
    @property
    def loaded(self):
        return self._module is not None

    @property
    def logined(self):
        return self._user_logined

    @property
    def is_simulation(self):
        return self._is_simulation

    @property
    def accounts(self):
        return self._accounts

    def close(self):
        """
        Close XingAPI
        """
        if self._module == None:
            return

        self._accounts.clear()

        if self._user_logined:
            self._module.ETK_Logout(self._hwnd)
            self._user_logined = False

        if self._server_connected:
            self._module.ETK_Disconnect()
            self._server_connected = False

    async def login(self, user_id: str, user_pwd: str, cert_pwd: str = "") -> bool:
        """
        """
        if self.logined:
            self.last_message = "Already connected"
            return True

        if self._module == None:
            self.last_message = "XingAPI.dll is not loaded"
            return False

        self.last_message = ""

        self._is_simulation = len(cert_pwd) == 0
        self._server_connected = self._module.ETK_Connect(self._hwnd, self.simul_domain if self._is_simulation else self.real_domain, 20001, self.XM_MSG_BASE, -1, -1)
        if self._server_connected:
            ret = self._module.ETK_Login(self._hwnd, user_id.encode(), user_pwd.encode(), cert_pwd.encode(), 0, False)
            if ret:
                self._user_logined = True
                return True

        self.close()
        return False


    def _window_proc(self, hwnd, wm_msg, wparam, lparam):
        xM: int = wm_msg - self.XM_MSG_BASE;
        if xM > 0 and xM < XING_MSG.XM_LAST:
            print(f"XingApi._window_proc: {xM}")
            match xM:
                case XING_MSG.XM_LOGIN:
                    pass

                case XING_MSG.XM_LOGOUT:
                    pass

                case XING_MSG.XM_DISCONNECT:
                    pass

                case XING_MSG.XM_RECEIVE_DATA:
                    pass

                case XING_MSG.XM_RECEIVE_REAL_DATA:
                    pass

                case XING_MSG.XM_TIMEOUT_DATA:
                    pass

                case XING_MSG.XM_RECEIVE_LINK_DATA:
                    pass

                case XING_MSG.XM_RECEIVE_REAL_DATA_CHART:
                    pass

                case XING_MSG.XM_RECEIVE_REAL_DATA_SEARCH:
                    pass

            return 0

        return win32gui.DefWindowProc(hwnd, wm_msg, wparam, lparam)
