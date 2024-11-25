# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    real_code = "S3_"   # 실시간 코드: (S3_: KOSPI체결, H1_: KOSPI호가잔량, DH1: KOSPI시간외단일가호가잔량, ...)
    key = "005930"      # 실시간 Key/종목코드: (005930: 삼성전자, ...)
    advise = True       # True 이면 실시간 시작, False 이면 실시간 중지

    if api.realtime(real_code, key, advise):
        print(f"요청 성공: {real_code}, {key}, {advise}")
    else:
        print(f"요청 실패: {api.last_message}")

if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(lambda tr_cd, key, datas: print(f"on_realtime: {tr_cd}, {key}, {datas}"))
    run_loop(sample(api), forever=True) # 무한루프로 실행

# Output:
'''
요청 성공: S3_, 005930, True
'''