using System.Runtime.InteropServices;

namespace LS.XingApi.Native;

/// <summary>
/// 실시간 데이터 수신
/// </summary>
[StructLayout(LayoutKind.Sequential, Pack = 1)]
internal struct REAL_RECV_PACKET
{
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 3)]
    public byte[] szTrCode;
    private byte _szTrCode;
    public int nKeyLength;
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
    public byte[] szKeyData;
    private byte _szKeyData;
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
    public byte[] szRegKey;
    private byte _szRegKey;
    public int nDataLength;
    public nint pszData;
}
