#pragma once

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



	FP_ETK_Connect					m_ETK_Connect;
	FP_ETK_IsConnected				m_ETK_IsConnected;
	FP_ETK_Disconnect				m_ETK_Disconnect;
	FP_ETK_Login					m_ETK_Login;
	FP_ETK_Logout					m_ETK_Logout;

	FP_ETK_GetLastError				m_ETK_GetLastError;
	FP_ETK_GetErrorMessage			m_ETK_GetErrorMessage;

	FP_ETK_Request					m_ETK_Request;
	FP_ETK_AdviseRealData			m_ETK_AdviseRealData;
	FP_ETK_UnadviseRealData			m_ETK_UnadviseRealData;
	FP_UNADVISEWINDOW			m_fpUnadviseWindow;
	FP_ETK_ReleaseRequestData		m_ETK_ReleaseRequestData;
	FP_RELEASEMESSAGEDATA		m_fpReleaseMessageData;

	FP_ETK_GetAccountListCount		m_ETK_GetAccountListCount;
	FP_ETK_GetAccountList			m_ETK_GetAccountList;
	FP_ETK_GetAccountName			m_ETK_GetAccountName;
	FP_ETK_GetAcctDetailName		m_ETK_GetAcctDetailName;
	FP_ETK_GetAcctNickname			m_ETK_GetAcctNickname;

	FP_ETK_GetCommMedia				m_ETK_GetCommMedia;
	FP_ETK_GetETKMedia				m_ETK_GetETKMedia;
	FP_ETK_GetClientIP				m_ETK_GetClientIP;
	FP_ETK_GetServerName			m_ETK_GetServerName;
	FP_ETK_GetAPIPath				m_ETK_GetAPIPath;

	FP_SETHEADERINFO			m_fpSetHeaderInfo;
	FP_SETUSEAPIVER				m_fpSetUseAPIVer;
	FP_ETK_SetMode					m_ETK_SetMode;

	FP_ETK_GetProcBranchNo			m_ETK_GetProcBranchNo;
	FP_ETK_GetUseOverFuture			m_ETK_GetUseOverFuture;
	FP_ETK_GetUseFX					m_ETK_GetUseFX;
	FP_ETK_GetUseOverStock			m_ETK_GetUseOverStock;

	FP_ETK_GetTRCountPerSec			m_ETK_GetTRCountPerSec;
	FP_ETK_GetTRCountBaseSec		m_ETK_GetTRCountBaseSec;
	FP_ETK_GetTRCountRequest		m_ETK_GetTRCountRequest;
	FP_ETK_GetTRCountLimit			m_ETK_GetTRCountLimit;

	FP_SETNOTIFYFLAG			m_fpSetNotifyFlag;

	FP_ETK_RequestService			m_ETK_RequestService;
	FP_ETK_RemoveService			m_ETK_RemoveService;

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

		m_ETK_Connect = (FP_ETK_Connect)GetProcAddress(m_hModule, "ETK_Connect");
		m_ETK_IsConnected = (FP_ETK_IsConnected)GetProcAddress(m_hModule, "ETK_IsConnected");
		m_ETK_Disconnect = (FP_ETK_Disconnect)GetProcAddress(m_hModule, "ETK_Disconnect");
		m_ETK_Login = (FP_ETK_Login)GetProcAddress(m_hModule, "ETK_Login");
		m_ETK_Logout = (FP_ETK_Logout)GetProcAddress(m_hModule, "ETK_Logout");

		m_ETK_GetLastError = (FP_ETK_GetLastError)GetProcAddress(m_hModule, "ETK_GetLastError");
		m_ETK_GetErrorMessage = (FP_ETK_GetErrorMessage)GetProcAddress(m_hModule, "ETK_GetErrorMessage");

		m_ETK_Request = (FP_ETK_Request)GetProcAddress(m_hModule, "ETK_Request");
		m_ETK_AdviseRealData = (FP_ETK_AdviseRealData)GetProcAddress(m_hModule, "ETK_AdviseRealData");
		m_ETK_UnadviseRealData = (FP_ETK_UnadviseRealData)GetProcAddress(m_hModule, "ETK_UnadviseRealData");
		m_fpUnadviseWindow = (FP_UNADVISEWINDOW)GetProcAddress(m_hModule, "ETK_UnadviseWindow");
		m_ETK_ReleaseRequestData = (FP_ETK_ReleaseRequestData)GetProcAddress(m_hModule, "ETK_ReleaseRequestData");
		m_fpReleaseMessageData = (FP_RELEASEMESSAGEDATA)GetProcAddress(m_hModule, "ETK_ReleaseMessageData");

		m_ETK_GetAccountListCount = (FP_ETK_GetAccountListCount)GetProcAddress(m_hModule, "ETK_GetAccountListCount");
		m_ETK_GetAccountList = (FP_ETK_GetAccountList)GetProcAddress(m_hModule, "ETK_GetAccountList");
		m_ETK_GetAccountName = (FP_ETK_GetAccountName)GetProcAddress(m_hModule, "ETK_GetAccountName");
		m_ETK_GetAcctDetailName = (FP_ETK_GetAcctDetailName)GetProcAddress(m_hModule, "ETK_GetAcctDetailName");
		m_ETK_GetAcctNickname = (FP_ETK_GetAcctNickname)GetProcAddress(m_hModule, "ETK_GetAcctNickname");

		m_ETK_GetCommMedia = (FP_ETK_GetCommMedia)GetProcAddress(m_hModule, "ETK_GetCommMedia");
		m_ETK_GetETKMedia = (FP_ETK_GetETKMedia)GetProcAddress(m_hModule, "ETK_GetETKMedia");
		m_ETK_GetClientIP = (FP_ETK_GetClientIP)GetProcAddress(m_hModule, "ETK_GetClientIP");
		m_ETK_GetServerName = (FP_ETK_GetServerName)GetProcAddress(m_hModule, "ETK_GetServerName");
		m_ETK_GetAPIPath = (FP_ETK_GetAPIPath)GetProcAddress(m_hModule, "ETK_GetAPIPath");

		m_fpSetHeaderInfo = (FP_SETHEADERINFO)GetProcAddress(m_hModule, "ETK_SetHeaderInfo");
		m_fpSetUseAPIVer = (FP_SETUSEAPIVER)GetProcAddress(m_hModule, "ETK_SetUseAPIVer");
		m_ETK_SetMode = (FP_ETK_SetMode)GetProcAddress(m_hModule, "ETK_SetMode");

		m_ETK_GetProcBranchNo = (FP_ETK_GetProcBranchNo)GetProcAddress(m_hModule, "ETK_GetProcBranchNo");
		m_ETK_GetUseOverFuture = (FP_ETK_GetUseOverFuture)GetProcAddress(m_hModule, "ETK_GetUseOverFuture");
		m_ETK_GetUseFX = (FP_ETK_GetUseFX)GetProcAddress(m_hModule, "ETK_GetUseFX");
		m_ETK_GetUseOverStock = (FP_ETK_GetUseOverStock)GetProcAddress(m_hModule, "ETK_GetUseOverStock");

		m_ETK_GetTRCountPerSec = (FP_ETK_GetTRCountPerSec)GetProcAddress(m_hModule, "ETK_GetTRCountPerSec");
		m_ETK_GetTRCountBaseSec = (FP_ETK_GetTRCountBaseSec)GetProcAddress(m_hModule, "ETK_GetTRCountBaseSec");
		m_ETK_GetTRCountRequest = (FP_ETK_GetTRCountRequest)GetProcAddress(m_hModule, "ETK_GetTRCountRequest");
		m_ETK_GetTRCountLimit = (FP_ETK_GetTRCountLimit)GetProcAddress(m_hModule, "ETK_GetTRCountLimit");

		m_fpSetNotifyFlag = (FP_SETNOTIFYFLAG)GetProcAddress(m_hModule, "ETK_SetNotifyFlag");

		m_ETK_RequestService = (FP_ETK_RequestService)GetProcAddress(m_hModule, "ETK_RequestService");
		m_ETK_RemoveService = (FP_ETK_RemoveService)GetProcAddress(m_hModule, "ETK_RemoveService");

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
