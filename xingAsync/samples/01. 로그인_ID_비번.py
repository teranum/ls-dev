# -*- coding: euc-kr -*-
from xingAsync import *

async def sample(api: XingApi):
    if api.logined:
        print("이미 로그인 되었습니다.")
        for x in api.accounts: print(x)
        return

    user_id = input("사용자 아이디:")
    user_pwd = input("사용자 패스워드:")
    cert_pwd = input("공인인증 패스워드 (미입력시 모의투자로 로그인):")

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
