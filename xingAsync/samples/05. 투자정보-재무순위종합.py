# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py ���Ͽ� ����� ID, ���, ���� ����� �����صΰ� import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")

    inputs = {
        'gubun': '0',   # ���屸��(0:��ü1:�ڽ���2:�ڽ���))
        'gubun1': '2',  # ��������(1:�����������2:��������������3:�����������������4:��ä����5:������6:EPS7:BPS8:ROE9:PERa:PBRb:PEG)
        'gubun2': '1',  # 1 ����
        'idx': 0,       # ù��ȸ�� space, ������ȸ�� Outblock�� idx �� ����
    }
    response = await api.request("t3341", inputs)
    if not response: return print(f'��û����: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
t8424: [00000] ���������� ��ȸ�� �Ϸ�Ǿ����ϴ�.
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
|     ��       ��      |  001   |
|     ��   ��  ��      |  002   |
|     ��   ��  ��      |  003   |
|     ��   ��  ��      |  004   |
|     �� �� �� ��      |  005   |
|     �� �� �� ��      |  006   |
|     �� �� �� ��      |  007   |
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