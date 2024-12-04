using System.Runtime.InteropServices;

namespace LS.XingApi.Native;

/// <summary>
/// HTS 에서 API로 연동 (HTS -> API) : 등록하면 해제할때까지 연동된다<br/>
/// hWnd			- 연동을 원하는 윈도우의 핸들<br/>
/// ※ HTS에서 연동 발생 시, XM_RECEIVE_LINK_DATA 로 메시지가 발생<br/>
/// WPARAM = LINK_DATA, LPARAM = LINKDATA_RECV_MSG_CLASS 구조체 데이터 <br/>
/// ★★★  사용방식은 Real 수신과 동일, LPARAM 메모리 수신 후 반드시 해제 필요
/// </summary>
[StructLayout(LayoutKind.Sequential)]
internal struct LINKDATA_RECV_MSG
{
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
    public byte[] sLinkName;
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
    public byte[] sLinkData;
    [MarshalAs(UnmanagedType.ByValArray, SizeConst = 64)]
    public byte[] sFiller;
}
