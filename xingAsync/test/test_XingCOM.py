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