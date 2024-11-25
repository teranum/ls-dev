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

    현재가 = response['t1102OutBlock']['price']
    print(f'삼성전자 현재가: {현재가}')


if __name__ == '__main__':
    api = XingApi()
    from qasync import QApplication, QEventLoop
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(sample(api))