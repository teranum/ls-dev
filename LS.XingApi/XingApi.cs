using LS.XingApi.Native;
using System.Runtime.InteropServices;
using System.Text;

namespace LS.XingApi
{
    /// <summary>API</summary>
    public partial class XingApi
    {
        [DllImport("kernel32.dll")] private static extern IntPtr LoadLibrary(string dllToLoad);
        class WndForm : Form
        {
            public Action<IntPtr, uint, IntPtr, IntPtr>? WndProcHandler;
            protected override void WndProc(ref Message m)
            {
                base.WndProc(ref m);
                WndProcHandler?.Invoke(m.HWnd, (uint)m.Msg, m.WParam, m.LParam);
            }
        }

        enum RECEIVE_FLAGS
        {
            REQUEST_DATA = 1,
            MESSAGE_DATA = 2,
            SYSTEM_ERROR_DATA = 3,
            RELEASE_DATA = 4,
        }
        class RECV_PACKET_CLASS
        {
            public RECV_PACKET_CLASS(nint ptr)
            {
                var packet = Marshal.PtrToStructure<RECV_PACKET>(ptr);
                nRqID = packet.nRqID;
                nDataLength = packet.nDataLength;
                nTotalDataBufferSize = packet.nTotalDataBufferSize;
                nElapsedTime = packet.nElapsedTime;
                nDataMode = packet.nDataMode;
                szTrCode = ByteToString(packet.szTrCode);
                cCont = (char)packet.cCont;
                szContKey = ByteToString(packet.szContKey);
                szUserData = ByteToString(packet.szUserData);
                szBlockName = ByteToString(packet.szBlockName);
                lpData = packet.lpData;
            }
            public readonly int nRqID;                       // Requests ID
            public readonly int nDataLength;                 // 받은 데이터 크기
            public readonly int nTotalDataBufferSize;        // lpData에 할당된 크기
            public readonly int nElapsedTime;                // 전송에서 수신까지 걸린시간(1/1000초)
            public readonly int nDataMode;                   // 1:BLOCK MODE, 2:NON-BLOCK MODE
            public readonly string szTrCode;                 // AP Code
            public readonly char cCont;                      // '0' : 다음조회 없음, '1' : 다음조회 있음
            public readonly string szContKey;                // 연속키, pszData Header가 B 인 경우에만 사용
            public readonly string szUserData;               // 사용자 데이터
            public readonly string szBlockName;              // Block 명, Block Mode 일때 사용
            public readonly nint lpData;
        }
        class MSG_PACKET_CLASS
        {
            public MSG_PACKET_CLASS(nint ptr)
            {
                var packet = Marshal.PtrToStructure<MSG_PACKET>(ptr);
                nRqID = packet.nRqID;
                nIsSystemError = packet.nIsSystemError;
                szMsgCode = ByteToString(packet.szMsgCode);
                nMsgLength = packet.nMsgLength;
                lpszMessageData = PtrToStringAnsi(packet.lpszMessageData);
            }
            public readonly int nRqID;                       // Requests ID
            public readonly int nIsSystemError;              // 0:일반메시지, 1:System Error 메시지
            public readonly string szMsgCode;                // 메시지 코드
            public readonly int nMsgLength;                  // Message 길이
            public readonly string lpszMessageData;          // Message Data
        }
        class LINKDATA_RECV_MSG_CLASS
        {
            public LINKDATA_RECV_MSG_CLASS(nint ptr)
            {
                var packet = Marshal.PtrToStructure<LINKDATA_RECV_MSG>(ptr);
                sLinkName = ByteToString(packet.sLinkName);
                sLinkData = ByteToString(packet.sLinkData);
                sFiller = ByteToString(packet.sFiller);
            }
            public readonly string sLinkName;
            public readonly string sLinkData;
            public readonly string sFiller;
        }
        class RecvDataMemory
        {
            public string TrCode = "";
            public int RequestID = 0;
            public IList<BlockData> BlockTextDatas = [];
        }
        class AsyncNode(object[] objs)
        {
            public readonly int _ident_id = GetIdentId(objs);

            public static int GetIdentId(object[] objs)
            {
                int id = 0;
                for (int i = 0; i < objs.Length; i++)
                {
                    id = id * 31 + objs[i].GetHashCode();
                }
                return id;
            }

            private readonly ManualResetEvent _async_wait = new(initialState: false);
            public Action<RECEIVE_FLAGS, object>? _async_OnReceiveDataHandler = null;

            public bool _async_evented = false;
            public int _async_result = 0;
            public string _async_code = string.Empty;
            public string _async_msg = string.Empty;

            public bool Set() => _async_wait.Set();
            public Task<bool> Wait(int millisecondsTimeout = -1)
            {
                return Task.Run(() =>
                {
                    if (!_async_wait.WaitOne(millisecondsTimeout))
                    {
                        if (!_async_evented)
                            _async_result = -902;
                        return false;
                    }
                    return true;
                });
            }
        }

        readonly List<AsyncNode> _async_list = [];

        private Form? _win32Window;
        private const int WM_USER = 0x0400;
        private const int AsyncTimeOut = 10000;

        const string _real_domain = "api.ls-sec.co.kr";
        const string _simul_domain = "demo.ls-sec.co.kr";
        const int _defaultTimeOut = 30;

        /// <inheritdoc cref="MessageEventArgs"/>
        public event EventHandler<MessageEventArgs>? OnMessageEvent;

        /// <inheritdoc cref="RealtimeEventArgs"/>
        public event EventHandler<RealtimeEventArgs>? OnRealtimeEvent;

        /// <summary>
        /// 모듈이 로딩 된 경우 true
        /// </summary>
        public bool ModuleLoaded => _dll.IsLoaded;

        /// <summary>모의투자 여부</summary>
        public bool IsSimulation { get; private set; }

        /// <summary>연결 여부</summary>
        public bool Connected { get; private set; }

        /// <summary>윈도우 핸들</summary>
        public nint Handle => _win32Window?.Handle ?? IntPtr.Zero;

        /// <summary>로그인 아이디</summary>
        public string UserID { get; private set; } = string.Empty;

        /// <summary>
        /// 마지막 에러 메시지
        /// </summary>
        public string LastErrorMessage { get; private set; } = string.Empty;

        private IXingApi _dll;
        /// <summary>API객체 생성</summary>
        public XingApi(string apiFolder = "")
        {
            _dll = new IXingApi(apiFolder);
            //_moduleHandle = _dll._moduleHandle;
            //if (!string.IsNullOrEmpty(apiFolder) && Directory.Exists(apiFolder))
            //{
            //    var curDir = Environment.CurrentDirectory;
            //    Environment.CurrentDirectory = apiFolder;
            //    _moduleHandle = LoadLibrary(XingNative.XING_DLL);
            //    Environment.CurrentDirectory = curDir;
            //}
            //else
            //{
            //    _moduleHandle = LoadLibrary(XingNative.XING_DLL);

            //    if (_moduleHandle == IntPtr.Zero)
            //    {
            //        // com ProgID로 경로 찾기
            //        string progId = "XA_Session.XASession";
            //        string? com_path = GetOcxDirectoryFromProgID(progId);
            //        if (com_path is not null)
            //        {
            //            string? com_folder = Path.GetDirectoryName(com_path);
            //            if (com_folder is not null && Directory.Exists(com_folder))
            //            {
            //                var curDir = Environment.CurrentDirectory;
            //                Environment.CurrentDirectory = com_folder;
            //                _moduleHandle = LoadLibrary(Path.Combine(com_folder, "XingAPI.dll"));
            //                Environment.CurrentDirectory = curDir;
            //            }
            //        }

            //        if (_moduleHandle == IntPtr.Zero)
            //            LastErrorMessage = "모듈 로드 실패";
            //    }
            //}

            //if (_moduleHandle != IntPtr.Zero)
            //{

            //}

            //static string? GetClassIDFromProgID(string progID)
            //{
            //    var regPath = progID + @"\CLSID\";
            //    return GetDefaultRegistryValue(Registry.ClassesRoot, regPath);
            //}
            //static string? GetOcxDirectoryFromProgID(string progID)
            //{
            //    if (GetClassIDFromProgID(progID) is string classID)
            //        return GetOcxPathFromClassID(classID);
            //    return default;
            //}
            //static string? GetOcxPathFromClassID(string clsID)
            //{
            //    var regPath = @"\CLSID\" + clsID + @"\InProcServer32\";
            //    return GetDefaultRegistryValue(Registry.ClassesRoot, regPath);
            //}
            //static string? GetDefaultRegistryValue(RegistryKey rootKey, string regPath)
            //{
            //    try
            //    {
            //        using var regKey = rootKey.OpenSubKey(regPath);
            //        if (regKey != null)
            //        {
            //            if (regKey.GetValue("") is string defaultValue)
            //            {
            //                return defaultValue;
            //            }
            //        }
            //    }
            //    catch
            //    {
            //        //log error
            //    }
            //    return null;
            //}
        }

        /// <summary>
        /// 에러 메시지 반환
        /// </summary>
        /// <param name="nErrCode">에러 코드</param>
        /// <returns></returns>
        public string GetErrorMessage(int nErrCode)
        {
            switch (nErrCode)
            {
                case -900:
                    return "DLL 모듈 로드 실패.";
                case -901:
                    return "이미 작동중 입니다.";
                case -902:
                    return "타임아웃.";
                case -903:
                    return "SYSTEM ERROR.";
                case -904:
                    return "수신데이터가 없습니다.";
                case -905:
                    return "자원정보가 없습니다.";

                default:
                    break;
            }
            IXingApi.GetErrorMessage(nErrCode);
            return IXingApi.GetErrorMessage(nErrCode);
        }


        bool _login_async_processing = false;

        /// <summary>
        /// 비동기 연결 요청
        /// </summary>
        /// <param name="userId">유저 아이디</param>
        /// <param name="password">HTS 패스워드</param>
        /// <param name="certPassword">공인인증 패스워드</param>
        /// <returns>ret: 0, 연결성공, 그외 오류코드</returns>
        /// <remarks>공인인증 패스워드 없는 경우, 모의서버로 로그인</remarks>
        public async Task<(int ret, string msg)> ConnectAsync(string userId, string password, string certPassword = "")
        {
            LastErrorMessage = string.Empty;
            int nErrCode = 0;
            if (!ModuleLoaded)
            {
                nErrCode = -900; // DLL 모듈 로드 실패
                return (nErrCode, GetErrorMessage(nErrCode));
            }

            if (Connected)
            {
                return (0, "이미 로그인 되었습니다.");
            }

            UserID = userId;

            if (_login_async_processing)
            {
                nErrCode = -901; // 이미 작동중 입니다.
                return (nErrCode, GetErrorMessage(nErrCode));
            }

            // 새로운 창을 생성
            _win32Window = new WndForm()
            {
                FormBorderStyle = FormBorderStyle.FixedToolWindow,
                ShowInTaskbar = false,
                StartPosition = FormStartPosition.Manual,
                Location = new Point(-2000, -2000),
                Size = new Size(1, 1),
                WndProcHandler = WndProc,
            };

            IsSimulation = certPassword.Length == 0;

            // 먼저 연결 진행
            bool ret = IXingApi.ETK_Connect(Handle, IsSimulation ? _simul_domain : _real_domain, 20001, WM_USER, -1, -1);
            if (!ret)
            {
                nErrCode = GetLastError();
                Close();
                return (nErrCode, GetErrorMessage(nErrCode));
            }

            // 로그인 진행
            ret = IXingApi.ETK_Login(Handle, userId, password, certPassword, 0, bShowCertErrDlg: false);
            if (!ret)
            {
                nErrCode = GetLastError();
                Close();
                return (nErrCode, GetErrorMessage(nErrCode));
            }

            _login_async_processing = true;

            var newAsync = new AsyncNode(["ConnectAsync"]);
            _async_list.Add(newAsync);
            await newAsync.Wait(AsyncTimeOut);
            _async_list.Remove(newAsync);

            nErrCode = newAsync._async_result;

            _login_async_processing = false;

            if (nErrCode < 0)
            {
                Close();
                return (nErrCode, GetErrorMessage(nErrCode));
            }

            if (!newAsync._async_code.Equals("0000"))
            {
                nErrCode = -2; // 서버접속 실패
                Close();
                return (nErrCode, newAsync._async_msg.Length > 0 ? newAsync._async_msg : GetErrorMessage(nErrCode));
            }

            Connected = true;

            // 계좌 정보 조회
            _accountInfos.Clear();
            int nCount = IXingApi.ETK_GetAccountListCount();
            for (int i = 0; i < nCount; i++)
            {
                string Number = IXingApi.GetAccountList(i);
                string Name = IXingApi.GetAccountName(Number);
                string DetailName = IXingApi.GetAcctDetailName(Number);

                _accountInfos.Add(new AccountInfo(Number, Name, DetailName, IsSimulation ? "0000" : string.Empty));
            }

            var saveLoginMessage = newAsync._async_msg;

            await ResManager.InitResourceAsnc(this);

            if (LastErrorMessage.Length == 0)
                LastErrorMessage = saveLoginMessage;
            return (0, LastErrorMessage);
        }

        /// <summary>연결 해제</summary>
        public bool Close()
        {
            if (_win32Window != null)
            {
                if (Connected)
                {
                    IXingApi.ETK_Logout(Handle);
                }
                _win32Window.Close();
                _win32Window = null;
            }

            Connected = false;
            return IXingApi.ETK_Disconnect();
        }


        private int GetLastError() => IXingApi.ETK_GetLastError();
        private List<AccountInfo> _accountInfos { get; } = [];

        private static string PtrToStringAnsi(IntPtr ptr) => Marshal.PtrToStringAnsi(ptr)?.TrimEnd('\0') ?? string.Empty;
        private static string PtrToStringAnsi(IntPtr ptr, int length) => Marshal.PtrToStringAnsi(ptr, length).TrimEnd('\0');
        private void WndProc(IntPtr hwnd, uint msg, IntPtr wParam, IntPtr lParam)
        {
            // Handle messages...

            XM xM = (XM)(msg - WM_USER);

            switch (xM)
            {
                case XM.XM_DISCONNECT:
                    {
                        Connected = false;
                        OnMessageEvent?.Invoke(this, new(IsSystemError: true, "-11111", "서버연결 해제"));
                    }
                    break;
                case XM.XM_RECEIVE_DATA:
                    {
                        // 조회 TR에 대한 응답을 받았을 때 호출
                        // WPARAM: RECEIVE_FLAGS 이며 각 값에 따라 처리방식이 다릅니다
                        // LPARAM: WPARAM의 값에 따라 다릅니다.

                        RECEIVE_FLAGS receiveFlag = (RECEIVE_FLAGS)wParam.ToInt32();
                        switch (receiveFlag)
                        {
                            case RECEIVE_FLAGS.REQUEST_DATA:
                                {
                                    // LPARAM : RECV_PACKET의 메모리 주소
                                    var data = new RECV_PACKET_CLASS(lParam);

                                    int async_ident_id = AsyncNode.GetIdentId([data.nRqID]);
                                    var async_node = _async_list.Find(x => x._ident_id == async_ident_id);
                                    if (async_node is not null)
                                        async_node._async_OnReceiveDataHandler?.Invoke(receiveFlag, data);
                                    //else
                                    //    OnReceiveData?.Invoke(this, new(receiveFlag, data));
                                }
                                break;
                            case RECEIVE_FLAGS.MESSAGE_DATA:
                            case RECEIVE_FLAGS.SYSTEM_ERROR_DATA:
                                {
                                    // LPARAM : MSG_PACKET_CLASS 메모리 주소
                                    var data = new MSG_PACKET_CLASS(lParam);
                                    if (data.nRqID > 0)
                                    {
                                        int async_ident_id = AsyncNode.GetIdentId([data.nRqID]);
                                        var async_node = _async_list.Find(x => x._ident_id == async_ident_id);
                                        if (async_node is not null)
                                        {
                                            async_node._async_OnReceiveDataHandler?.Invoke(receiveFlag, data);
                                            async_node.Set();
                                            break;
                                        }
                                    }

                                    if (data.nIsSystemError == 1)
                                    {
                                        int.TryParse(data.szMsgCode, out int nMsgCode);
                                        if (nMsgCode != _nRqID_last) // 이미 요청실패로 처리된 경우는 무시
                                            OnMessageEvent?.Invoke(this, new(IsSystemError: true, data.szMsgCode, data.lpszMessageData));
                                    }
                                    else
                                    {
                                        OnMessageEvent?.Invoke(this, new(IsSystemError: false, data.szMsgCode, data.lpszMessageData));
                                    }

                                    IXingApi.ETK_ReleaseMessageData(lParam);
                                    if (receiveFlag == RECEIVE_FLAGS.SYSTEM_ERROR_DATA)
                                    {
                                        IXingApi.ETK_ReleaseRequestData(data.nRqID);
                                    }
                                }
                                break;
                            case RECEIVE_FLAGS.RELEASE_DATA:
                                {
                                    // LPARAM : 정수로 Requests ID를 의미
                                    int nRequestID = lParam.ToInt32();

                                    int async_ident_id = AsyncNode.GetIdentId([nRequestID]);
                                    var async_node = _async_list.Find(x => x._ident_id == async_ident_id);
                                    if (async_node is not null)
                                    {
                                        async_node.Set();
                                    }
                                    //else
                                    //    OnReceiveData?.Invoke(this, new(receiveFlag, nRequestID));

                                    IXingApi.ETK_ReleaseRequestData(nRequestID);
                                }
                                break;
                            default:
                                break;
                        }
                    }
                    break;
                case XM.XM_LOGIN:
                    {
                        // ETK_Login() 함수가 호출 된 후 Login 과정이 완료되었을 때 호출
                        // WPARAM: Message Code, 문자열 형태,“0000” 이면 성공, 그 외에는 실패
                        // LPARAM: Message Text
                        string szCode = PtrToStringAnsi(wParam);
                        string szMsg = PtrToStringAnsi(lParam);

                        int async_ident_id = AsyncNode.GetIdentId(["ConnectAsync"]);
                        var async_node = _async_list.Find(x => x._ident_id == async_ident_id);
                        if (async_node is not null)
                        {
                            async_node._async_code = szCode;
                            async_node._async_msg = szMsg;
                            async_node.Set();
                        }
                    }
                    break;
                case XM.XM_LOGOUT:
                    {
                        Connected = false;
                        OnMessageEvent?.Invoke(this, new(IsSystemError: true, "-11111", "로그아웃"));
                    }
                    break;
                case XM.XM_TIMEOUT_DATA:
                    {
                        // 조회 TR에 대한 응답이 Timeout 되었을 때 호출
                        // WPARAM: 사용안함
                        // LPARAM: Requests ID
                        int nRequestID = lParam.ToInt32();

                        int async_ident_id = AsyncNode.GetIdentId([nRequestID]);
                        var async_node = _async_list.Find(x => x._ident_id == async_ident_id);
                        if (async_node is not null)
                        {
                            async_node._async_result = -902;
                            async_node.Set();
                        }
                        //OnReceiveData?.Invoke(this, new(RECEIVE_FLAGS.TIME_OUT_DATA, nRequestID));
                        IXingApi.ETK_ReleaseRequestData(nRequestID);
                    }
                    break;
                case XM.XM_RECEIVE_LINK_DATA:
                    {
                        // HTS -> API로 연동을 등록하면, HTS에서 연동 정보가 발생시에 호출, 사용방식은 XM_RECEIVE_REAL_DATA 수신과 동일
                        // WPARAM: LINK_DATA
                        // LPARAM: LINKDATRRA_RECV_MSG 구조체 데이터
                        var data = new LINKDATA_RECV_MSG_CLASS(lParam);
                        //OnReceiveData?.Invoke(this, new(RECEIVE_FLAGS.LINK_DATA, data));
                        IXingApi.ETK_ReleaseMessageData(lParam);
                    }
                    break;
                case XM.XM_RECEIVE_REAL_DATA:
                // LPARAM : REAL_RECV_PACKET의 메모리 주소
                case XM.XM_RECEIVE_REAL_DATA_CHART:
                // WPARAM: 지표데이터(“ChartIndex”) TR 조회 요청 시, 조회 결과 데이터의 ChartIndexOutBlock의 indexed(고유키)
                // LPARAM: REAL_RECV_PACKET의 메모리 주소, 지표데이터(“ChartIndex”) TR 조회 요청 시, 조회 결과 데이터의 ChartIndexOutBlock1
                case XM.XM_RECEIVE_REAL_DATA_SEARCH:
                    // 종목검색(신버전API용) 실시간 데이터에 대한 응답을 받았을 때 호출, (종목검색(신버전API용)조회 시, 실시간 구분을 “1”로 했을 경우)
                    // WPARAM: 사용안함
                    // LPARAM: REAL_RECV_PACKET의 메모리 주소, 종목검색(신버전API용)(“t1857”) TR 조회 요청 시, 조회 결과 데이터의 t1857OutBlock1
                    {
                        var real_recv_packet = Marshal.PtrToStructure<REAL_RECV_PACKET>(lParam);
                        string szTrCode = ByteToString(real_recv_packet.szTrCode).Trim();
                        string szKey = ByteToString(real_recv_packet.szKeyData).Trim();
                        var trInfo = ResManager.GetResInfo(szTrCode);
                        if (trInfo is not null && trInfo.ResSpec is not null)
                        {
                            var specOutBlock = trInfo.ResSpec.OutBlocks[0];
                            byte[] bytes = new byte[real_recv_packet.nDataLength];
                            Marshal.Copy(real_recv_packet.pszData, bytes, 0, real_recv_packet.nDataLength);
                            var fileds = trInfo.ResSpec.OutBlocks;
                            IntPtr nBufferAdr = real_recv_packet.pszData;
                            int nFrameSize = specOutBlock.Fields.Sum(x => (int)x.size);
                            if (trInfo.ResSpec.is_attr) nFrameSize += specOutBlock.Fields.Count;
                            string[] realTextDatas = new string[specOutBlock.Fields.Count];
                            for (int j = 0; j < specOutBlock.Fields.Count; j++)
                            {
                                int size = (int)specOutBlock.Fields[j].size;
                                realTextDatas[j] = PtrToStringAnsi(nBufferAdr, size);
                                if (trInfo.ResSpec.is_attr) size += 1;
                                nBufferAdr += size;
                            }
                            OnRealtimeEvent?.Invoke(this, new(szTrCode, szKey, realTextDatas));
                        }
                        else
                        {
                            OnRealtimeEvent?.Invoke(this, new(szTrCode, szKey, [PtrToStringAnsi(real_recv_packet.pszData)!]));
                        }
                    }
                    break;
                default:
                    break;
            }

            return;

        }
        static string ByteToString(byte[] bytes)
        {
            return PtrToStringAnsi(Marshal.UnsafeAddrOfPinnedArrayElement(bytes, 0), bytes.Length);
        }

        /// <summary>계좌정보 리스트. (로그인 시 자동 등록 됩니다)</summary>
        public IReadOnlyList<AccountInfo> AccountInfos => _accountInfos;

        /// <summary>
        /// TR의 초당 전송 가능 횟수, Base 시간(초단위), TR의 10분당 제한 건수, 10분내 요청한 해당 TR의 총 횟수를 반환합니다.
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <returns></returns>
        public RequestCount GetRequestCount(string tr_cd) => new()
        {
            PerSec = IXingApi.ETK_GetTRCountPerSec(tr_cd),
            BaseSec = IXingApi.ETK_GetTRCountBaseSec(tr_cd),
            Limit = IXingApi.ETK_GetTRCountLimit(tr_cd),
            Requests = IXingApi.ETK_GetTRCountRequest(tr_cd),
        };

        private int _nRqID_last = -9999;

        /// <summary>
        /// 비동기 TR 요청
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="indatas">입력 바이너리 데이터</param>
        /// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        /// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastErrorMessage 참고</returns>
        public Task<ResponseTrData> RequestAsync(string tr_cd, string indatas, string cont_key = "") => RequestAsync(tr_cd, indatas.Split([',']).ToList(), cont_key);

        /// <summary>
        /// 비동기 TR 요청
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="indatas">입력 바이너리 데이터</param>
        /// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        /// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastErrorMessage 참고</returns>
        public async Task<ResponseTrData> RequestAsync(string tr_cd, IEnumerable<string> indatas, string cont_key = "")
        {
            _nRqID_last = -9999;
            var response = new ResponseTrData()
            {
                tr_cd = tr_cd,
            };

            int nRet = -905; // 자원정보가 없습니다.

            var resInfo = await ResManager.GetResInfoAsync(tr_cd);
            if (resInfo == null)
            {
                response.rsp_msg = "TR 정보를 찾을 수 없습니다.";
                goto EndError;
            }
            response.ResInfo = resInfo;

            var resSpec = resInfo.ResSpec;
            if (resSpec == null || resSpec.Correct == false)
            {
                response.rsp_msg = "RES 정보를 찾을 수 없습니다.";
                goto EndError;
            }

            if (resSpec.Type != ResManager.ResSpec.TYPE.FUNC)
            {
                response.rsp_msg = "TR 요청이 아닙니다.";
                goto EndError;
            }

            var inblocks = resSpec.InBlocks;
            if (inblocks == null || inblocks.Count == 0)
            {
                response.rsp_msg = "INBLOCK 정보를 찾을 수 없습니다.";
                goto EndError;
            }

            var outblocks = resSpec.OutBlocks;
            if (outblocks == null || outblocks.Count == 0)
            {
                response.rsp_msg = "OUTBLOCK 정보를 찾을 수 없습니다.";
                goto EndError;
            }

            var indataArray = indatas.ToArray();
            var firstInBlockSpec = inblocks[0];
            var in_fields = firstInBlockSpec.Fields;

            var line0_indatas = new string[in_fields.Count];
            for (int i = 0; i < in_fields.Count; i++)
            {
                if (i < indataArray.Length)
                    line0_indatas[i] = indataArray[i];
                else
                    line0_indatas[i] = string.Empty;
            }
            List<string[]> copied_inblockData = [line0_indatas];
            byte[] inBytes;
            //var encoder = Encoding.GetEncoding("euc-kr");
            var encoder = Encoding.ASCII;
            var fieldLengths = in_fields.Select(x => (int)x.size).ToArray();
            if (fieldLengths.Length == 1 && fieldLengths[0] == 0)
            {
                inBytes = encoder.GetBytes(indataArray[0]);
            }
            else
            {
                int frameLength = fieldLengths.Sum();
                if (resSpec.is_attr) frameLength += fieldLengths.Length;
                inBytes = new byte[frameLength];

                // outDatas 0x20 으로 초기화
                for (int i = 0; i < frameLength; i++)
                {
                    inBytes[i] = 0x20;
                }
                int offset = 0;
                for (int i = 0; i < fieldLengths.Length; i++)
                {
                    if (i >= indataArray.Length) break;
                    var coldataText = indataArray[i];
                    if (coldataText is null) continue;
                    if (coldataText is not null)
                    {
                        byte[] bytes = encoder.GetBytes(coldataText);
                        int minLength = Math.Min(fieldLengths[i], bytes.Length);
                        Array.Copy(bytes, 0, inBytes, offset, minLength);
                    }
                    offset += fieldLengths[i];
                    if (resSpec.is_attr) offset += 1;
                }
            }

            LastErrorMessage = string.Empty;

            if (tr_cd.Equals("t1857") || tr_cd.Equals("CHARTINDEX") || tr_cd.Equals("CHARTEXCEL"))
                nRet = IXingApi.ETK_RequestService(Handle, tr_cd, inBytes);
            else
                nRet = IXingApi.ETK_Request(Handle, tr_cd, inBytes, inBytes.Length, cont_key.Length > 0, cont_key, _defaultTimeOut);
            _nRqID_last = nRet;
            response.nRet = nRet;
            if (nRet < 0)
            {
                goto EndError;
            }

            RECEIVE_FLAGS _receiveFlag = RECEIVE_FLAGS.REQUEST_DATA;
            RecvDataMemory recvDataMemory = new();

            string rsp_tr_code = string.Empty;
            char rsp_tr_cont = '0';
            string rsp_tr_cont_key = string.Empty;
            var newAsync = new AsyncNode([nRet])
            {
                _async_OnReceiveDataHandler = (receiveFlag, data) =>
                {
                    _receiveFlag = receiveFlag;
                    if (receiveFlag == RECEIVE_FLAGS.REQUEST_DATA)
                    {
                        var recv_pkg = (RECV_PACKET_CLASS)data;
                        rsp_tr_code = recv_pkg.szTrCode;

                        bool bNonBlockMode = recv_pkg.nDataMode == 2;

                        if (bNonBlockMode)
                        {
                            //throw new Exception("아직 코딩되지 않았습니다.");
                        }

                        int nDataLength = recv_pkg.nDataLength;
                        IntPtr nBufferAdr = recv_pkg.lpData;
                        var specOutBlocks = resSpec.OutBlocks;

                        if (resSpec.headtype.Equals("A"))
                        {
                            // 해당 OutBlock 데이터 수신된다.
                            var specOutBlock = specOutBlocks.FirstOrDefault(x => x.Name.Equals(recv_pkg.szBlockName));
                            if (specOutBlock is not null)
                            {
                                List<string[]> textDatas = [];
                                int nFrameSize = specOutBlock.Fields.Sum(x => (int)x.size);
                                if (nFrameSize == 0)
                                {
                                    // 입력데이터 전체를 출력에 넣는다.
                                    string[] strings = [PtrToStringAnsi(nBufferAdr, nDataLength)];
                                    textDatas.Add(strings);
                                }
                                else
                                {
                                    if (resSpec.is_attr) nFrameSize += specOutBlock.Fields.Count;
                                    int nFrameCount = nDataLength / nFrameSize;
                                    for (int i = 0; i < nFrameCount; i++)
                                    {
                                        string[] strings = new string[specOutBlock.Fields.Count];
                                        for (int j = 0; j < specOutBlock.Fields.Count; j++)
                                        {
                                            int size = (int)specOutBlock.Fields[j].size;
                                            strings[j] = PtrToStringAnsi(nBufferAdr, size);
                                            if (resSpec.is_attr) size += 1;
                                            nBufferAdr += size;
                                            nDataLength -= size;
                                        }
                                        textDatas.Add(strings);
                                    }
                                }
                                recvDataMemory.BlockTextDatas.Add(new(specOutBlock, textDatas));
                            }
                        }
                        else
                        {
                            // 한번에 모든 OutBlock 데이터 수신된다.
                            foreach (var specOutBlock in specOutBlocks)
                            {
                                List<string[]> textDatas = [];
                                if (specOutBlock.occurs)
                                {
                                    if (nDataLength < 5)
                                    {
                                        LastErrorMessage = "수신 데이터 길이 오류";
                                        break;
                                    }
                                    // 배열은 데이터 앞에 5byte로 배열 갯수 문자열이 온다.
                                    int nFrameCount = 0;
                                    if (int.TryParse(PtrToStringAnsi(nBufferAdr, 5), out nFrameCount))
                                    {
                                        nFrameCount = int.Parse(PtrToStringAnsi(nBufferAdr, 5));
                                        nBufferAdr += 5;
                                        nDataLength -= 5;
                                        int nFrameSize = specOutBlock.Fields.Sum(x => (int)x.size);
                                        if (resSpec.is_attr) nFrameSize += specOutBlock.Fields.Count;
                                        int nTotalFrameSize = nFrameSize * nFrameCount;
                                        if (nDataLength < nTotalFrameSize)
                                        {
                                            LastErrorMessage = "수신 데이터 길이 오류";
                                            break;
                                        }
                                        for (int i = 0; i < nFrameCount; i++)
                                        {
                                            string[] strings = new string[specOutBlock.Fields.Count];
                                            for (int j = 0; j < specOutBlock.Fields.Count; j++)
                                            {
                                                int size = (int)specOutBlock.Fields[j].size;
                                                strings[j] = PtrToStringAnsi(nBufferAdr, size);
                                                if (resSpec.is_attr) size += 1;
                                                nBufferAdr += size;
                                                nDataLength -= size;
                                            }
                                            textDatas.Add(strings);
                                        }
                                    }
                                }
                                else
                                {
                                    int nFrameSize = specOutBlock.Fields.Sum(x => (int)x.size);
                                    if (resSpec.is_attr) nFrameSize += specOutBlock.Fields.Count;
                                    if (nDataLength < nFrameSize)
                                    {
                                        LastErrorMessage = "수신 데이터 길이 오류";
                                        break;
                                    }
                                    string[] strings = new string[specOutBlock.Fields.Count];
                                    for (int j = 0; j < specOutBlock.Fields.Count; j++)
                                    {
                                        int size = (int)specOutBlock.Fields[j].size;
                                        strings[j] = PtrToStringAnsi(nBufferAdr, size);
                                        if (resSpec.is_attr) size += 1;
                                        nBufferAdr += size;
                                        nDataLength -= size;
                                    }
                                    textDatas.Add(strings);
                                }
                                recvDataMemory.BlockTextDatas.Add(new(specOutBlock, textDatas));
                            }
                        }

                        rsp_tr_cont = recv_pkg.cCont;
                        rsp_tr_cont_key = recv_pkg.szContKey;
                    }
                    else if (receiveFlag == RECEIVE_FLAGS.MESSAGE_DATA || receiveFlag == RECEIVE_FLAGS.SYSTEM_ERROR_DATA)
                    {
                        var msg_pkt = (MSG_PACKET_CLASS)data;
                        response.rsp_cd = msg_pkt.szMsgCode;
                        response.rsp_msg = msg_pkt.lpszMessageData;
                    }
                },
            };

            _async_list.Add(newAsync);
            await newAsync.Wait(AsyncTimeOut);
            _async_list.Remove(newAsync);

            nRet = newAsync._async_result;


            if (nRet < 0)
            {
                goto EndError;
            }

            if (_receiveFlag == RECEIVE_FLAGS.SYSTEM_ERROR_DATA)
            {
                nRet = -903;
                goto EndError;
            }

            if (_receiveFlag == RECEIVE_FLAGS.MESSAGE_DATA || _receiveFlag == RECEIVE_FLAGS.REQUEST_DATA)
            {
                var blockDatas = new List<BlockData>
                {
                    new(firstInBlockSpec, copied_inblockData),
                };
                blockDatas.AddRange(recvDataMemory.BlockTextDatas);
                response.cont_key = rsp_tr_cont.Equals('1') ? (rsp_tr_cont_key.Length != 0 ? rsp_tr_cont_key : "0") : string.Empty;
                response.ResInfo = resInfo;
                response.BlockDatas = blockDatas;
                return response;
            }
            nRet = -904;
        EndError:
            response.nRet = nRet;
            if (string.IsNullOrEmpty(response.rsp_msg))
            {
                response.rsp_msg = GetErrorMessage(nRet);
            }
            if (string.IsNullOrEmpty(response.rsp_cd))
            {
                response.rsp_cd = nRet.ToString();
            }
            return response;
        }

        /// <summary>
        /// 실시간 시세 등록/해제
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="tr_key">단축코드 6자리 또는 8자리 (단건, 연속)</param>
        /// <param name="bAdd">시세등록: true, 시세해제: false</param>
        /// <returns>true: 요청성공, false: 요청실패</returns>
        public async Task<bool> RequestRealtimeAsync(string tr_cd, string tr_key, bool bAdd)
        {
            var resInfo = await ResManager.GetResInfoAsync(tr_cd);
            if (resInfo == null)
            {
                LastErrorMessage = "TR 정보를 찾을 수 없습니다.";
                return false;
            }
            bool bRet;
            if (bAdd)
            {
                bRet = IXingApi.ETK_AdviseRealData(Handle, tr_cd, tr_key, tr_key.Length);
            }
            else
            {
                bRet = IXingApi.ETK_UnadviseRealData(Handle, tr_cd, tr_key, tr_key.Length);
            }
            if (!bRet)
            {
                int nErrorCode = GetLastError();
                LastErrorMessage = $"[{nErrorCode}]: {GetErrorMessage(nErrorCode)}";
            }
            return bRet;
        }

        /// <summary>
        /// 부가 서비스용 TR를 해제합니다.
        /// </summary>
        public int RemoveService(string szCode, string szData) => IXingApi.ETK_RemoveService(Handle, szCode, szData);
    }
}
