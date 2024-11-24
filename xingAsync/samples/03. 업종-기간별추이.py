# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py ���Ͽ� ����� ID, ���, ���� ����� �����صΰ� import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")

    inputs = {
        "upcode": "001",    # �����ڵ� (001: ����...)
        "gubun2": '1',       # '1: �Ϻ�, 2: �ֺ�, 3: ����
        "cnt": 100,         # ��ȸ�Ǽ�
        "rate_gbn": '2',    # ���߱��� (1: �ŷ���, 2: �ŷ����)
        }
    response = await api.request("t1514", "001   1          0100 2 ")
    if not response: return print(f'��û����: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
'''