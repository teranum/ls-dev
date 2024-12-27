using System.Diagnostics;
using System.Net.Http.Headers;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

namespace LS.OpenApi;
/// <summary>API</summary>
public class OpenApi
{
    private readonly HttpClient _httpClient;
    private ClientWebSocket? _wssClient;

    /// <summary>API 서버 주소</summary>
    private const string BaseUrl = "https://openapi.ls-sec.co.kr:8080";

    /// <summary>웹소켓 서버 주소(실시간)</summary>
    private const string WssUrlReal = "wss://openapi.ls-sec.co.kr:9443";

    /// <summary>웹소켓 서버 주소(모의투자)</summary>
    private const string WssUrlSimulation = "wss://openapi.ls-sec.co.kr:29443";

    /// <summary>API객체 생성</summary>
    public OpenApi()
    {
        //_jsonOptions = new()
        //{
        //    NumberHandling = JsonNumberHandling.AllowReadingFromString,
        //};

        _httpClient = new HttpClient
        {
            BaseAddress = new Uri(BaseUrl),
        };
    }

    #region Properties

    /// <inheritdoc cref="MessageEventArgs"/>
    public event EventHandler<MessageEventArgs>? OnMessageEvent;

    /// <inheritdoc cref="RealtimeEventArgs"/>
    public event EventHandler<RealtimeEventArgs>? OnRealtimeEvent;

    /// <summary>연결 여부</summary>
    public bool Connected { get; private set; }
    /// <summary>모의투자 여부</summary>
    public bool IsSimulation { get; private set; }
    /// <summary>마지막 메시지</summary>
    public string LastMessage { get; private set; } = string.Empty;
    /// <summary>MAC 주소 (법인 경우 필수 세팅)</summary>
    public string MacAddress { get; set; } = string.Empty;
    /// <summary>로그인 된 경우 액세스 토큰</summary>
    public string AccessToken { get; private set; } = string.Empty;
    /// <summary>로그인 된 경우 액세스 토큰 만료 시간</summary>
    public long Expires { get; private set; }
    #endregion

    #region Methods

    /// <summary>
    /// 비동기 연결
    /// </summary>
    /// <param name="appkey">고객 앱Key 또는 액서스 토큰</param>
    /// <param name="appsecretkey">고객 앱 비밀Key</param>
    /// <param name="wss_domain">웹소켓URL 수동으로 설정시 필요</param>
    /// <returns></returns>
    /// <remarks>고객 앱 비밀Key가 빈문자열시 고객 앱Key를 액서스 토큰으로 로그인</remarks>
    public async Task<bool> ConnectAsync(string appkey, string appsecretkey = "", string wss_domain = "")
    {
        if (Connected)
        {
            LastMessage = "Aleady connected";
            return true;
        }

        if (string.IsNullOrEmpty(appsecretkey))
        {
            AccessToken = appkey;
        }
        else
        {
            // 접근토큰 발급
            OAuth? oAuth = await PostUrlEncodedAsync<OAuth>("/oauth2/token",
                [
                    new("grant_type", "client_credentials"),
                    new("appkey", appkey),
                    new("appsecretkey", appsecretkey),
                    new("scope", "oob"),
                ]);

            if (oAuth == null)
            {
                LastMessage = $"인증키 가져오기 실패: {LastMessage}";
                return false;
            }
            // 인증성공
            AccessToken = oAuth.access_token;
            Expires = oAuth.expires_in;
        }
        _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", AccessToken);

        // 모의투자인지 실투자인지 구분한다
        var response = await RequestAsync("FOCCQ33600", """{"FOCCQ33600InBlock1":{}}""");
        if (response == null)
        {
            // 요청 실패
            return false;
        }
        if (!int.TryParse(response.rsp_cd, out var num_code))
        {
            // 요청 실패
            return false;
        }

        IsSimulation = response.rsp_msg.Contains("모의투자");

        // 실시간 웹소켓 연결
        if (string.IsNullOrEmpty(wss_domain))
        {
            wss_domain = IsSimulation ? WssUrlSimulation : WssUrlReal;
        }
        Uri wssUri = new(wss_domain + "/websocket");

        try
        {
            _wssClient = new ClientWebSocket();
            if (_wssClient.ConnectAsync(wssUri, CancellationToken.None).Wait(5000))
            {
                Connected = true;
                _ = WebsocketListen(_wssClient);
                OnMessageEvent?.Invoke(this, new($"Websocket: Connected.({wssUri})"));

                LastMessage = "Connected";
                return true;
            }
        }
        catch (Exception)
        {
            _wssClient = null;
            LastMessage = "Websocket서버 연결 응답 없습니다";
            return false;
        }

        return false;
    }

    /// <summary>Close</summary>
    public async Task CloseAsync()
    {
        if (Connected)
        {
            Connected = false;
            if (_wssClient is not null && _wssClient.State == WebSocketState.Open)
                await _wssClient.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);
        }
    }

    private async Task<T?> PostUrlEncodedAsync<T>(string path, IEnumerable<KeyValuePair<string, string>> nameValueCollection)
    {
        LastMessage = string.Empty;
        try
        {
            var response = await _httpClient.PostAsync(path, new FormUrlEncodedContent(nameValueCollection)).ConfigureAwait(false);
            if (response != null)
            {
                var bytes = await response.Content.ReadAsByteArrayAsync();
                var json_text = Encoding.UTF8.GetString(bytes);
                if (response.IsSuccessStatusCode)
                {
                    return JsonSerializer.Deserialize<T>(json_text);
                }
                LastMessage = json_text ?? response.StatusCode.ToString();
            }
        }
        catch (Exception ex)
        {
            LastMessage = ex.Message;
        }
        return default;
    }
    #endregion
    private async Task WebsocketListen(ClientWebSocket webSocket)
    {
        ArraySegment<byte> buffer = new(new byte[1024]);
        while (webSocket.State == WebSocketState.Open)
        {
            using var ms = new MemoryStream();
            WebSocketReceiveResult? result;
            do
            {
                result = await webSocket.ReceiveAsync(buffer, CancellationToken.None);

                if (result.MessageType == WebSocketMessageType.Close)
                {
                    OnMessageEvent?.Invoke(this, new($"Websocket: Closed.({result.CloseStatusDescription ?? string.Empty})"));
                    return;
                }

                await ms.WriteAsync(buffer.AsMemory(0, result.Count), CancellationToken.None);
            }
            while (!result.EndOfMessage);

            ms.Seek(0, SeekOrigin.Begin);

            if (result.MessageType == WebSocketMessageType.Text)
            {
                using var reader = new StreamReader(ms, Encoding.UTF8);
                OnWssReceive(await reader.ReadToEndAsync());
            }
        }
    }

    private void OnWssReceive(string stringData)
    {
        try
        {
            RealtimeResponseModel? response = JsonSerializer.Deserialize<RealtimeResponseModel>(stringData);
            if (response != null && response.header != null)
            {
                if (!string.IsNullOrEmpty(response.header.rsp_msg))
                {
                    OnMessageEvent?.Invoke(this, new($"{response.header.tr_cd}({response.header.tr_type}) : {response.header.rsp_msg}"));
                }

                if (response.body is JsonElement jsonElement)
                {
                    // JsonElement to Dictionary<string, object>
                    var dict = JsonElementConverter.JsonElementToDictionary(jsonElement);
                    OnRealtimeEvent?.Invoke(this, new(response.header.tr_cd, response.header.tr_key, dict));
                }
            }
        }
        catch (Exception ex)
        {
            LastMessage = ex.Message;
            OnMessageEvent?.Invoke(this, new(ex.Message));
        }
    }

    /// <summary>
    /// 비동기 TR 요청
    /// </summary>
    /// <param name="tr_cd">증권 거래코드</param>
    /// <param name="in_datas">입력 바이너리 데이터</param>
    /// <param name="cont_yn">연속여부</param>
    /// <param name="cont_key">연속일 경우 그전에 내려온 연속키 값 올림</param>
    /// <returns>응답데이터, null인경우 오류, 오류 메시지는 LastMessage 참고</returns>
    public async Task<ResponseTrData?> RequestAsync(string tr_cd, object in_datas, bool cont_yn = false, string cont_key = "")
    {
        var resInfo = ResManager.GetResInfo(tr_cd);
        if (resInfo == null)
        {
            LastMessage = $"TR 정보가 없습니다.({tr_cd})";
            return null;
        }

        if (resInfo.IsRealtime)
        {
            LastMessage = $"실시간 TR코드는 RequestAsync를 사용할 수 없습니다.({tr_cd})";
            return null;
        }

        ResponseTrData response = new()
        {
            tr_cd = tr_cd,
            res = resInfo,
        };

        try
        {
            string jsonRequest = string.Empty;
            if (in_datas is string in_data)
                jsonRequest = in_data;
            else
                jsonRequest = JsonSerializer.Serialize(in_datas);
            var content = new StringContent(jsonRequest, Encoding.UTF8, "application/json");
            HttpRequestMessage httpRequestMessage = new(HttpMethod.Post, resInfo.Url)
            {
                Content = content,
            };

            httpRequestMessage.Headers.Add("tr_cd", tr_cd);
            httpRequestMessage.Headers.Add("tr_cont", cont_yn ? "Y" : "N");
            httpRequestMessage.Headers.Add("tr_cont_key", cont_key);
            if (MacAddress.Length > 0) httpRequestMessage.Headers.Add("mac_address", MacAddress);

            Stopwatch stopwatch = Stopwatch.StartNew();
            var responseMsg = await _httpClient.SendAsync(httpRequestMessage).ConfigureAwait(false);

            if (responseMsg.Headers.TryGetValues("tr_cont", out IEnumerable<string>? list_tr_cont))
                response.cont_yn = list_tr_cont.First().Equals("Y");
            if (response.cont_yn)
            {
                if (responseMsg.Headers.TryGetValues("tr_cont_key", out IEnumerable<string>? list_tr_cont_key))
                    response.cont_key = list_tr_cont_key.First();
            }
            var jsonResponse = await responseMsg.Content.ReadAsStringAsync().ConfigureAwait(false);
            stopwatch.Stop();
            response.jsonResponse = jsonResponse;

            var jsonElement = JsonSerializer.Deserialize<JsonElement>(jsonResponse/*, _jsonOptions*/);
            var body = JsonElementConverter.JsonElementToDictionary(jsonElement);
            response.body = body ?? [];
            response.elapsed_ms = stopwatch.Elapsed.TotalMilliseconds;

            if (response.body.TryGetValue("rsp_cd", out var _rsp_cd))
            {
                response.rsp_cd = _rsp_cd.ToString()!;
                response.body.Remove("rsp_cd");
            }
            if (response.body.TryGetValue("rsp_msg", out var _rsp_msg))
            {
                response.rsp_msg = _rsp_msg.ToString()!;
                response.body.Remove("rsp_msg");
            }

            LastMessage = $"[{response.rsp_cd}] {response.rsp_msg}";
            return response;
        }
        catch (Exception ex)
        {
            LastMessage = ex.Message;
        }
        return null;
    }

    /// <summary>
    /// 실시간 시세 등록/해제
    /// </summary>
    /// <param name="tr_cd">증권 거래코드</param>
    /// <param name="tr_key">단축코드 6자리 또는 8자리 (단건, 연속)</param>
    /// <param name="advise">시세등록: true, 시세해제: false</param>
    /// <returns>true: 요청성공, false: 요청실패</returns>
    public async Task<bool> RealtimeAsync(string tr_cd, string tr_key, bool advise)
    {
        if (!Connected || _wssClient == null || _wssClient.State != WebSocketState.Open)
        {
            LastMessage = "Not connected";
            return false;
        }
        var resInfo = ResManager.GetResInfo(tr_cd);
        if (resInfo == null)
        {
            LastMessage = $"TR 정보가 없습니다.({tr_cd})";
            return false;
        }
        if (!resInfo.IsRealtime)
        {
            LastMessage = $"실시간 TR코드가 아닙니다.({tr_cd})";
            return false;
        }

        bool isAccount = ResManager.AccountRealTimes.Contains(tr_cd);

        string jsonbody = $"{{\"header\":{{\"token\":\"{AccessToken}\",\"tr_type\":\"{(isAccount ? (advise ? "1" : "2") : (advise ? "3" : "4"))}\"}},\"body\":{{\"tr_cd\":\"{tr_cd}\",\"tr_key\":\"{tr_key}\"}}}}";

        try
        {
            await _wssClient.SendAsync(Encoding.UTF8.GetBytes(jsonbody), WebSocketMessageType.Text, endOfMessage: true, CancellationToken.None);
        }
        catch (Exception ex)
        {
            LastMessage = ex.Message;
            return false;
        }
        return true;
    }
    record OAuth(string access_token, string scope, string token_type, long expires_in);
    record RealtimeResponseModel(RealtimeResponseModel.Header header, object body)
    {
        public record Header(string tr_type, string rsp_cd, string rsp_msg, string tr_cd, string tr_key);
    }
}
internal class JsonElementConverter
{
    public static Dictionary<string, object> JsonElementToDictionary(JsonElement jsonElement)
    {
        var dictionary = new Dictionary<string, object>();

        foreach (JsonProperty property in jsonElement.EnumerateObject())
        {
            dictionary[property.Name] = ConvertJsonElement(property.Value);
        }

        return dictionary;
    }

    private static object ConvertJsonElement(JsonElement element)
    {
        switch (element.ValueKind)
        {
            case JsonValueKind.Object:
                return JsonElementToDictionary(element);
            case JsonValueKind.Array:
                var list = new List<object>();
                foreach (var item in element.EnumerateArray())
                {
                    list.Add(ConvertJsonElement(item));
                }
                return list;
            case JsonValueKind.String:
                return element.GetString()!;
            case JsonValueKind.Number:
                if (element.TryGetInt32(out int intValue))
                    return intValue;
                if (element.TryGetInt64(out long longValue))
                    return longValue;
                if (element.TryGetDouble(out double doubleValue))
                    return doubleValue;
                break;
            case JsonValueKind.True:
                return true;
            case JsonValueKind.False:
                return false;
            case JsonValueKind.Null:
                return null!;
        }

        throw new InvalidOperationException($"Unsupported JsonValueKind: {element.ValueKind}");
    }
}