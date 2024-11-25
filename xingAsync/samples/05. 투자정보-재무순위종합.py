# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    inputs = {
        'gubun': '0',   # 시장구분(0:전체1:코스피2:코스닥))
        'gubun1': '2',  # 순위구분(1:매출액증가율2:영업이익증가율3:세전계속이익증가율4:부채비율5:유보율6:EPS7:BPS8:ROE9:PERa:PBRb:PEG)
        'gubun2': '1',  # 1 고정
        'idx': 0,       # 첫조회시 space, 연속조회시 Outblock의 idx 값 세팅
    }
    response = await api.request("t3341", inputs)
    if not response: return print(f'요청실패: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
t8424: [00000] 정상적으로 조회가 완료되었습니다.
Field Count = 1
t8424InBlock, Fields = 1, Count = 1
+--------+
| gubun1 |
+--------+
|   0    |
+--------+
t8424OutBlock, Fields = 2, Count = 242
+----------------------+--------+
|        hname         | upcode |
+----------------------+--------+
|     종       합      |  001   |
|     대   형  주      |  002   |
|     중   형  주      |  003   |
|     소   형  주      |  004   |
|     음 식 료 업      |  005   |
|     섬 유 의 복      |  006   |
|     종 이 목 재      |  007   |
...
| KP200 L KQ150 0.5 S  |  819   |
| KQ150 L KP200 0.5 S  |  820   |
+----------------------+--------+
+----------------------------+
|  request / elipsed times   |
+----------------------------+
| 2024-11-15 23:30:56.921416 |
|       0:00:00.005815       |
+----------------------------+
'''