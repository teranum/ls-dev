# LS증권 XingAPI wrapper

This is a simple package for XingApi (DLL and COM mode).

## Installation

```bash
pip install xingAsync
```

대체거래서 출범관련 TR변경으로 xingAsync 0.3.0 이상 사용. (2025.03.02 업데이트)

## Usage
DLL, COM 모드 지원. (DLL 권장)<br/>
DLL Wrapper class: XingApi<br/>
COM Wrapper class: XingCOM<br/>
COM base classes: XASession, XAQuery, XAReal<br/>

### 통합샘플파일
- [test/sample_XingApi.py](test/sample_XingApi.py): DLL모드 XingApi 이용 샘플
- [test/sample_XingCOM.py](test/sample_XingCOM.py): COM모드 XingCOM 이용 샘플

## DLL모드 XingApi 이용, DLL를 이용하기 쉽게 Wrapper
### 로그인/요청/실시간 조회
```python
import asyncio
from xingAsync import XingApi, run_loop
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

#######################################################
# DLL 이용한 XingApi 클래스 테스트
# * 가장빠름
# * 실시간 데이터 수신시 on_realtime 이벤트 처리 필요
#######################################################

async def sample(api:XingApi):
    # 로그인
    if not await api.login(user_id, user_pwd, cert_pwd):
        print(f"로그인 실패: {api.last_message}")
        return

    print(f"로그인 성공: {"모의투자" if api.is_simulation else "실투자"}")

    # 보유계좌 표시
    for x in api.accounts:
        print(x)

    # 요청 t1102: 주식 현재가(시세) 조회
    response = await api.request("t1102", {"shcode": "005930"}) # 005930: 삼성전자
    if not response:
        print(f"t1102 request failed: {api.last_message}")
        return

    # 요청 성공시, 조회된 데이터 확인
    print(f"t1102 request succeeded: {api.last_message}")
    price = response["t1102OutBlock"]["price"]
    print(f"삼성전자 현재가: {price}")

    # 추가작업
    ...

    # 실시간 시세 요청/이벤트 처리
    codes = ["005930", "000660"] # 삼성전자, SK하이닉스 실시간 체결 수신
    # codes = ["HSIG25", "HCEIG25"] # 항셍, 미니항셍 실시간 체결 수신, tr_cd: "OVC"
    if not api.realtime("S3_", codes, True):
        return print(f"실시간 요청 실패: {api.last_message}")

    print("실시간 요청 성공, 60초동안 실시간 수신...")
    await asyncio.sleep(60)

    # 실시간 해지
    api.realtime("", "", False) # 실시간 해지

def on_realtime(code: str, key: str, datas: dict):
    print(f"{code}, {key}, {datas}")


if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(on_realtime)
    run_loop(sample(api))

# Output:
'''
로그인 성공: 실투자
XXXXXXXXXXX 홍길동 홍길동 선물옵션
XXXXXXXXXXX 홍길동 홍길동 해외선옵
XXXXXXXXXXX 홍길동 홍길동 종합매매
t1102 request succeeded: [00000] 정상적으로 조회가 완료되었습니다.
삼성전자 현재가: 53100
실시간 요청 성공, 60초동안 실시간 수신...
S3_, 005930, {'chetime': '125618', 'sign': '2', 'change': '2000', 'drate': '3.92', 'price': '53000', 'opentime': '090010', 'open': '51600', 'hightime': '101356', 'high': '53600', 'lowtime': '090010', 'low': '51500', 'cgubun': '-', 'cvolume': '14', 'volume': '18796692', 'value': '994091', 'mdvolume': '7592337', 'mdchecnt': '46517', 'msvolume': '10388368', 'mschecnt': '59566', 'cpower': '136.83', 'w_avrg': '52886', 'offerho': '53100', 'bidho': '53000', 'status': '00', 'jnilvolume': '19530765', 'shcode': '005930'}
S3_, 000660, {'chetime': '125618', 'sign': '2', 'change': '1200', 'drate': '0.63', 'price': '192100', 'opentime': '090022', 'open': '192900', 'hightime': '101559', 'high': '194300', 'lowtime': '091001', 'low': '190100', 'cgubun': '-', 'cvolume': '1', 'volume': '4108984', 'value': '791376', 'mdvolume': '2096548', 'mdchecnt': '27010', 'msvolume': '1694527', 'mschecnt': '37787', 'cpower': '80.82', 'w_avrg': '192596', 'offerho': '192200', 'bidho': '192100', 'status': '00', 'jnilvolume': '5394963', 'shcode': '000660'}
S3_, 000660, {'chetime': '125618', 'sign': '2', 'change': '1300', 'drate': '0.68', 'price': '192200', 'opentime': '090022', 'open': '192900', 'hightime': '101559', 'high': '194300', 'lowtime': '091001', 'low': '190100', 'cgubun': '+', 'cvolume': '1', 'volume': '4108985', 'value': '791376', 'mdvolume': '2096548', 'mdchecnt': '27010', 'msvolume': '1694528', 'mschecnt': '37788', 'cpower': '80.82', 'w_avrg': '192596', 'offerho': '192200', 'bidho': '192100', 'status': '00', 'jnilvolume': '5394963', 'shcode': '000660'}
S3_, 005930, {'chetime': '125618', 'sign': '2', 'change': '2100', 'drate': '4.12', 'price': '53100', 'opentime': '090010', 'open': '51600', 'hightime': '101356', 'high': '53600', 'lowtime': '090010', 'low': '51500', 'cgubun': '+', 'cvolume': '3', 'volume': '18796695', 'value': '994091', 'mdvolume': '7592337', 'mdchecnt': '46517', 'msvolume': '10388371', 'mschecnt': '59567', 'cpower': '136.83', 'w_avrg': '52886', 'offerho': '53100', 'bidho': '53000', 'status': '00', 'jnilvolume': '19530765', 'shcode': '005930'}
S3_, 005930, {'chetime': '125618', 'sign': '2', 'change': '2100', 'drate': '4.12', 'price': '53100', 'opentime': '090010', 'open': '51600', 'hightime': '101356', 'high': '53600', 'lowtime': '090010', 'low': '51500', 'cgubun': '+', 'cvolume': '1', 'volume': '18796696', 'value': '994091', 'mdvolume': '7592337', 'mdchecnt': '46517', 'msvolume': '10388372', 'mschecnt': '59568', 'cpower': '136.83', 'w_avrg': '52886', 'offerho': '53100', 'bidho': '53000', 'status': '00', 'jnilvolume': '19530765', 'shcode': '005930'}
'''
```

## 프로퍼티/메소드/이벤트 (DLL 모드)

### 프로퍼티 (읽기전용)
```python
    loaded:         # xingApi.dll 로딩 여부 (True/False), xingApi가 설치되지 않은 경우 False
    logined:        # 로그인 여부 (True/False)
    is_simulation:  # 모의투자인 경우 True, 실계좌인 경우 False
    accounts:       # 계좌목록 (list)
    last_message:   # 마지막 수신 메시지, 요청 실패시 실패사유가 저장됨
```

### 메소드
```python
    login: # 로그인 (비동기)
        await api.login("user_id", "ser_pwd", "cert_pwd") # 모의투자인 경우 cert_pwd는 ''로 설정
        return: True/False, 로그인 성공여부, 실패시 last_message에 실패사유가 저장됨

    close: # 로그아웃
        api.close()

    request: TR 요청 (비동기)

        # t1102: 주식현재가 요청, 삼성전자 
        response = await api.request("t1102", "005930")
        # 또는 필드명을 지정하여 요청
        response = await api.request("t1102", {'shcode': '005930'})
        
        # 성공시 ResponseData 리턴, 실패시 None 리턴 (실패사유는 last_message에 저장됨)
        # 블록타입이 배열이 아닌 경우 dict 로 반환됨, 배열(occurs)인 경우 list[dict] 로 반환됨)

        # 입력은 dict, 문자열, 리스트 형태로 입력 가능
        # ex) t8407: 주식멀티현재가조회 (입력필드 2개: nrec, shcode)
        inputs = {"nrec": 2, "shcode": "005930000660"}"}    # ex1) dict로 입력
        inputs = "2,005930000660" 						    # ex2) 문자열로 입력 (',' 로 구분하여 필드 순서로 입력)
        inputs = ["2", "005930000660"] 					    # ex3) 리스트로 입력 (필드 순서로 입력)

        # 입력블록이 2개이상인 경우, 블록명을 지정하여 입력
        inputs = {
            "t1104InBlock": {
                "code": "005930",    # 종목코드
                "nrec": "4",         # 건수
                "exchgubun": "K",    # K:KRX, N:NXT, U:통합, 그외 입력값은 KRX로 처리
            },
            "t1104InBlock1": [
                {"indx": "0", "gubn": "1", "dat1": "2", "dat2": "1"}, 
                {"indx": "1", "gubn": "1", "dat1": "3", "dat2": "1"}, 
                {"indx": "2", "gubn": "4", "dat1": "1", "dat2": "5"}, 
                {"indx": "3", "gubn": "4", "dat1": "1", "dat2": "20"}, 
            ],
        }

        # t8410: 주식차트요청 (일주월분), 삼성전자
        inputs = {
            'shcode': '005930',     # 삼성전자
            'gubun': '2',           # 주기구분(2:일3:주4:월5:년)
            'qrycnt': 100,          # 요청건수(최대-압축:2000비압축:500)
            'sdate': '',            # 시작일자
            'edate': '99999999',    # 종료일자
            'cts_date': '',         # 연속일자
            'comp_yn': 'N',         # 압축여부(Y:압축N:비압축)
            'sujung': 'Y',          # 수정주가여부(Y:적용N:비적용)
        }
        response = await api.request("t8410", inputs)
        t8410OutBlock = response['t8410OutBlock']                   # t8410OutBlock 데이터 가져오기
        print(t8410OutBlock['jisiga'], t8410OutBlock['jiclose'])    # 전일시가, 전일종가 출력

        t8410OutBlock1 = response['t8410OutBlock1']                 # t8410OutBlock1 데이터 가져오기 (occurs 경우 list[dict] 로 반환됨)
        for data in t8410OutBlock1:
            print(data['date'], data['close'])                      # 날짜, 종가 출력

        # 연속조회
        if response.cont_yn:
            inputs['cts_date'] = response['cts_date']
            response = await api.request("t8410", inputs, True, response.cont_key)
            t8410OutBlock1 = response['t8410OutBlock1']
            for data in t8410OutBlock1:
                print(data['date'], data['close'])

    realtime: # 실시간 구독/해지
        realtime("S3_", "005930", True)                 # ex1): 단일종목: 삼성전자 구독
        realtime("S3_", "005930,000660", True)          # ex2): 복수종목: 삼성전자, SK하이닉스 구독
        realtime("S3_", ["005930", "000660"], True)     # ex3): 복수종목: 삼성전자, SK하이닉스 구독
        realtime("S3_", "005930", False)                # ex4): 단일종목: 삼성전자 실시간 해지
        realtime("S3_", "005930,000660", False)         # ex5): 복수종목: 삼성전자 실시간 해지
        realtime("S3_", ["005930", "000660"], False)    # ex6): 복수종목: 삼성전자 실시간 해지
        realtime("", "", False)                         # ex7): 모든 실시간 해지

    get_requests_count: TR 초당전송가능횟수, Base시간, 10분당 제한 건수, 10분내 요청 횟수 반환
        print(api.get_requests_count("t1102"))
        # (10, 1, 0, 1)
```

### 이벤트
```python
    on_message(msg: str): # 서버 오류 또는 중복로그인 연결 끊김시 수신 (ex. 'DISCONNECT')
        ex: 'DISCONNECT'

    on_realtime(tr_cd: str, key: str, datas: dict): # 실시간 데이터 수신
        ex: 'S3_', '005930', {'chetime': '090000', 'sign': '1', 'change': 100, 'drate': 0.1, 'price': 60000, ...}

    # 이벤트 핸들러 등록
    api.on_message.connect(lambda msg: print(f'오류: {msg}'))
    api.on_realtime.connect(lambda tr_cd, key, datas: print(f'실시간: {tr_cd}, {key}, {datas}'))
```


## COM모드 XingCOM 이용, COM객체를 이용하기 쉽게 Wrapper
### 로그인/요청/실시간 조회
```python
from xingAsync import XingCOM
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

#########################################################################################
# COM 객체 통합 Wrapper XingCOM 클래스 테스트
# * DLL모드와 인터페이스 동일 (가능한 DLL 모드 XingApi 이용 권장)
# * asyncio를 사용하지 않음, asyncio 이용 어려울 경우 사용
# * 부가서비스(t1857, ChartIndex) 실시간등록은 tr당 1개만 가능, 추가 필요시 XAQuery 이용
#########################################################################################

def sample(api:XingCOM):
    # 로그인
    if not api.login(user_id, user_pwd, cert_pwd):
        print(f"로그인 실패: {api.last_message}")
        return

    print(f"로그인 성공: {"모의투자" if api.is_simulation else "실투자"}")

    # 보유계좌 표시
    for x in api.accounts:
        print(x)

    # 요청 t1102: 주식 현재가(시세) 조회
    response = api.request("t1102", {"shcode": "005930"}) # 005930: 삼성전자
    if not response:
        print(f"t1102 request failed: {api.last_message}")
        return

    # 요청 성공시, 조회된 데이터 확인
    print(f"t1102 request succeeded: {api.last_message}")
    price = response["t1102OutBlock"]["price"]
    print(f"삼성전자 현재가: {price}")

    # 추가작업
    ...

    # 실시간 시세 요청/이벤트 처리
    codes = ["005930", "000660"] # 삼성전자, SK하이닉스 실시간 체결 수신
    # codes = ["HSIG25", "HCEIG25"] # 항셍, 미니항셍 실시간 체결 수신, tr_cd: "OVC"
    if not api.realtime("S3_", codes, True):
        return print(f"실시간 요청 실패: {api.last_message}")

def on_realtime(code: str, key: str, datas: dict):
    print(f"{code}, {key}, {datas}")


if __name__ == "__main__":
    api = XingCOM()
    api.on_realtime.connect(on_realtime)
    sample(api)
    # 실시간 데이터 수신시 메시지 루프 필요
    import pythoncom
    while True:
        pythoncom.PumpWaitingMessages()

# Output:
'''
로그인 성공: 실투자
XXXXXXXXXXX 홍길동 홍길동 선물옵션
XXXXXXXXXXX 홍길동 홍길동 해외선옵
XXXXXXXXXXX 홍길동 홍길동 종합매매
t1102 request succeeded: [00000] 정상적으로 조회가 완료되었습니다.
삼성전자 현재가: 53100
S3_, 005930, {'chetime': '125618', 'sign': '2', 'change': '2000', 'drate': '3.92', 'price': '53000', 'opentime': '090010', 'open': '51600', 'hightime': '101356', 'high': '53600', 'lowtime': '090010', 'low': '51500', 'cgubun': '-', 'cvolume': '14', 'volume': '18796692', 'value': '994091', 'mdvolume': '7592337', 'mdchecnt': '46517', 'msvolume': '10388368', 'mschecnt': '59566', 'cpower': '136.83', 'w_avrg': '52886', 'offerho': '53100', 'bidho': '53000', 'status': '00', 'jnilvolume': '19530765', 'shcode': '005930'}
S3_, 000660, {'chetime': '125618', 'sign': '2', 'change': '1200', 'drate': '0.63', 'price': '192100', 'opentime': '090022', 'open': '192900', 'hightime': '101559', 'high': '194300', 'lowtime': '091001', 'low': '190100', 'cgubun': '-', 'cvolume': '1', 'volume': '4108984', 'value': '791376', 'mdvolume': '2096548', 'mdchecnt': '27010', 'msvolume': '1694527', 'mschecnt': '37787', 'cpower': '80.82', 'w_avrg': '192596', 'offerho': '192200', 'bidho': '192100', 'status': '00', 'jnilvolume': '5394963', 'shcode': '000660'}
S3_, 000660, {'chetime': '125618', 'sign': '2', 'change': '1300', 'drate': '0.68', 'price': '192200', 'opentime': '090022', 'open': '192900', 'hightime': '101559', 'high': '194300', 'lowtime': '091001', 'low': '190100', 'cgubun': '+', 'cvolume': '1', 'volume': '4108985', 'value': '791376', 'mdvolume': '2096548', 'mdchecnt': '27010', 'msvolume': '1694528', 'mschecnt': '37788', 'cpower': '80.82', 'w_avrg': '192596', 'offerho': '192200', 'bidho': '192100', 'status': '00', 'jnilvolume': '5394963', 'shcode': '000660'}
S3_, 005930, {'chetime': '125618', 'sign': '2', 'change': '2100', 'drate': '4.12', 'price': '53100', 'opentime': '090010', 'open': '51600', 'hightime': '101356', 'high': '53600', 'lowtime': '090010', 'low': '51500', 'cgubun': '+', 'cvolume': '3', 'volume': '18796695', 'value': '994091', 'mdvolume': '7592337', 'mdchecnt': '46517', 'msvolume': '10388371', 'mschecnt': '59567', 'cpower': '136.83', 'w_avrg': '52886', 'offerho': '53100', 'bidho': '53000', 'status': '00', 'jnilvolume': '19530765', 'shcode': '005930'}
S3_, 005930, {'chetime': '125618', 'sign': '2', 'change': '2100', 'drate': '4.12', 'price': '53100', 'opentime': '090010', 'open': '51600', 'hightime': '101356', 'high': '53600', 'lowtime': '090010', 'low': '51500', 'cgubun': '+', 'cvolume': '1', 'volume': '18796696', 'value': '994091', 'mdvolume': '7592337', 'mdchecnt': '46517', 'msvolume': '10388372', 'mschecnt': '59568', 'cpower': '136.83', 'w_avrg': '52886', 'offerho': '53100', 'bidho': '53000', 'status': '00', 'jnilvolume': '19530765', 'shcode': '005930'}
...
'''
```


## COM 기본모드 XASession, XAQuery, XAReal 이용
### 로그인/요청/실시간 조회
```python
from xingAsync import XASession, XAQuery, XAReal
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

##########################################################################################################
# COM 객체 XASession, XAQuery, XAReal 테스트
# * asyncio를 사용하지 않음, asyncio 이용 어려울 경우 사용 (가능한 DLL 모드 XingApi 이용 권장)
# * Res파일 경로 설정 필요없음
# * OnLogin, OnReceiveData 이벤트 처리 필요없음, 실시간 데이터 수신시 OnReceiveRealData 이벤트 처리 필요
##########################################################################################################

def sample():
    # 로그인
    session = XASession()
    session.ConnectServer("api.ls-sec.co.kr", 20001)
    if not session.Login(user_id, user_pwd, cert_pwd, 0, 0):
        print(f"로그인 실패: {session.last_message}")
        return

    print(f"로그인 성공: {session.last_message}")

    # 보유계좌 표시
    acc_count = session.GetAccountListCount()
    print(f"Account List Count: {acc_count}")
    for i in range(acc_count):
        acc_num = session.GetAccountList(i)
        acc_name = session.GetAccountName(acc_num)
        acc_detail = session.GetAcctDetailName(acc_num)
        print(f"{acc_num} {acc_name} {acc_detail}")

    # 요청 t1102: 주식 현재가(시세) 조회
    query = XAQuery("t1102")
    query.SetFieldData("t1102InBlock", "shcode", 0, "005930") # 005930: 삼성전자
    ret = query.Request(False)
    if ret < 0:
        print(f"t1102 request failed: {query.last_message}")
        return

    # 요청 성공시, 조회된 데이터 확인
    print(f"t1102 request succeeded: {query.last_message}")
    price = query.GetFieldData('t1102OutBlock', 'price', 0)
    print(f"삼성전자 현재가: {price}")

    # 추가작업
    ...

    # 실시간 시세 요청/이벤트 처리
    real = XAReal("S3_")
    real.OnReceiveRealData = lambda code: print(f"RealData: {code}")
    real.SetFieldData("InBlock", "shcode", "005930")
    real.AdviseRealData()


if __name__ == "__main__":
    sample()
    # 실시간 데이터 수신시 메시지 루프 필요
    import pythoncom
    while True:
        pythoncom.PumpWaitingMessages()

# Output:
'''
로그인 성공: [0000] 로그인 성공
Account List Count: 3
XXXXXXXXXXX 홍길동 선물옵션
XXXXXXXXXXX 홍길동 해외선옵
XXXXXXXXXXX 홍길동 종합매매
t1102 request succeeded: [00000] 정상적으로 조회가 완료되었습니다.
삼성전자 현재가: 51000
RealData: S3_
RealData: S3_
RealData: S3_
...
'''
```

### XASession, XAQuery, XAReal 클래스 사용법
LS증권 COM 개발가이드 참조: [LS증권 COM 개발가이드](https://www.ls-sec.co.kr/apiguide/guide.jsp?cno=100)
