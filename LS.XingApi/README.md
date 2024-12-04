# [![NuGet version](https://badge.fury.io/nu/LS.XingApi.png)](https://badge.fury.io/nu/LS.XingApi) LS.XingApi C# Wrapper

LS증권 XingApi (DLL모드) 를 C#에서 사용하기 위한 Wrapper입니다.

## 개발환경
Visual Studio 2022, NET8.0
<br/>
 
### 1. 클래스 프로퍼티/메소드/이벤트
```csharp
	// 프로퍼티 (읽기전용)
	bool ModuleLoaded : DLL로딩 여부 (LS증권 XingAPI 설치되었을 경우 true, 아닐경우 false)
	bool Logined : 로그인 여부
	string UserId : 로그인 아이디
	bool IsSimulation: 로그인 후 실투자/모의투자 여부
	List<AccountInfo> AccountInfos: 계좌정보 리스트. (로그인 시 자동 등록 됩니다)
	string LastMessage: 마지막 메시지
	nint Handle: 윈도우 핸들

	// 메소드
	Task<bool> ConnectAsync : 비동기 로그인 요청 (반환값 true: 성공, false: 실패, 실패시 lastMessage에 오류메시지가 저장됩니다.)
	void Close : 연결 해제
	Task<ResponseTrData?> RequestAsync : 비동기 TR 요청, 성공시 TR 데이터 반환, 실패시 null 반환, 실패사유는 lastMessage에 저장됩니다.
	int RemoveService : 부가 서비스용 TR를 해제합니다. 반환값: 부가서비스에 따라 달라짐
	bool Realtime : 실시간 시세 등록/해제 (반환값 true: 성공, false: 실패, 실패시 lastMessage에 오류메시지가 저장됩니다.)

	// 이벤트
	OnMessageEvent : 메시지 이벤트 (LOGOUT 또는 DISCONNECT)
	OnRealtimeEvent : 실시간 이벤트 (true: 성공, false: 실패, 실패시 lastMessage에 오류메시지가 저장됩니다.)

```

### 2. 클래스 생성, 로그인 후 TR을 요청 합니다.

```csharp
	// 객체생성
	XingApi api = new();

	// 로그인
    bool await api.ConnectAsync(UserId, UserPwd, CertPwd);
	if (!api)
	{
		Console.WriteLine(api.LastMessage);
		return;
	}

	// TR 요청 (주식 현재가)
	var inputs = new Dictionary<string, object> {
		{ "shcode", "005930" }
	};
	var tr = await api.RequestAsync("t1102", inputs);
	if (tr == null)
	{
		Console.WriteLine(api.LastMessage);
		return;
	}

	// 실시간 등록 ("S3_": 주식 KOSPI체결, "005930": 삼성전자)
	api.Realtime("S3_", "005930", true);

	... 다른 작업 ...


	// 실시간 해제
	api.Realtime("S3_", "005930", false);
```

