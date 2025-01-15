from xingAsync import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        print(f'로그인 실패: {api.last_message}')
        return

    print(f'로그인 성공: {'모의투자' if api.is_simulation else '실투자'}')

    # 보유계좌 표시
    for x in api.accounts:
        print(x)

    # 삼성전자 현재가 조회
    response = await api.request('t1102', '005930') # 005930: 삼성전자
    if not response:
        print(f'요청실패: {api.last_message}')
        return

    price = response['t1102OutBlock']['price']
    print(f'삼성전자 현재가: {price}')

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
로그인 요청중...
로그인 성공: 실투자
XXXXXXXXXXX 홍길동 홍길동 선물옵션
XXXXXXXXXXX 홍길동 홍길동 해외선옵
XXXXXXXXXXX 홍길동 홍길동 종합매매
삼성전자 현재가: 53900
'''