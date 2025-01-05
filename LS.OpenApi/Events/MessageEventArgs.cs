namespace LS.OpenApi
{
    /// <summary>
    /// 서버 메시지 이벤트
    /// </summary>
    /// <param name="Message">응답메시지</param>
    public class MessageEventArgs(string Message) : EventArgs
    {
        /// <summary>응답메시지</summary>
        public string Message { get; } = Message;
    }
}
