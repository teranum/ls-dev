#######################
# XingAPI COM Wrapper
#######################
import inspect
import os
import time
import win32com.client
import pythoncom
from .models import AccountInfo, ResponseData
from .resource import ResourceManager, ResInfo

#region event sink
class _XSessionEvent:
    def OnLogin(self, code, msg): ...
    def OnLogout(self): ...
    def OnDisconnect(self): ...

class _XQueryEvent:
    def OnReceiveData(self, code): ...
    def OnReceiveMessage(self, is_system_error, code, msg): ...
    def OnReceiveChartRealData(self, code): ...
    def OnReceiveSearchRealData(self, code): ...

class _XRealEvent:
    def OnReceiveRealData(self, code): ...
    def OnRecieveLinkData(self, link_name, data, filter): ...

#endregion

#region implements base class: XASession, XAQuery, XAReal
class _XASession:
    def __init__(self):
        self.com = win32com.client.DispatchWithEvents("XA_Session.XASession", _XSessionEvent)

        self.com.OnLogin = self._OnLogin
        self.com.OnLogout = self._OnLogout
        self.com.OnDisconnect = self._OnDisconnect

        self.OnLogin = None
        self.OnLogout = None
        self.OnDisconnect = None

        self._last_message = str()
        self._event_received = False
        self._rsp_code = str()
        self._rsp_msg = str()

        self_funcs = dir(self)
        for x in [x for x in inspect.getmembers(self.com._obj_, predicate=inspect.ismethod) if not x[0].startswith("_")]:
            if x[0] not in self_funcs:
                setattr(self, x[0], x[1])

    @property
    def ConnectTimeOut(self):
        return self.com.ConnectTimeOut
    @ConnectTimeOut.setter
    def ConnectTimeOut(self, val):
        self.com.ConnectTimeOut = val

    @property
    def SendPacketSize(self):
        return self.com.SendPacketSize
    @SendPacketSize.setter
    def SendPacketSize(self, val):
        self.com.SendPacketSize = val

    @property
    def last_message(self):
        '''마지막 메시지'''
        return self._last_message
    
    def _OnLogin(self, code, msg):
        self._event_received = True
        self._rsp_code = code
        self._rsp_msg = msg
        if self.OnLogin:
            self.OnLogin(code, msg)

    def _OnLogout(self):
        if self.OnLogout:
            self.OnLogout()

    def _OnDisconnect(self):
        if self.OnDisconnect:
            self.OnDisconnect()

    def Login(self, szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg):
        if self.OnLogin:
            return self.com.Login(szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg)
        self._event_received = False
        if self.com.Login(szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg):
            while not self._event_received:
                pythoncom.PumpWaitingMessages()
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
            return self._rsp_code == "0000"
        err_code = self.GetLastError()
        self._last_message = f"[{err_code}] {self.GetErrorMessage(err_code)}"
        return False

class _XAQuery:
    def __init__(self, res_info = None):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", _XQueryEvent)
        self.com.OnReceiveData = self._OnReceiveData
        self.com.OnReceiveMessage = self._OnReceiveMessage
        self.com.OnReceiveChartRealData = self._OnReceiveChartRealData
        self.com.OnReceiveSearchRealData = self._OnReceiveSearchRealData
        if res_info:
            self.com.LoadFromResFile(res_info.filepath)
        self.res_info = res_info

        self._last_message = str()
        self._event_received = False
        self._rsp_code = str()
        self._rsp_msg = str()
        self._rsp_system_error = False

        self.OnReceiveData = None
        self.OnReceiveMessage = None
        self.OnReceiveChartRealData = None
        self.OnReceiveSearchRealData = None

        # setting com metyhods to self methods
        self_funcs = dir(self)
        for x in [x for x in inspect.getmembers(self.com._obj_, predicate=inspect.ismethod) if not x[0].startswith("_")]:
            if x[0] not in self_funcs:
                setattr(self, x[0], x[1])

    @property
    def ResFileName(self):
        return self.com.ResFileName
    @ResFileName.setter
    def ResFileName(self, val):
        raise NotImplementedError("aleady implement construct")
    def LoadFromResFile(self, szFileName):
        raise NotImplementedError("aleady implement construct")

    @property
    def IsNext(self):
        return self.com.IsNext
    @property
    def ContinueKey(self):
        return self.com.ContinueKey

    @property
    def last_message(self):
        return self._last_message

    def _OnReceiveData(self, code):
        self._event_received = True
        if self.OnReceiveData:
            self.OnReceiveData(code)
    def _OnReceiveMessage(self, is_system_error, code, msg):
        self._rsp_system_error = is_system_error
        self._rsp_code = code
        self._rsp_msg = msg
        if is_system_error:
            self._event_received = True
        if self.OnReceiveMessage:
            self.OnReceiveMessage(is_system_error, code, msg)
    def _OnReceiveChartRealData(self, code):
        if self.OnReceiveChartRealData:
            self.OnReceiveChartRealData(code)
    def _OnReceiveSearchRealData(self, code):
        if self.OnReceiveSearchRealData:
            self.OnReceiveSearchRealData(code)

    @property
    def last_message(self):
        return f"[{self._rsp_code}] {self._rsp_msg}"

    @property
    def rsp_code(self):
        return self._rsp_code

    @property
    def rsp_msg(self):
        return self._rsp_msg

    @property
    def rsp_system_error(self):
        return self._rsp_system_error

    def Request(self, next: bool) -> int:
        self._event_received = False
        rqid = self.com.Request(next)
        if rqid < 0:
            self._rsp_code = str(rqid)
            self._rsp_msg = self.GetErrorMessage(rqid)
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
            return rqid
        if not self.OnReceiveData:
            while not self._event_received:
                pythoncom.PumpWaitingMessages()
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
        return rqid

    def RequestService(self, code, data):
        self._event_received = False
        rqid = self.com.RequestService(code, data)
        if rqid < 0:
            self._rsp_code = str(rqid)
            self._rsp_msg = self.GetErrorMessage(rqid)
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
            return rqid
        if not self.OnReceiveData:
            while not self._event_received:
                pythoncom.PumpWaitingMessages()
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
        return rqid

class _XAReal:
    def __init__(self, res_info = None):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", _XRealEvent)
        self.com.OnReceiveRealData = self._OnReceiveRealData
        self.com.OnRecieveLinkData = self._OnRecieveLinkData
        if res_info:
            self.com.LoadFromResFile(res_info.filepath)
        self.res_info = res_info

        self.OnReceiveRealData = None
        self.OnRecieveLinkData = None

        # setting com metyhods to self methods
        self_funcs = dir(self)
        for x in [x for x in inspect.getmembers(self.com._obj_, predicate=inspect.ismethod) if not x[0].startswith("_")]:
            if x[0] not in self_funcs:
                setattr(self, x[0], x[1])

    @property
    def ResFileName(self):
        return self.com.ResFileName
    @ResFileName.setter
    def ResFileName(self, val):
        raise NotImplementedError("aleady implement construct")
    def LoadFromResFile(self, szFileName):
        raise NotImplementedError("aleady implement construct")

    def _OnReceiveRealData(self, code):
        if self.OnReceiveRealData:
            self.OnReceiveRealData(code)
    def _OnRecieveLinkData(self, link_name, data, filter):
        if self.OnRecieveLinkData:
            self.OnRecieveLinkData(link_name, data, filter)

#endregion

# region main interface

def _singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def XASession():
    return XingCOM()._get_session()

def XAQuery(tr_cd:str):
    return XingCOM()._get_query(tr_cd)

def XAReal(tr_cd:str):
    return XingCOM()._get_real(tr_cd)

@_singleton
class XingCOM:
    real_domain = "api.ls-sec.co.kr"
    simul_domain = "demo.ls-sec.co.kr"
    def __init__(self):
        self._package_folder = os.path.dirname(os.path.abspath(__file__))
        self._session = _XASession()
        self._session.OnDisconnect = lambda: self._inner_on_message('DISCONNECT')
        self._query = _XAQuery()
        self._t1857 = None #_XAQuery("t1857")
        self._ChartIndex = None #_XAQuery("ChartIndex")
        self._real = _XAReal()
        self._code_to_real = {}
        
        self._last_message = str()
        self._logined = False
        self._is_simulation = False
        self._res_manager = ResourceManager()
        self._accounts: list[AccountInfo] = []

        self._on_message = self._xingSignal()
        self._on_realtime = self._xingSignal()

    def _get_session(self):
        return self._session

    def _get_query(self, tr_cd:str):
        if not tr_cd:
            return self._query;
        res_info = self._res_manager.get(tr_cd)
        if not res_info:
            self._last_message = f"ResInfo not found: {tr_cd}"
            return None
        if not res_info.is_func:
            self._last_message = f"Incorrect request code: {tr_cd}"
            return None
        if tr_cd in ['t1857', 'ChartIndex']:
            new_query = _XAQuery(res_info)
            # if tr_cd == 't1857':
            #     new_query.OnReceiveSearchRealData = lambda _: self._inner_on_realtime(new_query, "t1857")
            # elif tr_cd == 'ChartIndex':
            #     new_query.OnReceiveChartRealData = lambda _: self._inner_on_realtime(new_query, "ChartIndex")
            return new_query

        if res_info != self._query.res_info:
            self._query.com.ResFileName = res_info.filepath
            self._query.res_info = res_info
        return self._query

    def _get_real(self, tr_cd:str):
        if not tr_cd:
            return self._real;
        res_info = self._res_manager.get(tr_cd)
        if not res_info:
            self._last_message = f"ResInfo not found: {tr_cd}"
            return None
        if res_info.is_func:
            self._last_message = f"Incorrect realtime code: {tr_cd}"
            return None
        exist_real = self._code_to_real.get(tr_cd)
        if exist_real:
            return exist_real
        new_real = _XAReal(res_info)
        new_real.OnReceiveRealData = lambda _: self._inner_on_realtime(new_real, tr_cd)
        self._code_to_real[tr_cd] = new_real
        return new_real

    def _inner_on_message(self, msg:str):
        self._on_message.emit_signal(msg)

    def _inner_on_realtime(self, obj, tr_cd:str):
        key = ''
        datas = {}
        res_info:ResInfo = obj.res_info
        if res_info:
            if tr_cd == "t1857":
                key = obj.AlertNum
                outblock = res_info.out_blocks[1]
                for field in outblock.fields:
                    datas[field.name] = obj.GetFieldSearchRealData(outblock.name, field.name)
            elif tr_cd == "ChartIndex":
                key = obj.indexid
                outblock = res_info.out_blocks[1]
                for field in outblock.fields:
                    datas[field.name] = obj.GetFieldChartRealData(outblock.name, field.name)
            else:
                outblock = res_info.out_blocks[0]
                if len(res_info.in_blocks[0].fields) > 0:
                    key = obj.GetFieldData(outblock.name, res_info.in_blocks[0].fields[0].name)
                for field in outblock.fields:
                    datas[field.name] = obj.GetFieldData(outblock.name, field.name)
        self._on_realtime.emit_signal(tr_cd, key, datas)

    @property
    def last_message(self):
        return self._last_message

    @property
    def logined(self):
        return self._logined

    @property
    def is_simulation(self):
        return self._is_simulation

    @property
    def accounts(self):
        return self._accounts

    @property
    def on_message(self):
        return self._on_message

    @property
    def on_realtime(self):
        return self._on_realtime

    def close(self):
        if self._logined:
            self.remove_service()
            self._session.Logout()
            self._logined = False
        self._session.DisconnectServer()

    def login(self, user_id:str, user_pwd:str, cert_pwd:str = '', server_ip:str = ''):
        if self._logined:
            self._last_message = "Already logined"
            return True
        if not server_ip:
            if cert_pwd:
                server_ip = self.real_domain
            else:
                server_ip = self.simul_domain
        self._is_simulation = server_ip == self.simul_domain
        if not self._session.ConnectServer(server_ip, 20001):
            self._last_message = "ConnectServer failed"
            return False
        ok = self._session.Login(user_id, user_pwd, cert_pwd, 0, 0)
        self._last_message = self._session.last_message
        if not ok:
            return False

        self._accounts.clear()
        for i in range(self._session.GetAccountListCount()):
            account = AccountInfo()
            account.number = self._session.GetAccountList(i)
            account.name = self._session.GetAccountName(account.number)
            account.detail_name = self._session.GetAcctDetailName(account.number)
            account.nick_name = self._session.GetAcctNickname(account.number)
            self._accounts.append(account)

        self._logined = True
        return True

    def request(self, tr_cd:str, indatas:dict|str|list, next:bool = False) -> ResponseData|None:
        if not self._logined:
            self._last_message = "Not logined"
            return None
        is_service = tr_cd in ("t1857", "ChartIndex")
        if is_service:
            if tr_cd == "t1857":
                if not self._t1857:
                    self._t1857 = self._get_query(tr_cd)
                    self._t1857.OnReceiveSearchRealData = lambda _: self._inner_on_realtime(self._t1857, "t1857")
                    self._t1857.AlertNum = str()
                query = self._t1857
                if query.AlertNum:
                    query.RemoveService("t1857", query.AlertNum)
                    query.AlertNum = ""
            elif tr_cd == "ChartIndex":
                if not self._ChartIndex:
                    self._ChartIndex = self._get_query(tr_cd)
                    self._ChartIndex.OnReceiveChartRealData = lambda _: self._inner_on_realtime(self._ChartIndex, "ChartIndex")
                    self._ChartIndex.indexid = str()
                query = self._ChartIndex
                if query.indexid:
                    query.RemoveService("ChartIndex", query.indexid)
                    query.indexid = ""
        else:
            query = self._get_query(tr_cd)
        if not query:
            return None
        res_info:ResInfo = query.res_info
        if not res_info:
            self._last_message = f"No res information {tr_cd}."
            return None
        first_inblock = res_info.in_blocks[0]
        service_data = str()
        if isinstance(indatas, dict):
            if first_inblock.name in indatas:
                for block_name, block_vals in indatas.items():
                    if isinstance(block_vals, dict):
                        for key, val in block_vals.items():
                            query.SetFieldData(block_name, key, 0, val)
                    elif isinstance(block_vals, list):
                        record_count = len(block_vals)
                        query.SetBlockCount(block_name, record_count)
                        for i, record_val in enumerate(block_vals):
                            if isinstance(record_val, dict):
                                for key, val in record_val.items():
                                    query.SetFieldData(block_name, key, i, val)
            else:
                for key, val in indatas.items():
                    query.SetFieldData(first_inblock.name, key, 0, val)
        else:
            if isinstance(indatas, str):
                indatas = indatas.split(',')
            if isinstance(indatas, list):
                if is_service and len(indatas) == 1:
                    service_data = indatas[0]
                else:
                    for i, val in enumerate(indatas):
                        query.SetFieldData(first_inblock.name, first_inblock.fields[i].name, 0, val)
            else:
                self._last_message = f"Invalid data type: {type(indatas)}"
                return None
        request_time = time.time()
        start_time = time.perf_counter_ns()
        if is_service:
            rqid = query.RequestService(tr_cd, service_data)
        else:
            rqid = query.Request(next)
        self._last_message = query.last_message
        if rqid < 0:
            return None
        response = ResponseData()
        response.body = {}
        for block in res_info.out_blocks:
            if block.is_occurs:
                if res_info.compressable:
                    comp_yn = query.GetFieldData(first_inblock.name, "comp_yn", 0)
                    if comp_yn == 'Y':
                        query.Decompress(block.name)
                body = []
                for i in range(query.GetBlockCount(block.name)):
                    row = {}
                    for field in block.fields:
                        row[field.name] = query.GetFieldData(block.name, field.name, i)
                    body.append(row)
                response.body[block.name] = body
            else:
                body = {}
                for field in block.fields:
                    body[field.name] = query.GetFieldData(block.name, field.name, 0)
                response.body[block.name] = body
        response.elapsed_ms = (time.perf_counter_ns() - start_time) / 1_000_000 # ms: client -> api -> server -> api-> get_data -> client
        response.tr_cd = tr_cd
        response.cont_yn = query.IsNext
        response.cont_key = query.ContinueKey
        response.rsp_cd = query.rsp_code
        response.rsp_msg = query.rsp_msg
        response.id = rqid
        response.request_time = request_time
        response.res = res_info

        if is_service:
            if tr_cd == "t1857":
                query.AlertNum = query.GetFieldData("t1857OutBlock", "AlertNum", 0)
            elif tr_cd == "ChartIndex":
                query.indexid = query.GetFieldData("ChartIndexOutBlock", "indexid", 0)

        return response

    def remove_service(self, tr_cd: str = "", data: str = ""):
        if not self._logined:
            self._last_message = "Not logined"
            return False
        if not tr_cd:
            if self._t1857 and self._t1857.AlertNum:
                self._t1857.RemoveService("t1857", self._t1857.AlertNum)
                self._t1857.AlertNum = ""
            if self._ChartIndex and self._ChartIndex.indexid:
                self._ChartIndex.RemoveService("ChartIndex", self._ChartIndex.indexid)
                self._ChartIndex.indexid = ""
            return True
        if tr_cd == "t1857":
            if self._t1857:
                if not data:
                    data = self._t1857.AlertNum
                if data:
                    self._t1857.RemoveService("t1857", data)
                return True
        elif tr_cd == "ChartIndex":
            if self._ChartIndex:
                if not data:
                    data = self._ChartIndex.indexid
                if data:
                    self._ChartIndex.RemoveService("ChartIndex", data)
                return True
        self._last_message = f"Service not found: {tr_cd}"
        return False

    def realtime(self, tr_cd:str, datas:str|list, advise:bool):
        if not self._logined:
            self._last_message = "Not logined"
            return False
        if not tr_cd and not advise:
            # all unadvise
            for real in self._code_to_real.values():
                real.UnadviseRealData()
            return True
        real = self._get_real(tr_cd)
        if not real:
            return False
        res_info = real.res_info
        first_inblock = res_info.in_blocks[0]
        if len(first_inblock.fields) > 0:
            field_name = first_inblock.fields[0].name
            if isinstance(datas, str):
                datas = datas.split(',')
            if len(datas) > 0:
                for key in datas:
                    if advise:
                        real.SetFieldData(first_inblock.name, field_name, key)
                        real.AdviseRealData()
                    else:
                        real.UnadviseRealDataWithKey(key)
            else:
                if not advise:
                    real.UnadviseRealData()
        else:
            if advise:
                real.AdviseRealData()
            else:
                real.UnadviseRealData()
        return True

    def get_requests_count(self, tr_cd: str):
        per_sec = self._query.GetTRCountPerSec(tr_cd)
        base_sec = self._query.GetTRCountBaseSec(tr_cd)
        limit = self._query.GetTRCountLimit(tr_cd)
        requests = self._query.GetTRCountRequest(tr_cd)
        return per_sec, base_sec, limit, requests

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

# endregion
