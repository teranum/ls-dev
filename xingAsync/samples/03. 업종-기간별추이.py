# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    inputs = {
        "upcode": "001",    # 업종코드 (001: 종합...)
        "gubun2": '1',       # '1: 일별, 2: 주별, 3: 월별
        "cnt": 100,         # 조회건수
        "rate_gbn": '2',    # 비중구분 (1: 거래량, 2: 거래대금)
        }
    response = await api.request("t1514", "001   1          0100 2 ")
    if not response: return print(f'요청실패: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
'''