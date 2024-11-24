#pragma once

namespace xing
{
	LPCSTR real_domain = "api.ls-sec.co.kr";
	LPCSTR simul_domain = "demo.ls-sec.co.kr";
	const int serveer_port = 20001;

	class IXingApi
	{
	public:
		IXingApi() {
			ZeroMemory(this, sizeof(IXingApi));
			m_hModule = NULL;
		}
		~IXingApi() {}

	private:
	protected:
		HMODULE			m_hModule;

	public:
		typedef BOOL(__stdcall* FP_ETK_Connect) (HWND, LPCTSTR, int, int, int, int);
		typedef BOOL(__stdcall* FP_ETK_IsConnected) ();
		typedef BOOL(__stdcall* FP_ETK_Disconnect) ();
		typedef BOOL(__stdcall* FP_ETK_Login) (HWND, LPCSTR, LPCSTR, LPCSTR, int, BOOL);
		typedef BOOL(__stdcall* FP_ETK_Logout) (HWND);

		typedef int(__stdcall* FP_ETK_GetLastError) ();
		typedef int(__stdcall* FP_ETK_GetErrorMessage) (int, LPSTR, int);

		typedef int(__stdcall* FP_ETK_Request) (HWND, LPCTSTR, LPCTSTR, int, BOOL, LPCTSTR, int);
		typedef void(__stdcall* FP_ETK_ReleaseRequestData) (int);
		typedef void(__stdcall* FP_RELEASEMESSAGEDATA) (LPARAM);

		typedef BOOL(__stdcall* FP_ETK_AdviseRealData) (HWND, LPCTSTR, LPCTSTR, int);
		typedef BOOL(__stdcall* FP_ETK_UnadviseRealData) (HWND, LPCTSTR, LPCTSTR, int);
		typedef BOOL(__stdcall* FP_UNADVISEWINDOW) (HWND);

		typedef int(__stdcall* FP_ETK_GetAccountListCount) ();
		typedef BOOL(__stdcall* FP_ETK_GetAccountList) (int, LPSTR, int);
		typedef BOOL(__stdcall* FP_ETK_GetAccountName) (LPCTSTR, LPSTR, int);
		typedef BOOL(__stdcall* FP_ETK_GetAcctDetailName) (LPCTSTR, LPSTR, int);
		typedef BOOL(__stdcall* FP_ETK_GetAcctNickname) (LPCTSTR, LPSTR, int);

		typedef void(__stdcall* FP_ETK_GetCommMedia) (LPTSTR);
		typedef void(__stdcall* FP_ETK_GetETKMedia) (LPTSTR);
		typedef void(__stdcall* FP_ETK_GetClientIP) (LPTSTR);
		typedef void(__stdcall* FP_ETK_GetServerName) (LPTSTR);
		typedef void(__stdcall* FP_ETK_GetAPIPath) (LPTSTR);

		typedef void(__stdcall* FP_SETHEADERINFO) (LPCTSTR, LPCTSTR);
		typedef void(__stdcall* FP_SETUSEAPIVER) (LPCTSTR);
		typedef void(__stdcall* FP_ETK_SetMode) (LPCTSTR, LPCTSTR);

		typedef void(__stdcall* FP_ETK_GetProcBranchNo) (LPTSTR);
		typedef BOOL(__stdcall* FP_ETK_GetUseOverFuture) ();
		typedef BOOL(__stdcall* FP_ETK_GetUseFX) ();

		typedef int(__stdcall* FP_ETK_GetTRCountPerSec) (LPCTSTR);
		typedef int(__stdcall* FP_ETK_GetTRCountBaseSec) (LPCTSTR);
		typedef int(__stdcall* FP_ETK_GetTRCountRequest) (LPCTSTR);
		typedef int(__stdcall* FP_ETK_GetTRCountLimit) (LPCTSTR);

		typedef void(__stdcall* FP_SETNOTIFYFLAG) (BOOL);

		typedef int(__stdcall* FP_ETK_RequestService) (HWND, LPCTSTR, LPCTSTR);
		typedef int(__stdcall* FP_ETK_RemoveService) (HWND, LPCTSTR, LPCTSTR);

		typedef int(__stdcall* FP_REQUESTLINKTOHTS) (HWND, LPCTSTR, LPCTSTR, LPCTSTR);
		typedef void(__stdcall* FP_ADVISELINKFROMHTS) (HWND);
		typedef void(__stdcall* FP_UNADVISELINKFROMHTS) (HWND);

		typedef int(__stdcall* FP_DECOMPRESS) (LPCTSTR, LPCTSTR, int);
		typedef BOOL(__stdcall* FP_ISCHARTLIB) ();

		typedef void(__stdcall* FP_SetMainWnd) (HWND);
		typedef int(__stdcall* FP_RequestData) (HWND hWnd, char* a2, void* a3, size_t Size, int a5, int a6, int a7, int a8, int a9, int a10);
		typedef int(__stdcall* FP_RequestDataEx) (int a1, int a2, int a3, size_t Size, int a5, int a6, int a7, int a8, int a9, int a10, int a11, int a12, int a13);
		typedef int(__stdcall* FP_SetProgramOrder) (int a1);
		typedef int(__stdcall* FP_GetProgramOrder) ();

		typedef BOOL(__stdcall* FP_ETK_GetUseOverStock) ();



		FP_ETK_Connect					ETK_Connect;
		FP_ETK_IsConnected				ETK_IsConnected;
		FP_ETK_Disconnect				ETK_Disconnect;
		FP_ETK_Login					ETK_Login;
		FP_ETK_Logout					ETK_Logout;

		FP_ETK_GetLastError				ETK_GetLastError;
		FP_ETK_GetErrorMessage			ETK_GetErrorMessage;

		FP_ETK_Request					ETK_Request;
		FP_ETK_AdviseRealData			ETK_AdviseRealData;
		FP_ETK_UnadviseRealData			ETK_UnadviseRealData;
		FP_UNADVISEWINDOW			m_fpUnadviseWindow;
		FP_ETK_ReleaseRequestData		ETK_ReleaseRequestData;
		FP_RELEASEMESSAGEDATA		m_fpReleaseMessageData;

		FP_ETK_GetAccountListCount		ETK_GetAccountListCount;
		FP_ETK_GetAccountList			ETK_GetAccountList;
		FP_ETK_GetAccountName			ETK_GetAccountName;
		FP_ETK_GetAcctDetailName		ETK_GetAcctDetailName;
		FP_ETK_GetAcctNickname			ETK_GetAcctNickname;

		FP_ETK_GetCommMedia				ETK_GetCommMedia;
		FP_ETK_GetETKMedia				ETK_GetETKMedia;
		FP_ETK_GetClientIP				ETK_GetClientIP;
		FP_ETK_GetServerName			ETK_GetServerName;
		FP_ETK_GetAPIPath				ETK_GetAPIPath;

		FP_SETHEADERINFO			m_fpSetHeaderInfo;
		FP_SETUSEAPIVER				m_fpSetUseAPIVer;
		FP_ETK_SetMode					ETK_SetMode;

		FP_ETK_GetProcBranchNo			ETK_GetProcBranchNo;
		FP_ETK_GetUseOverFuture			ETK_GetUseOverFuture;
		FP_ETK_GetUseFX					ETK_GetUseFX;
		FP_ETK_GetUseOverStock			ETK_GetUseOverStock;

		FP_ETK_GetTRCountPerSec			ETK_GetTRCountPerSec;
		FP_ETK_GetTRCountBaseSec		ETK_GetTRCountBaseSec;
		FP_ETK_GetTRCountRequest		ETK_GetTRCountRequest;
		FP_ETK_GetTRCountLimit			ETK_GetTRCountLimit;

		FP_SETNOTIFYFLAG			m_fpSetNotifyFlag;

		FP_ETK_RequestService			ETK_RequestService;
		FP_ETK_RemoveService			ETK_RemoveService;

		FP_REQUESTLINKTOHTS			m_fpRequestLinkToHTS;
		FP_ADVISELINKFROMHTS		m_fpAdviseLinkFromHTS;
		FP_UNADVISELINKFROMHTS		m_fpUnAdviseLinkFromHTS;

		FP_DECOMPRESS				m_fpDecompress;
		FP_ISCHARTLIB				m_fpIsChartLib;

		FP_SetMainWnd				m_fpSetMainWnd;
		FP_RequestData				m_fpRequestData;
		FP_RequestDataEx			m_fpRequestDataEx;
		FP_SetProgramOrder			m_fpSetProgramOrder;
		FP_GetProgramOrder			m_fpGetProgramOrder;


	public:
		BOOL IsInit() { return m_hModule != NULL; }
		BOOL Init(LPCTSTR szPath)
		{
			if (IsInit()) return TRUE;

			return LoadLibHelper(szPath);
		}

		BOOL LoadLibHelper(LPCTSTR szPath)
		{
			m_hModule = ::LoadLibrary(szPath);

			if (NULL == m_hModule) return FALSE;

			ETK_Connect = (FP_ETK_Connect)GetProcAddress(m_hModule, "ETK_Connect");
			ETK_IsConnected = (FP_ETK_IsConnected)GetProcAddress(m_hModule, "ETK_IsConnected");
			ETK_Disconnect = (FP_ETK_Disconnect)GetProcAddress(m_hModule, "ETK_Disconnect");
			ETK_Login = (FP_ETK_Login)GetProcAddress(m_hModule, "ETK_Login");
			ETK_Logout = (FP_ETK_Logout)GetProcAddress(m_hModule, "ETK_Logout");

			ETK_GetLastError = (FP_ETK_GetLastError)GetProcAddress(m_hModule, "ETK_GetLastError");
			ETK_GetErrorMessage = (FP_ETK_GetErrorMessage)GetProcAddress(m_hModule, "ETK_GetErrorMessage");

			ETK_Request = (FP_ETK_Request)GetProcAddress(m_hModule, "ETK_Request");
			ETK_AdviseRealData = (FP_ETK_AdviseRealData)GetProcAddress(m_hModule, "ETK_AdviseRealData");
			ETK_UnadviseRealData = (FP_ETK_UnadviseRealData)GetProcAddress(m_hModule, "ETK_UnadviseRealData");
			m_fpUnadviseWindow = (FP_UNADVISEWINDOW)GetProcAddress(m_hModule, "ETK_UnadviseWindow");
			ETK_ReleaseRequestData = (FP_ETK_ReleaseRequestData)GetProcAddress(m_hModule, "ETK_ReleaseRequestData");
			m_fpReleaseMessageData = (FP_RELEASEMESSAGEDATA)GetProcAddress(m_hModule, "ETK_ReleaseMessageData");

			ETK_GetAccountListCount = (FP_ETK_GetAccountListCount)GetProcAddress(m_hModule, "ETK_GetAccountListCount");
			ETK_GetAccountList = (FP_ETK_GetAccountList)GetProcAddress(m_hModule, "ETK_GetAccountList");
			ETK_GetAccountName = (FP_ETK_GetAccountName)GetProcAddress(m_hModule, "ETK_GetAccountName");
			ETK_GetAcctDetailName = (FP_ETK_GetAcctDetailName)GetProcAddress(m_hModule, "ETK_GetAcctDetailName");
			ETK_GetAcctNickname = (FP_ETK_GetAcctNickname)GetProcAddress(m_hModule, "ETK_GetAcctNickname");

			ETK_GetCommMedia = (FP_ETK_GetCommMedia)GetProcAddress(m_hModule, "ETK_GetCommMedia");
			ETK_GetETKMedia = (FP_ETK_GetETKMedia)GetProcAddress(m_hModule, "ETK_GetETKMedia");
			ETK_GetClientIP = (FP_ETK_GetClientIP)GetProcAddress(m_hModule, "ETK_GetClientIP");
			ETK_GetServerName = (FP_ETK_GetServerName)GetProcAddress(m_hModule, "ETK_GetServerName");
			ETK_GetAPIPath = (FP_ETK_GetAPIPath)GetProcAddress(m_hModule, "ETK_GetAPIPath");

			m_fpSetHeaderInfo = (FP_SETHEADERINFO)GetProcAddress(m_hModule, "ETK_SetHeaderInfo");
			m_fpSetUseAPIVer = (FP_SETUSEAPIVER)GetProcAddress(m_hModule, "ETK_SetUseAPIVer");
			ETK_SetMode = (FP_ETK_SetMode)GetProcAddress(m_hModule, "ETK_SetMode");

			ETK_GetProcBranchNo = (FP_ETK_GetProcBranchNo)GetProcAddress(m_hModule, "ETK_GetProcBranchNo");
			ETK_GetUseOverFuture = (FP_ETK_GetUseOverFuture)GetProcAddress(m_hModule, "ETK_GetUseOverFuture");
			ETK_GetUseFX = (FP_ETK_GetUseFX)GetProcAddress(m_hModule, "ETK_GetUseFX");
			ETK_GetUseOverStock = (FP_ETK_GetUseOverStock)GetProcAddress(m_hModule, "ETK_GetUseOverStock");

			ETK_GetTRCountPerSec = (FP_ETK_GetTRCountPerSec)GetProcAddress(m_hModule, "ETK_GetTRCountPerSec");
			ETK_GetTRCountBaseSec = (FP_ETK_GetTRCountBaseSec)GetProcAddress(m_hModule, "ETK_GetTRCountBaseSec");
			ETK_GetTRCountRequest = (FP_ETK_GetTRCountRequest)GetProcAddress(m_hModule, "ETK_GetTRCountRequest");
			ETK_GetTRCountLimit = (FP_ETK_GetTRCountLimit)GetProcAddress(m_hModule, "ETK_GetTRCountLimit");

			m_fpSetNotifyFlag = (FP_SETNOTIFYFLAG)GetProcAddress(m_hModule, "ETK_SetNotifyFlag");

			ETK_RequestService = (FP_ETK_RequestService)GetProcAddress(m_hModule, "ETK_RequestService");
			ETK_RemoveService = (FP_ETK_RemoveService)GetProcAddress(m_hModule, "ETK_RemoveService");

			m_fpRequestLinkToHTS = (FP_REQUESTLINKTOHTS)GetProcAddress(m_hModule, "ETK_RequestLinkToHTS");
			m_fpAdviseLinkFromHTS = (FP_ADVISELINKFROMHTS)GetProcAddress(m_hModule, "ETK_AdviseLinkFromHTS");
			m_fpUnAdviseLinkFromHTS = (FP_UNADVISELINKFROMHTS)GetProcAddress(m_hModule, "ETK_UnAdviseLinkFromHTS");

			m_fpDecompress = (FP_DECOMPRESS)GetProcAddress(m_hModule, "ETK_Decompress");
			m_fpIsChartLib = (FP_ISCHARTLIB)GetProcAddress(m_hModule, "ETK_IsChartLib");

			m_fpSetMainWnd = (FP_SetMainWnd)GetProcAddress(m_hModule, "_ETK_SetMainWnd@4");
			m_fpRequestData = (FP_RequestData)GetProcAddress(m_hModule, "ETK_RequestData");
			m_fpRequestDataEx = (FP_RequestDataEx)GetProcAddress(m_hModule, "ETK_RequestDataEx");
			m_fpSetProgramOrder = (FP_SetProgramOrder)GetProcAddress(m_hModule, "ETK_SetProgramOrder");
			m_fpGetProgramOrder = (FP_GetProgramOrder)GetProcAddress(m_hModule, "ETK_GetProgramOrder");

			return TRUE;
		}


	};

	// XING API Message
	enum XM
	{
		/// <summary>
		/// �������� ������ �������� ��� �߻�
		/// </summary>
		XM_DISCONNECT = 1,

		/// <summary>
		/// RequestData�� ��û�� �����Ͱ� �����κ��� �޾��� �� �߻�
		/// </summary>
		XM_RECEIVE_DATA = 3,

		/// <summary>
		/// AdviseData�� ��û�� �����Ͱ� �����κ��� �޾��� �� �߻�
		/// </summary>
		XM_RECEIVE_REAL_DATA = 4,

		/// <summary>
		/// �����κ��� �α��� ��� �޾����� �߻�
		/// </summary>
		XM_LOGIN = 5,

		/// <summary>
		/// �����κ��� �α׾ƿ� ��� �޾����� �߻�
		/// </summary>
		XM_LOGOUT = 6,

		/// <summary>
		/// RequestData�� ��û�� �����Ͱ� Timeout �� �߻�������
		/// </summary>
		XM_TIMEOUT_DATA = 7,

		/// <summary>
		/// HTS ���� ���� �����Ͱ� �߻����� ��	: by zzin 2013.11.11
		/// </summary>
		XM_RECEIVE_LINK_DATA = 8,

		/// <summary>
		/// �ǽð� �ڵ� ����� �� ��Ʈ ��ȸ ��, ��ǥ�ǽð� �����͸� �޾��� ��  : by zzin 2013.08.14
		/// </summary>
		XM_RECEIVE_REAL_DATA_CHART = 10,

		/// <summary>
		/// ����˻� �ǽð� �����͸� �޾��� �� 			: by 2017.11.24 LSW
		/// </summary>
		XM_RECEIVE_REAL_DATA_SEARCH = 11,


		XM_LAST
	};

	// RECEIVE_DATA FLAG
	enum RF
	{
		REQUEST_DATA = 1,
		MESSAGE_DATA = 2,
		SYSTEM_ERROR_DATA = 3,
		RELEASE_DATA = 4,
	};

	// Structure ����
#pragma pack( push, 1 )

	// ��ȸTR ���� Packet
	typedef struct _RECV_PACKET
	{
		_RECV_PACKET() { ZeroMemory(this, sizeof(_RECV_PACKET)); }

		int					nRqID;						// Request ID
		int					nDataLength;				// ���� ������ ũ��
		int					nTotalDataBufferSize;		// lpData�� �Ҵ�� ũ��
		int					nElapsedTime;				// ���ۿ��� ���ű��� �ɸ��ð�(1/1000��)
		int					nDataMode;					// 1:BLOCK MODE, 2:NON-BLOCK MODE
		char				szTrCode[10 + 1];			// AP Code
		char				cCont[1];					// '0' : ������ȸ ����, '1' : ������ȸ ����
		char				szContKey[18 + 1];			// ����Ű, Data Header�� B �� ��쿡�� ���
		char				szUserData[30 + 1];			// ����� ������
		char				szBlockName[17];			// Block ��, Block Mode �϶� ���
		unsigned char* lpData;							// Data	
	} RECV_PACKET, * LPRECV_PACKET;

	// �޽��� ���� Packet
	typedef struct _MSG_PACKET
	{
		_MSG_PACKET() { ZeroMemory(this, sizeof(_MSG_PACKET)); }

		int					nRqID;						// Request ID
		int					nIsSystemError;				// 0:�Ϲݸ޽���, 1:System Error �޽���
		char				szMsgCode[5 + 1];			// �޽��� �ڵ�
		int					nMsgLength;					// Message ����
		unsigned char* lpszMessageData;					// Message Data
	} MSG_PACKET, * LPMSG_PACKET;

	// �ǽð�TR ���� Packet
	typedef struct _REAL_RECV_PACKET
	{
		_REAL_RECV_PACKET() { ZeroMemory(this, sizeof(_REAL_RECV_PACKET)); }

		char				szTrCode[3 + 1];			// TR Code
		int					nKeyLength;					// Key ����
		char				szKeyData[32 + 1];			// Key Data
		char				szRegKey[32 + 1];			// ��� Key
		int					nDataLength;
		char* pszData;
	} RECV_REAL_PACKET, * LPRECV_REAL_PACKET;

	// HTS���� API�� �����Ǿ� ���ŵǴ� Packet
	typedef struct _LINKDATA_RECV_MSG
	{
		_LINKDATA_RECV_MSG() { ZeroMemory(this, sizeof(_LINKDATA_RECV_MSG)); }

		char				sLinkName[32];
		char				sLinkData[32];
		char				sFiller[64];
	}LINKDATA_RECV_MSG, * LPLINKDATA_RECV_MSG;

#pragma pack( pop )
}
