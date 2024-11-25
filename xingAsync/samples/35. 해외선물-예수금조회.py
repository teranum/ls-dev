# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd, acc_pwd_number # app_key.py 파일에 사용자 ID, 비번, 공증 비번, 계좌비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    # 계좌번호 가져오기
    acc_name = ["해외선물", "해외선옵"]
    acc = next((item for item in api.accounts if item.detail_name in acc_name), None)
    if not acc: return print(f"{acc_name} 계좌가 없습니다.")
    pass_number = "0000" if api.is_simulation else acc_pwd_number

    # CIDBQ05300: 해외선물 계좌예탁자산 조회
    inputs = {'RecCnt': 1, 'OvrsAcntTpCode': '1', 'AcntNo': acc.number, 'AcntPwd': pass_number, 'CrcyCode': 'ALL'}
    response = await api.request("CIDBQ05300", inputs)
    if not response: return print(f'요청실패: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
CIDBQ03000: [00200] 조회내역이 없습니다.
CIDBQ03000InBlock1, Fields = 5, Count = 1
+--------+------------+-------------+---------+-------+
| RecCnt | AcntTpCode |    AcntNo   | AcntPwd | TrdDt |
+--------+------------+-------------+---------+-------+
|   1    |     1      | XXXXXXXXXXX |   0000  |       |
+--------+------------+-------------+---------+-------+
CIDBQ03000OutBlock1, Fields = 5, Count = 1
+--------+------------+-------------+----------+-------+
| RecCnt | AcntTpCode |    AcntNo   | AcntPwd  | TrdDt |
+--------+------------+-------------+----------+-------+
|   1    |     1      | XXXXXXXXXXX | ******** |       |
+--------+------------+-------------+----------+-------+
CIDBQ03000OutBlock2, Fields = 17, Count = 0
+--------+-------+-------------+-------------+---------------+--------------------+-----------------+-----------+--------------+-----------------+----------------+----------------------+--------------------+--------------------+----------------+----------------+-------------------+
| AcntNo | TrdDt | CrcyObjCode | OvrsFutsDps | CustmMnyioAmt | AbrdFutsLqdtPnlAmt | AbrdFutsCmsnAmt | PrexchDps | EvalAssetAmt | AbrdFutsCsgnMgn | AbrdFutsAddMgn | AbrdFutsWthdwAbleAmt | AbrdFutsOrdAbleAmt | AbrdFutsEvalPnlAmt | LastSettPnlAmt | OvrsOptSettAmt | OvrsOptBalEvalAmt |
+--------+-------+-------------+-------------+---------------+--------------------+-----------------+-----------+--------------+-----------------+----------------+----------------------+--------------------+--------------------+----------------+----------------+-------------------+
+--------+-------+-------------+-------------+---------------+--------------------+-----------------+-----------+--------------+-----------------+----------------+----------------------+--------------------+--------------------+----------------+----------------+-------------------+
+----------------------------+
|  request / elipsed times   |
+----------------------------+
| 2024-11-16 16:31:37.973237 |
|       0:00:00.013117       |
+----------------------------+
'''