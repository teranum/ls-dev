# [![NuGet version](https://badge.fury.io/nu/LS.OpenApi.png)](https://badge.fury.io/nu/LS.OpenApi) LS.OpenApi C# Wrapper

LS증권 OpenApi 를 C#에서 사용하기 위한 Wrapper.

### 개발환경
Visual Studio 2022, NET8.0
 
### 1. 클래스 프로퍼티/메소드/이벤트
```csharp
// 프로퍼티 (읽기전용)
bool Connected : 연결 여부
bool IsSimulation: 로그인 후 모의투자/실투자 여부
string LastMessage: 마지막 메시지
string MacAddress: MAC 주소 (법인 경우 필수 세팅, 쓰기 가능)
string AccessToken: 로그인 된 경우 액세스 토큰, 당일 재로그인시 사용
long Expires: 로그인 된 경우 액세스 토큰 만료 시간

// 메소드
Task<bool> ConnectAsync : 비동기 연결 (반환값 true: 성공, false: 실패, 실패시 LastMessage에 오류메시지가 저장.)
Task CloseAsync : 비동기 연결 해제
Task<ResponseTrData?> RequestAsync : 비동기 TR 요청, 성공시 TR 데이터 반환, 실패시 null 반환, 실패사유는 LastMessage에 저장.
Task<bool> RealtimeAsync : 실시간 시세 등록/해제 (반환값 true: 성공, false: 실패, 실패시 LastMessage에 오류메시지가 저장.)

// 이벤트
OnMessageEvent : 메시지 이벤트 (웹소켓 연결/해제, 또는 오류 발생시)
OnRealtimeEvent : 실시간 이벤트

```

### 2. 클래스 생성, 로그인 후 TR을 요청.

```csharp
    // 객체생성
    OpenApi api = new();

    // 로그인
    bool await api.ConnectAsync(AppKey, AppSecretKey);
    if (!api)
    {
        Console.WriteLine(api.LastMessage);
        return;
    }

    // TR 요청 (주식 현재가)
    var inputs =
        new Dictionary<string, object>
        {
            ["t1102InBlock"] = new Dictionary<string, object>
            {
                ["shcode"] = "005930",  // 삼성전자
            },
        };
    var response = await api.RequestAsync("t1102", inputs);
    if (response == null)
    {
        Console.WriteLine(api.LastMessage);
        return;
    }

    // 실시간 등록 ("S3_": 주식 KOSPI체결, "005930": 삼성전자)
    await api.RealtimeAsync("S3_", "005930", true);

    ... 다른 작업 ...


    // 실시간 해제
    await api.RealtimeAsync("S3_", "005930", false);
```

### 3. TR 요청.

```csharp
    // 방법1: 딕셔너리 형태로 입력값을 설정하고 TR 요청.
    var inputs =
        new Dictionary<string, object>
        {
            ["t8410InBlock"] = new Dictionary<string, object>
            {
                ["shcode"] = "005930",  // 삼성전자
                ["gubun"] = "2",        // 주기구분(2:일3:주4:월5:년)
                ["qrycnt"] = 500,       // 요청건수(최대-압축:2000비압축:500)
                ["edate"] = "99999999", // 종료일자
                ["comp_yn"] = "N",      // 압축여부(Y:압축N:비압축)
                ["sujung"] = "Y",       // 수정주가여부(Y:적용N:비적용)
            },
        };
    var response = await api.RequestAsync("t8410", inputs);

    // 방법2: JSON 형태로 입력값을 설정하고 TR 요청.
    var inputs =
        """
        {
            "t8410InBlock" : {
                "shcode" : "005930",
                "gubun" : "2",
                "qrycnt" : 500,
                "edate" : "99999999",
                "comp_yn" : "N",
                "sujung" : "Y"
            }
        }
        """;
    var response = await api.RequestAsync("t1102", inputs);

    // 연속요청
    // response.cont_yn 이 true인 경우, response.cont_key 값을 입력하여 다음 페이지를 요청.
    // 3번째 인자에 true, 4번째 인자에 response.cont_key 값을 입력
    var response = await api.RequestAsync("t8410", inputs, true, cont_key);

```

