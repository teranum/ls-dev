using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

#pragma warning disable MA0091 // Sender should be 'this' for instance events

namespace LS.XACom;

/// <summary>
/// 서버 메시지 이벤트
/// </summary>
/// <param name="Message">응답메시지</param>
public class MessageEventArgs(string Message) : EventArgs
{
    /// <summary>응답메시지</summary>
    public string Message { get; } = Message;
}

/// <summary>
/// 실시간 이벤트
/// </summary>
/// <param name="szTrCode">Tr코드</param>
public class RealtimeEventArgs(string szTrCode) : EventArgs
{
    /// <summary>Tr코드</summary>
    public string szTrCode { get; } = szTrCode;
}

/// <summary>
/// 실시간 LinkData 이벤트
/// </summary>
public class LinkDataEventArgs(string szLinkName, string szData, string szFiller) : EventArgs
{
    /// <summary>LinkName</summary>
    public string szLinkName = szLinkName;
    /// <summary>Data</summary>
    public string szData = szData;
    /// <summary>Filler</summary>
    public string szFiller = szFiller;
}

/// <summary>
/// XA_Control
/// </summary>
public class XAControl
{
    /// <summary>인스턴스</summary>
    public static XAControl Instance => _instance;
    private static readonly XAControl _instance = new XAControl();
    private readonly XASessionClass _sesssion;
    private readonly XAQueryClass _query;
    private readonly XARealClass _real;
    private Dictionary<string, XARealClass> _realDic = [];
    private XAControl()
    {
        _sesssion = new XASessionClass();
        _query = new XAQueryClass();
        _real = new XARealClass();

        Created = _sesssion.Created && _query.Created && _real.Created;
        if (!Created)
            return;

        _sesssion.OnLogin += _sesssion_OnLogin;
        _sesssion.OnLogout += _sesssion_OnLogout;
        _sesssion.OnDisconnect += _sesssion_OnDisconnect;

        _query.OnReceiveData += _query_OnReceiveData;
        _query.OnReceiveMessage += _query_OnReceiveMessage;
        _query.OnReceiveSearchRealData += _query_OnReceiveSearchRealData;
        _query.OnReceiveChartRealData += _query_OnReceiveChartRealData;

        _real.OnRecieveLinkData += _real_OnRecieveLinkData;
    }

    private void _sesssion_OnLogin(object sender, _IXASessionEvents_LoginEventArgs e)
    {
        if (_async_node.IsWaiting)
        {
            _async_node.Code = e.szCode;
            _async_node.Msg = e.szMsg;
            _async_node._async_wait.Set();
        }
    }
    private void _sesssion_OnLogout(object sender, EventArgs e)
    {
        IsLogined = false;
        OnMessageEvent?.Invoke(sender, new MessageEventArgs("Logout"));
    }
    private void _sesssion_OnDisconnect(object sender, EventArgs e)
    {
        IsLogined = false;
        OnMessageEvent?.Invoke(sender, new MessageEventArgs("Disconnect"));
    }
    private void _query_OnReceiveData(object sender, _IXAQueryEvents_ReceiveDataEventArgs e)
    {
        if (_async_node.IsWaiting)
        {
            _async_node._async_wait.Set();
        }
    }
    private void _query_OnReceiveMessage(object sender, _IXAQueryEvents_ReceiveMessageEventArgs e)
    {
        if (_async_node.IsWaiting)
        {
            _async_node.IsSystmeError = e.bIsSystemError;
            _async_node.Code = e.nMessageCode;
            _async_node.Msg = e.szMessage;

            if (e.bIsSystemError)
                _async_node._async_wait.Set();
        }
    }
    private void _query_OnReceiveSearchRealData(object sender, _IXAQueryEvents_ReceiveSearchRealDataEventArgs e)
    {
        OnRealtimeEvent?.Invoke(sender, new RealtimeEventArgs("t1857"));
    }
    private void _query_OnReceiveChartRealData(object sender, _IXAQueryEvents_ReceiveChartRealDataEventArgs e)
    {
        OnRealtimeEvent?.Invoke(sender, new RealtimeEventArgs("ChartIndex"));
    }

    private void _real_OnRecieveLinkData(object sender, _IXARealEvents_RecieveLinkDataEventArgs e)
    {
        OnLinkDataEvent?.Invoke(sender, new LinkDataEventArgs(e.szLinkName, e.szData, e.szFiller));
    }

    /// <inheritdoc cref="MessageEventArgs"/>
    public event EventHandler<MessageEventArgs> OnMessageEvent;

    /// <inheritdoc cref="RealtimeEventArgs"/>
    public event EventHandler<RealtimeEventArgs> OnRealtimeEvent;

    /// <inheritdoc cref="LinkDataEventArgs"/>
    public event EventHandler<LinkDataEventArgs> OnLinkDataEvent;

    /// <summary>Session</summary>
    public XASessionClass Session => _sesssion;
    /// <summary>Query</summary>
    public XAQueryClass Quuery => _query;

    /// <summary>COM 생성여부</summary>
    public bool Created { get; private set; }
    /// <summary>로그인 여부</summary>
    public bool IsLogined { get; private set; }
    /// <summary>마지막 메시지</summary>
    public string LastMessage { get; protected set; } = string.Empty;

    #region 비동기 확장함수 추가

    class AsyncNode()
    {
        private bool _isWaiting = false;
        public readonly ManualResetEvent _async_wait = new(initialState: false);
        public async Task<bool> WaitAsync(int rel_time = -1)
        {
            if (_isWaiting)
                return false;
            _isWaiting = true;
            var ret = await Task.Run(() => _async_wait.WaitOne(rel_time));
            _isWaiting = false;
            return ret;
        }
        public bool IsWaiting => _isWaiting;
        public bool IsSystmeError = false;
        public string Code = string.Empty;
        public string Msg = string.Empty;

        // 이벤트 콜백 정의
        public void Reset()
        {
            if (_isWaiting)
                throw new InvalidOperationException("Reset while waiting");
            _async_wait.Reset();
            IsSystmeError = false;
            Code = string.Empty;
            Msg = string.Empty;
        }
    }

    private AsyncNode _async_node = new();
    private int _async_TimeOut = 5000;
    /// <summary>비동기 타임아웃</summary>
    public int AsyncTimeOut
    {
        get => _async_TimeOut;
        set => _async_TimeOut = (value < 1000) ? 1000 : value;
    }


    /// <summary>
    /// 비동기 로그인
    /// <inheritdoc cref="XASessionClass.Login"/>
    /// </summary>
    public async Task<bool> LoginAsync(string serverIP, string szID, string szPwd, string szCertPwd, int nServerType, bool bShowCertErrDlg)
    {
        LastMessage = string.Empty;
        if (IsLogined)
        {
            LastMessage = "Already Connected";
            return true;
        }

        if (!Created)
        {
            LastMessage = "Not Created";
            return false;
        }

        if (_async_node.IsWaiting)
        {
            LastMessage = "duplicate request";
            return false;
        }

        if (!_sesssion.IsConnected())
        {
            bool ok = _sesssion.ConnectServer(serverIP, 20001);
            if (!ok)
            {
                LastMessage = "ConnectServer Fail";
                return false;
            }
        }

        _async_node.Reset();
        var ret = _sesssion.Login(szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg);
        if (ret)
        {
            if (await _async_node.WaitAsync())
            {
                if (string.Equals(_async_node.Code, "0000"))
                {
                    LastMessage = $"[{_async_node.Code}] {_async_node.Msg}";
                    IsLogined = true;
                    return true;
                }
            }
            else
                LastMessage = "LoginAsync Timeout";
        }
        else
            LastMessage = "LoginAsync Fail";
        return false;
    }

    /// <summary>로그아웃</summary>
    public void Close()
    {
        if (IsLogined)
            _sesssion.Logout();
        _sesssion.DisconnectServer();
    }

    #region Static Methods
    /// <inheritdoc cref="XASessionClass.GetLastError"/>
    public long GetLastError() => _sesssion.GetLastError();
    /// <inheritdoc cref="XASessionClass.GetErrorMessage"/>
    public string GetErrorMessage(int nErrorCode) => _sesssion.GetErrorMessage(nErrorCode);
    /// <inheritdoc cref="XASessionClass.GetServerName"/>
    public string GetCommMedia() => _sesssion.GetCommMedia();
    /// <inheritdoc cref="XASessionClass.GetETKMedia"/>
    public string GetETKMedia() => _sesssion.GetETKMedia();
    /// <inheritdoc cref="XASessionClass.GetClientIP"/>
    public string GetClientIP() => _sesssion.GetClientIP();
    /// <inheritdoc cref="XASessionClass.GetServerName"/>
    public string GetServerName() => _sesssion.GetServerName();
    /// <inheritdoc cref="XASessionClass.GetAccountListCount"/>
    public int GetAccountListCount() => _sesssion.GetAccountListCount();
    /// <inheritdoc cref="XASessionClass.GetAccountList"/>
    public string GetAccountList(int nIndex) => _sesssion.GetAccountList(nIndex);
    /// <inheritdoc cref="XASessionClass.GetAccountName"/>
    public string GetAccountName(string szAccount) => _sesssion.GetAccountName(szAccount);
    /// <inheritdoc cref="XASessionClass.GetAcctDetailName"/>
    public string GetAcctDetailName(string szAccount) => _sesssion.GetAcctDetailName(szAccount);
    /// <inheritdoc cref="XASessionClass.GetAcctNickname"/>
    public string GetAcctNickname(string szAccount) => _sesssion.GetAcctNickname(szAccount);
    /// <inheritdoc cref="XASessionClass.SetMode"/>
    public bool SetMode(string szMode, string szValue) => _sesssion.SetMode(szMode, szValue);

    /// <inheritdoc cref="XAQueryClass.GetTRCountPerSec"/>
    public int GetTRCountPerSec(string szCode) => _query.GetTRCountPerSec(szCode);
    /// <inheritdoc cref="XAQueryClass.GetTRCountBaseSec"/>
    public int GetTRCountBaseSec(string szCode) => _query.GetTRCountBaseSec(szCode);
    /// <inheritdoc cref="XAQueryClass.GetTRCountRequest"/>
    public int GetTRCountRequest(string szCode) => _query.GetTRCountRequest(szCode);
    /// <inheritdoc cref="XAQueryClass.GetTRCountLimit"/>
    public int GetTRCountLimit(string szCode) => _query.GetTRCountLimit(szCode);
    /// <inheritdoc cref="XAQueryClass.GetProgramOrder"/>
    public bool GetProgramOrder() => _query.GetProgramOrder();
    /// <inheritdoc cref="XAQueryClass.SetProgramOrder"/>
    public void SetProgramOrder(bool bProgramOrder) => _query.SetProgramOrder(bProgramOrder);

    /// <inheritdoc cref="XARealClass.AdviseLinkFromHTS"/>
    public void AdviseLinkFromHTS() => _real.AdviseLinkFromHTS();
    /// <inheritdoc cref="XARealClass.UnAdviseLinkFromHTS"/>
    public void UnAdviseLinkFromHTS() => _real.UnAdviseLinkFromHTS();

    #endregion



    /// <summary>
    /// 비동기 조회
    /// <inheritdoc cref="XAQueryClass.Request"/>
    /// </summary>
    public async Task<XAQueryClass> RequestAsync(string tr_cd, object inputs, bool bNext = false)
    {
        if (!IsLogined)
        {
            LastMessage = "Not Logined";
            return null;
        }

        if (_async_node.IsWaiting)
        {
            LastMessage = "duplicate request";
            return null;
        }

        if (string.IsNullOrEmpty(tr_cd))
        {
            LastMessage = "Empty TrCode";
            return null;
        }

        if (!tr_cd.Equals(_query.GetTrCode()))
        {
            string res_path = "Res\\" + tr_cd + ".res";
            if (!_query.LoadFromResFile(res_path))
            {
                LastMessage = "LoadFromResFile Fail";
                return null;
            }
        }

        var query = _query;
        if (inputs is IDictionary dicts)
        {
            var blockNames = dicts.Keys;
            foreach (var blockName in blockNames)
            {
                var text_blockName = blockName.ToString();
                query.ClearBlockdata(text_blockName);
                var block_content = dicts[blockName];
                if (block_content is IDictionary sub_dict)
                {
                    var sub_keys = sub_dict.Keys;
                    foreach (var key in sub_keys)
                    {
                        query.SetFieldData(text_blockName, key.ToString(), 0, sub_dict[key].ToString());
                    }
                }
                else if (block_content is ICollection list)
                {
                    int nRowIndex = 0;
                    foreach (var item in list)
                    {
                        if (item is IDictionary row_content)
                        {
                            var sub_keys = row_content.Keys;
                            foreach (var key in sub_keys)
                            {
                                query.SetFieldData(text_blockName, key.ToString(), nRowIndex, row_content[key].ToString());
                            }
                        }
                        else
                        {
                            LastMessage = "Invalid Inputs";
                            return null;
                        }
                        nRowIndex++;
                    }
                }
                else
                {
                    LastMessage = "Invalid Inputs";
                    return null;
                }
            }
        }
        else
        {
            LastMessage = "Invalid Inputs";
            return null;
        }

        _async_node.Reset();
        var ret = query.Request(bNext);
        if (ret >= 0)
        {
            if (await _async_node.WaitAsync())
            {
                LastMessage = $"[{_async_node.Code}] {_async_node.Msg}";
                if (!_async_node.IsSystmeError)
                {
                    if (int.TryParse(_async_node.Code, out int code))
                    {
                        if (code >= 0 && code < 1000)
                        {
                            return query;
                        }
                    }
                }

                return null;
            }
            LastMessage = "Request Timeout";
        }
        else
        {
            LastMessage = $"[{ret}] {query.GetErrorMessage(ret)}";
        }
        return null;
    }

    /// <summary>
    /// 비동기 서비스 요청
    /// </summary>
    /// <param name="tr_cd"></param>
    /// <param name="inputs"></param>
    /// <returns></returns>
    public async Task<XAQueryClass> RequestServiceAsync(string tr_cd, object inputs)
    {
        if (!IsLogined)
        {
            LastMessage = "Not Logined";
            return null;
        }

        if (_async_node.IsWaiting)
        {
            LastMessage = "duplicate request";
            return null;
        }

        if (string.IsNullOrEmpty(tr_cd))
        {
            LastMessage = "Empty TrCode";
            return null;
        }

        var query = new XAQueryClass();
        string res_path = "Res\\" + tr_cd + ".res";
        if (!query.LoadFromResFile(res_path))
        {
            LastMessage = "LoadFromResFile Fail";
            return null;
        }
        string data = string.Empty;
        if (inputs is IDictionary dicts)
        {
            var blockNames = dicts.Keys;
            foreach (var blockName in blockNames)
            {
                var text_blockName = blockName.ToString();
                query.ClearBlockdata(text_blockName);
                var block_content = dicts[blockName];
                if (block_content is IDictionary sub_dict)
                {
                    var sub_keys = sub_dict.Keys;
                    foreach (var key in sub_keys)
                    {
                        query.SetFieldData(text_blockName, key.ToString(), 0, sub_dict[key].ToString());
                    }
                }
                else if (block_content is ICollection list)
                {
                    int nRowIndex = 0;
                    foreach (var item in list)
                    {
                        if (item is IDictionary row_content)
                        {
                            var sub_keys = row_content.Keys;
                            foreach (var key in sub_keys)
                            {
                                query.SetFieldData(text_blockName, key.ToString(), nRowIndex, row_content[key].ToString());
                            }
                        }
                        else
                        {
                            LastMessage = "Invalid Inputs";
                            return null;
                        }
                        nRowIndex++;
                    }
                }
                else
                {
                    LastMessage = "Invalid Inputs";
                    return null;
                }
            }
        }
        else if (inputs is string)
        {
            data = inputs.ToString();
        }
        else
        {
            LastMessage = "Invalid Inputs";
            return null;
        }

        query.OnReceiveChartRealData += _query_OnReceiveChartRealData;
        query.OnReceiveData += _query_OnReceiveData;
        query.OnReceiveMessage += _query_OnReceiveMessage;
        query.OnReceiveSearchRealData += _query_OnReceiveSearchRealData;

        _async_node.Reset();
        var ret = query.RequestService(tr_cd, data);
        if (ret >= 0)
        {
            if (await _async_node.WaitAsync())
            {
                LastMessage = $"[{_async_node.Code}] {_async_node.Msg}";
                if (!_async_node.IsSystmeError)
                {
                    if (int.TryParse(_async_node.Code, out int code))
                    {
                        if (code >= 0 && code < 1000)
                        {
                            return query;
                        }
                    }
                }

                return null;
            }
            LastMessage = "RequestService Timeout";
        }
        else
        {
            LastMessage = $"[{ret}] {query.GetErrorMessage(ret)}";
        }
        return null;
    }

    /// <summary>
    /// 실시간 데이터 요청
    /// </summary>
    /// <param name="tr_cd"></param>
    /// <param name="fieldName"></param>
    /// <param name="datas"></param>
    /// <returns></returns>
    public XARealClass AdviseRealData(string tr_cd, string fieldName, ICollection<string> datas)
    {
        if (!IsLogined)
        {
            LastMessage = "Not Logined";
            return null;
        }

        if (!_realDic.TryGetValue(tr_cd, out var real))
        {
            real = new XARealClass();
            if (!real.LoadFromResFile("Res\\" + tr_cd + ".res"))
            {
                LastMessage = "LoadFromResFile Fail";
                return null;
            }
            _realDic.Add(tr_cd, real);
        }

        if (datas.Count > 0)
        {
            foreach (var value in datas)
            {
                real.SetFieldData("InBlock", fieldName, value);
                real.AdviseRealData();
            }
        }
        else
        {
            real.AdviseRealData();
        }

        return real;
    }

    #endregion

}
