# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd, acc_pwd_number # app_key.py 파일에 사용자 ID, 비번, 공증 비번, 계좌비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    # 계좌번호 가져오기
    acc_name = "선물옵션"
    acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
    if not acc: return print(f"{acc_name} 계좌가 없습니다.")
    pass_number = "0000" if api.is_simulation else acc_pwd_number

    # CFOBQ10500: 선물옵션 계좌예탁금증거금조회
    inputs = {'RecCnt': 1, 'AcntNo': acc.number, 'Pwd': pass_number}
    response = await api.request("CFOBQ10500", inputs)
    if not response: return print(f'요청실패: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
CFOBQ10500: [00136] 조회가 완료되었습니다.
CFOBQ10500InBlock1, Fields = 3, Count = 1
+--------+-------------+------+
| RecCnt |    AcntNo   | Pwd  |
+--------+-------------+------+
|   1    | XXXXXXXXXXX | 0000 |
+--------+-------------+------+
CFOBQ10500OutBlock1, Fields = 3, Count = 1
+--------+-------------+----------+
| RecCnt |    AcntNo   |   Pwd    |
+--------+-------------+----------+
|   1    | XXXXXXXXXXX | ******** |
+--------+-------------+----------+
CFOBQ10500OutBlock2, Fields = 24, Count = 1
+--------+--------+--------------+-----+----------+-------------------+----------+------------+--------------+------------------+--------------------+-----+--------+------------+---------------+--------+-----------+-------------------+----------------------+----------------------+---------------+---------------+---------------+-----------------+
| RecCnt | AcntNm | DpsamtTotamt | Dps | SubstAmt | FilupDpsamtTotamt | FilupDps | FutsPnlAmt | WthdwAbleAmt | PsnOutAbleCurAmt | PsnOutAbleSubstAmt | Mgn | MnyMgn | OrdAbleAmt | MnyOrdAbleAmt | AddMgn | MnyAddMgn | AmtPrdayChckInAmt | FnoPrdaySubstSellAmt | FnoCrdaySubstSellAmt | FnoPrdayFdamt | FnoCrdayFdamt | FcurrSubstAmt |  FnoAcntAfmgnNm |
+--------+--------+--------------+-----+----------+-------------------+----------+------------+--------------+------------------+--------------------+-----+--------+------------+---------------+--------+-----------+-------------------+----------------------+----------------------+---------------+---------------+---------------+-----------------+
|   1    | 홍길동 |      0       |  0  |    0     |         0         |    0     |     0      |      0       |        0         |         0          |  0  |   0    |     0      |       0       |   0    |     0     |         0         |          0           |          0           |       0       |       0       |       0       | 사전증거금 계좌 |
+--------+--------+--------------+-----+----------+-------------------+----------+------------+--------------+------------------+--------------------+-----+--------+------------+---------------+--------+-----------+-------------------+----------------------+----------------------+---------------+---------------+---------------+-----------------+
CFOBQ10500OutBlock3, Fields = 18, Count = 0
+-------------+------------+--------+---------+------------+--------+--------+--------------+---------+----------+----------------+-----------------+---------------+----------------+------------+----------------+------------+------------+
| PdGrpCodeNm | NetRiskMgn | PrcMgn | SprdMgn | PrcFlctMgn | MinMgn | OrdMgn | OptNetBuyAmt | CsgnMgn | MaintMgn | FutsBuyExecAmt | FutsSellExecAmt | OptBuyExecAmt | OptSellExecAmt | FutsPnlAmt | TotRiskCsgnMgn | UndCsgnMgn | MgnRdctAmt |
+-------------+------------+--------+---------+------------+--------+--------+--------------+---------+----------+----------------+-----------------+---------------+----------------+------------+----------------+------------+------------+
+-------------+------------+--------+---------+------------+--------+--------+--------------+---------+----------+----------------+-----------------+---------------+----------------+------------+----------------+------------+------------+
+----------------------------+
|  request / elipsed times   |
+----------------------------+
| 2024-11-16 16:25:10.743924 |
|       0:00:00.025808       |
+----------------------------+
'''