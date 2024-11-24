import os, asyncio, ctypes, win32gui, win32api
from datetime import datetime
from xingAsync.models import AccountInfo, ResponseData
from xingAsync.native import XING_MSG, RECV_FLAG, MSG_PACKET, RECV_PACKET

class XingApi:
    real_domain = b"api.ls-sec.co.kr"
    simul_domain = b"demo.ls-sec.co.kr";
    XM_MSG_BASE: int = 1024
    enc = 'euc-kr'

    class _xing_signal:
        def __init__(self):
            self.__slots = []
        def connect(self, slot):
            self.__slots.append(slot)
        def disconnect(self, slot):
            self.__slots.remove(slot)
        def disconnect(self):
            self.__slots.clear()
        def _emit(self, *args):
            for slot in self.__slots:
                slot(*args)

    def __init__(self, xing_folder: str = "C:/LS_SEC/xingAPI"):
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

        self._default_timeout = 10
        self._server_connected = False
        self._user_logined = False
        self._is_simulation = False
        self._asyncNodes: list[XingApi._asyncNode] = []
        self._accounts: list[AccountInfo] = []

        self.last_message = str()

        self.on_message = self._xing_signal()
        """
        메시지 핸들러 (서버연결 끊김, 로그아웃 등)
        on_message(msg: str)
        """

        self.on_realtime = self._xing_signal()
        """
        실시간 이벤트 핸들러
        on_realtime(tr_cd: str, key: str, datas: dict | list)
        """

        pass

    #properties
    @property
    def loaded(self):
        """ return True if XingAPI.dll is loaded """
        return self._module is not None

    @property
    def logined(self):
        """ return True if user logined """
        return self._user_logined

    @property
    def is_simulation(self):
        """ return True if simulation mode """
        return self._is_simulation

    @property
    def accounts(self):
        """ return list of account numbers """
        return self._accounts

    def close(self):
        """
        close XingAPI
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

    def get_error_message(self, err_code: int) -> str:
        """
        get error message by code
        """
        if self._module == None:
            return "XingAPI.dll is not loaded"
        buffer = ctypes.create_string_buffer(255)
        self._module.ETK_GetErrorMessage(err_code, buffer, 255)
        return buffer.value.decode(self.enc)

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
        self._accounts.clear()

        self._is_simulation = len(cert_pwd) == 0
        self._server_connected = self._module.ETK_Connect(self._hwnd, self.simul_domain if self._is_simulation else self.real_domain, 20001, self.XM_MSG_BASE, -1, -1)
        if self._server_connected:
            ret = self._module.ETK_Login(self._hwnd, user_id.encode(self.enc), user_pwd.encode(self.enc), cert_pwd.encode(self.enc), 0, False)
            if ret:
                code_msg = ['', '']
                def callback(wparam, lparam):
                    code_msg[0] = ctypes.string_at(wparam).decode(self.enc)
                    code_msg[1] = ctypes.string_at(lparam).decode(self.enc)
                    pass
                node = XingApi._asyncNode(0, callback)
                self._asyncNodes.append(node)
                await node.wait()
                self._asyncNodes.remove(node)
                self.last_message = f"[{code_msg[0]}] {code_msg[1]}"
                if code_msg[0] == "0000":
                    self.last_message = code_msg[1]
                    account_count = self._module.ETK_GetAccountListCount()
                    MAX_PATH = 255
                    buffer = ctypes.create_string_buffer(MAX_PATH)
                    for i in range(account_count):
                        account = AccountInfo()
                        self._module.ETK_GetAccountList(i, buffer, MAX_PATH)
                        account.number = buffer.value.decode(self.enc)
                        ansi_number = account.number.encode(self.enc)
                        self._module.ETK_GetAccountName(ansi_number, buffer, MAX_PATH)
                        account.name = buffer.value.decode(self.enc)
                        self._module.ETK_GetAcctDetailName(ansi_number, buffer, MAX_PATH)
                        account.detail_name = buffer.value.decode(self.enc)
                        self._module.ETK_GetAcctNickname(ansi_number, buffer, MAX_PATH)
                        account.nick_name = buffer.value.decode(self.enc)
                        if self._is_simulation:
                            account.pass_number = '0000'
                        self._accounts.append(account)

                    self._user_logined = True
                    return True
            else:
                self.last_message = "ETK_Login failed"

        self.close()
        return False

    async def request(self, tr_cd:str, in_datas:str, cont_yn:bool = False, cont_key:str = '') -> dict:
        """
        request data to server
        """
        if not self.logined:
            self.last_message = "Not logined"
            return None
        response = ResponseData()
        response.tr_cd = tr_cd
        response.nRqID = 0
        self.last_message = ""
        enc_in_datas = in_datas.encode(self.enc)
        response.nRqID = self._module.ETK_Request(self._hwnd, tr_cd.encode(self.enc), enc_in_datas, len(enc_in_datas), cont_yn, cont_key.encode(self.enc), 0)
        if response.nRqID < 0:
            self.last_message = f"[{response.nRqID}] {self.get_error_message(response.nRqID)}"
            return None
        def callback(wparam, lparam):
            if wparam in [RECV_FLAG.MESSAGE_DATA, RECV_FLAG.SYSTEM_ERROR_DATA]:
                unpack_result = ctypes.cast(lparam, ctypes.POINTER(MSG_PACKET)).contents
                response.rsp_cd = unpack_result.szMsgCode.decode(self.enc)
                response.rsp_msg = ctypes.string_at(unpack_result.szMessageData).decode(self.enc).strip()
                try:
                    num_code = int(response.rsp_cd)
                    if num_code < 0:
                        response.nRqID = num_code
                except :
                    response.nRqID = -1;
            else:
                unpack_result = ctypes.cast(lparam, ctypes.POINTER(RECV_PACKET)).contents
                response.cont_yn = unpack_result.cCont == b'1'
                response.cont_key = unpack_result.szContKey.decode(self.enc)
                response.body[unpack_result.szBlockName.decode(self.enc).strip()] = ctypes.string_at(unpack_result.lpData, unpack_result.nDataLength).decode(self.enc, "ignore").strip()


        node = XingApi._asyncNode(response.nRqID, callback)
        self._asyncNodes.append(node)
        await node.wait(self._default_timeout)
        self._asyncNodes.remove(node)
        self.last_message = f"[{response.rsp_cd}] {response.rsp_msg}"
        if response.nRqID < 0:
            return None
        return response

    def _window_proc(self, hwnd, wm_msg, wparam, lparam):
        xM: int = wm_msg - self.XM_MSG_BASE;
        if xM > 0 and xM < XING_MSG.XM_LAST:
            print(f"XingApi._window_proc: {xM}")
            match xM:
                case XING_MSG.XM_LOGIN:
                    hash_id = 0
                    for node in self._asyncNodes:
                        if node.hash_id == hash_id:
                            node.callback(wparam, lparam)
                            node.set()
                            break


                case XING_MSG.XM_LOGOUT:
                    self.on_message._emit('XM_LOGOUT')

                case XING_MSG.XM_DISCONNECT:
                    self.on_message._emit('XM_DISCONNECT')

                case XING_MSG.XM_RECEIVE_DATA:
                    match wparam:
                        case RECV_FLAG.REQUEST_DATA | RECV_FLAG.MESSAGE_DATA | RECV_FLAG.SYSTEM_ERROR_DATA:
                            hash_id = ctypes.cast(lparam, ctypes.POINTER(ctypes.c_int32)).contents.value
                            node = next((node for node in self._asyncNodes if node.hash_id == hash_id), None)
                            if node:
                                node.async_evented = True
                                node.callback(wparam, lparam)
                            if wparam == RECV_FLAG.MESSAGE_DATA or wparam == RECV_FLAG.SYSTEM_ERROR_DATA:
                                self._module.ETK_ReleaseMessageData(lparam);

                        case RECV_FLAG.RELEASE_DATA:
                            hash_id = lparam
                            for node in self._asyncNodes:
                                if node.hash_id == hash_id:
                                    node.set()
                                    break
                            self._module.ETK_ReleaseRequestData(lparam)

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

    class _asyncNode:
        def __init__(self, hashid, callback):
            self.__event = asyncio.Event()
            self.hash_id = hashid
            self.async_evented : bool = False
            self.async_code : str = ''
            self.async_msg : str = ''
            self.async_result = 0
            self.callback = callback

        def __hash__(self):
            return self.hash_id

        def __eq__(self, other):
            return self.hash_id == other.hashid

        def set(self):
            self.__event.set()

        async def wait(self, timeout=None):
            if timeout is None:
                await self.__event.wait()
                return True
            try:
                await asyncio.wait_for(self.__event.wait(), timeout)
                return True
            except asyncio.TimeoutError:
                if self.async_evented is False:
                    self.async_result = -902
                return False
