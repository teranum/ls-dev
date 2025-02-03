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
로그인 요청중...
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