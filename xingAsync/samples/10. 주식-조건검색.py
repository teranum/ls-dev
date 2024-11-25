# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    response = await api.request("t1866", {"user_id": user_id, "gb":"0"}) # t1826: 종목Q클릭검색리스트
    if not response: return print(f'서버리스트 요청실패: {api.last_message}')

    print(response)
    if response['t1866OutBlock']['result_count'] == 0:
        return print("조건식이 없습니다.")

    # 첫번째 조건식 요청한다
    response = await api.request("t1857", ["0", "S", response['t1866OutBlock1'][0]['query_index']]) # t1857: e종목검색(API용)
    if not response: return print(f'종목검색 요청실패: {api.last_message}')
    print(response)



if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
t1866: [00000] 조회성공
t1866InBlock, Fields = 5, Count = 1
+----------+----+------------------------------------------+------+------------------------------------------+
| user_id  | gb |                group_name                | cont |                 contkey                  |
+----------+----+------------------------------------------+------+------------------------------------------+
| XXXXXXXX | 0  |                                          |      |                                          |
+----------+----+------------------------------------------+------+------------------------------------------+
t1866OutBlock, Fields = 3, Count = 1
+--------------+------+---------+
| result_count | cont | contkey |
+--------------+------+---------+
|      1       |      |         |
+--------------+------+---------+
t1866OutBlock1, Fields = 3, Count = 1
+--------------+------------+------------+
| query_index  | group_name | query_name |
+--------------+------------+------------+
| XXXXXXXX0001 |  돌파전략  |  이평돌파  |
+--------------+------------+------------+
nRqID=21, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 10:32:59.598256 |
|       0:00:02.071660       |
+----------------------------+
t1857: []
t1857InBlock, Fields = 3, Count = 1
+-----------+-------------+--------------+
| sRealFlag | sSearchFlag | query_index  |
+-----------+-------------+--------------+
|     0     |      S      | XXXXXXXX0001 |
+-----------+-------------+--------------+
t1857OutBlock, Fields = 3, Count = 1
+--------------+-------------+----------+
| result_count | result_time | AlertNum |
+--------------+-------------+----------+
|      2       |    103302   |          |
+--------------+-------------+----------+
t1857OutBlock1, Fields = 8, Count = 2
+--------+-------------------+-------+------+--------+------+--------+---------+
| shcode |       hname       | price | sign | change | diff | volume | JobFlag |
+--------+-------------------+-------+------+--------+------+--------+---------+
| 091170 |     KODEX 은행    |  8660 |  2   |   85   | 0.99 | 130189 |    N    |
| 364970 | TIGER 바이오TOP10 |  7665 |  2   |   95   | 1.25 | 486851 |    N    |
+--------+-------------------+-------+------+--------+------+--------+---------+
nRqID=22, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 10:33:01.679280 |
|       0:00:00.293146       |
+----------------------------+
'''