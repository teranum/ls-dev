namespace LS.XingApi;

/// <summary>응답 데이터</summary>
public class ResponseTrData
{
    /// <summary>요청코드, 0보다 크면 성공, 아닐시 실패</summary>
    public int id { get; }
    /// <summary>TR Code</summary>
    public required string tr_cd { get; init; }
    /// <summary>연속키</summary>
    public string cont_key { get; } = string.Empty;
    /// <summary>응답코드</summary>
    public string rsp_cd { get; } = string.Empty;
    /// <summary>응답메시지</summary>
    public string rsp_msg { get; } = string.Empty;
    /// <summary>body</summary>
    public object body = null!;

    /// <summary>resource info</summary>
    public object ResInfo = null!;
}
