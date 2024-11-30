using System.Runtime.InteropServices;

namespace LS.XingApi;

// API에서 사용하는 데이터 구조체
// 고정길이 문자열은 byte[]로 처리, 뒤붙어진 0x00을 제거하여 string으로 변환, 마지막 바이트는 더미바이트로 사용
[StructLayout(LayoutKind.Sequential, Pack = 1)]
internal struct RECV_PACKET
{
    /// <summary>Requests ID</summary>
    public int nRqID;
    /// <summary>받은 데이터 크기</summary>
    public int nDataLength;
    /// <summary>lpData에 할당된 크기</summary>
    public int nTotalDataBufferSize;
    /// <summary>전송에서 수신까지 걸린시간(1/1000초)</summary>
    public int nElapsedTime;
    /// <summary>1:BLOCK MODE, 2:NON-BLOCK MODE</summary>
    public int nDataMode;
    /// <summary>AP Code</summary>
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 10)]
    public byte[] szTrCode;
    private byte _szTrCode;
    /// <summary>'0' : 다음조회 없음, '1' : 다음조회 있음</summary>
    public byte cCont;
    /// <summary>연속키, pszData Header가 B 인 경우에만 사용</summary>
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 18)]
    public byte[] szContKey;
    private byte _szContKey;
    /// <summary>사용자 데이터</summary>
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 30)]
    public byte[] szUserData;
    private byte _szUserData;
    /// <summary>Block 명, Block Mode 일때 사용</summary>
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 16)]
    public byte[] szBlockName;
    private byte _szBlockName;
    public IntPtr lpData;
}
