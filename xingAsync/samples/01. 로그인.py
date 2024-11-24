# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if api.logined:
        print("이미 로그인 되었습니다.")
        print(api.accounts, "보유계좌")
        return

    print("로그인 요청중...")
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")
    print(f"로그인 성공: {"모의투자" if api.is_simulation else "실투자"}")

    print(api.accounts, "보유계좌")


if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api), True) # 루프 실행, 또는 아래와 같이 실행
