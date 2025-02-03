from xingAsync import XingCOM
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

########################################################################################
# COM 객체 통합 Wrapper XingCOM 클래스 테스트
# * asyncio를 사용하지 않음, asyncio 이용 어려울 경우 사용 (가능한 DLL 모드 XingApi 이용 권장)
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
    api.on_realtime = on_realtime
    sample(api)
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
...
'''