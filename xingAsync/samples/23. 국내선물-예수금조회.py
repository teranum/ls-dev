# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd, acc_pwd_number # app_key.py ���Ͽ� ����� ID, ���, ���� ���, ���º���� �����صΰ� import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")

    # ���¹�ȣ ��������
    acc_name = "�����ɼ�"
    acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
    if not acc: return print(f"{acc_name} ���°� �����ϴ�.")
    pass_number = "0000" if api.is_simulation else acc_pwd_number

    # CFOBQ10500: �����ɼ� ���¿�Ź�����ű���ȸ
    inputs = {'RecCnt': 1, 'AcntNo': acc.number, 'Pwd': pass_number}
    response = await api.request("CFOBQ10500", inputs)
    if not response: return print(f'��û����: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
CFOBQ10500: [00136] ��ȸ�� �Ϸ�Ǿ����ϴ�.
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
|   1    | ȫ�浿 |      0       |  0  |    0     |         0         |    0     |     0      |      0       |        0         |         0          |  0  |   0    |     0      |       0       |   0    |     0     |         0         |          0           |          0           |       0       |       0       |       0       | �������ű� ���� |
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