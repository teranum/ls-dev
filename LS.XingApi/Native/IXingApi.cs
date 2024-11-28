using System.Runtime.InteropServices;
using System.Text;
using HWND = nint;
using LPARAM = nint;

#nullable disable

namespace LS.XingApi.Native
{
    /// <summary>
    /// XingAPI.dll의 Native 함수를 호출하기 위한 클래스
    /// </summary>
    internal class IXingApi
    {
        private const string XING_DLL = "XingAPI.dll";
        private const string XING64_DLL = "XingAPI64.dll";
        [DllImport("kernel32.dll")] private static extern IntPtr LoadLibrary(string dllToLoad);

        // GetProcAddress
        [DllImport("kernel32.dll")] private static extern IntPtr GetProcAddress(IntPtr hModule, string procedureName);

        // FreeLibrary
        [DllImport("kernel32.dll")] private static extern bool FreeLibrary(IntPtr hModule);

        private IntPtr _moduleHandle;
        /// <summary>
        /// Returns true if the DLL is loaded.
        /// </summary>
        public bool IsLoaded => _moduleHandle != IntPtr.Zero;
        /// <summary>
        /// XingAPI.dll의 Native 함수를 호출하기 위한 클래스
        /// </summary>
        /// <param name="dll_path"></param>
        public IXingApi(string dll_path = "")
        {
            _moduleHandle = LoadLibrary(dll_path);
            if (_moduleHandle != 0)
            {
                _ETK_Connect = GetDelegateFromFuncName<ETK_Connect_Handler>();
                _ETK_IsConnected = GetDelegateFromFuncName<ETK_IsConnected_Handler>();
                _ETK_Disconnect = GetDelegateFromFuncName<ETK_Disconnect_Handler>();
                _ETK_Login = GetDelegateFromFuncName<ETK_Login_Handler>();
                _ETK_Logout = GetDelegateFromFuncName<ETK_Logout_Handler>();
                _ETK_GetLastError = GetDelegateFromFuncName<ETK_GetLastError_Handler>();
                _ETK_GetErrorMessage = GetDelegateFromFuncName<ETK_GetErrorMessage_Handler>();
                _ETK_Request = GetDelegateFromFuncName<ETK_Request_Handler>();
                _ETK_ReleaseRequestData = GetDelegateFromFuncName<ETK_ReleaseRequestData_Handler>();
                _ETK_ReleaseMessageData = GetDelegateFromFuncName<ETK_ReleaseMessageData_Handler>();
                _ETK_AdviseRealData = GetDelegateFromFuncName<ETK_AdviseRealData_Handler>();
                _ETK_UnadviseRealData = GetDelegateFromFuncName<ETK_UnadviseRealData_Handler>();
                _ETK_UnadviseWindow = GetDelegateFromFuncName<ETK_UnadviseWindow_Handler>();
                _ETK_GetAccountListCount = GetDelegateFromFuncName<ETK_GetAccountListCount_Handler>();
                _ETK_GetAccountList = GetDelegateFromFuncName<ETK_GetAccountList_Handler>();
                _ETK_GetAccountName = GetDelegateFromFuncName<ETK_GetAccountName_Handler>();
                _ETK_GetAcctDetailName = GetDelegateFromFuncName<ETK_GetAcctDetailName_Handler>();
                _ETK_GetAcctNickname = GetDelegateFromFuncName<ETK_GetAcctNickname_Handler>();
                _ETK_GetCommMedia = GetDelegateFromFuncName<ETK_GetCommMedia_Handler>();
                _ETK_GetETKMedia = GetDelegateFromFuncName<ETK_GetETKMedia_Handler>();
                _ETK_GetClientIP = GetDelegateFromFuncName<ETK_GetClientIP_Handler>();
                _ETK_GetServerName = GetDelegateFromFuncName<ETK_GetServerName_Handler>();
                _ETK_GetAPIPath = GetDelegateFromFuncName<ETK_GetAPIPath_Handler>();
                _ETK_SetHeaderInfo = GetDelegateFromFuncName<ETK_SetHeaderInfo_Handler>();
                _ETK_SetUseAPIVer = GetDelegateFromFuncName<ETK_SetUseAPIVer_Handler>();
                _ETK_SetMode = GetDelegateFromFuncName<ETK_SetMode_Handler>();
                _ETK_GetProcBranchNo = GetDelegateFromFuncName<ETK_GetProcBranchNo_Handler>();
                _ETK_GetUseOverFuture = GetDelegateFromFuncName<ETK_GetUseOverFuture_Handler>();
                _ETK_GetUseFX = GetDelegateFromFuncName<ETK_GetUseFX_Handler>();
                _ETK_GetTRCountPerSec = GetDelegateFromFuncName<ETK_GetTRCountPerSec_Handler>();
                _ETK_GetTRCountBaseSec = GetDelegateFromFuncName<ETK_GetTRCountBaseSec_Handler>();
                _ETK_GetTRCountRequest = GetDelegateFromFuncName<ETK_GetTRCountRequest_Handler>();
                _ETK_GetTRCountLimit = GetDelegateFromFuncName<ETK_GetTRCountLimit_Handler>();
                _ETK_SetNotifyFlag = GetDelegateFromFuncName<ETK_SetNotifyFlag_Handler>();
                _ETK_RequestService = GetDelegateFromFuncName<ETK_RequestService_Handler>();
                _ETK_RemoveService = GetDelegateFromFuncName<ETK_RemoveService_Handler>();
                _ETK_RequestLinkToHTS = GetDelegateFromFuncName<ETK_RequestLinkToHTS_Handler>();
                _ETK_AdviseLinkFromHTS = GetDelegateFromFuncName<ETK_AdviseLinkFromHTS_Handler>();
                _ETK_UnAdviseLinkFromHTS = GetDelegateFromFuncName<ETK_UnAdviseLinkFromHTS_Handler>();
                _ETK_Decompress = GetDelegateFromFuncName<ETK_Decompress_Handler>();
                _ETK_IsChartLib = GetDelegateFromFuncName<ETK_IsChartLib_Handler>();
                _ETK_SetProgramOrder = GetDelegateFromFuncName<ETK_SetProgramOrder_Handler>();
                _ETK_GetProgramOrder = GetDelegateFromFuncName<ETK_GetProgramOrder_Handler>();
                _ETK_GetUseOverStock = GetDelegateFromFuncName<ETK_GetUseOverStock_Handler>();
            }
        }

        /// <summary>
        /// Returns a delegate for a function inside the DLL.
        /// </summary>
        /// <typeparam name="TDelegate">The type of the delegate.</typeparam>
        /// <returns>A delegate instance of type TDelegate</returns>
        private TDelegate GetDelegateFromFuncName<TDelegate>() where TDelegate : class
        {
            string funcName = typeof(TDelegate).Name;
            // 마지막 "_Handler" 제거
            if (funcName.EndsWith("_Handler"))
                funcName = funcName.Substring(0, funcName.Length - 8);
            var ptr = GetProcAddress(_moduleHandle, funcName);
            if (ptr == IntPtr.Zero)
                return null!;
            var func = Marshal.GetDelegateForFunctionPointer(ptr, typeof(TDelegate)) as TDelegate;
            return func!;
        }

        /// <summary>
        /// 서버에 연결합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle</param>
        /// <param name="pszSvrIP">연결할 서버 IP</param>
        /// <param name="nPort">연결할 서버 Port</param>
        /// <param name="nStartMsgID">시작 MessageID</param>
        /// <param name="nTimeOut">연결시도 시간 - millisecond단위(1/1000초), -1 은 기본값(10초)으로 설정</param>
        /// <param name="nSendMaxPacketSize">전송시 최대 Packet Size, -1은 기본값으로 설정</param>
        /// <returns>0(FALSE) 이면 실패, 1(TRUE) 이면 성공</returns>
        public static bool ETK_Connect(HWND hWnd, string pszSvrIP, int nPort, int nStartMsgID, int nTimeOut, int nSendMaxPacketSize)
            => _ETK_Connect(hWnd, pszSvrIP, nPort, nStartMsgID, nTimeOut, nSendMaxPacketSize);
        private delegate bool ETK_Connect_Handler(HWND hWnd, string pszSvrIP, int nPort, int nStartMsgID, int nTimeOut, int nSendMaxPacketSize);
        private static ETK_Connect_Handler _ETK_Connect;

        /// <summary>
        /// 서버와의 연결여부를 취득합니다.
        /// </summary>
        /// <returns>0(FALSE) 이면 연결중 아님, 1(TRUE) 이면 연결중</returns>
        public bool ETK_IsConnected() => _ETK_IsConnected();
        private delegate bool ETK_IsConnected_Handler();
        private ETK_IsConnected_Handler _ETK_IsConnected;


        /// <summary>
        /// 서버와의 연결을 종료합니다.
        /// </summary>
        /// <returns>무조건 1(TRUE)</returns>
        public static bool ETK_Disconnect() => _ETK_Disconnect();
        private delegate bool ETK_Disconnect_Handler();
        private static ETK_Disconnect_Handler _ETK_Disconnect;

        // 로그인
        /// <summary>
        /// 서버에 로그인합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle</param>
        /// <param name="pszID">로그인 ID</param>
        /// <param name="pszPwd">로그인 ID에 대한 비밀번호</param>
        /// <param name="pszCertPwd">공인인증 비밀번호</param>
        /// <param name="nType">무조건 0</param>
        /// <param name="bShowCertErrDlg">공인인증 시 발생한 에러에 대해 미리 정의된 Dialog를 표시할 지 여부</param>
        /// <returns>0 이 아니면 성공(로그인 성공이 아니라 서버로 로그인요청 전송성공을 의미), 0 이면 실패</returns>
        public static bool ETK_Login(HWND hWnd, string pszID, string pszPwd, string pszCertPwd, int nType, bool bShowCertErrDlg)
            => _ETK_Login(hWnd, pszID, pszPwd, pszCertPwd, nType, bShowCertErrDlg);
        private delegate bool ETK_Login_Handler(HWND hWnd, string pszID, string pszPwd, string pszCertPwd, int nType, bool bShowCertErrDlg);
        private static ETK_Login_Handler _ETK_Login;

        /// <summary>
        /// 로그아웃합니다.
        /// </summary>
        /// <param name="hWnd"></param>
        /// <returns></returns>
        public static bool ETK_Logout(HWND hWnd) => _ETK_Logout(hWnd);
        private delegate bool ETK_Logout_Handler(HWND hWnd);
        /// <inheritdoc cref="ETK_Logout_Handler"/>
        private static ETK_Logout_Handler _ETK_Logout;

        /// <summary>
        /// 마지막에 발생한 Error Code를 취득합니다.
        /// </summary>
        /// <returns></returns>
        public static int ETK_GetLastError() => _ETK_GetLastError();
        private delegate int ETK_GetLastError_Handler();
        /// <inheritdoc cref="ETK_GetLastError_Handler"/>
        private static ETK_GetLastError_Handler _ETK_GetLastError;

        /// <summary>
        /// Error Code에 대한 메시지를 취득합니다.
        /// </summary>
        /// <param name="nErrorCode">Error Code</param>
        /// <param name="pszMsg">Message를 받을 Buffer, 충분한 메모리가 확보되어야 합니다</param>
        /// <param name="nMsgSize">Buffer 크기</param>
        /// <returns>Message 길이</returns>
        public static int ETK_GetErrorMessage(int nErrorCode, StringBuilder pszMsg, int nMsgSize)
            => _ETK_GetErrorMessage(nErrorCode, pszMsg, nMsgSize);
        private delegate int ETK_GetErrorMessage_Handler(int nErrorCode, StringBuilder pszMsg, int nMsgSize);
        private static ETK_GetErrorMessage_Handler _ETK_GetErrorMessage;


        /// <summary>
        /// 조회TR을 서버에 전송하기 위해 사용합니다.
        /// 조회TR에 대한 수신데이터는 XM_RECEIVE_DATA 메시지로 전송됩니다.
        /// </summary>
        /// <param name="hWnd">Window Handle. 수신 데이터를 받을 윈도우입니다. 수신데이터는 XM_RECEIVE_DATA 메시지로 옵니다.</param>
        /// <param name="pszCode">요청할 TR Code</param>
        /// <param name="lpData">요청할 pszData</param>
        /// <param name="nDataSize">pszData 의 메모리 크기</param>
        /// <param name="bNext">연속조회 여부. 연속조회일 경우에 설정합니다</param>
        /// <param name="pszNextKey">연속조회 키</param>
        /// <param name="nTimeOut">설정한 시간(초)내에 수신 데이터가 오지 않을 경우 XM_TIMEOUT 이 발생합니다.</param>
        /// <returns>0보다 작을 경우엔 실패이며, 0 또는 0보다 클 경우엔 Requests ID를 반환합니다.</returns>
        public static int ETK_Request(HWND hWnd, string pszCode, byte[] lpData, int nDataSize, bool bNext, string pszNextKey, int nTimeOut)
            => _ETK_Request(hWnd, pszCode, lpData, nDataSize, bNext, pszNextKey, nTimeOut);
        private delegate int ETK_Request_Handler(HWND hWnd, string pszCode, [MarshalAs(UnmanagedType.LPArray, SizeParamIndex = 0)] byte[] lpData, int nDataSize, bool bNext, string pszNextKey, int nTimeOut);
        private static ETK_Request_Handler _ETK_Request;

        /// <summary>
        /// 수신 데이터를 삭제하고 RequestID를 해제합니다.
        /// MSG_PACKET의 메모리를 해제합니다.
        /// MSG_PACKET이 System Error 이면 Requests ID도 같이 해제합니다.
        /// </summary>
        /// <param name="nRequestID">해제할 Requests ID</param>
        public static void ETK_ReleaseRequestData(int nRequestID) => _ETK_ReleaseRequestData(nRequestID);
        private delegate void ETK_ReleaseRequestData_Handler(int nRequestID);
        private static ETK_ReleaseRequestData_Handler _ETK_ReleaseRequestData;

        /// <summary>
        /// 수신 메시지를 삭제합니다.<br/>
        /// MSG_PACKET이 System Error 이면 Requests ID도 같이 해제합니다
        /// </summary>
        /// <param name="lparam">XM_RECEIVE_DATA로 받은 LPARAM 데이터, MSG_PACKET_CLASS 의 Memory Pointer 입니다.</param>
        public static void ETK_ReleaseMessageData(LPARAM lparam) => _ETK_ReleaseMessageData(lparam);
        private delegate void ETK_ReleaseMessageData_Handler(LPARAM lparam);
        private static ETK_ReleaseMessageData_Handler _ETK_ReleaseMessageData;

        /// <summary>
        /// 실시간 TR을 등록합니다.
        /// 실시간 데이터를 요청합니다.
        /// 수신데이터는 XM_RECEIVE_REAL_DATA 메시지로 전송됩니다.
        /// ETK_UnadviseRealData() 를 요청하기 전까지 실시간 데이터가 수신됩니다.
        /// 한번 요청시에 여러 데이터를 요청할 수 있습니다 "078020005930", 데이터 사이즈는 6
        /// </summary>
        /// <param name="hWnd">Window Handle, XM_RECEIVE_REAL_DATA 메시지가 전송됩니다</param>
        /// <param name="pszTrCode">등록할 TR Code</param>
        /// <param name="pszData">등록할 데이터</param>
        /// <param name="nDataUnitLen">등록할 데이터의 Unit 크기</param>
        /// <returns>0(FALSE)이면 실패, 1(TRUE)이면 성공</returns>
        public static bool ETK_AdviseRealData(HWND hWnd, string pszTrCode, string pszData, int nDataUnitLen)
            => _ETK_AdviseRealData(hWnd, pszTrCode, pszData, nDataUnitLen);
        private delegate bool ETK_AdviseRealData_Handler(HWND hWnd, string pszTrCode, string pszData, int nDataUnitLen);
        private static ETK_AdviseRealData_Handler _ETK_AdviseRealData;

        /// <summary>
        /// 등록된 실시간 TR을 해제합니다.
        /// 한번 해제 시에 여러 데이터를 해제할 수 있습니다 "078020005930", 데이터 사이즈는 6
        /// 등록할 때 A 종목과 B 종목을 한번에 등록하고 C 종목과 D 종목을 한번에 등록하였어도 해제할 때는 A,C 종목을 한번에 해제 가능하며 각각 해제도 가능합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle. 실시간이 등록된 윈도우</param>
        /// <param name="pszTrCode">등록 해제할 TR Code</param>
        /// <param name="pszData">등록 해제할 데이터</param>
        /// <param name="nDataUnitLen">등록 해제할 데이터의 Unit 크기</param>
        /// <returns>0(FALSE)이면 실패, 1(TRUE)이면 성공</returns>
        public static bool ETK_UnadviseRealData(HWND hWnd, string pszTrCode, string pszData, int nDataUnitLen)
            => _ETK_UnadviseRealData(hWnd, pszTrCode, pszData, nDataUnitLen);
        private delegate bool ETK_UnadviseRealData_Handler(HWND hWnd, string pszTrCode, string pszData, int nDataUnitLen);
        private static ETK_UnadviseRealData_Handler _ETK_UnadviseRealData;

        /// <summary>
        /// 윈도우에 등록된 모든 실시간 TR을 해제합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle. 실시간이 등록된 윈도우</param>
        /// <returns>0(FALSE)이면 실패, 1(TRUE)이면 성공</returns>
        public bool ETK_UnadviseWindow(HWND hWnd) => _ETK_UnadviseWindow(hWnd);
        private delegate bool ETK_UnadviseWindow_Handler(HWND hWnd);
        private ETK_UnadviseWindow_Handler _ETK_UnadviseWindow;

        /// <summary>
        /// 계좌리스트의 개수를 취득합니다.
        /// </summary>
        /// <returns>계좌 갯수</returns>
        public static int ETK_GetAccountListCount() => _ETK_GetAccountListCount();
        private delegate int ETK_GetAccountListCount_Handler();
        private static ETK_GetAccountListCount_Handler _ETK_GetAccountListCount;

        /// <summary>
        /// 계좌를 취득합니다.
        /// </summary>
        /// <param name="nIndex">받아올 계좌의 Index. 0 &lt;= Index &lt; ETK_GetAccountListCount().</param>
        /// <param name="pszData">계좌를 받을 Buffer. 최소 12 바이트는 할당되어 있어야 합니다.</param>
        /// <param name="nDataSize">pszData의 사이즈</param>
        /// <returns>0(FALSE)이면 실패, 1(TRUE)이면 성공</returns>
        public static bool ETK_GetAccountList(int nIndex, StringBuilder pszData, int nDataSize) => _ETK_GetAccountList(nIndex, pszData, nDataSize);
        private delegate bool ETK_GetAccountList_Handler(int nIndex, StringBuilder pszData, int nDataSize);
        private static ETK_GetAccountList_Handler _ETK_GetAccountList;

        /// <summary>
        /// 계좌의 이름을 취득합니다.
        /// </summary>
        /// <param name="pszAcc">계좌번호</param>
        /// <param name="pszData">데이터를 받을 Buffer, 최소 41바이트가 할당되어 있어야 합니다</param>
        /// <param name="nDataSize">pszData의 사이즈</param>
        public static void ETK_GetAccountName(string pszAcc, StringBuilder pszData, int nDataSize) => _ETK_GetAccountName(pszAcc, pszData, nDataSize);
        private delegate void ETK_GetAccountName_Handler(string pszAcc, StringBuilder pszData, int nDataSize);
        private static ETK_GetAccountName_Handler _ETK_GetAccountName;

        /// <summary>
        /// 계좌 상세명을 취득합니다.
        /// </summary>
        /// <param name="pszAcc">계좌번호</param>
        /// <param name="pszData">데이터를 받을 Buffer, 최소 41바이트가 할당되어 있어야 합니다</param>
        /// <param name="nDataSize">pszData의 사이즈</param>
        public static void ETK_GetAcctDetailName(string pszAcc, StringBuilder pszData, int nDataSize) => _ETK_GetAcctDetailName(pszAcc, pszData, nDataSize);
        private delegate void ETK_GetAcctDetailName_Handler(string pszAcc, StringBuilder pszData, int nDataSize);
        private static ETK_GetAcctDetailName_Handler _ETK_GetAcctDetailName;

        /// <summary>
        /// 계좌 별명을 취득합니다.
        /// </summary>
        /// <param name="pszAcc">계좌번호</param>
        /// <param name="pszData">데이터를 받을 Buffer, 최소 51바이트가 할당되어 있어야 합니다</param>
        /// <param name="nDataSize">pszData의 사이즈</param>
        public static void ETK_GetAcctNickname(string pszAcc, StringBuilder pszData, int nDataSize) => _ETK_GetAcctNickname(pszAcc, pszData, nDataSize);
        private delegate void ETK_GetAcctNickname_Handler(string pszAcc, StringBuilder pszData, int nDataSize);
        private static ETK_GetAcctNickname_Handler _ETK_GetAcctNickname;

        /// <summary>
        /// 통신매체를 구한다.
        /// </summary>
        /// <param name="pszData"></param>
        /// <returns></returns>
        public static void ETK_GetCommMedia(StringBuilder pszData) => _ETK_GetCommMedia(pszData);
        private delegate void ETK_GetCommMedia_Handler(StringBuilder pszData);
        private static ETK_GetCommMedia_Handler _ETK_GetCommMedia;

        /// <summary>
        /// 당사매체를 구한다.
        /// </summary>
        /// <param name="pszData"></param>
        public static void ETK_GetETKMedia(StringBuilder pszData) => _ETK_GetETKMedia(pszData);
        private delegate void ETK_GetETKMedia_Handler(StringBuilder pszData);
        private static ETK_GetETKMedia_Handler _ETK_GetETKMedia;

        /// <summary>
        /// 공인IP를 구한다.
        /// </summary>
        /// <param name="pszData"></param>
        public static void ETK_GetClientIP(StringBuilder pszData) => _ETK_GetClientIP(pszData);
        private delegate void ETK_GetClientIP_Handler(StringBuilder pszData);
        private static ETK_GetClientIP_Handler _ETK_GetClientIP;

        /// <summary>
        /// 접속한 서버의 서버명을 취득합니다.
        /// </summary>
        /// <param name="pszData">데이터를 받을 Buffer, 최소 51바이트가 할당되어 있어야 합니다.</param>
        public static void ETK_GetServerName(StringBuilder pszData) => _ETK_GetServerName(pszData);
        private delegate void ETK_GetServerName_Handler(StringBuilder pszData);
        private static ETK_GetServerName_Handler _ETK_GetServerName;

        /// <summary>
        /// 실행중인 xingAPI의 경로
        /// </summary>
        /// <param name="pszData"></param>
        public static void ETK_GetAPIPath(StringBuilder pszData) => _ETK_GetAPIPath(pszData);
        private delegate void ETK_GetAPIPath_Handler(StringBuilder pszData);
        private static ETK_GetAPIPath_Handler _ETK_GetAPIPath;

        /// <summary>
        /// ETK_SetHeaderInfo
        /// </summary>
        /// <param name="szType"></param>
        /// <param name="szValue"></param>
        public void ETK_SetHeaderInfo(string szType, string szValue) => _ETK_SetHeaderInfo(szType, szValue);
        private delegate void ETK_SetHeaderInfo_Handler(string szType, string szValue);
        private ETK_SetHeaderInfo_Handler _ETK_SetHeaderInfo;

        /// <summary>
        /// ETK_SetUseAPIVer
        /// </summary>
        /// <param name="szUserAPIVer"></param>
        public void ETK_SetUseAPIVer(string szUserAPIVer) => _ETK_SetUseAPIVer(szUserAPIVer);
        private delegate void ETK_SetUseAPIVer_Handler(string szUserAPIVer);
        private ETK_SetUseAPIVer_Handler _ETK_SetUseAPIVer;

        /// <summary>
        /// DevCenter인 경우 사용할 수 있는 기능을 설정합니다.<br/>
        /// ETK_SetMode("_ServiceMode_", "DevCenter");<br/>
        /// LoadLibHelper 호출 후 사용해야 합니다.
        /// </summary>
        /// <param name="pszMode"></param>
        /// <param name="pszValue"></param>
        public void ETK_SetMode(string pszMode, string pszValue) => _ETK_SetMode(pszMode, pszValue);
        private delegate void ETK_SetMode_Handler(string pszMode, string pszValue);
        private ETK_SetMode_Handler _ETK_SetMode;

        /// <summary>
        /// 처리점을 구한다.
        /// </summary>
        /// <param name="pszData"></param>
        public static void ETK_GetProcBranchNo(StringBuilder pszData) => _ETK_GetProcBranchNo(pszData);
        private delegate void ETK_GetProcBranchNo_Handler(StringBuilder pszData);
        private static ETK_GetProcBranchNo_Handler _ETK_GetProcBranchNo;

        /// <summary>
        /// 해외선물 사용권한
        /// </summary>
        public bool ETK_GetUseOverFuture() => _ETK_GetUseOverFuture();
        private delegate bool ETK_GetUseOverFuture_Handler();
        private ETK_GetUseOverFuture_Handler _ETK_GetUseOverFuture;

        /// <summary>
        /// FX 사용권한
        /// </summary>
        public bool ETK_GetUseFX() => _ETK_GetUseFX();
        private delegate bool ETK_GetUseFX_Handler();
        private ETK_GetUseFX_Handler _ETK_GetUseFX;

        /// <summary>
        /// TR의 초당 전송 가능 횟수를 취득합니다.
        /// </summary>
        /// <param name="pszCode">TR Code</param>
        /// <returns>TR의 초당 전송 가능 횟수</returns>
        public static int ETK_GetTRCountPerSec(string pszCode) => _ETK_GetTRCountPerSec(pszCode);
        private delegate int ETK_GetTRCountPerSec_Handler(string pszCode);
        private static ETK_GetTRCountPerSec_Handler _ETK_GetTRCountPerSec;

        /// <summary>
        /// TR의 초당 전송 가능 횟수(Base)를 취득합니다.
        /// 1초당 1건 전송 가능시 1, 5초당 1건 전송 가능시 5를 취득합니다.
        /// </summary>
        /// <param name="pszCode">TR Code</param>
        /// <returns>Base 시간(초단위)</returns>
        public static int ETK_GetTRCountBaseSec(string pszCode) => ETK_GetTRCountBaseSec(pszCode);
        private delegate int ETK_GetTRCountBaseSec_Handler(string pszCode);
        private static ETK_GetTRCountBaseSec_Handler _ETK_GetTRCountBaseSec;

        /// <summary>
        /// TR의 초당 전송 가능 횟수를 취득합니다.
        /// </summary>
        /// <param name="pszCode">TR Code</param>
        /// <returns>10분내 요청한 해당 TR의 총 횟수</returns>
        public static int ETK_GetTRCountRequest(string pszCode) => _ETK_GetTRCountRequest(pszCode);
        private delegate int ETK_GetTRCountRequest_Handler(string pszCode);
        private static ETK_GetTRCountRequest_Handler _ETK_GetTRCountRequest;

        /// <summary>
        /// TR의 초당 전송 가능 횟수를 취득합니다.
        /// </summary>
        /// <param name="pszCode">TR Code</param>
        /// <returns>TR의 10분당 제한 건수. 제한이 없는 경우 0 을 반환합니다.</returns>
        public static int ETK_GetTRCountLimit(string pszCode) => _ETK_GetTRCountLimit(pszCode);
        private delegate int ETK_GetTRCountLimit_Handler(string pszCode);
        private static ETK_GetTRCountLimit_Handler _ETK_GetTRCountLimit;

        /// <summary>
        /// 긴급메시지, 서버접속 단절통지 등의 통보 설정 (지원 예정)
        /// </summary>
        /// <param name="bNotifyFlag"></param>
        public void ETK_SetNotifyFlag(bool bNotifyFlag) => _ETK_SetNotifyFlag(bNotifyFlag);
        private delegate void ETK_SetNotifyFlag_Handler(bool bNotifyFlag);
        private ETK_SetNotifyFlag_Handler _ETK_SetNotifyFlag;

        /// <summary>
        /// 부가 서비스용 TR을 서버에 요청합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle. 수신 데이터를 받을 윈도우입니다. 수신데이터는 XM_RECEIVE_DATA 메시지로 옵니다.</param>
        /// <param name="pszCode"></param>
        /// <param name="pszData"></param>
        /// <returns>ETK_Request() 함수와 동일합니다. 0보다 작을 경우엔 실패이며, 0 또는 0보다 클 경우엔 Requests ID를 반환합니다.</returns>
        /// <remarks>
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★  [1] 종목 검색        
        /// <br/> ★★★★★
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/>
        /// <br/>     pszCode		- "t1833" (HTS '[1807] 종목검색' 에서 'API 로 내보내기' 저장한 조건의 종목을 검색하는 TR)
        /// <br/>     lpData		- 'API로 내보내기' 한 파일의 전체 경로 지정, NULL 입력시 파일다이얼로그 표시
        /// <br/>
        /// <br/>     ex) HTS '[1807] 종목검색' 에서 'API 로 내보내기' 저장한 파일이 "D:\test.adf"
        /// <br/>			pszCode = "t1833", pszData = "D:\test.adf"   
        /// <br/>			int nReqID = RequestService( hWnd, "t1833", "D:\test.adf" );	
        /// <br/> 
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★  [2] ~ [3] 차트 기초데이터를 이용해 지표데이터를 제공
        /// <br/> ★★★★★
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/>
        /// <br/>	지표데이터는 챠트 기초데이터를 수신받아 API내부에서 가공하여 제공하는 것으로 조회 및 실시간 응답에 
        /// <br/>  다소 시간이 걸릴 수 있습니다.
        /// <br/>  자료실게시판 내에 "ChartApiSample(VC++ 2012)" 샘플을 참고하시기 바랍니다.
        /// <br/>
        /// <br/>  ※ 조회시 실시간 자동등록을 하면, 실시간 지표데이터 발생시 XM_RECEIVE_REAL_DATA_CHART 로 메시지가 수신
        /// <br/>	  WPARAM = 해당 없음 
        /// <br/>	  LPARAM = LPRECV_REAL_PACKET (RECV_REAL_PACKET 의 pszData  = 조회 TR의 outblock1과 동일)
        /// <br/>
        /// <br/>
        /// <br/>  [2] 차트 지표데이터 조회 (HTS '[4201]xing차트1'의 수식관리자내 지표와 동일하며, DevCenter 메뉴 [부가서비스-수식관리자] 를 통해 지표 저장)
        /// <br/>
        /// <br/>     pszCode		- "ChartIndex" (차트 지표데이터 조회용 TR)
        /// <br/>     lpData		- "ChartIndex" TR내 Inblock의 데이터 구조체
        /// <br/>
        /// <br/>     ex) "MACD" 지표데이터 조회
        /// <br/>         ChartIndexInBlock sInBlock;
        /// <br/>         sInBlock.indexid		= 지표ID	 // 최초 조회시 공백, '동일 종목 - 동일 지표' 조회시 이전 조회 ChartIndexOutBlock의 indexid
        /// <br/>         sInBlock.indexname	= "MACD" 
        /// <br/>         sInBlock.market		= "1"		 // 주식
        /// <br/>         ...생략.. 
        /// <br/>		   RemoveService( hWnd, "ChartIndex", sInBlock.indexid );				
        /// <br/>         int nReqID = RequestService( hWnd, "ChartIndex", <![CDATA[&]]>sInBlock );	
        /// <br/> 
        /// <br/> 
        /// <br/> [3] 차트 엑셀데이터 조회 (HTS '[4201]xing차트1'의 수식관리자내 지표와 동일하며, DevCenter 메뉴 [부가서비스-수식관리자] 를 통해 지표 저장)
        /// <br/>     직접 저장한 차트 기초데이터를 엑셀 포맷으로 변경한 후, RequestService() 호출 시 지표데이터로 가공하여 제공  
        /// <br/>     ("xingAPI 설치폴더/엑셀샘플/ChartExcelData.xls" 참고)
        /// <br/>
        /// <br/>     pszCode		- "ChartExcel" (차트 지표데이터 조회용 TR)
        /// <br/>     lpData		- "ChartExcel" TR내 Inblock의 데이터 구조체
        /// <br/>
        /// <br/>     ex) 직접 쌓은 시고저종 데이터를 엑셀 포맷으로 변환하여 저장한 파일이 "C:\ebest\xingAPI\엑셀샘플\ChartExcelData.xls"
        /// <br/>         ChartExcelInBlock sInBlock;
        /// <br/>          sInBlock.indexid		= 지표ID	 // 최초 조회시 공백, '동일 종목 - 동일 지표' 조회시 이전 조회 ChartIndexOutBlock의 indexid
        /// <br/>         sInBlock.indexname		= "MACD"		
        /// <br/>         sInBlock.excelfilename	= "C:\ebest\xingAPI\엑셀샘플\ChartExcelData.xls"
        /// <br/>         ...생략.. 
        /// <br/>         RemoveService( hWnd, "ChartExcel", sInBlock.indexid );				
        /// <br/>         int nReqID = RequestService( hWnd, "ChartExcel", <![CDATA[&]]>sInBlock );	
        /// <br/> 
        /// <br/>
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★  [4] ~ [5] e종목검색 실시간 데이터 제공
        /// <br/> ★★★★★
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/>
        /// <br/>  자료실게시판 내에 "XingAPI_Sample_eSearch" 샘플을 참고하시기 바랍니다.
        /// <br/>
        /// <br/>  ※ 조회시 실시간 자동등록을 하면, 실시간 데이터 발생시 XM_RECEIVE_REAL_DATA_SEARCH 로 메시지가 수신
        /// <br/>	  WPARAM = 해당 없음 
        /// <br/>	  LPARAM = LPRECV_REAL_PACKET (RECV_REAL_PACKET 의 pszData  = 조회 TR의 outblock1과 동일)
        /// <br/>
        /// <br/>
        /// <br/>  [4] 종목검색 데이터 조회
        /// <br/>
        /// <br/>     pszCode		- "t1857" (HTS '[1892] e종목검색' 에서 'API 로 내보내기' 혹은 '전략관리 -> 서버저장' 으로  저장한 조건의 종목을 검색하는 TR)
        /// <br/>     lpData		- "t1857" TR내 Inblock의 데이터 구조체
        /// <br/>
        /// <br/>     ex) 종목검색 
        /// <br/>         t1857InBlock	pckInBlock;
        /// <br/>		   TCHAR		szTrNo[]	= "t1857";
        /// <br/>		   char			szNextKey[]	= "";
        /// <br/>         ...생략.. 
        /// <br/>		   SetPacketData( pckInBlock.sRealFlag		, sizeof( pckInBlock.sRealFlag		), str_Real	   , DATA_TYPE_STRING );	// 실시간 여부 1:등록 0:조회만
        /// <br/>		   SetPacketData( pckInBlock.sSearchFlag	, sizeof( pckInBlock.sSearchFlag	), str_Flag	   , DATA_TYPE_STRING );	// 조회구분값 S:서버 F:파일
        /// <br/>		   SetPacketData( pckInBlock.query_index	, sizeof( pckInBlock.query_index	), str_Index   , DATA_TYPE_STRING );	// 종목검색입력값
        /// <br/>         int nReqID = RequestService( hWnd, szTrNo, (LPCTSTR)<![CDATA[&]]>pckInBlock );	
        /// <br/> 
        /// <br/> 
        /// <br/> [5] 종목검색 실시간 데이터 발생 시 XM_RECEIVE_REAL_DATA_SEARCH로 메세지 수신
        /// <br/>
        /// <br/>	   WPARAM = 해당 없음 
        /// <br/>	   LPARAM = LPRECV_REAL_PACKET (RECV_REAL_PACKET 의 pszData  = 조회 TR의 outblock1과 동일)
        /// <br/>
        /// <br/>     ex) LPRECV_REAL_PACKET pRealPacket = (LPRECV_REAL_PACKET)lParam;
        /// <br/>		   LPt1857OutBlock1 pOutBlock = (LPt1857OutBlock1)pRealPacket->pszData;
        /// <br/> 
        /// <br/> 	
        /// </remarks>
        public static int ETK_RequestService(HWND hWnd, string pszCode, byte[] pszData) => _ETK_RequestService(hWnd, pszCode, pszData);
        private delegate int ETK_RequestService_Handler(HWND hWnd, string pszCode, [MarshalAs(UnmanagedType.LPArray, SizeParamIndex = 0)] byte[] pszData);
        private static ETK_RequestService_Handler _ETK_RequestService;

        /// <summary>
        /// 부가 서비스용 TR을 해제합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle. 수신 데이터를 받을 윈도우입니다.</param>
        /// <param name="pszCode"></param>
        /// <param name="pszData"></param>
        /// <returns></returns>
        /// <remarks>
        /// <br/> 부가 서비스 조회 TR 해제
        /// <br/>     반환값       - 부가서비스에 따라 달라짐
        /// <br/>     hWnd			- 조회 결과를 받을 윈도우의 핸들
        /// <br/>
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★  [1] 종목 검색
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/>
        /// <br/>		해당 없음
        /// <br/>
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★  [2] ~ [3] 차트데이터 조회 
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/>
        /// <br/>		지표데이터는 챠트 기초데이터를 수신받아 API내부에서 가공하여 제공하는 것으로
        /// <br/>      많이 조회할수록 API에 부하가 갈 수 있으니, 사용하지 않는 지표는 해제하는 것이 좋습니다.
        /// <br/>
        /// <br/>
        /// <br/>		※ 조회 시 자동등록한 실시간을 해제할 때도 호출함
        /// <br/>
        /// <br/>     pszCode		- "ChartIndex" or "ChartExcel" 
        /// <br/>     lpData		- 각 TR의  OutBlock의 indexid
        /// <br/>
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★  [4] ~ [5] e종목검색 조회 
        /// <br/> ★★★★★ 
        /// <br/> ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
        /// <br/>
        /// <br/>		실시간 종목검색은 등록 갯수에 제한이 있기때문에, 사용하지 않는 경우 해제하는 것이 좋습니다(기본 2개)
        /// <br/>
        /// <br/>
        /// <br/>
        /// <br/>     pszCode		- "t1857"
        /// <br/>     lpData		- t1857 TR의 OutBlock의 AlertNum 값
        /// <br/>
        /// </remarks>
        public static int ETK_RemoveService(HWND hWnd, string pszCode, string pszData) => _ETK_RemoveService(hWnd, pszCode, pszData);
        private delegate int ETK_RemoveService_Handler(HWND hWnd, string pszCode, string pszData);
        private static ETK_RemoveService_Handler _ETK_RemoveService;

        /// <summary>
        /// API에서 HTS로의 연동을 원할 때, 요청합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle. 수신 데이터를 받을 윈도우입니다. 수신데이터는 XM_RECEIVE_LINK_DATA 메시지로 옵니다.</param>
        /// <param name="pszLinkKey">STOCK_CODE, OPEN_SCREEN...</param>
        /// <param name="pszData">상품별 종목코드, HTS에서 열고자 원하는 화면번호</param>
        /// <param name="pszFiller">사용 안 함</param>
        /// <returns>TRUE면 연동이 성공이며, FALSE면 연동이 실패한 것입니다.</returns>
        /// <remarks>
        /// <br/> [1] 종목 연동
        /// <br/>     pszLinkKey	-
        /// <br/>
        /// <br/>                    <![CDATA[&]]>STOCK_CODE				: 주식 종목코드
        /// <br/>                    <![CDATA[&]]>ETF_CODE					: ETF 종목코드
        /// <br/>                    <![CDATA[&]]>ELW_CODE					: ELW 종목코드
        /// <br/>                    <![CDATA[&]]>KONEX_CODE				: 코넥스 종목코드
        /// <br/>                    <![CDATA[&]]>FREEBOARD_CODE			: 프리보드 종목코드
        /// <br/>                    <![CDATA[&]]>KSPI_CODE				: 코스피 업종 코드
        /// <br/>                    <![CDATA[&]]>KSQI_CODE				: 코스닥 업종 코드
        /// <br/>                    <![CDATA[&]]>FUTURE_CODE				: 선물종목코드
        /// <br/>                    <![CDATA[&]]>OPTION_CODE				: 옵션종목코드
        /// <br/>                    <![CDATA[&]]>FUTOPT_CODE				: 선물/옵션 종목코드 
        /// <br/>                    <![CDATA[&]]>FUTSP_CODE				: 선물스프레드 종목코드
        /// <br/>                    <![CDATA[&]]>STOCK_FUTURE_CODE		: 주식 선물 종목코드
        /// <br/>                    <![CDATA[&]]>STOCK_OPTION_CODE		: 주식 옵션 종목코드
        /// <br/>                    <![CDATA[&]]>STOCK_FUTOPT_CODE		: 주식 선물옵션 종목코드 
        /// <br/>                    <![CDATA[&]]>STOCK_FUTSP_CODE			: 주식 선물스프레드 종목코드
        /// <br/>                    <![CDATA[&]]>FUTOPT_STOCK_FUTOPT_CODE : 선물옵션 <![CDATA[&]]> 주식 선물옵션 종목코드
        /// <br/>                    <![CDATA[&]]>US_CODE					: 해외종목코드
        /// <br/>                    <![CDATA[&]]>COMMODITY_FUTOPT_CODE	: 상품선물/선물옵션
        /// <br/>                    <![CDATA[&]]>COMMODITY_FUTURE_CODE	: 상품선물
        /// <br/>                    <![CDATA[&]]>COMMODITY_STAR_CODE		: 스타선물
        /// <br/>                    <![CDATA[&]]>CME_FUTURE_CODE			: CME야간선물
        /// <br/>                    <![CDATA[&]]>EUREX_OPTION_CODE		: EUREX야간옵션
        /// <br/>                    <![CDATA[&]]>NIGHT_FUTOPT_CODE		: 야간선물옵션
        /// <br/>
        /// <br/>     pszData    	- 상품별 종목코드  
        /// <br/>
        /// <br/>     ex) 주식 종목 연동 : pszLinkKey = "<![CDATA[&]]>STOCK_CODE", pszData = "078020"
        /// <br/>         선물 종목 연동 : pszLinkKey = "<![CDATA[&]]>FUTURE_CODE", pszData = "101HC000"
        /// <br/>     
        /// <br/> [2] HTS 화면 열기 
        /// <br/>     pszLinkKey	- <![CDATA[&]]>OPEN_SCREEN : 화면 열기
        /// <br/>     pszData    	- 열고 싶은 화면 번호
        /// <br/>
        /// <br/>     ex) HTS의 '[6602]선옵원장 미결제잔고' 열기
        /// <br/>         pszLinkKey = <![CDATA[&]]>OPEN_SCREEN, pszData = "6602"	
        /// </remarks>
        public int ETK_RequestLinkToHTS(HWND hWnd, string pszLinkKey, string pszData, string pszFiller)
            => _ETK_RequestLinkToHTS(hWnd, pszLinkKey, pszData, pszFiller);
        private delegate int ETK_RequestLinkToHTS_Handler(HWND hWnd, string pszLinkKey, string pszData, string pszFiller);
        private ETK_RequestLinkToHTS_Handler _ETK_RequestLinkToHTS;

        /// <summary>
        /// HTS에서 API로의 연동을 등록합니다.
        /// 연동을 등록한 시점부터 HTS상에서 연동정보가 발생할 때마다 데이터 수신이 가능합니다<br/>
        /// 수신데이터는 XM_RECEIVE_LINK_DATA 메시지로 옵니다<br/>
        /// ★★★  사용방식은 Real 수신과 동일, LPARAM 메모리 수신 후 반드시 해제 필요
        /// </summary>
        /// <param name="hWnd">Window Handle. 수신 데이터를 받을 윈도우입니다. .</param>
        public void ETK_AdviseLinkFromHTS(HWND hWnd) => _ETK_AdviseLinkFromHTS(hWnd);
        private delegate void ETK_AdviseLinkFromHTS_Handler(HWND hWnd);
        private ETK_AdviseLinkFromHTS_Handler _ETK_AdviseLinkFromHTS;

        /// <summary>
        /// HTS에서 API로의 연동을 해제합니다.
        /// </summary>
        /// <param name="hWnd">Window Handle</param>
        public void ETK_UnAdviseLinkFromHTS(HWND hWnd) => _ETK_UnAdviseLinkFromHTS(hWnd);
        private delegate void ETK_UnAdviseLinkFromHTS_Handler(HWND hWnd);
        private ETK_UnAdviseLinkFromHTS_Handler _ETK_UnAdviseLinkFromHTS;

        /// <summary>
        /// t8411 TR 처럼 압축데이터 수신이 가능한 TR에 압축 해제용으로 사용합니다.
        /// </summary>
        /// <param name="pszSrc">압축상태 데이터</param>
        /// <param name="pszDest">압축을 해제한 데이터를 저장할 메모리, (Outblock 구조체 사이즈 최대 2000건)</param>
        /// <param name="nSrcLen">pszSrc 데이터의 길이</param>
        /// <returns>압축을 해제한 데이터(pszDest)의 길이</returns>
        /// <remarks>
        /// 데이터의 압축을 해제한다 : 틱챠트 데이터 등에서 압축상태로 수신받은 경우 사용
        ///     반환값       - 압축을 해제한 데이터(pszDest)의 길이
        ///
        ///     pszSrc		- 압축상태 데이터
        ///     pszDest		- 압축을 해제한 데이터를 저장할 메모리 (Outblock 구조체 사이즈 최대 2000건)
        ///	   nSrcLen	    - pszSrc 데이터의 길이
        /// 
        /// <br/> 사용 방법 
        /// <br/>     ex) t8411 TR 이용시, InBlock의 comp_yn(압축여부) 필드에 "Y" 입력 후 조회
        /// <br/>          ReceiveData() 에서 Occurs 블럭(t8411OutBlock1)이 압축되어 수신되므로, 해당 블럭 압축을 해제
        /// <br/> 
        ///	<_async_code>
        /// LRESULT t8411_Wnd::OnXMReceiveData( WPARAM wParam, LPARAM lParam )
        /// {
        ///     //-------------------------------------------------------------------------------------
        ///     // Data를 받음
        ///     if( wParam == REQUEST_DATA )
        ///     {
        ///         LPRECV_PACKET pRpData = (LPRECV_PACKET)lParam;
        ///  
        ///         if( strcmp( pRpData->szBlockName, NAME_t8411OutBlock ) == 0 )
        ///         {
        ///         }
        ///         else if( strcmp( pRpData->szBlockName, NAME_t8411OutBlock1 ) == 0 )
        ///         {
        ///             LPt8411OutBlock1 pOutBlock1 = (LPt8411OutBlock1)pRpData->lpData;
        ///  
        ///             t8411OutBlock1 szOutBlock1[2000];		// 압축 해제시 최대 2000건 수신
        ///             int nDestSize = g_iXingAPI.Decompress((char *)pOutBlock1, (char *)<![CDATA[&]]>szOutBlock1[0], pRpData->nDataLength);
        ///  
        ///             // Occurs 일 경우
        ///             // Header가 'A' 이면 전체길이에서 OutBlock의 길이를 나눠서 갯수를 구한다.
        ///             if (nDestSize > 0)
        ///             {
        ///                 int nCount = nDestSize / sizeof( t8411OutBlock1 );
        ///  
        ///                 for( int i=0; i<![CDATA[<]]>nCount; i++ )
        ///                 {
        ///                     데이터 표시 
        ///                 }
        ///             }
        ///         }
        ///     }
        /// }
        ///	</_async_code>
        /// </remarks>
        public int ETK_Decompress(string pszSrc, string pszDest, int nSrcLen) => _ETK_Decompress(pszSrc, pszDest, nSrcLen);
        private delegate int ETK_Decompress_Handler(string pszSrc, string pszDest, int nSrcLen);
        private ETK_Decompress_Handler _ETK_Decompress;

        /// <summary>차트라이브러리 연결</summary>
        public bool ETK_IsChartLib() => _ETK_IsChartLib();
        private delegate bool ETK_IsChartLib_Handler();
        private ETK_IsChartLib_Handler _ETK_IsChartLib;

        /// <summary>
        /// ETK_SetProgramOrder
        /// </summary>
        /// <param name="bProgramOrder"></param>
        public void ETK_SetProgramOrder(bool bProgramOrder) => _ETK_SetProgramOrder(bProgramOrder);
        private delegate void ETK_SetProgramOrder_Handler(bool bProgramOrder);
        private ETK_SetProgramOrder_Handler _ETK_SetProgramOrder;

        /// <summary>
        /// ETK_GetProgramOrder
        /// </summary>
        /// <returns></returns>
        public bool ETK_GetProgramOrder() => _ETK_GetProgramOrder();
        private delegate bool ETK_GetProgramOrder_Handler();
        private ETK_GetProgramOrder_Handler _ETK_GetProgramOrder;

        /// <summary>
        /// 해외주식 사용권한
        /// </summary>
        /// <returns></returns>
        public bool ETK_GetUseOverStock() => _ETK_GetUseOverStock();
        private delegate bool ETK_GetUseOverStock_Handler();
        private ETK_GetUseOverStock_Handler _ETK_GetUseOverStock;

        #region ETK 확장 메소드


        /// <inheritdoc cref="ETK_GetErrorMessage"/>
        public static string GetErrorMessage(int nErrorCode)
        {
            StringBuilder sb = new(255);
            _ = ETK_GetErrorMessage(nErrorCode, sb, sb.Capacity);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetAccountList"/>
        public static string GetAccountList(int nIndex)
        {
            StringBuilder sb = new(255);
            ETK_GetAccountList(nIndex, sb, sb.Capacity);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetAccountName"/>
        public static string GetAccountName(string szAccNumber)
        {
            StringBuilder sb = new(255);
            ETK_GetAccountName(szAccNumber, sb, sb.Capacity);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetAcctDetailName"/>
        public static string GetAcctDetailName(string szAccNumber)
        {
            StringBuilder sb = new(255);
            ETK_GetAcctDetailName(szAccNumber, sb, sb.Capacity);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetAcctNickname"/>
        public static string GetAcctNickname(string szAccNumber)
        {
            StringBuilder sb = new(255);
            ETK_GetAcctNickname(szAccNumber, sb, sb.Capacity);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetCommMedia"/>
        public static string GetCommMedia()
        {
            StringBuilder sb = new(255);
            ETK_GetCommMedia(sb);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetETKMedia"/>
        public static string GetETKMedia()
        {
            StringBuilder sb = new(255);
            ETK_GetETKMedia(sb);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetClientIP"/>
        public static string GetClientIP()
        {
            StringBuilder sb = new(255);
            ETK_GetClientIP(sb);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetServerName"/>
        public static string GetServerName()
        {
            StringBuilder sb = new(255);
            ETK_GetServerName(sb);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetAPIPath"/>
        public static string GetAPIPath()
        {
            StringBuilder sb = new(255);
            ETK_GetAPIPath(sb);
            return sb.ToString();
        }

        /// <inheritdoc cref="ETK_GetProcBranchNo"/>
        public static string GetProcBranchNo()
        {
            StringBuilder sb = new(255);
            ETK_GetProcBranchNo(sb);
            return sb.ToString();
        }

        #endregion
    }
}
