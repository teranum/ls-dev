import os, asyncio, ctypes, win32gui, win32api
import time
from datetime import datetime
from xingAsync.models import AccountInfo, ResponseData
from xingAsync.native import XING_MSG, RECV_FLAG, MSG_PACKET, RECV_PACKET
from xingAsync.resource import FieldSpec, ResInfo, ResourceManager

class XingApi:
    real_domain = b"api.ls-sec.co.kr"
    simul_domain = b"demo.ls-sec.co.kr";
    XM_MSG_BASE: int = 1024
    enc = 'euc-kr'

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
        self._resManager = ResourceManager()

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

    def get_res_info(self, tr_cd: str):
        return self._resManager.get(tr_cd)

    def set_res_info(self, full_path: str):
        return self._resManager.set_from_filepath(full_path)

    def get_error_message(self, err_code: int) -> str:
        """
        get error message by code
        """
        if self._module == None:
            return "XingAPI.dll is not loaded"
        buffer = ctypes.create_string_buffer(255)
        self._module.ETK_GetErrorMessage(err_code, buffer, 255)
        return buffer.value.decode(self.enc)

    def get_requests_count(self, tr_cd: str):
        """ TR의 초당 전송 가능 횟수, Base 시간(초단위), TR의 10분당 제한 건수, 10분내 요청한 해당 TR의 총 횟수를 반환합니다. """
        tr_cd_b = tr_cd.encode('ansi')
        per_sec:int = self._module.ETK_GetTRCountPerSec(tr_cd_b)
        base_sec:int = self._module.ETK_GetTRCountBaseSec(tr_cd_b)
        limit:int = self._module.ETK_GetTRCountLimit(tr_cd_b)
        requests:int = self._module.ETK_GetTRCountRequest(tr_cd_b)
        return per_sec, base_sec, limit, requests

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
                self.last_message = f"로그인 서버전송에 실패하였습니다."
        else:
            err_code = self._module.ETK_GetLastError()
            self.last_message = f"[{err_code}] {self.get_error_message(err_code)}"
        self.close()
        return False

    async def request(self, tr_cd:str, in_datas:str, cont_yn:bool = False, cont_key:str = '') -> dict:
        """
        request data to server
        """
        # self._last_nRqID = -9999
        if not self.logined:
            self.last_message = "Not logined"
            return None

        res_info = self.get_res_info(tr_cd)
        if res_info is None:
            self.last_message = "자원 정보를 찾을 수 없습니다."
            return None

        if not res_info.is_func:
            self.last_message = "실시간 요청은 advise_realtime 함수를 이용하세요."
            return None

        response = ResponseData()
        response.tr_cd = tr_cd
        response.tag = res_info

        # input reorder
        if isinstance(in_datas, str):
            in_datas = [x.strip() for x in in_datas.split(",")]

        in_blocks = res_info.in_blocks
        out_blocks = res_info.out_blocks

        in_blocks_count = len(in_blocks)
        indata_line = b''
        if in_blocks_count == 1:
            in_block = res_info.in_blocks[0]
            in_block_field_count = len(in_block.fields)
            aligned_in_block_datas = [None] * in_block_field_count
            correct_in_block_dict = dict()

            def get_correct_field_value(field: FieldSpec, value: object) -> str:
                # return value, error
                size = field.size
                if size == 0: return value, ''
                size = field.size
                str_val = ''
                if field.var_type == FieldSpec.VarType.STRING:
                    if value is None:
                        str_val = ''
                    else:
                        str_val = str(value)
                    if len(str_val) > size:
                        return str_val, 'overflow'
                    return str_val.ljust(size), ''
                if field.var_type == FieldSpec.VarType.INT:
                    if value is None:
                        # 0으로 size만큼 채움
                        return '0'.rjust(size), ''
                    if isinstance(value, str):
                        str_val = str(value)
                    else:
                        try:
                            str_val = str(int(value))
                        except :
                            return str(value), 'invalid int value'
                    if len(str_val) > size:
                        return str_val, 'overflow'
                    # 문자열 앞에 0으로 채움
                    return str_val.rjust(size, '0'), ''
                if field.var_type == FieldSpec.VarType.FLOAT:
                    flag_B = res_info.headtype == 'B'
                    if flag_B:
                        # 실수: 소수점을 포함, 소수점 자리수는 dot_size
                        if value is None:
                            str_val = '0'
                        else:
                            try:
                                str_val = str(float(value))
                            except :
                                return str(value), 'invalid float value'
                        if '.' not in str_val:
                            str_val += '.'
                            # 소수점 자리수만큼 0으로 채움
                            str_val += '0' * field.dot_size
                        else:
                            # 소수점 위치
                            dot_pos = str_val.index('.')
                            # 소수점 이하 자리수
                            dot_len = len(str_val) - dot_pos - 1
                            if dot_len > field.dot_size:
                                # 소수점 이하 자리수가 dot_size보다 크면 잘라냄
                                str_val = str_val[:dot_pos + field.dot_size + 1]
                            else:
                                # 소수점 이하 자리수가 dot_size보다 작으면 0으로 채움
                                str_val += '0' * (field.dot_size - dot_len)
                        if len(str_val) > size:
                            return str_val, 'overflow'
                        return str_val.rjust(size, '0'), ''
                    else:
                        # 실수: 소수점을 포함하지 않음, 소수점 자리수는 dot_size
                        if value is None:
                            str_val = '0'
                        else:
                            try:
                                str_val = str(float(value))
                            except :
                                return str(value), 'invalid float value'
                        if '.' not in str_val:
                            # 소수점 자리수만큼 0으로 채움
                            str_val += '0' * field.dot_size
                        else:
                            # 소수점 위치
                            dot_pos = str_val.index('.')
                            # 소수점 이하 자리수
                            dot_len = len(str_val) - dot_pos - 1
                            if dot_len > field.dot_size:
                                # 소수점 이하 자리수가 dot_size보다 크면 잘라냄
                                str_val = str_val[:dot_pos + field.dot_size]
                            else:
                                # 소수점 이하 자리수가 dot_size보다 작으면 0으로 채움
                                str_val += '0' * (field.dot_size - dot_len)
                        if len(str_val) > size:
                            return str_val, 'overflow'
                        return str_val.rjust(size, '0'), ''
                return value, 'invalid type'

            if isinstance(in_datas, dict):
                for i in range(in_block_field_count):
                    field = in_block.fields[i]
                    if field.name in in_datas:
                        obj_val = in_datas[field.name]
                    else:
                        obj_val = None
                    str_val, error = get_correct_field_value(field, obj_val)
                    if len(error) > 0:
                        self.last_message = f"[{field.name}] {error}"
                        return None
                    aligned_in_block_datas[i] = str_val
                    correct_in_block_dict[field.name] = str_val.strip()
            elif isinstance(in_datas, list):
                # list
                indata_count = len(in_datas)
                for i in range(in_block_field_count):
                    field = in_block.fields[i]
                    if i < indata_count:
                        obj_val = in_datas[i]
                    else:
                        obj_val = None
                    str_val, error = get_correct_field_value(field, obj_val)
                    if len(error) > 0:
                        self.last_message = f"[{field.name}] {error}"
                        return None
                    aligned_in_block_datas[i] = str_val
                    correct_in_block_dict[field.name] = str_val.strip()
            else:
                self.last_message = "입력 데이터 형식 오류"
                return None

            response.body[in_block.name] = correct_in_block_dict

            for i in range(in_block_field_count):
                size = in_block.fields[i].size
                enc_val = aligned_in_block_datas[i].encode("ansi")
                if len(enc_val) > size:
                    enc_val = enc_val[:size]
                indata_line += enc_val
                if res_info.is_attr:
                    indata_line += b" "
        elif in_blocks_count == 2:
            # 입력 블록이 2개 이상인 경우, 따로 처리
            if response.tr_cd == 'o3127': # 해외선물옵션관심종목조회(o3127)-API용
                # 입력 포멧: "F선물코드1, F선물코드2, O옵션코드1, O옵션코드2..."
                if isinstance(in_datas, list):
                    mktgb_symbols = []
                    for in_data in in_datas:
                        if len(in_data) > 2:
                            mktgb: str = in_data[0]
                            symbol = in_data[1:]
                            if mktgb == 'F' or mktgb == 'O':
                                mktgb_symbols.append((mktgb, symbol))
                                continue
                        self.last_message = "입력 데이터 형식 오류"
                        return None
                    array_len = len(mktgb_symbols)
                    if array_len == 0:
                        self.last_message = "입력 데이터 형식 오류"
                        return None
                    response.body[res_info.in_blocks[0].name] = {'nrec':array_len}
                    o3127InBlock1 = []
                    indata_line = b""
                    indata_line += str(array_len).rjust(4, '0').encode("ansi")
                    if res_info.is_attr:
                        indata_line += b" "
                    for mktgb, symbol in mktgb_symbols:
                        indata_line += mktgb.encode("ansi")
                        if res_info.is_attr:
                            indata_line += b" "
                        indata_line += symbol.ljust(16, ' ').encode("ansi")
                        if res_info.is_attr:
                            indata_line += b" "
                        o3127InBlock1.append({'mktgb':mktgb, 'symbol':symbol})
                    response.body[res_info.in_blocks[1].name] = o3127InBlock1
                else:
                    self.last_message = "입력 데이터 형식 오류"
                    return None
            else:
                self.last_message = "현재 버전에서 지원하지 않습니다."
                return None
        elif in_blocks_count > 2:
            self.last_message = "자원정보 inblock개수가 2이상입니다, 현재버전 지원 불가."
            return None
        else:
            self.last_message = "자원정보에 inblock이 없습니다, 현재버전 지원 불가."
            return None

        self.last_message = ""
        start_time = time.perf_counter_ns()
        if tr_cd in ["t1857", "ChartIndex", "ChartExcel"]:
            # 서비스 요청
            nRqID = self._module.ETK_RequestService(self._hwnd, tr_cd.encode(self.enc), indata_line)
        else:
            # TR 요청
            nRqID = self._module.ETK_Request(self._hwnd, tr_cd.encode(self.enc), indata_line, len(indata_line), cont_yn, cont_key.encode(self.enc), self._default_timeout)
        # self._last_nRqID = nRqID
        response.id = nRqID
        response.ticks.append(time.perf_counter_ns() - start_time)
        if response.id < 0:
            self.last_message = f"[{response.id}] {self.get_error_message(response.id)}"
            return None
        def callback(wparam, lparam):
            if wparam == RECV_FLAG.RELEASE_DATA:
                pass
                # response.ticks.append(time.perf_counter_ns() - start_time)
            elif wparam in [RECV_FLAG.MESSAGE_DATA, RECV_FLAG.SYSTEM_ERROR_DATA]:
                unpack_result = ctypes.cast(lparam, ctypes.POINTER(MSG_PACKET)).contents
                response.rsp_cd = unpack_result.szMsgCode.decode(self.enc).strip()
                response.rsp_msg = ctypes.string_at(unpack_result.szMessageData).decode(self.enc).strip()
                try:
                    num_code = int(response.rsp_cd)
                    if num_code < 0:
                        response.id = num_code
                except :
                    response.id = -1;
            elif wparam == RECV_FLAG.REQUEST_DATA:
                # time_start = time.perf_counter_ns()
                # response.ticks.append(time_start - start_time)
                unpack_result = ctypes.cast(lparam, ctypes.POINTER(RECV_PACKET)).contents
                response.cont_yn = unpack_result.cCont == b'1'
                response.cont_key = unpack_result.szContKey.decode(self.enc)
                nDataLength = unpack_result.nDataLength
                lpData = unpack_result.lpData
                # response.body[unpack_result.szBlockName.decode(self.enc).strip()] = ctypes.string_at(unpack_result.lpData, unpack_result.nDataLength).decode(self.enc, "ignore")
                if res_info.headtype == "A":
                    # 해당 OutBlock 데이터 수신된다.
                    out_block_name = unpack_result.szBlockName.decode(self.enc).strip()
                    out_block = next((x for x in out_blocks if x.name == out_block_name), None)
                    if out_block is not None:
                        if out_block.record_size == 0:
                            response.body[out_block.name] = ctypes.string_at(lpData, nDataLength).decode(self.enc, errors="ignore").strip()
                        else:
                            nFrameCount = nDataLength // out_block.record_size
                            rows, cols = (nFrameCount, len(out_block.fields))
                            datas = [None] * rows
                            for i in range(rows):
                                row_datas = dict()
                                for j in range(cols):
                                    field = out_block.fields[j]
                                    size = field.size
                                    text_data = ctypes.string_at(lpData, size).rstrip(b'\0').decode(self.enc, errors="ignore").strip()
                                    text_len = len(text_data)
                                    try:
                                        if field.var_type == FieldSpec.VarType.INT:
                                            if text_len == 0:
                                                cell_data = 0
                                            else:
                                                cell_data = int(text_data)
                                        elif field.var_type == FieldSpec.VarType.FLOAT:
                                            if text_len == 0:
                                                cell_data = 0.0
                                            else:
                                                cell_data = float(text_data)
                                                if field.dot_value > 0 and '.' not in text_data:
                                                    cell_data /= field.dot_value
                                        else:
                                            cell_data = text_data
                                        pass
                                    except :
                                        cell_data = text_data
                                    row_datas[field.name] = cell_data
                                    if res_info.is_attr:
                                        size += 1
                                    lpData += size

                                datas[i] = row_datas

                            if out_block.is_occurs:
                                response.body[out_block.name] = datas
                            else:
                                response.body[out_block.name] = datas[0]
                else:
                    # 한번에 모든 OutBlock 데이터 수신된다.
                    for out_block in out_blocks:
                        nFrameCount = 0
                        if out_block.is_occurs:
                            if nDataLength < 5:
                                # errMsg = "수신 데이터 길이 오류."
                                break
                            str_count = ctypes.string_at(lpData, 5).decode('ansi')
                            nFrameCount = int(str_count)
                            lpData += 5
                            nDataLength -= 5
                        else:
                            nFrameCount = 1
                        rows, cols = (nFrameCount, len(out_block.fields))
                        datas = [None] * rows
                        if nDataLength < out_block.record_size * nFrameCount:
                            # errMsg = "수신 데이터 길이 오류."
                            break
                        for i in range(rows):
                            row_datas = dict() # [None] * cols
                            for field in out_block.fields:
                                size = field.size
                                text_data = ctypes.string_at(lpData, size).rstrip(b'\0').decode('ansi', errors="ignore").strip()
                                text_len = len(text_data)
                                try:
                                    if field.var_type == FieldSpec.VarType.INT:
                                        if text_len == 0:
                                            cell_data = 0
                                        else:
                                            cell_data = int(text_data)
                                    elif field.var_type == FieldSpec.VarType.FLOAT:
                                        if text_len == 0:
                                            cell_data = 0.0
                                        else:
                                            cell_data = float(text_data)
                                            if field.dot_value > 0 and '.' not in text_data:
                                                cell_data /= field.dot_value
                                    else:
                                        cell_data = text_data
                                except :
                                    cell_data = text_data
                                row_datas[field.name] = cell_data
                                if res_info.is_attr:
                                    size += 1
                                lpData += size
                                nDataLength -= size
                            datas[i] = row_datas

                        if out_block.is_occurs:
                            response.body[out_block.name] = datas
                        else:
                            response.body[out_block.name] = datas[0]
                # response.ticks.append(time.perf_counter_ns() - time_start)

        node = XingApi._asyncNode(response.id, callback)
        self._asyncNodes.append(node)
        await node.wait(self._default_timeout)
        response.ticks.append(time.perf_counter_ns() - start_time)
        self._asyncNodes.remove(node)
        self.last_message = f"[{response.rsp_cd}] {response.rsp_msg}"
        if response.id < 0:
            return None

        return response

    def _window_proc(self, hwnd, wm_msg, wparam, lparam):
        xM: int = wm_msg - self.XM_MSG_BASE;
        if xM > 0 and xM < XING_MSG.XM_LAST:
            # print(f"XingApi._window_proc: {xM}")
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
                            node = next((node for node in self._asyncNodes if node.hash_id == hash_id), None)
                            if node:
                                node.callback(wparam, lparam)
                                node.set()
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
