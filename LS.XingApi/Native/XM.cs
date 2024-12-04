namespace LS.XingApi.Native;

/// <summary>
/// 서버메시지
/// </summary>
internal enum XM
{
    /// <summary>
    /// 서버와의 연결이 끊어졌을 경우 발생
    /// </summary>
    XM_DISCONNECT = 1,

    /// <summary>
    /// RequestData로 요청한 데이터가 서버로부터 받았을 때 발생
    /// </summary>
    XM_RECEIVE_DATA = 3,

    /// <summary>
    /// AdviseData로 요청한 데이터가 서버로부터 받았을 때 발생
    /// </summary>
    XM_RECEIVE_REAL_DATA = 4,

    /// <summary>
    /// 서버로부터 로그인 결과 받았을때 발생
    /// </summary>
    XM_LOGIN = 5,

    /// <summary>
    /// 서버로부터 로그아웃 결과 받았을때 발생
    /// </summary>
    XM_LOGOUT = 6,

    /// <summary>
    /// RequestData로 요청한 데이터가 Timeout 이 발생했을때
    /// </summary>
    XM_TIMEOUT_DATA = 7,

    /// <summary>
    /// HTS 에서 연동 데이터가 발생했을 때	: by zzin 2013.11.11
    /// </summary>
    XM_RECEIVE_LINK_DATA = 8,

    /// <summary>
    /// 실시간 자동 등록한 후 차트 조회 시, 지표실시간 데이터를 받았을 때  : by zzin 2013.08.14
    /// </summary>
    XM_RECEIVE_REAL_DATA_CHART = 10,

    /// <summary>
    /// 종목검색 실시간 데이터를 받았을 때 			: by 2017.11.24 LSW
    /// </summary>
    XM_RECEIVE_REAL_DATA_SEARCH = 11,
}
