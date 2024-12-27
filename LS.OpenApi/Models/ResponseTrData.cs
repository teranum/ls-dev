namespace LS.OpenApi
{
    /// <summary>응답 데이터</summary>
    public class ResponseTrData
    {
        /// <summary>TR Code</summary>
        public required string tr_cd { get; init; }

        /// <summary>연속여부</summary>
        public bool cont_yn;

        /// <summary>연속키</summary>
        public string cont_key = string.Empty;

        /// <summary>JSON응답 데이터</summary>
        public string jsonResponse = string.Empty;

        /// <summary>응답코드</summary>
        public string rsp_cd = string.Empty;

        /// <summary>응답메시지</summary>
        public string rsp_msg = string.Empty;

        /// <summary>Block 데이터, InBlock, OutBlock, ... OutBlockN 순으로 들어옵니다.</summary>
        public Dictionary<string, object> body = [];

        /// <summary>resource info</summary>
        public ResInfo res = null!;

        /// <summary>elapsed elapsed_ms</summary>
        public double elapsed_ms;

        /// <summary>Get the elements in dictionary</summary>
        public object? this[string key] => body[key];
    }
}
