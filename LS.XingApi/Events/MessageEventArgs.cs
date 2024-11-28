namespace LS.XingApi
{
    /// <summary>
    /// 서버 메시지 이벤트
    /// </summary>
    /// <param name="IsSystemError">시스템오류 여부</param>
    /// <param name="Code">응답코드</param>
    /// <param name="Message">응답메시지</param>
    public class MessageEventArgs(bool IsSystemError, string Code, string Message) : EventArgs
    {
        /// <summary>시스템오류 여부</summary>
        public bool IsSystemError { get; } = IsSystemError;
        /// <summary>응답코드</summary>
        public string Code { get; } = Code;
        /// <summary>응답메시지</summary>
        public string Message { get; } = Message;
    }
}
