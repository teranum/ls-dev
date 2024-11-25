# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    inputs = {
        'delaygb': "R",  # 지연구분, 'R'로 설정
        'natcode': "US", # 국가구분
        'exgubun': "2",  # 거래소구분, 1:뉴욕, 2:나스닥, 3:아멕스, 4:미국전체
        'cts_value': '', # 연속키
        }
    response = await api.request("g3190", inputs) # 해외주식 API 마스터 조회
    if not response: return print(f'요청실패: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
g3190: [00000] 조회완료
g3190InBlock, Fields = 5, Count = 1
+---------+---------+---------+---------+-----------+
| delaygb | natcode | exgubun | readcnt | cts_value |
+---------+---------+---------+---------+-----------+
|    R    |    US   |    2    |    0    |           |
+---------+---------+---------+---------+-----------+
g3190OutBlock, Fields = 5, Count = 1
+---------+---------+---------+------------------+-----------+
| delaygb | natcode | exgubun |    cts_value     | rec_count |
+---------+---------+---------+------------------+-----------+
|    R    |    US   |    2    | 0000000000000001 |    4474   |
+---------+---------+---------+------------------+-----------+
g3190OutBlock1, Fields = 30, Count = 4474
+-----------+---------+--------+--------+---------+--------------------------------------------------------------+--------------------------------------------------------------+----------+--------------+------------+----------+-------------+--------------+--------+---------+-------------+-------------+----------+-------------+-------------+---------+----------+----------+-------+----------+----------+------+------+------+-------+
| keysymbol | natcode | exchcd | symbol | seccode |                           korname                            |                           engname                            | currency |     isin     | floatpoint | indusury |    share    |  marketcap   |  par   | parcurr | bidlotsize2 | asklotsize2 |   clos   | listed_date | expire_date | suspend |   bymd   | sellonly | stamp | ticktype |   pcls   | vcmf | casf | posf | point |
+-----------+---------+--------+--------+---------+--------------------------------------------------------------+--------------------------------------------------------------+----------+--------------+------------+----------+-------------+--------------+--------+---------+-------------+-------------+----------+-------------+-------------+---------+----------+----------+-------+----------+----------+------+------+------+-------+
|   82AACG  |    US   |   82   |  AACG  |  82AACG |                 ATA 크리에티비티 글로벌(ADR)                 |      ATA CREATIVITY GLOBAL SPON ADS EACH REP 2 ORD SHS       |   USD    | US00211V1061 |     4      |   3540   |   31964505  |    674728    |  0.0   |         |      1      |      1      |   1.02   |   20191017  |   00000000  |    N    | 20241120 |    0     |       |    1     |   1.02   |      |      |      |   N   |
|   82AADI  |    US   |   82   |  AADI  |  82AADI |                     AADI 바이오사이언스                      |                     AADI BIOSCIENCE INC                      |   USD    | US00032Q1040 |     4      |   4010   |   24647400  |     2000     |  0.0   |         |      1      |      1      |   2.21   |   20210827  |   00000000  |    N    | 20241120 |    0     |       |    1     |   2.21   |      |      |      |   N   |
|   82AADR  |    US   |   82   |  AADR  |  82AADR |   ADVISORSHARES TRUST ADVISORSHARES DORSEY WRIGHT ADR ETF    |   ADVISORSHARES TRUST ADVISORSHARES DORSEY WRIGHT ADR ETF    |   USD    | US00768Y2063 |     4      |   9010   |    380000   |      0       |  0.0   |         |      1      |      1      |  66.83   |   20210603  |   00000000  |    N    | 20241120 |    0     |       |    1     |  66.83   |      |      |      |   N   |
|   82AAL   |    US   |   82   |  AAL   |  82AAL  |                   아메리칸 에어라인스 그룹                   |                 AMERICAN AIRLINES GROUP INC                  |   USD    | US02376R1023 |     4      |   2040   |  657131000  |   7000000    |  0.01  |   USD   |      1      |      1      |  14.33   |   20131210  |   00000000  |    N    | 20241120 |    0     |       |    1     |  14.33   |      |      |      |   Y   |
|   82AAME  |    US   |   82   |  AAME  |  82AAME |                      애틀랜틱 아메리칸                       |                    ATLANTIC AMERICAN CORP                    |   USD    | US0482091008 |     4      |   4520   |   20399800  |   22401000   |  1.0   |   USD   |      1      |      1      |   1.6    |   19840907  |   00000000  |    N    | 20241120 |    0     |       |    1     |   1.6    |      |      |      |   N   |
|   82AAOI  |    US   |   82   |  AAOI  |  82AAOI |                 어플라이드 옵토일렉트로닉스                  |                 APPLIED OPTOELECTRONICS INC                  |   USD    | US03823U1025 |     4      |   2510   |   45078200  |    45000     |  0.0   |         |      1      |      1      |  28.55   |   20130925  |   00000000  |    N    | 20241120 |    0     |       |    1     |  28.55   |      |      |      |   N   |
|   82AAON  |    US   |   82   |  AAON  |  82AAON |                          에이에이온                          |                           AAON INC                           |   USD    | US0003602069 |     4      |   2010   |   81279600  |    325000    |  0.0   |         |      1      |      1      |  131.16  |   19910108  |   00000000  |    N    | 20241120 |    0     |       |    1     |  131.16  |      |      |      |   N   |
|   82AAPB  |    US   |   82   |  AAPB  |  82AAPB |        GRANITESHARES ETF TRUST 2X LONG AAPL DAILY ETF        |        GRANITESHARES ETF TRUST 2X LONG AAPL DAILY ETF        |   USD    | US38747R8842 |     4      |   9010   |    770001   |      0       |  0.0   |         |      1      |      1      |  28.39   |   20220809  |   00000000  |    N    | 20241120 |    0     |       |    1     |  28.39   |      |      |      |   N   |
|   82AAPD  |    US   |   82   |  AAPD  |  82AAPD |       DIREXION SHARES ETF TRUST DAILY AAPL BEAR 1X SHS       |       DIREXION SHARES ETF TRUST DAILY AAPL BEAR 1X SHS       |   USD    | US25461A3041 |     4      |   9010   |   1475000   |      0       |  0.0   |         |      1      |      1      |  16.84   |   20220809  |   00000000  |    N    | 20241120 |    0     |       |    1     |  16.84   |      |      |      |   N   |
|   82AAPL  |    US   |   82   |  AAPL  |  82AAPL |                             애플                             |                          APPLE INC                           |   USD    | US0378331005 |     4      |   2520   | 15115800000 | 83276000000  |  0.0   |         |      1      |      1      |  228.28  |   19801212  |   00000000  |    N    | 20241120 |    0     |       |    1     |  228.28  |      |      |      |   Y   |
...
|   82ZVRA  |    US   |   82   |  ZVRA  |  82ZVRA |                      지브러 테라퓨틱스                       |                    ZEVRA THERAPEUTICS INC                    |   USD    | US4884452065 |     4      |   4010   |   53375900  |     5000     |  0.0   |         |      1      |      1      |   8.97   |   20230301  |   00000000  |    N    | 20241120 |    0     |       |    1     |   8.97   |      |      |      |   N   |
|   82ZVSA  |    US   |   82   |  ZVSA  |  82ZVSA |                     자이버사 테라퓨틱스                      |                   ZYVERSA THERAPEUTICS INC                   |   USD    | US98987D3008 |     4      |   4010   |   1074196   |     107      |  0.0   |         |      1      |      1      |   1.23   |   20221213  |   00000000  |    N    | 20241120 |    0     |       |    1     |   1.23   |      |      |      |   N   |
|   82ZYME  |    US   |   82   |  ZYME  |  82ZYME |                           자임웍스                           |                      ZYMEWORKS INC (US)                      |   USD    | US98985Y1082 |     4      |   4010   |   68877500  |  1022515000  |  0.0   |         |      1      |      1      |  14.77   |   20221216  |   00000000  |    N    | 20241120 |    0     |       |    1     |  14.77   |      |      |      |   N   |
|   82ZYXI  |    US   |   82   |  ZYXI  |  82ZYXI |                            지넥스                            |                          ZYNEX INC                           |   USD    | US98986M1036 |     4      |   4020   |   31845500  |    32000     |  0.0   |         |      1      |      1      |   7.82   |   20190212  |   00000000  |    N    | 20241120 |    0     |       |    1     |   7.82   |      |      |      |   N   |
|   82ZZZ   |    US   |   82   |  ZZZ   |  82ZZZ  |     ONEFUND TRUST CYBER HORNET S&P 500 & BITCOIN 75/25 S     |     ONEFUND TRUST CYBER HORNET S&P 500 & BITCOIN 75/25 S     |   USD    | US45407J4094 |     4      |   9010   |    125000   |      0       |  0.0   |         |      1      |      1      |  27.532  |   20231228  |   00000000  |    N    | 20241120 |    0     |       |    1     |  27.532  |      |      |      |   N   |
+-----------+---------+--------+--------+---------+--------------------------------------------------------------+--------------------------------------------------------------+----------+--------------+------------+----------+-------------+--------------+--------+---------+-------------+-------------+----------+-------------+-------------+---------+----------+----------+-------+----------+----------+------+------+------+-------+
nRqID=23, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-21 06:42:09.779295 |
|       0:00:00.228221       |
+----------------------------+
'''