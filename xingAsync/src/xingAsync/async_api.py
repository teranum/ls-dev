import os, asyncio, ctypes, time, win32gui, win32api
from .models import AccountInfo, ResponseData
from .native import XING_MSG, RECV_FLAG, MSG_PACKET, RECV_PACKET, REAL_RECV_PACKET
from .resource import FieldSpec, ResourceManager

class XingApi:
    real_domain = b"api.ls-sec.co.kr"
    simul_domain = b"demo.ls-sec.co.kr"
    XM_MSG_BASE: int = 1024
    enc = 'euc-kr'
    default_timeout = 10

    _module = None
    _user_logined = False
    _user_id = str()
    _is_simulation = False
    _accounts: list[AccountInfo] = []
    _xing_folder = str()

    def __init__(self, xing_folder: str = ""):
        """ XingApi class """
        if not self._module:
            is_64bit = ctypes.sizeof(ctypes.c_void_p) == 8

            if not os.path.exists(xing_folder):
                import winreg as wrg
                try:
                    if is_64bit:
                        regKey = wrg.OpenKeyEx(wrg.HKEY_CLASSES_ROOT, r"WOW6432Node\\CLSID\\{7FEF321C-6BFD-413C-AA80-541A275434A1}\\InprocServer32")
                    else:
                        regKey = wrg.OpenKeyEx(wrg.HKEY_CLASSES_ROOT, r"CLSID\\{7FEF321C-6BFD-413C-AA80-541A275434A1}\\InprocServer32")
                    def_value = wrg.QueryValueEx(regKey, None)
                    wrg.CloseKey(regKey)
                    if len(def_value[0]) > 0:
                        xing_folder = os.path.dirname(def_value[0])
                except:
                    pass

            try:
                save_cur_dir = os.getcwd()
                os.chdir(xing_folder)
                if is_64bit:
                    pack_dll_path = os.path.dirname(os.path.abspath(__file__)) + "\\native" + '\\xingAPI64.dll'
                    if os.path.exists(pack_dll_path):
                        XingApi._module = ctypes.WinDLL(pack_dll_path)
                    else:
                        XingApi._module = ctypes.WinDLL(os.path.join(xing_folder, "xingAPI64.dll"))
                    self._module.ETK_ReleaseRequestData.argtypes = [ctypes.c_int] # not used
                    self._module.ETK_ReleaseMessageData.argtypes = [ctypes.c_voidp] # not used
                    self._module.ETK_Decompress.argtypes = [ctypes.c_voidp, ctypes.c_voidp, ctypes.c_int] # for decompress
                    if not self._module.XING64_Init(xing_folder.encode()):
                        XingApi._module = None
                else:
                    XingApi._module = ctypes.WinDLL(os.path.join(xing_folder, "xingAPI.dll"))
                os.chdir(save_cur_dir)
            except:
                XingApi._module = None

            XingApi._xing_folder = xing_folder

        class_name = 'XingApiClientClass-' + str(time.perf_counter_ns())
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self._window_proc
        wc.lpszClassName = class_name
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)

        self._hwnd = win32gui.CreateWindow(class_atom, class_name, 0, 100, 100, 100, 100, 0, 0, wc.hInstance, None)
        self._async_nodes: list[XingApi._asyncNode] = []
        self._res_manager = ResourceManager(self._xing_folder)
        self._last_message = str()
        self._on_message = self._xingSignal()
        self._on_realtime = self._xingSignal()

    # region properties
    @property
    def loaded(self):
        """ return True if xingAPI.dll is loaded """
        return self._module is not None

    @property
    def logined(self):
        """ return True if user logined """
        return self._user_logined

    @property
    def user_id(self):
        """ return user id """
        return self._user_id

    @property
    def is_simulation(self):
        """ return True if simulation mode """
        return self._is_simulation

    @property
    def accounts(self):
        """ return list of account numbers """
        return self._accounts

    @property
    def last_message(self):
        """ last message from XingAPI """
        return self._last_message

    @property
    def on_message(self):
        """
        메시지 핸들러 (LOGOUT, DISCONNECT ...)
        on_message(msg: str)
        """
        return self._on_message

    @property
    def on_realtime(self):
        """
        실시간 이벤트 핸들러
        on_realtime(tr_cd: str, key: str, datas: dict | list)
        """
        return self._on_realtime

    # endregion

    #region methods
    def close(self):
        """
        close XingAPI
        """
        if not self._module:
            return

        self._accounts.clear()

        if self._user_logined:
            self._module.ETK_Logout(self._hwnd)
            XingApi._user_logined = False

        if self._module.ETK_IsConnected():
            self._module.ETK_Disconnect()

    async def login(self, user_id: str, user_pwd: str, cert_pwd: str = "", server_ip:str = "") -> bool:
        """
        서버에 로그인, 성공시 True 반환, 오류시 False 반환(last_message에 오류 메시지)
        cert_pwd가 비어있으면 시뮬레이션 모드
        """
        if self.logined:
            self._last_message = "이미 로그인 되었습니다."
            return True

        if not self._module:
            self._last_message = "XingAPI.dll is not loaded"
            return False

        self._last_message = ""
        self._accounts.clear()

        XingApi._is_simulation = len(cert_pwd) == 0
        if len(server_ip) == 0:
            server_ip = self.simul_domain if self._is_simulation else self.real_domain
        if not self._module.ETK_IsConnected():
            self._module.ETK_Connect(self._hwnd, server_ip, 20001, self.XM_MSG_BASE, -1, -1)
        if self._module.ETK_IsConnected():
            ret = self._module.ETK_Login(self._hwnd, user_id.encode(self.enc), user_pwd.encode(self.enc), cert_pwd.encode(self.enc), 0, False)
            if ret:
                code_msg = ['', '']
                def callback(wparam, lparam):
                    code_msg[0] = ctypes.string_at(wparam).decode(self.enc)
                    code_msg[1] = ctypes.string_at(lparam).decode(self.enc)
                node = XingApi._asyncNode(0, callback)
                self._async_nodes.append(node)
                await node.wait()
                self._async_nodes.remove(node)
                self._last_message = f"[{code_msg[0]}] {code_msg[1]}"
                if code_msg[0] == "0000":
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

                    XingApi._user_logined = True
                    XingApi._user_id = user_id
                    return True
            else:
                self._last_message = "로그인 실패."
        else:
            err_code = self._module.ETK_GetLastError()
            self._last_message = f"[{err_code}] {self._get_error_message(err_code)}"
        self.close()
        return False

    async def request(self, tr_cd:str, in_datas:str, cont_yn:bool = False, cont_key:str = ''):
        """
        request data to server
        """
        if not self.logined:
            self._last_message = "로그인 후 사용 가능합니다."
            return None

        res_info = self._res_manager.get(tr_cd)
        if res_info is None:
            self._last_message = "자원 정보를 찾을 수 없습니다."
            return None

        if not res_info.is_func:
            self._last_message = "실시간 요청은 realtime 함수를 이용하세요."
            return None

        response = ResponseData()
        response.tr_cd = tr_cd
        response.res = res_info

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
            correct_in_block_dict = {}

            def get_correct_field_value(field: FieldSpec, value: object):
                # return value, error
                size = field.size
                if size == 0: return value, ''
                str_val = ''
                if field.var_type == FieldSpec.VarType.STRING:
                    if value is None:
                        str_val = ''
                    else:
                        str_val = str(value)
                    if len(str_val) > size:
                        return str_val, f'자리수 초과, 최대 {size}자리'
                    return str_val.ljust(size), ''
                if field.var_type == FieldSpec.VarType.INT:
                    if value is None:
                        return '0'.rjust(size), ''
                    if isinstance(value, str):
                        str_val = str(value)
                    else:
                        try:
                            str_val = str(int(value))
                        except:
                            return str(value), '입력 타입 오류'
                    if len(str_val) > size:
                        return str_val, f'자리수 초과, 최대 {size}자리'
                    return str_val.rjust(size, '0'), ''
                if field.var_type == FieldSpec.VarType.FLOAT:
                    flag_B = res_info.headtype == 'B'
                    if flag_B:
                        if value is None:
                            str_val = '0'
                        else:
                            try:
                                str_val = str(float(value))
                            except:
                                return str(value), '입력 타입 오류'
                        if '.' not in str_val:
                            str_val += '.'
                            str_val += '0' * field.dot_size
                        else:
                            dot_pos = str_val.index('.')
                            dot_len = len(str_val) - dot_pos - 1
                            if dot_len > field.dot_size:
                                str_val = str_val[:dot_pos + field.dot_size + 1]
                            else:
                                str_val += '0' * (field.dot_size - dot_len)
                        if len(str_val) > size:
                            return str_val, f'자리수 초과, 최대 {size}자리'
                        return str_val.rjust(size, '0'), ''
                    if value is None:
                        str_val = '0'
                    else:
                        try:
                            str_val = str(float(value))
                        except:
                            return str(value), '입력 타입 오류'
                    if '.' not in str_val:
                        str_val += '0' * field.dot_size
                    else:
                        dot_pos = str_val.index('.')
                        dot_len = len(str_val) - dot_pos - 1
                        if dot_len > field.dot_size:
                            str_val = str_val[:dot_pos + field.dot_size]
                        else:
                            str_val += '0' * (field.dot_size - dot_len)
                    if len(str_val) > size:
                        return str_val, f'자리수 초과, 최대 {size}자리'
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
                        self._last_message = f"[{field.name}] {error}"
                        return None
                    aligned_in_block_datas[i] = str_val
                    correct_in_block_dict[field.name] = str_val.strip()
            elif isinstance(in_datas, list):
                indata_count = len(in_datas)
                for i in range(in_block_field_count):
                    field = in_block.fields[i]
                    if i < indata_count:
                        obj_val = in_datas[i]
                    else:
                        obj_val = None
                    str_val, error = get_correct_field_value(field, obj_val)
                    if len(error) > 0:
                        self._last_message = f"[{field.name}] {error}"
                        return None
                    aligned_in_block_datas[i] = str_val
                    correct_in_block_dict[field.name] = str_val.strip()
            else:
                self._last_message = "입력 타입 오류"
                return None

            response.body[in_block.name] = correct_in_block_dict

            for i in range(in_block_field_count):
                size = in_block.fields[i].size
                enc_val = aligned_in_block_datas[i].encode(self.enc)
                if len(enc_val) > size:
                    enc_val = enc_val[:size]
                indata_line += enc_val
                if res_info.is_attr:
                    indata_line += b" "
        elif in_blocks_count == 2:
            if response.tr_cd == 'o3127': # 해외선물옵션관심종목조회(o3127)-API용
                # 입력 포멧: "F선물코드1, F선물코드2, O옵션코드1, O옵션코드2..."
                if isinstance(in_datas, list):
                    mktgb_symbols = []
                    for in_data in in_datas:
                        if len(in_data) > 2:
                            mktgb: str = in_data[0]
                            symbol = in_data[1:]
                            if mktgb in ['F', 'O']:
                                mktgb_symbols.append((mktgb, symbol))
                                continue
                        self._last_message = "입력 데이터 형식 오류"
                        return None
                    array_len = len(mktgb_symbols)
                    if array_len == 0:
                        self._last_message = "입력 데이터 형식 오류"
                        return None
                    str_array_len = str(array_len).rjust(4, '0')
                    response.body[res_info.in_blocks[0].name] = {'nrec':str_array_len}
                    o3127InBlock1 = []
                    indata_line = b""
                    indata_line += str_array_len.encode(self.enc)
                    if res_info.is_attr:
                        indata_line += b" "
                    for mktgb, symbol in mktgb_symbols:
                        indata_line += mktgb.encode(self.enc)
                        if res_info.is_attr:
                            indata_line += b" "
                        aligned_symbol = symbol.ljust(16, ' ')
                        indata_line += aligned_symbol.encode(self.enc)
                        if res_info.is_attr:
                            indata_line += b" "
                        o3127InBlock1.append({'mktgb':mktgb, 'symbol':aligned_symbol.strip()})
                    response.body[res_info.in_blocks[1].name] = o3127InBlock1
                else:
                    self._last_message = "invalid inputs type"
                    return None
            else:
                self._last_message = "현재 버전에서 지원하지 않습니다."
                return None
        elif in_blocks_count > 2:
            self._last_message = "자원정보 inblock개수가 2이상입니다, 현재버전 지원 불가."
            return None
        else:
            self._last_message = "자원정보에 inblock이 없습니다, 현재버전 지원 불가."
            return None

        self._last_message = ""
        start_time = time.perf_counter_ns()
        if tr_cd in ["t1857", "ChartIndex", "ChartExcel"]:
            nRqID = self._module.ETK_RequestService(self._hwnd, tr_cd.encode(self.enc), indata_line)
        else:
            nRqID = self._module.ETK_Request(self._hwnd, tr_cd.encode(self.enc), indata_line, len(indata_line), cont_yn, cont_key.encode(self.enc), self.default_timeout)
        response.id = nRqID
        if response.id < 0:
            self._last_message = f"[{response.id}] {self._get_error_message(response.id)}"
            return None
        def callback(wparam, lparam):
            if wparam in [RECV_FLAG.MESSAGE_DATA, RECV_FLAG.SYSTEM_ERROR_DATA]:
                unpack_result = ctypes.cast(lparam, ctypes.POINTER(MSG_PACKET)).contents
                response.rsp_cd = unpack_result.szMsgCode.decode(self.enc).strip()
                response.rsp_msg = ctypes.string_at(unpack_result.szMessageData).decode(self.enc).strip()
                try:
                    num_code = int(response.rsp_cd)
                    if num_code < 0:
                        response.id = num_code
                except:
                    response.id = -1
            elif wparam == RECV_FLAG.REQUEST_DATA:
                unpack_result = ctypes.cast(lparam, ctypes.POINTER(RECV_PACKET)).contents
                response.cont_yn = unpack_result.cCont == b'1'
                response.cont_key = unpack_result.szContKey.decode(self.enc)
                nDataLength = unpack_result.nDataLength
                lpData = unpack_result.lpData
                if res_info.headtype == "A":
                    out_block_name = unpack_result.szBlockName.decode(self.enc).strip()
                    out_block = next((x for x in out_blocks if x.name == out_block_name), None)
                    if out_block is not None:
                        if out_block.record_size == 0:
                            response.body[out_block.name] = ctypes.string_at(lpData, nDataLength).decode(self.enc, errors="ignore").strip()
                        else:
                            if res_info.compressable and out_block.is_occurs:
                                if response.body.get(in_blocks[0].name)['comp_yn'] == 'Y':
                                    rec_count = response.body.get(out_blocks[0].name)['rec_count']
                                    target_size = rec_count * out_block.record_size
                                    buffer = ctypes.create_string_buffer(target_size)
                                    new_pointer = ctypes.cast(buffer, ctypes.c_void_p).value
                                    nDataLength = self._module.ETK_Decompress(lpData, new_pointer, nDataLength)
                                    lpData = new_pointer
                            nFrameCount = nDataLength // out_block.record_size
                            rows, cols = (nFrameCount, len(out_block.fields))
                            datas = [None] * rows
                            for i in range(rows):
                                col_datas = {}
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
                                    except:
                                        cell_data = text_data
                                    col_datas[field.name] = cell_data
                                    if res_info.is_attr:
                                        size += 1
                                    lpData += size

                                datas[i] = col_datas

                            if out_block.is_occurs:
                                response.body[out_block.name] = datas
                            else:
                                response.body[out_block.name] = datas[0]
                else:
                    for out_block in out_blocks:
                        nFrameCount = 0
                        if out_block.is_occurs:
                            if nDataLength < 5:
                                # errMsg = "수신 데이터 길이 오류."
                                break
                            str_count = ctypes.string_at(lpData, 5).decode(self.enc)
                            nFrameCount = int(str_count)
                            lpData += 5
                            nDataLength -= 5
                        else:
                            nFrameCount = 1
                        rows, cols = (nFrameCount, len(out_block.fields))
                        if nDataLength < out_block.record_size * rows:
                            # errMsg = "수신 데이터 길이 오류."
                            break
                        datas = [None] * rows
                        for i in range(rows):
                            col_datas = {}
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
                                except:
                                    cell_data = text_data
                                col_datas[field.name] = cell_data
                                if res_info.is_attr:
                                    size += 1
                                lpData += size
                                nDataLength -= size
                            datas[i] = col_datas

                        if out_block.is_occurs:
                            response.body[out_block.name] = datas
                        else:
                            response.body[out_block.name] = datas[0]

        node = XingApi._asyncNode(response.id, callback)
        self._async_nodes.append(node)
        await node.wait()
        response.elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000
        self._async_nodes.remove(node)
        if node.async_result == -902:
            self._last_message = "[-902] TIME_OUT"
            return None
        self._last_message = f"[{response.rsp_cd}] {response.rsp_msg}"
        if response.id < 0:
            return None

        return response

    def remove_service(self, tr_cd: str, data: str) -> bool:
        ret = self._module.ETK_RemoveService(self._hwnd, tr_cd.encode(self.enc), data.encode(self.enc))
        if ret < 0:
            self._last_message = f"[{ret}] {self._get_error_message(ret)}"
            return False
        self._last_message = ""
        return True

    def realtime(self, tr_cd:str, in_datas:str, advise: bool):
        """
        advise / unadvise realtime data to server
        """
        if not self.logined:
            self._last_message = "로그인 후 사용 가능합니다."
            return False

        if not advise and len(tr_cd) == 0 :
            if self._module.ETK_UnadviseWindow(self._hwnd):
                self._last_message = "모든 실시간 해제 성공."
                return True
            self._last_message = "모든 실시간 해제 실패."
            return False

        res_info = self._res_manager.get(tr_cd)
        if res_info is None:
            self._last_message = "자원 정보를 찾을 수 없습니다."
            return False

        if res_info.is_func:
            self._last_message = "실시간 요청이 아닙니다."
            return False

        in_datas = [x.strip() for x in in_datas.split(",")]
        in_datas_count = len(in_datas)
        in_blocks = res_info.in_blocks
        in_blocks_count = len(in_blocks)
        indata_line = b''
        data_unit_len = 0
        if in_blocks_count == 1:
            in_block = res_info.in_blocks[0]
            in_block_field_count = len(in_block.fields)
            if in_block_field_count > 0:
                field_inf = in_block.fields[0]
                field_size = field_inf.size
                data_unit_len = field_size
                for i in range(in_datas_count):
                    enc_val = in_datas[i].encode(self.enc)
                    enc_val = enc_val.ljust(field_size, b' ')
                    indata_line += enc_val

        if advise:
            ok = self._module.ETK_AdviseRealData(self._hwnd, tr_cd.encode(self.enc), indata_line, data_unit_len)
        else:
            ok = self._module.ETK_UnadviseRealData(self._hwnd, tr_cd.encode(self.enc), indata_line, data_unit_len)

        if not ok:
            err_code = self._get_last_error()
            self._last_message = f"[{err_code}] {self._get_error_message(err_code)}"
            return False

        self._last_message = ""
        return True

    # def advise_realtime(self, tr_cd:str, in_datas:str):
    #     return self.realtime(tr_cd, in_datas, True)

    # def unadvise_realtime(self, tr_cd:str, in_datas:str):
    #     return self.realtime(tr_cd, in_datas, False)

    def get_requests_count(self, tr_cd: str):
        """
        TR의 초당 전송 가능 횟수, Base 시간(초단위), TR의 10분당 제한 건수, 10분내 요청한 해당 TR의 총 횟수를 반환합니다.
        """
        tr_cd_b = tr_cd.encode(self.enc)
        per_sec:int = self._module.ETK_GetTRCountPerSec(tr_cd_b)
        base_sec:int = self._module.ETK_GetTRCountBaseSec(tr_cd_b)
        limit:int = self._module.ETK_GetTRCountLimit(tr_cd_b)
        requests:int = self._module.ETK_GetTRCountRequest(tr_cd_b)
        return per_sec, base_sec, limit, requests

    def set_mode(self, mode: str, value:str):
        """
        set mode
        """
        if not self._module:
            self._last_message = "XingAPI.dll is not loaded"
            return False
        self._module.ETK_SetMode(mode.encode(self.enc), value.encode(self.enc))
        return True
    #endregion

    def _get_last_error(self):
        if not self._module:
            return -1
        return self._module.ETK_GetLastError()

    def _get_error_message(self, err_code: int) -> str:
        if not self._module:
            return "XingAPI.dll is not loaded"
        buffer = ctypes.create_string_buffer(255)
        self._module.ETK_GetErrorMessage(err_code, buffer, 255)
        return buffer.value.decode(self.enc)

    def _window_proc(self, hwnd, wm_msg, wparam, lparam):
        xM: int = wm_msg - self.XM_MSG_BASE
        if xM > 0 and xM < XING_MSG.XM_LAST:
            match xM:
                case XING_MSG.XM_LOGIN:
                    hash_id = 0
                    for node in self._async_nodes:
                        if node.hash_id == hash_id:
                            node.callback(wparam, lparam)
                            node.set()
                            break

                case XING_MSG.XM_LOGOUT:
                    XingApi._user_logined = False
                    self.on_message.emit_signal('LOGOUT')

                case XING_MSG.XM_DISCONNECT:
                    XingApi._user_logined = False
                    self.on_message.emit_signal('DISCONNECT')

                case XING_MSG.XM_RECEIVE_DATA:
                    match wparam:
                        case RECV_FLAG.REQUEST_DATA:
                            hash_id = ctypes.cast(lparam, ctypes.POINTER(ctypes.c_int32)).contents.value
                            node = next((node for node in self._async_nodes if node.hash_id == hash_id), None)
                            if node:
                                node.async_evented = True
                                node.callback(wparam, lparam)

                        case RECV_FLAG.MESSAGE_DATA | RECV_FLAG.SYSTEM_ERROR_DATA:
                            hash_id = ctypes.cast(lparam, ctypes.POINTER(ctypes.c_int32)).contents.value
                            node = next((node for node in self._async_nodes if node.hash_id == hash_id), None)
                            if node:
                                node.async_evented = True
                                node.callback(wparam, lparam)
                                node.set()
                            self._module.ETK_ReleaseMessageData(lparam)
                            if wparam == RECV_FLAG.SYSTEM_ERROR_DATA:
                                self._module.ETK_ReleaseRequestData(hash_id)

                        case RECV_FLAG.RELEASE_DATA:
                            hash_id = int(lparam)
                            node = next((node for node in self._async_nodes if node.hash_id == hash_id), None)
                            if node:
                                node.async_evented = True
                                node.set()
                            self._module.ETK_ReleaseRequestData(lparam)

                case XING_MSG.XM_TIMEOUT_DATA:
                    hash_id = int(lparam)
                    node = next((node for node in self._async_nodes if node.hash_id == hash_id), None)
                    if node:
                        node.async_result = -902
                        node.set()
                    self._module.ETK_ReleaseRequestData(hash_id)

                case XING_MSG.XM_RECEIVE_LINK_DATA:
                    if wparam == RECV_FLAG.LINK_DATA:
                        self._module.ETK_ReleaseMessageData(lparam)

                case XING_MSG.XM_RECEIVE_REAL_DATA | XING_MSG.XM_RECEIVE_REAL_DATA_SEARCH | XING_MSG.XM_RECEIVE_REAL_DATA_CHART:
                    unpack_result = ctypes.cast(lparam, ctypes.POINTER(REAL_RECV_PACKET)).contents

                    szTrCode = unpack_result.szTrCode.decode(self.enc).strip()
                    szKeyData = unpack_result.szKeyData.decode(self.enc).strip()
                    nDataLength = unpack_result.nDataLength
                    pszData = unpack_result.pszData

                    if xM == XING_MSG.XM_RECEIVE_REAL_DATA_SEARCH:
                        szTrCode = "t1857"
                        real_cd = "t1857"
                    elif xM == XING_MSG.XM_RECEIVE_REAL_DATA_CHART:
                        szTrCode = f"ChartIndex-{wparam}"
                        real_cd = "ChartIndex"
                    else:
                        real_cd = szTrCode

                    res_info = self._res_manager.get(real_cd)
                    if res_info:
                        if xM in [XING_MSG.XM_RECEIVE_REAL_DATA_SEARCH, xM == XING_MSG.XM_RECEIVE_REAL_DATA_CHART]:
                            out_block = res_info.out_blocks[1]
                        else:
                            out_block = res_info.out_blocks[0]

                        if nDataLength >= out_block.record_size:
                            field_count = len(out_block.fields)
                            col_datas = {}
                            for i in range(field_count):
                                field = out_block.fields[i]
                                size = field.size
                                text_data = ctypes.string_at(pszData, size).decode(self.enc, errors="ignore").strip()
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
                                except:
                                    cell_data = text_data
                                col_datas[field.name] = cell_data
                                if res_info.is_attr:
                                    size += 1
                                pszData += size
                            self.on_realtime.emit_signal(szTrCode, szKeyData, col_datas)

            return 0

        return win32gui.DefWindowProc(hwnd, wm_msg, wparam, lparam)

    class _xingSignal:
        def __init__(self):
            self.__slots = []
        def connect(self, slot):
            self.__slots.append(slot)
        def disconnect(self, slot):
            self.__slots.remove(slot)
        def disconnect_all(self):
            self.__slots.clear()
        def emit_signal(self, *args):
            for slot in self.__slots:
                slot(*args)

    class _asyncNode:
        def __init__(self, hashid: int, callback):
            self.__event = asyncio.Event()
            self.hash_id = hashid
            self.async_evented : bool = False
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
