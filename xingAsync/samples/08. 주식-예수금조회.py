# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd, acc_pwd_number # app_key.py 파일에 사용자 ID, 비번, 공증 비번, 계좌비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    # 계좌번호 가져오기
    acc_name = "종합매매"
    acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
    if not acc: return print(f"{acc_name} 계좌가 없습니다.")
    pass_number = "0000" if api.is_simulation else acc_pwd_number

    # CSPAQ22200: 현물계좌예수금 주문가능금액 총평가2
    inputs = {"RecCnt":1, "AcntNo": acc.number, "Pwd": pass_number, "BalCreTp": "0"}
    response = await api.request("CSPAQ22200", inputs)
    if not response: return print(f'요청실패: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
CSPAQ22200: [00136] 조회가 완료되었습니다.
CSPAQ22200InBlock1, Fields = 5, Count = 1
+--------+-----------+-------------+------+----------+
| RecCnt | MgmtBrnNo |    AcntNo   | Pwd  | BalCreTp |
+--------+-----------+-------------+------+----------+
|   1    |           | XXXXXXXXXXX | 0000 |    0     |
+--------+-----------+-------------+------+----------+
CSPAQ22200OutBlock1, Fields = 5, Count = 1
+--------+-----------+-------------+----------+----------+
| RecCnt | MgmtBrnNo |    AcntNo   |   Pwd    | BalCreTp |
+--------+-----------+-------------+----------+----------+
|   1    |           | XXXXXXXXXXX | ******** |    0     |
+--------+-----------+-------------+----------+----------+
CSPAQ22200OutBlock2, Fields = 37, Count = 1
+--------+-------------+--------+---------------+-----------------+--------------+---------------+----------------+------------------------+--------------------+--------------------+----------------+-----+----------+--------+----------+-------+-------+----------+-------------------+-------------------+----------+--------------+-------------+----------+---------------+---------------+----------------+------------------+-------+-----------------+---------------+-------------------+------------------+-------------------+------------------+---------------+
| RecCnt |    BrnNm    | AcntNm | MnyOrdAbleAmt | SubstOrdAbleAmt | SeOrdAbleAmt | KdqOrdAbleAmt | CrdtPldgOrdAmt | MgnRat100pctOrdAbleAmt | MgnRat35ordAbleAmt | MgnRat50ordAbleAmt | CrdtOrdAbleAmt | Dps | SubstAmt | MgnMny | MgnSubst | D1Dps | D2Dps | RcvblAmt | D1ovdRepayRqrdAmt | D2ovdRepayRqrdAmt | MloanAmt | ChgAfPldgRat | RqrdPldgAmt | PdlckAmt | OrgPldgSumAmt | SubPldgSumAmt | CrdtPldgAmtMny | CrdtPldgSubstAmt | Imreq | CrdtPldgRuseAmt | DpslRestrcAmt | PrdaySellAdjstAmt | PrdayBuyAdjstAmt | CrdaySellAdjstAmt | CrdayBuyAdjstAmt | CslLoanAmtdt1 |
+--------+-------------+--------+---------------+-----------------+--------------+---------------+----------------+------------------------+--------------------+--------------------+----------------+-----+----------+--------+----------+-------+-------+----------+-------------------+-------------------+----------+--------------+-------------+----------+---------------+---------------+----------------+------------------+-------+-----------------+---------------+-------------------+------------------+-------------------+------------------+---------------+
|   1    | 다이렉트205 | 홍길동 |       0       |        0        |      0       |       0       |       0        |           0            |         0          |         0          |       0        |  0  |    0     |   0    |    0     |   0   |   0   |    0     |         0         |         0         |    0     |     0.0      |      0      |    0     |       0       |       0       |       0        |        0         |   0   |        0        |       0       |         0         |        0         |         0         |        0         |       0       |
+--------+-------------+--------+---------------+-----------------+--------------+---------------+----------------+------------------------+--------------------+--------------------+----------------+-----+----------+--------+----------+-------+-------+----------+-------------------+-------------------+----------+--------------+-------------+----------+---------------+---------------+----------------+------------------+-------+-----------------+---------------+-------------------+------------------+-------------------+------------------+---------------+
+----------------------------+
|  request / elipsed times   |
+----------------------------+
| 2024-11-16 16:20:15.028677 |
|       0:00:00.019998       |
+----------------------------+
'''