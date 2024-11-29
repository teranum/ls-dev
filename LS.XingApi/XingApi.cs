using LS.XingApi.Native;
using Microsoft.Win32;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
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

        /// <summary>API자원관리자</summary>
        public ResManager ResourceManager => _resManager;

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
            return _module.GetErrorMessage(nErrCode);
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
            _server_connected = _module.ETK_Connect(Handle, IsSimulation ? SIMUL_DOMAIN : REAL_DOMAIN, 20001, WM_USER, -1, -1);

            if (_server_connected)
            {
                var ret = _module.ETK_Login(Handle, userId, password, certPassword, 0, bShowCertErrDlg: false);
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
                        var account_count = _module.ETK_GetAccountListCount();
                        for (var i = 0; i < account_count; i++)
                        {
                            var Number = _module.GetAccountList(i);
                            var Name = _module.GetAccountName(Number);
                            var DetailName = _module.GetAcctDetailName(Number);
                            var NickName = _module.GetAcctNickname(Number);
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
                _module.ETK_Logout(Handle);
                Connected = false;
            }
            if (_server_connected)
            {
                _module.ETK_Disconnect();
                _server_connected = false;
            }
        }

        private int GetLastError() => _module.ETK_GetLastError();
        private List<AccountInfo> _accountInfos { get; } = [];

        private static string PtrToStringAnsi(IntPtr ptr) => Marshal.PtrToStringAnsi(ptr)?.TrimEnd('\0').Trim() ?? string.Empty;
        private static string PtrToStringAnsi(IntPtr ptr, int length) => Marshal.PtrToStringAnsi(ptr, length).TrimEnd('\0').Trim();
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
            PerSec = _module.ETK_GetTRCountPerSec(tr_cd),
            BaseSec = _module.ETK_GetTRCountBaseSec(tr_cd),
            Limit = _module.ETK_GetTRCountLimit(tr_cd),
            Requests = _module.ETK_GetTRCountRequest(tr_cd),
        };

        /// <summary>
        /// 비동기 TR 요청
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="in_datas">입력 바이너리 데이터</param>
        /// <param name="cont_yn">연속여부</param>
        /// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        /// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastMessage 참고</returns>
        public Task<ResponseTrData?> RequestAsync(string tr_cd, object in_datas, bool cont_yn = false, string cont_key = "")
            => Inter_RequestAsync(tr_cd, in_datas, cont_yn, cont_key);

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

        ///// <summary>
        ///// 비동기 TR 요청
        ///// </summary>
        ///// <param name="tr_cd">증권 거래코드</param>
        ///// <param name="in_datas">입력 바이너리 데이터</param>
        ///// <param name="cont_yn">연속여부</param>
        ///// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        ///// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastMessage 참고</returns>
        //public async Task<ResponseTrData?> RequestAsync(string tr_cd, IList<object> in_datas, bool cont_yn = false, string cont_key = "")
        //    => await Inter_RequestAsync(tr_cd, in_datas, cont_yn, cont_key);

        ///// <summary>
        ///// 비동기 TR 요청
        ///// </summary>
        ///// <param name="tr_cd">증권 거래코드</param>
        ///// <param name="in_datas">입력 바이너리 데이터</param>
        ///// <param name="cont_yn">연속여부</param>
        ///// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
        ///// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastMessage 참고</returns>
        //public Task<ResponseTrData?> RequestAsync(string tr_cd, IDictionary<string, object> in_datas, bool cont_yn = false, string cont_key = "")
        //    => Inter_RequestAsync(tr_cd, in_datas, cont_yn, cont_key);

        private async Task<ResponseTrData?> Inter_RequestAsync(string tr_cd, object in_datas, bool cont_yn = false, string cont_key = "")
        {
            var res_info = _resManager.GetResInfo(tr_cd);
            if (res_info is null)
            {
                LastMessage = "TR 정보를 찾을 수 없습니다.";
                return null;
            }

            if (!Connected)
            {
                LastMessage = "Not connected";
                return null;
            }

            if (!res_info.is_func)
            {
                LastMessage = "TR 요청이 아닙니다.";
                return null;
            }

            var response = new ResponseTrData()
            {
                tr_cd = res_info.tr_cd,
                res = res_info,
            };

            var inblocks_count = res_info.in_blocks.Count;
            var is_heade_A = res_info.headtype.Equals("A");
            var is_heade_B = res_info.headtype.Equals("B");
            var indata_line = new StringBuilder();
            if (inblocks_count == 1)
            {
                var in_block = res_info.in_blocks[0];
                var in_fields = in_block.fields;
                var in_block_field_count = in_fields.Count;
                var aligned_in_block_datas = new string[in_block_field_count];
                var correct_in_block_dict = new Dictionary<string, string>();
                (string value, string error) get_correct_field_value(FieldSpec field, string in_str)
                {
                    if (in_str is null)
                        return (string.Empty, "Value is null.");
                    var size = field.size;
                    if (size == 0)
                        return (in_str, string.Empty);
                    if (field.type == FieldSpec.VarType.STRING)
                    {
                        if (in_str.Length > size)
                            return (string.Empty, "length is over.");
                        return (in_str.PadRight(size, ' '), string.Empty);
                    }
                    if (field.type == FieldSpec.VarType.INT || field.type == FieldSpec.VarType.LONG)
                    {
                        if (in_str.Length == 0)
                            in_str = "0";
                        if (long.TryParse(in_str, out long int_val))
                        {
                            var conv_str = int_val.ToString();
                            if (conv_str.Length > size)
                                return (string.Empty, "length is over.");
                            return (conv_str.PadLeft(size, '0'), string.Empty);
                        }
                        return (string.Empty, "Value is not integer.");
                    }
                    if (field.type == FieldSpec.VarType.DOUBLE)
                    {
                        if (in_str.Length == 0)
                            in_str = "0";
                        if (double.TryParse(in_str, out double float_val))
                        {
                            var conv_str = is_heade_B
                                ? float_val.ToString($"F{field.size}")
                                : float_val.ToString($"F{field.size}").Replace(".", string.Empty);
                            if (conv_str.Length > size)
                                return (string.Empty, "length is over.");
                            return (conv_str.PadLeft(size, '0'), string.Empty);
                        }
                        return (string.Empty, "Value is not float.");
                    }
                    return (string.Empty, "invalid type");
                }

                if (in_datas is IDictionary in_dict)
                {
                    for (int i = 0; i < in_block_field_count; i++)
                    {
                        var field = in_fields[i];
                        string in_value_str;
                        if (in_dict.Contains(field.name))
                        {
                            in_value_str = in_dict[field.name]!.ToString()!.Trim();
                        }
                        else
                        {
                            in_value_str = string.Empty;
                        }
                        var (correct_value, error) = get_correct_field_value(field, in_value_str);
                        if (error.Length > 0)
                        {
                            LastMessage = $"{field.name}: {error}";
                            return null;
                        }
                        aligned_in_block_datas[i] = correct_value;
                        correct_in_block_dict.Add(field.name, correct_value.Trim());
                    }
                }
                else if (in_datas is IList in_list)
                {
                    var in_list_count = in_list.Count;
                    for (int i = 0; i < in_block_field_count; i++)
                    {
                        var field = in_fields[i];
                        string in_value_str;
                        if (i < in_list_count)
                        {
                            in_value_str = in_list[i]!.ToString()!.Trim();
                        }
                        else
                        {
                            in_value_str = string.Empty;
                        }
                        var (correct_value, error) = get_correct_field_value(field, in_value_str);
                        if (error.Length > 0)
                        {
                            LastMessage = $"{field.name}: {error}";
                            return null;
                        }
                        aligned_in_block_datas[i] = correct_value;
                        correct_in_block_dict.Add(field.name, correct_value);
                    }
                }
                else if (in_datas is IEnumerable in_Enumarable)
                {
                    var in_enumable_list = in_Enumarable.Cast<object>().ToList();
                    var in_list_count = in_enumable_list.Count;
                    for (int i = 0; i < in_block_field_count; i++)
                    {
                        var field = in_fields[i];
                        string in_value_str;
                        if (i < in_list_count)
                        {
                            in_value_str = in_enumable_list[i]!.ToString()!.Trim();
                        }
                        else
                        {
                            in_value_str = string.Empty;
                        }
                        var (correct_value, error) = get_correct_field_value(field, in_value_str);
                        if (error.Length > 0)
                        {
                            LastMessage = $"{field.name}: {error}";
                            return null;
                        }
                        aligned_in_block_datas[i] = correct_value;
                        correct_in_block_dict.Add(field.name, correct_value);
                    }
                }
                else
                {
                    LastMessage = "inblock data type error.";
                    return null;
                }

                response.body[in_block.name] = correct_in_block_dict;

                foreach (var item in aligned_in_block_datas)
                {
                    indata_line.Append(item);
                    if (res_info.is_attr)
                        indata_line.Append(' ');
                }
            }
            else if (inblocks_count == 2)
            {
                if (response.tr_cd.Equals("o3127")) // 해외선물옵션관심종목조회(o3127)-API용
                {
                    // 입력 포멧: "F선물코드1, F선물코드2, O옵션코드1, O옵션코드2..."
                    if (in_datas is IList<object> in_symbols)
                    {
                        var in_symbols_count = in_symbols.Count;
                        if (in_symbols_count == 0)
                        {
                            LastMessage = "입력 데이터가 없습니다.";
                            return null;
                        }
                        var o3127InBlock1 = new List<string>();
                        for (int i = 0; i < in_symbols_count; i++)
                        {
                            var in_symbol = in_symbols[i].ToString()!.Trim().PadLeft(16);
                            o3127InBlock1.Append(in_symbol);
                            indata_line.Append(in_symbol);
                            if (res_info.is_attr)
                                indata_line.Append(' ');
                        }
                        response.body["o3127InBlock1"] = o3127InBlock1;
                    }
                    else
                    {
                        LastMessage = "입력 데이터 형식 오류.";
                        return null;
                    }
                }
                else
                {
                    LastMessage = $"{response.tr_cd}: 현재 버전에서 지원하지 않습니다.";
                    return null;
                }
            }
            else
            {
                if (inblocks_count > 2)
                {
                    LastMessage = "자원정보 inblock개수가 2 이상입니다, 현재버전 지원 불가.";
                    return null;
                }

                LastMessage = "자원정보에 inblock이 없습니다, 현재버전 지원 불가.";
                return null;
            }

            LastMessage = string.Empty;
            var stopwatch = Stopwatch.StartNew();
            int nRqID;
            if (res_info.tr_cd.Equals("t1857") || tr_cd.Equals("ChartIndex") || tr_cd.Equals("ChartExcel"))
            {
                nRqID = _module.ETK_RequestService(Handle, tr_cd, indata_line.ToString());
            }
            else
                nRqID = _module.ETK_Request(Handle, tr_cd, indata_line.ToString(), indata_line.Length, cont_yn, cont_key, AsyncTimeOut);
            if (nRqID < 0)
            {
                LastMessage = $"[{nRqID}]: {GetErrorMessage(nRqID)}";
                return null;
            }
            response.id = nRqID;
            response.ticks.Add(stopwatch.ElapsedTicks);

            var node = new AsyncNode(nRqID, callback);
            _async_nodes.Add(node);
            await node.Wait();
            _async_nodes.Remove(node);

            response.ticks.Add(stopwatch.ElapsedTicks);
            LastMessage = $"[{response.rsp_cd}] {response.rsp_msg}";

            if (response.id < 0)
                return null;

            return response;

            void callback(WPARAM wParam, LPARAM lParam)
            {
                RECEIVE_FLAGS receiveFlag = (RECEIVE_FLAGS)wParam.ToInt32();
                switch (receiveFlag)
                {
                    case RECEIVE_FLAGS.MESSAGE_DATA:
                    case RECEIVE_FLAGS.SYSTEM_ERROR_DATA:
                        {
                            var packet = Marshal.PtrToStructure<MSG_PACKET>(lParam);
                            response.rsp_cd = ByteToString(packet.szMsgCode);
                            response.rsp_msg = PtrToStringAnsi(packet.lpszMessageData, packet.nMsgLength);

                            if (int.TryParse(response.rsp_cd, out var num_code))
                            {
                                if (num_code < 0)
                                    response.id = num_code;
                            }
                            else
                            {
                                response.id = -1;
                            }
                        }
                        break;
                    case RECEIVE_FLAGS.REQUEST_DATA:
                        {
                            var packet = Marshal.PtrToStructure<RECV_PACKET>(lParam);
                            response.cont_yn = packet.cCont == '1';
                            response.cont_key = ByteToString(packet.szContKey);
                            var nDataLength = packet.nDataLength;
                            var lpData = packet.lpData;

                            if (is_heade_A)
                            {
                                var out_block_name = ByteToString(packet.szBlockName);
                                var out_block = res_info.out_blocks.First(x => x.name.Equals(out_block_name));
                                if (out_block != null)
                                {
                                    if (out_block.record_size == 0)
                                        response.body[out_block.name] = PtrToStringAnsi(lpData, nDataLength);
                                    else
                                    {
                                        if (res_info.compressable
                                            && out_block.is_occurs
                                            && response.body.TryGetValue(res_info.in_blocks[0].name, out var in_block_base)
                                            && in_block_base is IDictionary dict
                                            && dict.Contains("comp_yn")
                                            )
                                        {
                                            var comp_yn = dict["comp_yn"];
                                            if (string.Equals(comp_yn, "Y") && int.TryParse(((IDictionary)response.body[res_info.out_blocks[0].name])["rec_count"]!.ToString(), out var rec_count))
                                            {
                                                var target_size = rec_count * out_block.record_size;
                                                var buffer = new byte[target_size];
                                                var buffer_adr = Marshal.UnsafeAddrOfPinnedArrayElement(buffer, 0);
                                                nDataLength = _module.ETK_Decompress(lpData, buffer_adr, nDataLength);
                                                lpData = buffer_adr;
                                            }
                                        }

                                        var nFrameCount = nDataLength / out_block.record_size;
                                        var rows = nFrameCount;
                                        var cols = out_block.fields.Count;
                                        var datas = new List<Dictionary<string, object>>(rows);
                                        for (int i = 0; i < rows; i++)
                                        {
                                            var col_datas = new Dictionary<string, object>(cols);
                                            for (int j = 0; j < cols; j++)
                                            {
                                                var field = out_block.fields[j];
                                                var value = PtrToStringAnsi(lpData, field.size);
                                                col_datas[field.name] = ConvFieldData(field, value);
                                                lpData += field.size;
                                                if (res_info.is_attr)
                                                    lpData++;
                                            }
                                            datas.Add(col_datas);
                                        }

                                        if (out_block.is_occurs)
                                        {
                                            response.body[out_block.name] = datas;
                                        }
                                        else
                                        {
                                            response.body[out_block.name] = datas[0];
                                        }
                                    }
                                }
                            }
                            else
                            {
                                foreach (var out_block in res_info.out_blocks)
                                {
                                    if (nDataLength <= 0)
                                        break;
                                    var nFrameCount = 0;
                                    if (out_block.is_occurs)
                                    {
                                        if (nDataLength < 5)
                                            // errMsg = "수신 데이터 길이 오류."
                                            break;
                                        var str_count = PtrToStringAnsi(lpData, 5);
                                        nFrameCount = int.Parse(str_count);
                                        lpData += 5;
                                        nDataLength -= 5;
                                    }
                                    else
                                    {
                                        nFrameCount = 1;
                                    }
                                    var rows = nFrameCount;
                                    var cols = out_block.fields.Count;
                                    var datas = new List<Dictionary<string, object>>(rows);
                                    for (int i = 0; i < rows; i++)
                                    {
                                        var col_datas = new Dictionary<string, object>(cols);
                                        for (int j = 0; j < cols; j++)
                                        {
                                            var field = out_block.fields[j];
                                            var value = PtrToStringAnsi(lpData, field.size);
                                            col_datas[field.name] = ConvFieldData(field, value);
                                            lpData += field.size;
                                            nDataLength -= field.size;
                                            if (res_info.is_attr)
                                            {
                                                lpData++;
                                                nDataLength--;
                                            }
                                        }
                                        datas.Add(col_datas);
                                    }
                                    if (out_block.is_occurs)
                                    {
                                        response.body[out_block.name] = datas;
                                    }
                                    else
                                    {
                                        response.body[out_block.name] = datas[0];
                                    }
                                }
                            }
                        }
                        break;
                    default:
                        break;
                }

            }
        }
        object ConvFieldData(FieldSpec field_spec, string value)
        {
            if (field_spec.type == FieldSpec.VarType.STRING)
                return value;
            if (field_spec.type == FieldSpec.VarType.INT)
            {
                if (int.TryParse(value, out var i))
                    return i;
                return value;
            }
            if (field_spec.type == FieldSpec.VarType.LONG)
            {
                if (long.TryParse(value, out var l))
                    return l;
                return value;
            }
            if (field_spec.type == FieldSpec.VarType.DOUBLE)
            {
                if (double.TryParse(value, out var d))
                {
                    if (!value.Contains('.'))
                        d = d / field_spec.dot_value;
                    return d;
                }
                return value;
            }
            return null!;
        }

        /// <summary>
        /// 실시간 시세 등록/해제
        /// </summary>
        /// <param name="tr_cd">증권 거래코드</param>
        /// <param name="tr_key">단축코드 6자리 또는 8자리 (단건, 연속)</param>
        /// <param name="advise">시세등록: true, 시세해제: false</param>
        /// <returns>true: 요청성공, false: 요청실패</returns>
        public bool Realtime(string tr_cd, string tr_key, bool advise)
        {
            if (!Connected)
            {
                LastMessage = "Not connected";
                return false;
            }

            if (!advise && tr_cd.Length == 0)
            {
                if (_module.ETK_UnadviseWindow(Handle))
                {
                    LastMessage = "모든 실시간 해제 성공.";
                    return true;
                }
                LastMessage = "모든 실시간 해제 실패.";
                return false;
            }

            var resInfo = _resManager.GetResInfo(tr_cd);
            if (resInfo == null)
            {
                LastMessage = "자원 정보를 찾을 수 없습니다.";
                return false;
            }

            if (resInfo.is_func)
            {
                LastMessage = "실시간 요청이 아닙니다.";
                return false;
            }

            var in_datas = tr_key.Split([',']).ToList();
            var indata_line = new StringBuilder();

            if (resInfo.in_blocks.Count == 1)
            {
                var in_block = resInfo.in_blocks[0];
                if (in_block.fields.Count > 0)
                {
                    var field = in_block.fields[0];
                    if (in_datas.Count == 1)
                    {
                        var trim_data = in_datas[0].Trim();
                        if (trim_data.Length < field.size)
                        {
                            indata_line.Append(trim_data.PadRight(field.size, ' '));
                        }
                        else
                        {
                            indata_line.Append(trim_data);
                        }
                    }
                    else
                    {
                        foreach (var in_data in in_datas)
                        {
                            var trim_data = in_data.Trim();
                            if (trim_data.Length > field.size)
                            {
                                LastMessage = $"{trim_data}: 입력 데이터 길이 오류.";
                                return false;
                            }
                            indata_line.Append(trim_data.PadRight(field.size, ' '));
                        }
                    }
                }
            }
            bool bRet;
            if (advise)
            {
                bRet = _module.ETK_AdviseRealData(Handle, tr_cd, indata_line.ToString(), indata_line.Length);
            }
            else
            {
                bRet = _module.ETK_UnadviseRealData(Handle, tr_cd, indata_line.ToString(), indata_line.Length);
            }
            LastMessage = bRet ? "Realtime 요청성공" : "Realtime 요청실패";
            return bRet;
        }

        /// <summary>
        /// 부가 서비스용 TR를 해제합니다.
        /// </summary>
        public int RemoveService(string szCode, string szData) => _module.ETK_RemoveService(Handle, szCode, szData);

        private void WndProc(IntPtr hwnd, uint msg, IntPtr wParam, IntPtr lParam)
        {
            // Handle messages...

            XM xM = (XM)(msg - WM_USER);

            switch (xM)
            {
                case XM.XM_LOGOUT:
                    {
                        Connected = false;
                        OnMessageEvent?.Invoke(this, new("LOGOUT"));
                    }
                    break;
                case XM.XM_DISCONNECT:
                    {
                        Connected = false;
                        _server_connected = false;
                        OnMessageEvent?.Invoke(this, new("DISCONNECT"));
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

                                    _module.ETK_ReleaseMessageData(lParam);
                                    if (receiveFlag == RECEIVE_FLAGS.SYSTEM_ERROR_DATA)
                                    {
                                        _module.ETK_ReleaseRequestData(nRqID);
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
                                    _module.ETK_ReleaseRequestData(nRqID);
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
                        _module.ETK_ReleaseRequestData(nRqID);
                    }
                    break;
                case XM.XM_RECEIVE_LINK_DATA:
                    {
                        // HTS -> API로 연동을 등록하면, HTS에서 연동 정보가 발생시에 호출, 사용방식은 XM_RECEIVE_REAL_DATA 수신과 동일
                        // WPARAM: LINK_DATA
                        // LPARAM: LINKDATRRA_RECV_MSG 구조체 데이터
                        //var data = new LINKDATA_RECV_MSG_CLASS(lParam);
                        _module.ETK_ReleaseMessageData(lParam);
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
                        var packet = Marshal.PtrToStructure<REAL_RECV_PACKET>(lParam);
                        string szTrCode = ByteToString(packet.szTrCode);
                        string szKey = ByteToString(packet.szKeyData);
                        var nDataLength = packet.nDataLength;
                        var pszData = packet.pszData;

                        string real_cd = szTrCode;
                        if (xM == XM.XM_RECEIVE_REAL_DATA_SEARCH)
                        {
                            szTrCode = "t1857";
                            real_cd = "t1857";
                        }
                        else if (xM == XM.XM_RECEIVE_REAL_DATA_CHART)
                        {
                            szTrCode = $"ChartIndex-{wParam}";
                            real_cd = "ChartIndex";
                        }

                        var res_info = _resManager.GetResInfo(real_cd);
                        if (res_info is not null)
                        {
                            var out_block = res_info.out_blocks[0];
                            if (xM == XM.XM_RECEIVE_REAL_DATA_SEARCH || xM == XM.XM_RECEIVE_REAL_DATA_CHART)
                                out_block = res_info.out_blocks[1];

                            if (nDataLength >= out_block.record_size)
                            {
                                var cols = out_block.fields.Count;
                                var col_datas = new Dictionary<string, object>(cols);
                                for (int j = 0; j < cols; j++)
                                {
                                    var field = out_block.fields[j];
                                    var value = PtrToStringAnsi(pszData, field.size);
                                    col_datas[field.name] = ConvFieldData(field, value);
                                    pszData += field.size;
                                    if (res_info.is_attr)
                                    {
                                        pszData++;
                                    }
                                }
                                OnRealtimeEvent?.Invoke(this, new(szTrCode, szKey, col_datas));
                            }
                        }
                    }
                    break;
                default:
                    break;
            }

            return;

        }

        /// <summary>
        /// 모드 설정
        /// </summary>
        /// <param name="mode"></param>
        /// <param name="value"></param>
        public void SetMode(string mode, string value)
        {
            _module.ETK_SetMode(mode, value);
        }
    }
}
