# LS증권 XingAPI wrapper

This is a simple package for XingApi (DLL and COM mode).

## Installation

```bash
pip install xingAsync
```

## Usage
DLL, COM 모드 지원. (DLL 권장)<br/>
DLL Wrapper class: XingApi<br/>
COM Wrapper class: XingCOM<br/>
COM base classes: XASession, XAQuery, XAReal<br/>

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

    # 요청: 삼성전자("005930") 현재가 조회
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
    if not api.realtime("OVC", codes, True):
    # if not api.realtime("S3_", codes, True):
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
삼성전자 현재가: 51000
실시간 요청 성공, 60초동안 실시간 수신...
S3_, 000660, {'chetime': '155035', 'sign': '5', 'change': 8300, 'drate': -4.17, 'price': 190900, 'opentime': '090010', 'open': 191500, 'hightime': '090314', 'high': 193200, 'lowtime': '101207', 'low': 186900, 'cgubun': '-', 'cvolume': 30, 'volume': 7668632, 'value': 1457842, 'mdvolume': 4020761, 'mdchecnt': 94515, 'msvolume': 3098169, 'mschecnt': 65613, 'cpower': 77.05, 'w_avrg': 190104, 'offerho': 191000, 'bidho': 190900, 'status': '04', 'jnilvolume': 11827867, 'shcode': '000660'}
S3_, 005930, {'chetime': '155035', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 1, 'volume': 32014833, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181567, 'mschecnt': 171443, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155035', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 1, 'volume': 32014834, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181568, 'mschecnt': 171444, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155035', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 2, 'volume': 32014836, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181570, 'mschecnt': 171445, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155038', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 3, 'volume': 32014839, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181573, 'mschecnt': 171446, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155038', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 100, 'volume': 32014939, 'value': 1632742, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181673, 'mschecnt': 171447, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155038', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 19, 'volume': 32014958, 'value': 1632743, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181692, 'mschecnt': 171448, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
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
        # 또는
        response = await api.request("t1102", {'shcode': '005930'})

        # 성공시 ResponseData 리턴, 실패시 None 리턴 (실패사유는 last_message에 저장됨)
        # 블록타입이 배열이 아닌 경우 dict 로 반환됨, 배열(occurs)인 경우 list[dict] 로 반환됨)

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

########################################################################################
# COM 객체 통합 Wrapper XingCOM 클래스 테스트
# * asyncio를 사용하지 않음, asyncio 이용 어려울 경우 사용 (가능한 DLL 모드 XingApi 이용 권장)
# * DLL모드와 인터페이스 동일
# * t1857, ChartIndex 서비스요청은 XAQuery 이용
########################################################################################

def sample(api:XingCOM):
    # 로그인
    if not api.login(user_id, user_pwd, cert_pwd):
        print(f"로그인 실패: {api.last_message}")
        return

    print(f"로그인 성공: {"모의투자" if api.is_simulation else "실투자"}")

    # 보유계좌 표시
    for x in api.accounts:
        print(x)

    # 요청: 삼성전자("005930") 현재가 조회
    response = api.request("t1102", {"shcode": "005930"})
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
삼성전자 현재가: 51000
S3_, 000660, {'chetime': '155035', 'sign': '5', 'change': 8300, 'drate': -4.17, 'price': 190900, 'opentime': '090010', 'open': 191500, 'hightime': '090314', 'high': 193200, 'lowtime': '101207', 'low': 186900, 'cgubun': '-', 'cvolume': 30, 'volume': 7668632, 'value': 1457842, 'mdvolume': 4020761, 'mdchecnt': 94515, 'msvolume': 3098169, 'mschecnt': 65613, 'cpower': 77.05, 'w_avrg': 190104, 'offerho': 191000, 'bidho': 190900, 'status': '04', 'jnilvolume': 11827867, 'shcode': '000660'}
S3_, 005930, {'chetime': '155035', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 1, 'volume': 32014833, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181567, 'mschecnt': 171443, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155035', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 1, 'volume': 32014834, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181568, 'mschecnt': 171444, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155035', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 2, 'volume': 32014836, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181570, 'mschecnt': 171445, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155038', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 3, 'volume': 32014839, 'value': 1632737, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181573, 'mschecnt': 171446, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155038', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 100, 'volume': 32014939, 'value': 1632742, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181673, 'mschecnt': 171447, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
S3_, 005930, {'chetime': '155038', 'sign': '5', 'change': 1400, 'drate': -2.67, 'price': 51000, 'opentime': '090009', 'open': 51100, 'hightime': '090024', 'high': 51400, 'lowtime': '120604', 'low': 50800, 'cgubun': '+', 'cvolume': 19, 'volume': 32014958, 'value': 1632743, 'mdvolume': 13697992, 'mdchecnt': 70651, 'msvolume': 15181692, 'mschecnt': 171448, 'cpower': 110.83, 'w_avrg': 51000, 'offerho': 51000, 'bidho': 50900, 'status': '04', 'jnilvolume': 42078071, 'shcode': '005930'}
...
'''
```


## COM 기본모드 XASession, XAQuery, XAReal 이용
### 로그인/요청/실시간 조회
```python
from xingAsync import XASession, XAQuery, XAReal
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

########################################################################################
# COM 객체 XASession, XAQuery, XAReal 테스트
# * asyncio를 사용하지 않음, asyncio 이용 어려울 경우 사용 (가능한 DLL 모드 XingApi 이용 권장)
# * Res파일 경로 설정 필요없음
# * OnLogin, OnReceiveData 이벤트 처리 필요없음, 실시간 데이터 수신시 OnReceiveRealData 이벤트 처리 필요
########################################################################################

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

    # 요청: 삼성전자("005930") 현재가 조회
    query = XAQuery("t1102")
    query.SetFieldData("t1102InBlock", "shcode", 0, "005930")
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
