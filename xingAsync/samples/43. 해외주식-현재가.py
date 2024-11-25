# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py ���Ͽ� ����� ID, ���, ���� ����� �����صΰ� import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")

    keysymbol = '82TSLA' # 82TSLA: �׽���, 82AAPL: ����

    response = await api.request("g3101", ['R', keysymbol, keysymbol[:2], keysymbol[2:]])
    if not response: return print(f'��û����: {api.last_message}')

    print(response)

if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api))

# Output:
'''
g3101: [00000] ��ȸ�Ϸ�
g3101InBlock, Fields = 4, Count = 1
+---------+-----------+--------+--------+
| delaygb | keysymbol | exchcd | symbol |
+---------+-----------+--------+--------+
|    R    |   82TSLA  |   82   |  TSLA  |
+---------+-----------+--------+--------+
g3101OutBlock, Fields = 26, Count = 1
+---------+-----------+--------+----------+---------+----------+--------+---------+----------------+------------+----------+--------+------+------+-------+----------+-------------+---------+----------+---------+---------+-------+----------+-------+-------+------+
| delaygb | keysymbol | exchcd | exchange | suspend | sellonly | symbol | korname |    induname    | floatpoint | currency | price  | sign | diff |  rate |  volume  |    amount   | high52p |  low52p  | uplimit | dnlimit |  open |   high   |  low  |  perv | epsv |
+---------+-----------+--------+----------+---------+----------+--------+---------+----------------+------------+----------+--------+------+------+-------+----------+-------------+---------+----------+---------+---------+-------+----------+-------+-------+------+
|    R    |   82TSLA  |   82   |   0537   |    N    |    0     |  TSLA  |  �׽��� | �ڵ��� �� ��ǰ |     4      |   USD    | 342.03 |  5   | 3.97 | -1.15 | 50690663 | 17227510001 |  358.64 | 138.8025 |   0.0   |   0.0   | 345.0 | 346.5999 | 334.3 | 94.78 | 3.65 |
+---------+-----------+--------+----------+---------+----------+--------+---------+----------------+------------+----------+--------+------+------+-------+----------+-------------+---------+----------+---------+---------+-------+----------+-------+-------+------+
nRqID=21, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-21 07:05:54.311689 |
|       0:00:00.002999       |
+----------------------------+
'''