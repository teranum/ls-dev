namespace LS.OpenApi
{
    /// <summary>
    /// 실시간 이벤트
    /// </summary>
    /// <param name="TrCode">Tr코드</param>
    /// <param name="Key">키</param>
    /// <param name="RealtimeBody">실시간응답(Dictionary)</param>
    public class RealtimeEventArgs(string TrCode, string Key, Dictionary<string, object> RealtimeBody) : EventArgs
    {
        /// <summary>Tr코드</summary>
        public string TrCode { get; } = TrCode;
        /// <summary>키</summary>
        public string Key { get; } = Key;
        /// <summary>실시간응답(Dictionary)</summary>
        public Dictionary<string, object> RealtimeBody { get; } = RealtimeBody;
    }
}
