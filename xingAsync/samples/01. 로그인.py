# -*- coding: euc-kr -*-
from xingAsync import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if api.logined:
        print("이미 로그인 되었습니다.")
        for x in api.accounts: print(x)
        return

    print("로그인 요청중...")
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")
    print(f"로그인 성공: {"모의투자" if api.is_simulation else "실투자"}")

    for x in api.accounts: print(x)


if __name__ == "__main__":
    api = XingApi()
    from qasync import QApplication, QEventLoop
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(sample(api))
