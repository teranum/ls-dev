#######################
# Xing API COM Wrapper
#######################
import inspect
import os
from xml.dom import NotSupportedErr
import win32com.client
import pythoncom

_com_session = None
_com_query = None
_com_code_to_real = {}
_com_package_folder = os.path.dirname(os.path.abspath(__file__))

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
    def OnRecieveLinkData(self, code): ...

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
        self._event_raised = False
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
        self._event_raised = True
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
        self._event_raised = False
        if self.com.Login(szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg):
            while not self._event_raised:
                pythoncom.PumpWaitingMessages()
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
            return self._rsp_code == "0000"
        err_code = self.GetLastError()
        self._last_message = f"[{err_code}] {self.GetErrorMessage(err_code)}"
        return False

class _XAQuery:
    def __init__(self, code):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", _XQueryEvent)
        if code:
            self.com.LoadFromResFile(f"{_com_package_folder}\\res\\{code}.res")
        self.com.OnReceiveData = self._OnReceiveData
        self.com.OnReceiveMessage = self._OnReceiveMessage
        self.com.OnReceiveChartRealData = self._OnReceiveChartRealData
        self.com.OnReceiveSearchRealData = self._OnReceiveSearchRealData

        self._last_message = str()
        self._event_raised = False
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
        raise NotSupportedErr("aleady implement construct")
    def LoadFromResFile(self, szFileName):
        raise NotSupportedErr("aleady implement construct")

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
        self._event_raised = True
        if self.OnReceiveData:
            self.OnReceiveData(code)
    def _OnReceiveMessage(self, is_system_error, code, msg):
        self._rsp_system_error = is_system_error
        self._rsp_code = code
        self._rsp_msg = msg
        if is_system_error:
            self._event_raised = True
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
        self._event_raised = False
        ret = self.com.Request(next)
        if ret < 0:
            self._rsp_code = str(ret)
            self._rsp_msg = self.GetErrorMessage(ret)
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
            return ret
        if not self.OnReceiveData:
            while not self._event_raised:
                pythoncom.PumpWaitingMessages()
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
        return ret

    def RequestService(self, code, data):
        self._event_raised = False
        ret = self.com.RequestService(code, data)
        if ret < 0:
            self._rsp_code = str(ret)
            self._rsp_msg = self.GetErrorMessage(ret)
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
            return ret
        if not self.OnReceiveData:
            while not self._event_raised:
                pythoncom.PumpWaitingMessages()
            self._last_message = f"[{self._rsp_code}] {self._rsp_msg}"
        return ret

class _XAReal:
    def __init__(self, code):
        self.com = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", _XRealEvent)
        if code:
            self.com.ResFileName = f"{_com_package_folder}\\res\\{code}.res"
        self.com.OnReceiveRealData = self._OnReceiveRealData
        self.com.OnRecieveLinkData = self._OnRecieveLinkData

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
        raise NotSupportedErr("aleady implement construct")
    def LoadFromResFile(self, szFileName):
        raise NotSupportedErr("aleady implement construct")

    def _OnReceiveRealData(self, code):
        if self.OnReceiveRealData:
            self.OnReceiveRealData(code)
    def _OnRecieveLinkData(self, link_name, data, filter):
        if self.OnRecieveLinkData:
            self.OnRecieveLinkData(link_name, data, filter)

#endregion


def XASession():
    global _com_session
    if _com_session is None:
        _com_session = _XASession()
    return _com_session

def XAQuery(code:str = ''):
    if code in ['t1857', 'ChartIndex']:
        new_query = _XAQuery(code)
        return new_query

    global _com_query
    if _com_query is None:
        _com_query = _XAQuery(code)
        return _com_query

    if not code:
        return _com_query

    path = f"{_com_package_folder}\\res\\{code}.res"
    if path != _com_query.com.ResFileName:
        _com_query.com.ResFileName = path
    return _com_query

def XAReal(code:str):
    exist_real = _com_code_to_real.get(code)
    if exist_real:
        return exist_real
    new_real = _XAReal(code)
    _com_code_to_real[code] = new_real
    return new_real
