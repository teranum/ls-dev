namespace LS.XingApi
{
    /// <summary>응답 데이터</summary>
    public class ResponseTrData
    {
        /// <summary>요청코드, 0보다 크면 성공, 아닐시 실패</summary>
        public int id;

        /// <summary>TR Code</summary>
        public required string tr_cd { get; init; }

        /// <summary>연속여부</summary>
        public bool cont_yn;

        /// <summary>연속키</summary>
        public string cont_key = string.Empty;

        /// <summary>응답코드</summary>
        public string rsp_cd = string.Empty;

        /// <summary>응답메시지</summary>
        public string rsp_msg = string.Empty;

        /// <summary>Block 데이터, InBlock, OutBlock, ... OutBlockN 순으로 들어옵니다.</summary>
        public IDictionary<string, object> body = null!;

        /// <summary>resource info</summary>
        public ResInfo res = null!;

        /// <summary>resource info</summary>
        public IList<long> ticks = [];
    }
}
