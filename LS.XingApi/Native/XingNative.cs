using System.Runtime.InteropServices;
using System.Text;
using HWND = nint;
using LPARAM = nint;

namespace LS.XingApi.Native;

#nullable disable
#pragma warning disable MA0069 // Non-constant static fields should not be visible

/// <summary>
/// XingAPI.dll의 Native 함수를 호출하기 위한 클래스
/// </summary>
internal class XingNative
{
    private const string XING_DLL = "XingAPI.dll";
    [DllImport("kernel32.dll")] private static extern IntPtr LoadLibrary(string dllToLoad);

    // GetProcAddress
    [DllImport("kernel32.dll")] private static extern IntPtr GetProcAddress(IntPtr hModule, string procedureName);
    private IntPtr _moduleHandle;

    public XingNative(string apiFolder)
    {
        var fullPath = Path.Combine(apiFolder, XING_DLL);
        // check if the file exists
        if (!File.Exists(fullPath))
        {
            throw new FileNotFoundException($"File not found: {fullPath}");
        }

        _moduleHandle = LoadLibrary(fullPath);
        if (_moduleHandle == IntPtr.Zero)
        {
            throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());
        }

        ETK_Connect = GetDelegate<ETK_Connect_Handler>();
    }

    private TDelegate GetDelegate<TDelegate>() where TDelegate : class
    {
        string funcName = typeof(TDelegate).Name;
        if (funcName.EndsWith("_Handler"))
            funcName = funcName.Substring(0, funcName.Length - 8);
        else
            throw new ArgumentException($"Invalid delegate type name", funcName);
        var ptr = GetProcAddress(_moduleHandle, funcName);
        if (ptr == IntPtr.Zero)
            return null!;
        var func = Marshal.GetDelegateForFunctionPointer(ptr, typeof(TDelegate)) as TDelegate;
        return func!;
    }

    public delegate bool ETK_Connect_Handler(HWND hWnd, string pszSvrIP, int nPort, int nStartMsgID, int nTimeOut, int nSendMaxPacketSize);
    public static ETK_Connect_Handler ETK_Connect;

    public delegate bool ETK_IsConnected_Handler();
    public ETK_IsConnected_Handler ETK_IsConnected;

    public delegate bool ETK_Disconnect_Handler();
    public static ETK_Disconnect_Handler _ETK_Disconnect;

    public delegate bool ETK_Login_Handler(HWND hWnd, string pszID, string pszPwd, string pszCertPwd, int nType, bool bShowCertErrDlg);
    public static ETK_Login_Handler ETK_Login;

    public delegate bool ETK_Logout_Handler(HWND hWnd);
    public static ETK_Logout_Handler ETK_Logout;

    public delegate int ETK_GetLastError_Handler();
    public static ETK_GetLastError_Handler ETK_GetLastError;

    public delegate int ETK_GetErrorMessage_Handler(int nErrorCode, StringBuilder pszMsg, int nMsgSize);
    public static ETK_GetErrorMessage_Handler ETK_GetErrorMessage;

    public delegate int ETK_Request_Handler(HWND hWnd, string pszCode, [MarshalAs(UnmanagedType.LPArray, SizeParamIndex = 0)] byte[] lpData, int nDataSize, bool bNext, string pszNextKey, int nTimeOut);
    public static ETK_Request_Handler ETK_Request;

    public delegate void ETK_ReleaseRequestData_Handler(int nRequestID);
    public static ETK_ReleaseRequestData_Handler ETK_ReleaseRequestData;

    public delegate void ETK_ReleaseMessageData_Handler(LPARAM lparam);
    public static ETK_ReleaseMessageData_Handler ETK_ReleaseMessageData;

}
