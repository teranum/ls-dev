# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    response = await api.request("o3101", "")
    if not response: return print(f'o3101 요청실패: {api.last_message}')

    comp_BscGdsCd = ''
    recent_code_lists = []
    market_items = response['o3101OutBlock']
    for item in market_items:
        BscGdsCd = item['BscGdsCd']
        if BscGdsCd != comp_BscGdsCd:
            comp_BscGdsCd = BscGdsCd
            recent_code_lists.append(item['Symbol'])
    print(f'해외선물시장 {len(market_items)}종목중 최근월물 {len(recent_code_lists)}종목 조회')
    # 매 데이터 앞에 'F'문자를 붙인 후 ','로 연결
    recent_code_str = ','.join(['F'+code for code in recent_code_lists])
    response = await api.request("o3127", recent_code_str)

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
해외선물시장 44종목중 최근월물 8종목 조회
o3127: [00000] 정상적으로 조회가 완료되었습니다.
o3127InBlock, Fields = 1, Count = 1
+------+
| nrec |
+------+
|  8   |
+------+
o3127InBlock1, Fields = 2, Count = 8
+-------+---------+
| mktgb |  symbol |
+-------+---------+
|   F   |  CUSX24 |
|   F   | HCEIX24 |
|   F   | HCHHX24 |
|   F   | HMCEX24 |
|   F   |  HMHX24 |
|   F   |  HSIX24 |
|   F   |  HTIX24 |
|   F   |  MCAZ24 |
+-------+---------+
o3127OutBlock, Fields = 21, Count = 8
+---------+---------------------------------------+---------+------+--------+-------+--------+-----------+---------+---------+---------+----------+---------+-----------+---------+-----------+---------+----------+--------+-------+-----+
|  symbol |               symbolname              |  price  | sign | change |  diff | volume | jnilclose |   open  |   high  |   low   | offerho1 |  bidho1 | offercnt1 | bidcnt1 | offerrem1 | bidrem1 | offercnt | bidcnt | offer | bid |
+---------+---------------------------------------+---------+------+--------+-------+--------+-----------+---------+---------+---------+----------+---------+-----------+---------+-----------+---------+----------+--------+-------+-----+
|  CUSX24 |       Renminbi_USD/CNH(2024.11)       |  7.241  |  3   |  0.0   |  0.0  |   0    |   7.241   |   0.0   |   0.0   |   0.0   |   0.0    |   0.0   |     0     |    0    |     0     |    0    |    0     |   0    |   0   |  0  |
| HCEIX24 |            H-Share(2024.11)           |  7071.0 |  2   |  2.0   |  0.03 |  3805  |   7069.0  |  7070.0 |  7091.0 |  7061.0 |  7072.0  |  7070.0 |     4     |    3    |     7     |    7    |    30    |   24   |   54  |  47 |
| HCHHX24 |         CES China 120(2024.11)        |   0.0   |  3   |  0.0   |  0.0  |   0    |   5831.0  |   0.0   |   0.0   |   0.0   |   0.0    |   0.0   |     0     |    0    |     0     |    0    |    0     |   0    |   0   |  0  |
| HMCEX24 |         Mini H-Shares(2024.11)        |  7071.0 |  2   |  3.0   |  0.04 |  290   |   7068.0  |  7067.0 |  7092.0 |  7063.0 |  7072.0  |  7070.0 |     2     |    2    |     2     |    3    |    8     |   10   |   11  |  15 |
|  HMHX24 |        Mini Hang Seng(2024.11)        | 19606.0 |  5   |  5.0   | -0.03 |  2223  |  19611.0  | 19606.0 | 19662.0 | 19589.0 | 19607.0  | 19604.0 |     3     |    1    |     3     |    1    |    18    |   22   |   29  |  40 |
|  HSIX24 |           Hang Seng(2024.11)          | 19607.0 |  2   |  2.0   |  0.01 |  2502  |  19605.0  | 19610.0 | 19663.0 | 19589.0 | 19607.0  | 19604.0 |     5     |    3    |     5     |    3    |    23    |   21   |   23  |  21 |
|  HTIX24 |        Hang Seng TECH(2024.11)        |  4359.0 |  2   |  3.0   |  0.07 |  1670  |   4356.0  |  4355.0 |  4370.0 |  4350.0 |  4359.0  |  4358.0 |     3     |    2    |     14    |    3    |    35    |   30   |   72  | 196 |
|  MCAZ24 | MSCI China A50 Connect Index(2024.12) |  2131.8 |  2   |  0.6   |  0.03 |  213   |   2131.2  |  2132.6 |  2135.6 |  2131.2 |  2132.0  |  2131.2 |     2     |    1    |     2     |    1    |    6     |   6    |   9   |  10 |
+---------+---------------------------------------+---------+------+--------+-------+--------+-----------+---------+---------+---------+----------+---------+-----------+---------+-----------+---------+----------+--------+-------+-----+
nRqID=22, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 20:45:14.269670 |
|       0:00:00.006002       |
+----------------------------+
'''