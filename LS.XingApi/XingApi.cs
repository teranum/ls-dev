using LS.XingApi.Native;
using Microsoft.Win32;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Policy;
using LPARAM = nint;
using WPARAM = nint;

namespace LS.XingApi
{
    /// <summary>API</summary>
    public partial class XingApi
    {
        [DllImport("kernel32.dll")] private static extern IntPtr LoadLibrary(string dllToLoad);
        [DllImport("kernel32.dll")] private static extern IntPtr GetProcAddress(IntPtr hModule, string procedureName);
        private const string XING_DLL = "xingAPI.dll";
        private const string XING64_DLL = "xingAPI64.dll";
        private delegate bool XING64_Init_Handler(string szFolder);
        private const string REAL_DOMAIN = "api.ls-sec.co.kr";
        private const string SIMUL_DOMAIN = "demo.ls-sec.co.kr";

        class WndForm : Form
        {
            public Action<IntPtr, uint, IntPtr, IntPtr>? WndProcHandler;
            protected override void WndProc(ref Message m)
            {
                base.WndProc(ref m);
                WndProcHandler?.Invoke(m.HWnd, (uint)m.Msg, m.WParam, m.LParam);
            }
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
        //class RecvDataMemory
        //{
        //    public string TrCode = "";
        //    public int RequestID = 0;
        //    public IList<BlockData> BlockTextDatas = [];
        //}
        class AsyncNode(int ident_id, Action<WPARAM, LPARAM> callback)
        {
            public readonly int ident_id = ident_id;
            public Action<WPARAM, LPARAM> callback = callback;

            private readonly ManualResetEvent _async_wait = new(initialState: false);

            public bool _async_evented = false;
            public string _async_code = string.Empty;
            public string _async_msg = string.Empty;
            public int _async_result = 0;

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

        readonly List<AsyncNode> _async_nodes = [];

        private Form _win32Window;
        private const int WM_USER = 0x0400;
        private const int AsyncTimeOut = 10000;

        private ResManager _resManager;
        private IXingApi _module;
        private string _xing_folder;
        private bool _server_connected;

        /// <inheritdoc cref="MessageEventArgs"/>
        public event EventHandler<MessageEventArgs>? OnMessageEvent;

        /// <inheritdoc cref="RealtimeEventArgs"/>
        public event EventHandler<RealtimeEventArgs>? OnRealtimeEvent;

        /// <summary>
        /// XingAPI 폴더
        /// </summary>
        public string XingFolder => _xing_folder;

        /// <summary>
        /// 모듈이 로딩 된 경우 true
        /// </summary>
        public bool ModuleLoaded => _module.IsLoaded;

        /// <summary>모의투자 여부</summary>
        public bool IsSimulation { get; private set; }

        /// <summary>연결 여부</summary>
        public bool Connected { get; private set; }

        /// <summary>윈도우 핸들</summary>
        public nint Handle => _win32Window.Handle;

        /// <summary>로그인 아이디</summary>
        public string UserID { get; private set; } = string.Empty;

        /// <summary>
        /// 마지막 메시지
        /// </summary>
        public string LastMessage { get; private set; } = string.Empty;

        /// <summary>API객체 생성</summary>
        public XingApi(string apiFolder = "")
        {
            bool is_64bit = Environment.Is64BitProcess;
            if (!Directory.Exists(apiFolder))
            {
                var regKey = is_64bit
                    ? Registry.ClassesRoot.OpenSubKey("WOW6432Node\\CLSID\\{7FEF321C-6BFD-413C-AA80-541A275434A1}\\InprocServer32")
                    : Registry.ClassesRoot.OpenSubKey("CLSID\\{7FEF321C-6BFD-413C-AA80-541A275434A1}\\InprocServer32");
                if (regKey is not null)
                {
                    if (regKey.GetValue("") is string defaultValue)
                    {
                        apiFolder = Path.GetDirectoryName(defaultValue) ?? string.Empty;
                    }
                    regKey.Close();
                }
            }

            nint handle;
            var exe_folder = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!;
            if (is_64bit)
            {
                var pack_dll_path = Path.Combine(exe_folder, XING64_DLL);
                if (File.Exists(pack_dll_path))
                    handle = LoadLibrary(pack_dll_path);
                else
                    handle = LoadLibrary(Path.Combine(apiFolder, XING64_DLL));

                if (handle != 0)
                {
                    var XING64_Init_Handle = GetProcAddress(handle, "XING64_Init");
                    if (XING64_Init_Handle != IntPtr.Zero)
                    {
                        var XING64_Init = Marshal.GetDelegateForFunctionPointer<XING64_Init_Handler>(XING64_Init_Handle);
                        if (!XING64_Init(apiFolder))
                        {
                            handle = 0;
                        }
                    }
                }
            }
            else
                handle = LoadLibrary(Path.Combine(apiFolder, XING_DLL));

            _resManager = new ResManager(exe_folder, apiFolder);

            _module = new IXingApi(handle);
            _xing_folder = apiFolder;

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

        /// <summary>
        /// 비동기 연결 요청
        /// </summary>
        /// <param name="userId">유저 아이디</param>
        /// <param name="password">HTS 패스워드</param>
        /// <param name="certPassword">공인인증 패스워드</param>
        /// <returns>ret: 0, 연결성공, 그외 오류코드</returns>
        /// <remarks>공인인증 패스워드 없는 경우, 모의서버로 로그인</remarks>
        public async Task<bool> ConnectAsync(string userId, string password, string certPassword = "")
        {
            if (Connected)
            {
                LastMessage = "Already connected";
                return true;
            }

            if (!ModuleLoaded)
            {
                LastMessage = "XingAPI.dll is not loaded";
                return false;
            }

            LastMessage = string.Empty;
            _accountInfos.Clear();

            IsSimulation = certPassword.Length == 0;
            _server_connected = IXingApi.ETK_Connect(Handle, IsSimulation ? SIMUL_DOMAIN : REAL_DOMAIN, 20001, WM_USER, -1, -1);

            if (_server_connected)
            {
                var ret = IXingApi.ETK_Login(Handle, userId, password, certPassword, 0, bShowCertErrDlg: false);
                if (ret)
                {
                    var code_msg = (string.Empty, string.Empty);
                    var node = new AsyncNode(0, (wParam, lParam) =>
                    {
                        code_msg = (PtrToStringAnsi(wParam), PtrToStringAnsi(lParam));
                    });
                    _async_nodes.Add(node);
                    await node.Wait();
                    _async_nodes.Remove(node);

                    LastMessage = $"[{code_msg.Item1}] {code_msg.Item2}";
                    if (code_msg.Item1.Equals("0000"))
                    {
                        var account_count = IXingApi.ETK_GetAccountListCount();
                        for (var i = 0; i < account_count; i++)
                        {
                            var Number = IXingApi.GetAccountList(i);
                            var Name = IXingApi.GetAccountName(Number);
                            var DetailName = IXingApi.GetAcctDetailName(Number);
                            var NickName = IXingApi.GetAcctNickname(Number);
                            _accountInfos.Add(new AccountInfo(Number, Name, DetailName, NickName));
                        }
                        Connected = true;
                        UserID = userId;
                        return true;
                    }
                }
                else
                {
                    LastMessage = "로그인 실패.";
                }
            }
            else
            {
                int nErrCode = GetLastError();
                LastMessage = $"[{nErrCode}] {GetErrorMessage(nErrCode)}";
            }

            Close();
            return false;
        }

        /// <summary>연결 해제</summary>
        public void Close()
        {
            if (!ModuleLoaded)
                return;
            if (Connected)
            {
                IXingApi.ETK_Logout(Handle);
                Connected = false;
            }
            if (_server_connected)
            {
                IXingApi.ETK_Disconnect();
                _server_connected = false;
            }
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
                        OnMessageEvent?.Invoke(this, new("DISCONNECT"));
                    }
                    break;
                case XM.XM_LOGOUT:
                    {
                        Connected = false;
                        OnMessageEvent?.Invoke(this, new("LOGOUT"));
                    }
                    break;
                case XM.XM_LOGIN:
                    {
                        // ETK_Login() 함수가 호출 된 후 Login 과정이 완료되었을 때 호출
                        // WPARAM: Message Code, 문자열 형태,“0000” 이면 성공, 그 외에는 실패
                        // LPARAM: Message Text
                        int ident_id = 0;
                        var async_node = _async_nodes.Find(x => x.ident_id == ident_id);
                        if (async_node is not null)
                        {
                            async_node.callback(wParam, lParam);
                            async_node.Set();
                        }
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
                                    int nRqID = Marshal.PtrToStructure<int>(lParam);
                                    var async_node = _async_nodes.Find(x => x.ident_id == nRqID);
                                    async_node?.callback(wParam, lParam);
                                }
                                break;
                            case RECEIVE_FLAGS.MESSAGE_DATA:
                            case RECEIVE_FLAGS.SYSTEM_ERROR_DATA:
                                {
                                    int nRqID = Marshal.PtrToStructure<int>(lParam);
                                    var async_node = _async_nodes.Find(x => x.ident_id == nRqID);
                                    if (async_node is not null)
                                    {
                                        async_node.callback(wParam, lParam);
                                        async_node.Set();
                                    }

                                    IXingApi.ETK_ReleaseMessageData(lParam);
                                    if (receiveFlag == RECEIVE_FLAGS.SYSTEM_ERROR_DATA)
                                    {
                                        IXingApi.ETK_ReleaseRequestData(nRqID);
                                    }
                                }
                                break;
                            case RECEIVE_FLAGS.RELEASE_DATA:
                                {
                                    // LPARAM : 정수로 Requests ID를 의미
                                    int nRqID = lParam.ToInt32();
                                    var async_node = _async_nodes.Find(x => x.ident_id == nRqID);
                                    if (async_node is not null)
                                    {
                                        async_node.callback(wParam, lParam);
                                        async_node.Set();
                                    }
                                    IXingApi.ETK_ReleaseRequestData(nRqID);
                                }
                                break;
                            default:
                                break;
                        }
                    }
                    break;
                case XM.XM_TIMEOUT_DATA:
                    {
                        // 조회 TR에 대한 응답이 Timeout 되었을 때 호출
                        // WPARAM: 사용안함
                        // LPARAM: Requests ID
                        int nRqID = lParam.ToInt32();

                        var async_node = _async_nodes.Find(x => x.ident_id == nRqID);
                        if (async_node is not null)
                        {
                            async_node._async_result = -902;
                            async_node.Set();
                        }
                        IXingApi.ETK_ReleaseRequestData(nRqID);
                    }
                    break;
                case XM.XM_RECEIVE_LINK_DATA:
                    {
                        // HTS -> API로 연동을 등록하면, HTS에서 연동 정보가 발생시에 호출, 사용방식은 XM_RECEIVE_REAL_DATA 수신과 동일
                        // WPARAM: LINK_DATA
                        // LPARAM: LINKDATRRA_RECV_MSG 구조체 데이터
                        //var data = new LINKDATA_RECV_MSG_CLASS(lParam);
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
                        var trInfo = _resManager.GetResInfo(szTrCode);
                        //if (trInfo is not null && trInfo.ResSpec is not null)
                        //{
                        //    var specOutBlock = trInfo.ResSpec.OutBlocks[0];
                        //    byte[] bytes = new byte[real_recv_packet.nDataLength];
                        //    Marshal.Copy(real_recv_packet.pszData, bytes, 0, real_recv_packet.nDataLength);
                        //    var fileds = trInfo.ResSpec.OutBlocks;
                        //    IntPtr nBufferAdr = real_recv_packet.pszData;
                        //    int nFrameSize = specOutBlock.Fields.Sum(x => (int)x.size);
                        //    if (trInfo.ResSpec.is_attr) nFrameSize += specOutBlock.Fields.Count;
                        //    string[] realTextDatas = new string[specOutBlock.Fields.Count];
                        //    for (int j = 0; j < specOutBlock.Fields.Count; j++)
                        //    {
                        //        int size = (int)specOutBlock.Fields[j].size;
                        //        realTextDatas[j] = PtrToStringAnsi(nBufferAdr, size);
                        //        if (trInfo.ResSpec.is_attr) size += 1;
                        //        nBufferAdr += size;
                        //    }
                        //    OnRealtimeEvent?.Invoke(this, new(szTrCode, szKey, realTextDatas));
                        //}
                        //else
                        //{
                        //    OnRealtimeEvent?.Invoke(this, new(szTrCode, szKey, [PtrToStringAnsi(real_recv_packet.pszData)!]));
                        //}
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

        /// <summary>
        /// 비동기 TR 요청
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="in_datas">입력 바이너리 데이터</param>
        /// <param name="cont_yn">연속여부</param>
        /// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        /// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastMessage 참고</returns>
        public Task<ResponseTrData?> RequestAsync(string tr_cd, string in_datas, bool cont_yn = false, string cont_key = "")
            => Inter_RequestAsync(tr_cd, in_datas.Split([',']).ToList(), cont_yn, cont_key);

        /// <summary>
        /// 비동기 TR 요청
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="in_datas">입력 바이너리 데이터</param>
        /// <param name="cont_yn">연속여부</param>
        /// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        /// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastMessage 참고</returns>
        public async Task<ResponseTrData?> RequestAsync(string tr_cd, IList<string> in_datas, bool cont_yn = false, string cont_key = "")
            => await Inter_RequestAsync(tr_cd, in_datas, cont_yn, cont_key);

        /// <summary>
        /// 비동기 TR 요청
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="in_datas">입력 바이너리 데이터</param>
        /// <param name="cont_yn">연속여부</param>
        /// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        /// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastMessage 참고</returns>
        public Task<ResponseTrData?> RequestAsync(string tr_cd, IDictionary<string, object> in_datas, bool cont_yn = false, string cont_key = "")
            => Inter_RequestAsync(tr_cd, in_datas, cont_yn, cont_key);

        private async Task<ResponseTrData?> Inter_RequestAsync(string tr_cd, object in_datas, bool cont_yn = false, string cont_key = "")
        {
            if (!Connected)
            {
                LastMessage = "Not connected";
                return null;
            }

            var res_info = _resManager.GetResInfo(tr_cd);
            if (res_info is null)
            {
                LastMessage = "TR 정보를 찾을 수 없습니다.";
                return null;
            }

            if (!res_info.is_func)
            {
                LastMessage = "TR 요청이 아닙니다.";
                return null;
            }

            var response = new ResponseTrData()
            {
                tr_cd = tr_cd,
                res = res_info,
            };

            var inblocks_count = res_info.in_blocks.Count;
            if (inblocks_count == 1)
            {
                var inblock = res_info.in_blocks[0];
                var in_fields = inblock.fields;
                var in_block_field_count = in_fields.Count;
                var aligned_in_block_datas = new string[in_block_field_count];
                var correct_in_block_dict = new Dictionary<string, object>();
                (string value, string error) get_correct_field_value(FieldSpec field, object value)
                {
                    var size = field.size;
                    if (size == 0)
                        return (value.ToString()!, string.Empty);
                    if (value is null)
                        return ("null", "Value is null.");
                    var str_val = string.Empty;
                    if (field.type == FieldSpec.VarType.STRING)
                    {
                        return (value.ToString()!, string.Empty);

                    }
                    //if (field.type == FieldSpec.FieldType.INT)
                    //    return ((int)value).ToString();
                    //if (field.type == FieldSpec.FieldType.LONG)
                    //    return ((long)value).ToString();
                    //if (field.type == FieldSpec.FieldType.FLOAT)
                    //    return ((float)value).ToString();
                    //if (field.type == FieldSpec.FieldType.DOUBLE)
                    //    return ((double)value).ToString();
                    return (string.Empty, string.Empty);
                }
            }
            else if (inblocks_count == 2)
            {

            }
            else if (inblocks_count > 2)
            {
                LastMessage = "자원정보 inblock개수가 2이상입니다, 현재버전 지원 불가.";
                return null;
            }
            else
            {
                LastMessage = "자원정보에 inblock이 없습니다, 현재버전 지원 불가.";
                return null;
            }
            /*
            int nRet = -905; // 자원정보가 없습니다.

            var resInfo = _resManager.GetResInfo(tr_cd);
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

            LastMessage = string.Empty;

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
                                        LastMessage = "수신 데이터 길이 오류";
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
                                            LastMessage = "수신 데이터 길이 오류";
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
                                        LastMessage = "수신 데이터 길이 오류";
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
            */
            return response;
        }

        /// <summary>
        /// 실시간 시세 등록/해제
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="tr_key">단축코드 6자리 또는 8자리 (단건, 연속)</param>
        /// <param name="bAdd">시세등록: true, 시세해제: false</param>
        /// <returns>true: 요청성공, false: 요청실패</returns>
        public bool RequestRealtimeAsync(string tr_cd, string tr_key, bool bAdd)
        {
            var resInfo = _resManager.GetResInfo(tr_cd);
            if (resInfo == null)
            {
                LastMessage = "TR 정보를 찾을 수 없습니다.";
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
                LastMessage = $"[{nErrorCode}]: {GetErrorMessage(nErrorCode)}";
            }
            return bRet;
        }

        /// <summary>
        /// 부가 서비스용 TR를 해제합니다.
        /// </summary>
        public int RemoveService(string szCode, string szData) => IXingApi.ETK_RemoveService(Handle, szCode, szData);
    }
}
