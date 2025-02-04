import os, asyncio, ctypes, time
import win32gui, win32api
from .models import AccountInfo, ResponseData
from .native import LINKDATA_RECV_MSG, XING_MSG, RECV_FLAG, MSG_PACKET, RECV_PACKET, REAL_RECV_PACKET
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
        on_realtime(tr_cd: str, key: str, datas: dict)
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
        서버에 로그인
        user_id: 사용자 ID
        user_pwd: 사용자 비밀번호
        cert_pwd: 공인인증 비밀번호 (default: "", 비어있는 경우 모의투자로 로그인)
        server_ip: 서버 IP (default: "")

        return:
        성공시 True 반환, 오류시 False 반환(last_message에 오류 메시지)
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
        else:
            server_ip = server_ip.encode(self.enc)
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

    async def request(self, tr_cd:str, in_datas:str|list|dict, cont_yn:bool = False, cont_key:str = ''):
        """
        TR 요청
        tr_cd: TR 코드
        in_datas: 입력값
        cont_yn: 연속여부 (default: False)
        cont_key: 연속키 (default: '')

        return: 성공시 ResponseData 객체, 실패시 None, last_message에 오류 메시지

        in_datas: 입력데이터 설정 방법 4가지
            1) 딕셔너리로 입력값을 설정
                inputs = { "shcode": "005930", "count": 100 }
            2) 리스트로 입력값을 설정, 이 경우 입력값의 순서가 맞아야 함
                inputs = ["005930", 100]
            3) 문자열로 입력값을 설정, ','로 구분하여 입력, 이 경우 입력값의 순서가 맞아야 함
                inputs = "005930,100"
            4) 다중입력블럭 경우 딕셔너리로 구분하여 설정
                ex) t1104: 주식현재가시세메모, (삼성전자 고가, 저가, 5이평, 20이평 가져오기)
                inputs = {
                    "t1104InBlock": {
                        "code": "005930",    # 종목코드
                        "nrec": "4",         # 건수
                    },
                    "t1104InBlock1": [
                        {"indx": "0", "gubn": "1", "dat1": "2", "dat2": "1"}, 
                        {"indx": "1", "gubn": "1", "dat1": "3", "dat2": "1"}, 
                        {"indx": "2", "gubn": "4", "dat1": "1", "dat2": "5"}, 
                        {"indx": "3", "gubn": "4", "dat1": "1", "dat2": "20"}, 
                    ],
                }
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

        in_blocks = res_info.in_blocks
        out_blocks = res_info.out_blocks

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

        # check and order input datas
        first_inblock = in_blocks[0]
        indata_line = b''
        if isinstance(in_datas, dict) and first_inblock.name in in_datas:
            b_first = True
            for in_block in in_blocks:
                if in_block.name not in in_datas:
                    if b_first:
                        self._last_message = f"입력 데이터 오류.({in_block.name} 필요)"
                        return None
                    continue
                b_first = False
                block_input = in_datas[in_block.name]
                if not in_block.is_occurs:
                    if not isinstance(block_input, dict):
                        self._last_message = f"입력 데이터 타입 오류({in_block.name}). dict입력 필요"
                        return None
                    dict_in_block_data = dict()
                    for field in in_block.fields:
                        str_val, error = get_correct_field_value(field, block_input.get(field.name))
                        if len(error) > 0:
                            self._last_message = f"[{field.name}] {error}"
                            return None
                        indata_line += str_val.encode(self.enc)
                        if res_info.is_attr:
                            indata_line += b" "
                        dict_in_block_data[field.name] = str_val.strip()
                    response.body[in_block.name] = dict_in_block_data
                else:
                    if not isinstance(block_input, list):
                        self._last_message = f"입력 데이터 타입 오류({in_block.name}). list입력 필요"
                        return None
                    list_inblock_datas = []
                    for record_input in block_input:
                        if not isinstance(record_input, dict):
                            self._last_message = f"입력 데이터 타입 오류({in_block.name}). list[dict]입력 필요"
                            return None
                        dict_in_block_data = dict()
                        for field in in_block.fields:
                            str_val, error = get_correct_field_value(field, record_input.get(field.name))
                            if len(error) > 0:
                                self._last_message = f"[{field.name}] {error}"
                                return None
                            indata_line += str_val.encode(self.enc)
                            if res_info.is_attr:
                                indata_line += b" "
                            dict_in_block_data[field.name] = str_val.strip()
                        list_inblock_datas.append(dict_in_block_data)
                    response.body[in_block.name] = list_inblock_datas
        else:
            # input reorder
            if isinstance(in_datas, str):
                in_datas = [x.strip() for x in in_datas.split(",")]

            if isinstance(in_datas, dict):
                if len(in_blocks) != 1:
                    self._last_message = "다중 블록입력은 딕셔너리로 구분하여 입력."
                    return None
                list_datas = []
                for field in in_blocks[0].fields:
                    if field.name in in_datas:
                        list_datas.append(in_datas[field.name])
                    else:
                        list_datas.append(None)
                in_datas = list_datas

            if not isinstance(in_datas, list):
                self._last_message = "입력 데이터 타입 오류."
                return None

            in_datas_count = len(in_datas)
            in_datas_index = 0

            for in_block in in_blocks:
                list_inblock_datas = []
                while True:
                    correct_in_block_dict = {}
                    for field in in_block.fields:
                        if in_datas_index < in_datas_count:
                            obj_val = in_datas[in_datas_index]
                        else:
                            obj_val = None
                        str_val, error = get_correct_field_value(field, obj_val)
                        if len(error) > 0:
                            self._last_message = f"[{field.name}] {error}"
                            return None
                        indata_line += str_val.encode(self.enc)
                        correct_in_block_dict[field.name] = str_val.strip()
                        if res_info.is_attr:
                            indata_line += b" "
                        in_datas_index += 1
                    if not in_block.is_occurs:
                        response.body[in_block.name] = correct_in_block_dict
                        break
                    list_inblock_datas.append(correct_in_block_dict)
                    if in_datas_index >= in_datas_count:
                        break
                if in_block.is_occurs and len(list_inblock_datas) > 0:
                    response.body[in_block.name] = list_inblock_datas

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
                            response.body[out_block.name] = {out_block.fields[0].name : ctypes.string_at(lpData, nDataLength).decode(self.enc, errors="ignore").strip()}
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
                                    text_data = ctypes.string_at(lpData, size).rstrip(b'\0 ').decode(self.enc, errors="ignore").strip()
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
                            str_count = ctypes.string_at(lpData, 5).rstrip(b'\0').decode(self.enc)
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
                                text_data = ctypes.string_at(lpData, size).rstrip(b'\0 ').decode(self.enc, errors="ignore").strip()
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

        self._last_message = ""
        is_service = tr_cd in ["t1857", "ChartIndex", "ChartExcel"]
        response.request_time = time.time()
        start_time = time.perf_counter_ns()
        if is_service:
            nRqID = self._module.ETK_RequestService(self._hwnd, tr_cd.encode(self.enc), indata_line)
        else:
            nRqID = self._module.ETK_Request(self._hwnd, tr_cd.encode(self.enc), indata_line, len(indata_line), cont_yn, cont_key.encode(self.enc), self.default_timeout)
        response.id = nRqID
        if response.id < 0:
            self._last_message = f"[{response.id}] {self._get_error_message(response.id)}"
            return None

        node = XingApi._asyncNode(response.id, callback)
        self._async_nodes.append(node)
        await node.wait()
        response.elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000 # ms: client -> api -> server -> api-> get_data -> client
        self._async_nodes.remove(node)
        if node.async_result == -902:
            self._last_message = "[-902] TIME_OUT"
            return None
        self._last_message = f"[{response.rsp_cd}] {response.rsp_msg}"
        if response.id < 0:
            return None

        return response

    def remove_service(self, tr_cd: str, data: str) -> bool:
        """
        remove service
        """
        ret = self._module.ETK_RemoveService(self._hwnd, tr_cd.encode(self.enc), data.encode(self.enc))
        if ret < 0:
            self._last_message = f"[{ret}] {self._get_error_message(ret)}"
            return False
        self._last_message = ""
        return True

    def realtime(self, tr_cd:str, in_datas:str | list[str], advise: bool):
        """
        실시간 등록/해제
        return 성공시 True, 실패시 False, last_message에 오류 메시지

        ex1) realtime('S3_', '005930', True)
        ex2) realtime('S3_', '005930,000660', True)
        ex3) realtime('S3_', ['005930', '000660'], True)
        ex4) realtime('', '', False) # remove all realtime data
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
        if isinstance(in_datas, str):
            in_datas = [x.strip() for x in in_datas.split(",")]
        in_datas_count = len(in_datas)
        in_blocks = res_info.in_blocks
        in_blocks_count = len(in_blocks)
        enc_tr_cd = tr_cd.encode(self.enc)
        if in_blocks_count == 1:
            data_unit_len = 0
            in_block = res_info.in_blocks[0]
            in_block_field_count = len(in_block.fields)
            if in_block_field_count > 0:
                field_inf = in_block.fields[0]
                field_size = field_inf.size
                data_unit_len = field_size
                for i in range(0, in_datas_count, 100):
                    indata_line = b''
                    codes = in_datas[i:i+100]
                    for code in codes:
                        enc_val = code.encode(self.enc).ljust(field_size, b' ')
                        indata_line += enc_val
                    if advise:
                        ok = self._module.ETK_AdviseRealData(self._hwnd, enc_tr_cd, indata_line, data_unit_len)
                    else:
                        ok = self._module.ETK_UnadviseRealData(self._hwnd, enc_tr_cd, indata_line, data_unit_len)
                    if not ok:
                        self._last_message = "함수요청 실패"
                        return False
                self._last_message = "함수요청 성공"
                return True

        if advise:
            ok = self._module.ETK_AdviseRealData(self._hwnd, enc_tr_cd, b'', 0)
        else:
            ok = self._module.ETK_UnadviseRealData(self._hwnd, enc_tr_cd, b'', 0)

        if not ok:
            self._last_message = "함수요청 실패"
            return False

        self._last_message = "함수요청 성공"
        return True

    def request_link_to_hts(self, link_key: str, link_data: str):
        """
        API에서 HTS로의 연동을 원할 때 요청합니다.
        [1] 종목연동
            link_key: 연동키
                &STOCK_CODE : 주식 종목코드 &ETF_CODE : ETF 종목코드
                &ELW_CODE : ELW 종목코드 &KONEX_CODE : 코넥스 종목코드
                &FREEBOARD_CODE : 프리보드 종목코드
                &KSPI_CODE : 코스피 업종 코드 &KSQI_CODE : 코스닥 업종 코드
                &FUTURE_CODE : 선물종목코드 &OPTION_CODE : 옵션종목코드
                &FUTOPT_CODE : 선물/옵션 종목코드
                &FUTSP_CODE : 선물스프레드 종목코드
                &STOCK_FUTURE_CODE : 주식 선물 종목코드
                &STOCK_OPTION_CODE : 주식 옵션 종목코드
                &STOCK_FUTOPT_CODE : 주식 선물옵션 종목코드
                &STOCK_FUTSP_CODE : 주식 선물스프레드 종목코드
                &FUTOPT_STOCK_FUTOPT_CODE : 선물옵션 & 주식 선물옵션 종목코드
                &US_CODE : 해외종목코드
                &COMMODITY_FUTOPT_CODE : 상품선물/선물옵션
                &COMMODITY_FUTURE_CODE : 상품선물
                &COMMODITY_STAR_CODE : 스타선물
                &CME_FUTURE_CODE : CME야간선물
                &EUREX_OPTION_CODE : EUREX야간옵션
                &NIGHT_FUTOPT_CODE : 야간선물옵션

            link_data: 상품별 종목코드

        [2] HTS 화면열기
            link_key: 연동키
                &OPEN_SCREEN
            link_data: HTS에서 열고자 원하는 화면번호

        """
        if not self.logined:
            self._last_message = "로그인 후 사용 가능합니다."
            return False
        if self._module.ETK_RequestLinkToHTS(self._hwnd, link_key.encode(self.enc), link_data.encode(self.enc), "".encode(self.enc)) > 0:
            return True
        self._last_message = "HTS연동 요청 실패."
        return False

    def link_from_hts(self, advise: bool):
        """
        HTS에서 API로의 연동을 등록/해지 합니다.
        """
        if not self.logined:
            self._last_message = "로그인 후 사용 가능합니다."
            return False
        if advise:
            self._module.ETK_AdviseLinkFromHTS(self._hwnd)
        else:
            self._module.ETK_UnAdviseLinkFromHTS(self._hwnd)
        return True

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
                    self._on_message.emit_signal('LOGOUT')

                case XING_MSG.XM_DISCONNECT:
                    XingApi._user_logined = False
                    self._on_message.emit_signal('DISCONNECT')

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
                        unpack_result = ctypes.cast(lparam, ctypes.POINTER(LINKDATA_RECV_MSG)).contents

                        col_datas = {}
                        col_datas["sLinkName"] = unpack_result.sLinkName.decode(self.enc).strip()
                        col_datas["sLinkData"] = unpack_result.sLinkData.decode(self.enc).strip()
                        # col_datas["sFiller"] = unpack_result.sFiller
                        self._on_realtime.emit_signal("LinkData", "", col_datas)

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
                        szTrCode = "ChartIndex"
                        IndexID = int(wparam)
                        szKeyData = f"{IndexID}"
                        real_cd = "ChartIndex"
                    else:
                        real_cd = szTrCode

                    res_info = self._res_manager.get(real_cd)
                    if res_info:
                        if xM in [XING_MSG.XM_RECEIVE_REAL_DATA_SEARCH, XING_MSG.XM_RECEIVE_REAL_DATA_CHART]:
                            out_block = res_info.out_blocks[1]
                        else:
                            out_block = res_info.out_blocks[0]

                        if nDataLength >= out_block.record_size:
                            field_count = len(out_block.fields)
                            col_datas = {}
                            for i in range(field_count):
                                field = out_block.fields[i]
                                size = field.size
                                text_data = ctypes.string_at(pszData, size).rstrip(b'\0 ').decode(self.enc, errors="ignore").strip()
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
                            self._on_realtime.emit_signal(szTrCode, szKeyData, col_datas)

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
