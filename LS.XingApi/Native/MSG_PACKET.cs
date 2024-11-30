using System.Runtime.InteropServices;

namespace LS.XingApi.Native;

/// <summary>
/// 서버에서 전달되는 메시지
/// </summary>
[StructLayout(LayoutKind.Sequential, Pack = 1)]
internal struct MSG_PACKET
{
    /// <summary>Requests ID</summary>
    public int nRqID;
    /// <summary>0:일반메시지, 1:System Error 메시지</summary>
    public int nIsSystemError;
    /// <summary>메시지 코드</summary>
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 5)]
    public byte[] szMsgCode;
    private byte _szMsgCode;
    /// <summary>Message 길이</summary>
    public int nMsgLength;
    /// <summary>Message Data</summary>
    public nint lpszMessageData;
}
