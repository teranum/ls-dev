namespace LS.XingApi
{
    /// <summary>
    /// TR요청 횟수, <see cref="XingApi.GetRequestCount(string)"/> 함수를 사용하여 가져옵니다.
    /// </summary>
    public class RequestCount
    {
        /// <summary>TR의 초당 전송 가능 횟수</summary>
        public int PerSec;
        /// <summary>Base 시간(초단위): 1초당 1건 전송 가능시 1, 5초당 1건 전송 가능시 5</summary>
        public int BaseSec;
        /// <summary>10분내 요청한 해당 TR의 총 횟수</summary>
        public int Requests;
        /// <summary>TR의 10분당 제한 건수</summary>
        public int Limit;
    }
}
