# xingAsync Package

This is a simple package for aysnc XingApi (dll mode).

## Installation

```bash
pip install xingAsync
```

### 로그인 / 조회
```python
# -*- coding: euc-kr -*-
from xingAsync import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    print('로그인 요청중...')
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f'로그인 실패: {api.last_message}')
    print(f'로그인 성공: {'모의투자' if api.is_simulation else '실투자'}')

    # 보유계좌 표시
    for x in api.accounts: print(x)

    # 삼성전자 현재가 조회
    response = await api.request('t1102', '005930') # 005930: 삼성전자
    if not response: return print(f'요청실패: {api.last_message}')

    price = response['t1102OutBlock']['price']
    print(f'삼성전자 현재가: {price}')


if __name__ == "__main__":
    api = XingApi()
    from qasync import QApplication, QEventLoop
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(sample(api))

```

## 프로퍼티/메소드/이벤트

### 프로퍼티 (읽기전용)
    loaded:         xingApi.dll 로딩 여부 (True/False), xingApi가 설치되지 않은 경우 False
    logined:        로그인 여부 (True/False)
    is_simulation:  모의투자인 경우 True, 실계좌인 경우 False
    accounts:       계좌목록 (list)
    last_message:   마지막 수신 메시지, 요청 실패시 실패사유가 저장됨


### 메소드
    login: 로그인 (비동기)
        await api.login("user_id", "ser_pwd", "cert_pwd") # 모의투자인 경우 cert_pwd는 ''로 설정
        return: True/False, 로그인 성공여부, 실패시 last_message에 실패사유가 저장됨

    close: 로그아웃
        api.close()

    request: TR 요청 (비동기)

        # t1102: 주식현재가 요청, 삼성전자 
        response = await api.request("t1102", "005930")
        또는
        response = await api.request("t1102", {'shcode': '005930'})

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

        # 성공시 ResponseData 리턴, 실패시 None 리턴 (실패사유는 last_message에 저장됨)
        out_block = response['t1102OutBlock']               # t1102OutBlock 데이터 가져오기 (occurs 아닌 경우 dict)
        print(out_block['price'])                           # 삼성전자 현재가 출력

        out_block = response['t8410OutBlock']               # t8410OutBlock 데이터 가져오기 (occurs 아닌 경우 dict)
        print(out_block['jisiga'], out_block['jiclose'])    # 전일시가, 전일종가 출력

        out_block = response['t8410OutBlock1']              # t8410OutBlock1 데이터 가져오기 (occurs 경우 list)
        for data in out_block:
            print(data['date'], data['close'])              # 날짜, 종가 출력


    realtime: 실시간 구독/해지
        realtime("S3_", "005930", True) # 삼성전자 실시간 구독
        realtime("S3_", "005930", False) # 삼성전자 실시간 해지
        realtime("", "", False) # 모든 실시간 해지

    get_requests_count: TR 초당전송가능횟수, Base시간, 10분당 제한 건수, 10분내 요청 횟수 반환
        tr_per_sec, base_time, limit_count, request_count = api.get_requests_count("t1102")


### 이벤트
    on_message(msg: str): 서버 오류시 수신 (ex. 'LOGOUT', 'DISCONNECT')
    on_realtime(tr_cd: str, key: str, datas: dict): 실시간 데이터 수신
        ex: 'S3_', '005930', {'chetime': '090000', 'sign': '1', 'change': 100, 'drate': 0.1, 'price': 60000, ...}

