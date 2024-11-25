# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")
    
    inputs = {
        'shcode': '005930',     # 삼성전자
        'gubun': '2',           # 주기구분(2:일3:주4:월5:년)
        'qrycnt': 100,          # 요청건수(최대-압축:2000비압축:500)
        'sdate': '',            # 시작일자
        'edate': '99999999',    # 종료일자
        'cts_date': '',         # 연속일자
        'comp_yn': 'N',         # 압축여부(Y:압축N:비압축)
        'sujung': 'Y',          # 수정주가여부(Y:적용N:비적용)
    }
    response = await api.request("t8410", inputs)
    if not response: return print(f'요청실패: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
t8410: [00000] 정상적으로 조회가 완료되었습니다.
t8410InBlock, Fields = 8, Count = 1
+--------+-------+--------+-------+----------+----------+---------+--------+
| shcode | gubun | qrycnt | sdate |  edate   | cts_date | comp_yn | sujung |
+--------+-------+--------+-------+----------+----------+---------+--------+
| 005930 |   2   |  0100  |       | 99999999 |          |    N    |   Y    |
+--------+-------+--------+-------+----------+----------+---------+--------+
t8410OutBlock, Fields = 19, Count = 1
+--------+--------+--------+-------+---------+----------+--------+--------+-------+---------+---------+--------+----------+--------+--------+--------+-----------+----------------+----------------+
| shcode | jisiga | jihigh | jilow | jiclose | jivolume | disiga | dihigh | dilow | diclose | highend | lowend | cts_date | s_time | e_time | dshmin | rec_count | svi_uplmtprice | svi_dnlmtprice |
+--------+--------+--------+-------+---------+----------+--------+--------+-------+---------+---------+--------+----------+--------+--------+--------+-----------+----------------+----------------+
| 005930 | 56100  | 56500  | 54800 |  55300  | 20834397 | 54900  | 55600  | 54700 |  55500  |  71800  | 38800  | 20240625 | 090000 | 153000 |   10   |    100    |     60400      |     49400      |
+--------+--------+--------+-------+---------+----------+--------+--------+-------+---------+---------+--------+----------+--------+--------+--------+-----------+----------------+----------------+
t8410OutBlock1, Fields = 12, Count = 100
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
|   date   |  open |  high |  low  | close | jdiff_vol |  value  | jongchk | rate | pricechk | ratevalue | sign |
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
| 20240626 | 80100 | 81400 | 79900 | 81300 |  15860957 | 1280215 |    0    | 0.0  |    0     |     0     |  2   |
| 20240627 | 81300 | 81600 | 80500 | 81600 |  11623067 |  943736 |    0    | 0.0  |    0     |     0     |  2   |
| 20240628 | 81900 | 81900 | 80800 | 81500 |  8766207  |  712734 |    0    | 0.0  |    0     |     0     |  5   |
| 20240701 | 81500 | 82100 | 81300 | 81800 |  11317202 |  925401 |    0    | 0.0  |    0     |     0     |  2   |
| 20240702 | 82500 | 82600 | 81500 | 81800 |  14462912 | 1185273 |    0    | 0.0  |    0     |     0     |  3   |
| 20240703 | 82300 | 82300 | 81000 | 81800 |  11440328 |  933802 |    0    | 0.0  |    0     |     0     |  3   |
...
| 20241112 | 54600 | 54600 | 53000 | 53000 |  33146740 | 1780062 |    0    | 0.0  |    0     |     0     |  5   |
| 20241113 | 52000 | 53000 | 50500 | 50600 |  51256083 | 2638273 |    0    | 0.0  |    0     |     0     |  5   |
| 20241114 | 50200 | 51800 | 49900 | 49900 |  45688129 | 2322056 |    0    | 0.0  |    0     |     0     |  5   |
| 20241115 | 50300 | 54200 | 50300 | 53500 |  44273164 | 2332587 |    0    | 0.0  |    0     |     0     |  2   |
| 20241118 | 57000 | 57500 | 55900 | 56700 |  47922973 | 2716382 |    0    | 0.0  |    0     |     0     |  2   |
| 20241119 | 56500 | 57500 | 55900 | 56300 |  31539632 | 1786885 |    0    | 0.0  |    0     |     0     |  5   |
| 20241120 | 56100 | 56500 | 54800 | 55300 |  20834397 | 1154360 |    0    | 0.0  |    0     |     0     |  5   |
| 20241121 | 54900 | 55600 | 54700 | 55500 |  5087736  |  280699 |    0    | 0.0  |    0     |     0     |  2   |
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
nRqID=12, cont_yn=True, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-21 10:03:19.053163 |
|       0:00:00.008966       |
+----------------------------+
'''