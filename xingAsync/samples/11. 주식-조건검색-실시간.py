# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py ���Ͽ� ����� ID, ���, ���� ����� �����صΰ� import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")

    response = await api.request("t1866", {"user_id": user_id, "gb":"0"}) # t1826: ����QŬ���˻�����Ʈ
    if not response: return print(f'��������Ʈ ��û����: {api.last_message}')

    print(response)
    if response['t1866OutBlock']['result_count'] == 0:
        return print("���ǽ��� �����ϴ�.")

    # ù��° ���ǽ� ��û�Ѵ�
    response = await api.request("t1857", ["1", "S", response['t1866OutBlock1'][0]['query_index']]) # t1857: e����˻�(API��)
    if not response: return print(f'����˻� ��û����: {api.last_message}')
    print(response)


if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(lambda tr_cd, key, datas: print(f"on_realtime: {tr_cd}, {key}, {datas}"))
    run_loop(sample(api), forever=True) # ���ѷ����� ����

# Output:
'''
t1866: [00000] ��ȸ����
t1866InBlock, Fields = 5, Count = 1
+----------+----+------------------------------------------+------+------------------------------------------+
| user_id  | gb |                group_name                | cont |                 contkey                  |
+----------+----+------------------------------------------+------+------------------------------------------+
| XXXXXXXX | 0  |                                          |      |                                          |
+----------+----+------------------------------------------+------+------------------------------------------+
t1866OutBlock, Fields = 3, Count = 1
+--------------+------+---------+
| result_count | cont | contkey |
+--------------+------+---------+
|      1       |      |         |
+--------------+------+---------+
t1866OutBlock1, Fields = 3, Count = 1
+--------------+------------+------------+
| query_index  | group_name | query_name |
+--------------+------------+------------+
| XXXXXXXX0001 |  ��������  |  ������  |
+--------------+------------+------------+
nRqID=21, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 10:32:59.598256 |
|       0:00:02.071660       |
+----------------------------+
t1857: []
t1857InBlock, Fields = 3, Count = 1
+-----------+-------------+--------------+
| sRealFlag | sSearchFlag | query_index  |
+-----------+-------------+--------------+
|     1     |      S      | XXXXXXXX0001 |
+-----------+-------------+--------------+
t1857OutBlock, Fields = 3, Count = 1
+--------------+-------------+-------------+
| result_count | result_time |   AlertNum  |
+--------------+-------------+-------------+
|      2       |    103302   | 1033020200J |
+--------------+-------------+-------------+
t1857OutBlock1, Fields = 8, Count = 2
+--------+----------------------------------+-------+------+--------+-------+--------+---------+
| shcode |              hname               | price | sign | change |  diff | volume | JobFlag |
+--------+----------------------------------+-------+------+--------+-------+--------+---------+
| 024110 |             �������             | 14350 |  2   |  120   |  0.84 | 322412 |    N    |
| 071970 |          HD���븶������          | 19030 |  5   |  150   | -0.78 | 110473 |    N    |
| 214320 |              �̳��              | 19890 |  5   |   70   | -0.35 |  3908  |    N    |
| 381180 | TIGER �̱��ʶ��Ǿƹݵ�ü������ | 17870 |  5   |  405   | -2.22 | 958432 |    N    |
| 950160 |           �ڿ���Ƽ����           | 16580 |  5   |   90   | -0.54 | 94130  |    N    |
+--------+----------------------------------+-------+------+--------+-------+--------+---------+
nRqID=22, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 10:33:01.679280 |
|       0:00:00.293146       |
+----------------------------+
on_realtime: UFR, 1033020200J, {'shcode': '381180', 'hname': 'TIGER �̱��ʶ��Ǿƹݵ�ü������', 'price': 17870, 'sign': '5', 'change': -405, 'diff': -2.21, 'volume': 958761, 'JobFlag': 'R'}
on_realtime: UFR, 1033020200J, {'shcode': '381180', 'hname': 'TIGER �̱��ʶ��Ǿƹݵ�ü������', 'price': 17865, 'sign': '5', 'change': -410, 'diff': -2.24, 'volume': 958861, 'JobFlag': 'O'}
on_realtime: UFR, 1033020200J, {'shcode': '530125', 'hname': '�Ｚ �ι��� 2X �Ϻ�������225���� ETN(H)', 'price': 19295, 'sign': '2', 'change': 350, 'diff': 1.84, 'volume': 13489, 'JobFlag': 'N'}
on_realtime: UFR, 1033020200J, {'shcode': '484880', 'hname': 'SOL ���������÷�������', 'price': 11370, 'sign': '2', 'change': 95, 'diff': 0.84, 'volume': 46877, 'JobFlag': 'N'}
on_realtime: UFR, 1033020200J, {'shcode': '950160', 'hname': '�ڿ���Ƽ����', 'price': 16570, 'sign': '5', 'change': -100, 'diff': -0.59, 'volume': 94230, 'JobFlag': 'O'}
on_realtime: UFR, 1033020200J, {'shcode': '102960', 'hname': 'KODEX ������', 'price': 6960, 'sign': '2', 'change': 90, 'diff': 1.31, 'volume': 5907, 'JobFlag': 'N'}
on_realtime: UFR, 1033020200J, {'shcode': '105840', 'hname': '����', 'price': 8070, 'sign': '2', 'change': 160, 'diff': 2.02, 'volume': 57856, 'JobFlag': 'N'}
on_realtime: UFR, 1033020200J, {'shcode': '210780', 'hname': 'TIGER �ڽ��ǰ���', 'price': 15020, 'sign': '2', 'change': 180, 'diff': 1.21, 'volume': 2837, 'JobFlag': 'N'}
on_realtime: UFR, 1033020200J, {'shcode': '005670', 'hname': 'Ǫ����', 'price': 5320, 'sign': '2', 'change': 120, 'diff': 2.69, 'volume': 12122, 'JobFlag': 'N'}
on_realtime: UFR, 1033020200J, {'shcode': '005670', 'hname': 'Ǫ����', 'price': 5300, 'sign': '2', 'change': 100, 'diff': 1.92, 'volume': 12172, 'JobFlag': 'O'}
'''