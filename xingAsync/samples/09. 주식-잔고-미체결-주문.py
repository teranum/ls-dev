# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd, acc_pwd_number # app_key.py ���Ͽ� ����� ID, ���, ���� ���, ���º���� �����صΰ� import

'''
1. ���� �ǽð� ���, �ܰ� / ��ü�� ��ȸ
2. �ֹ���û : (�ż�, �ŵ�, ����, ���), (���尡, ������)
'''

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")

    # ���¹�ȣ ��������
    acc_name = "���ոŸ�"
    acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
    if not acc: return print(f"{acc_name} ���°� �����ϴ�.")
    pass_number = "0000" if api.is_simulation else acc_pwd_number

    print('�ֽİ��� �ǽð� ���')
    for real_cd in ['SC0', 'SC1', 'SC2', 'SC3', 'SC4']: # SC0: �ֽ��ֹ�����, SC1: �ֽ��ֹ�ü��, SC2: �ֽ��ֹ�����, SC3: �ֽ��ֹ����, SC4: �ֽ��ֹ��ź�
        if not api.realtime(real_cd, '', True):
            return print(f'{real_cd} �ǽð� ��Ͻ���: {api.last_message}')

    while True:
        # �ܰ� ǥ��
        print('�ܰ���ȸ��...')
        inputs = {
            'accno': acc.number,    # ���¹�ȣ
            'passwd': pass_number,  # ���º�й�ȣ
            'prcgb': '1',           # �ܰ����� : 1:��մܰ�, 2:BEP�ܰ�
            'chegb': '2',           # ü�ᱸ�� : 0: ���������ܰ�, 2: ü������ܰ�(�ܰ� ���� ������ ����)
            'dangb': '0',           # ���ϰ����� : 0:������, 1:�ð��� ���ϰ�
            'charge': '1',          # ��������Կ��� : 0:������, 1:����
            'cts_expcode': '',      # CTS�����ȣ : ���� ��ȸ�ÿ� ���� ��ȸ�� OutBlock�� cts_expcode ������ ����
        }
        response = await api.request('t0424', inputs)
        if not response:
            print(f'�ܰ� ��û����: {api.last_message}')
            break
        # print(response)
        if not response['t0424OutBlock1']:
            print('�ܰ����� �����ϴ�.')
        else:
            balances = [dict({
                '�����ڵ�': x['expcode'],
                '�����': x['hname'],
                '�ܰ����': x['janqty'],
                '�ŵ����ɼ���': x['mdposqt'],
                '��մܰ�': x['pamt'],
                '���簡': x['price'],
                '������': x['sunikrt'],
            }) for x in response['t0424OutBlock1']]
            print(balances)

        # ��ü�� ǥ��
        print('��ü����ȸ��...')
        inputs = {
            'accno': acc.number,    # ���¹�ȣ
            'passwd': pass_number,  # ���º�й�ȣ
            'expcode': '',          # �����ڵ�
            'chegb': '2',           # ü�ᱸ�� : 0:��ü, 1:ü��, 2:��ü��
            'medosu': '0',          # �ŵ������� : 0:��ü, 1:�ŵ�, 2:�ż�
            'sortgb': '1',          # ���ı��� : 1:�ֹ���ȣ ����, 2:�ֹ���ȣ ��
            'cts_ordno': '',        # ������ȸŰ : ������ȸ�� ���
        }
        response = await api.request('t0425', inputs)
        if not response:
            print(f'��ü�� ��û����: {api.last_message}')
            break
        # print(response)
        if not response['t0425OutBlock1']:
            print('��ü�᳻���� �����ϴ�.')
        else:
            unfills = [dict({
                '�ֹ���ȣ': x['ordno'],
                '�����ڵ�': x['expcode'],
                '����': x['medosu'],
                '�ֹ�����': x['qty'],
                '�ֹ�����': x['price'],
                '��ü���ܷ�': x['ordrem'],
                '���簡': x['price1'],
                '���ֹ���ȣ': x['orgordno'],
                '�ֹ��ð�': x['ordtime'],
            }) for x in response['t0425OutBlock1']]
            print(unfills)

        # �ֹ���û �Է�
        �ֹ���û = input(f'�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):')
        if len(�ֹ���û) == 0:
            break
        if �ֹ���û == '1' or �ֹ���û == '2':
            # �ֹ� ���� �Է�
            try:
                �����ڵ� = input(f'�����ڵ� 6�ڸ��� �Է��ϼ��� (ex �Ｚ������ ��� 005930):')
                �Ÿű��� = '2' if �ֹ���û == '1' else '1'
                �ֹ����� = input(f'�ֹ������� �Է��ϼ��� (00:������, 03:���尡):')
                �ֹ����� = int(0 if �ֹ����� == '03' else input(f'�ֹ������� �Է��ϼ���:'))
                �ֹ����� = int(input(f'�ֹ������� �Է��ϼ���:'))
            except :
                print("�Է¿���")
                break
        
            # �ű��ֹ� ��û
            inputs = {
                'AcntNo': acc.number,       # ���¹�ȣ
                'InptPwd': pass_number,     # �Էº�й�ȣ
                'IsuNo': 'A'+�����ڵ�,      # �����ڵ�: �ֽ�/ETF : �����ڵ� or A+�����ڵ�(�������ڴ� A+�����ڵ�)
                'OrdQty': �ֹ�����,         # �ֹ�����
                'OrdPrc': �ֹ�����,         # �ֹ���
                'BnsTpCode': �Ÿű���,      # �Ÿű���: 1:�ŵ� 2:�ż�
                'OrdprcPtnCode': �ֹ�����,  # ȣ�������ڵ�: 00:������ 03:���尡
                'MgntrnCode': '000',        # �ſ�ŷ��ڵ�: 000:����
                'LoanDt': '',               # ������: YYYYMMDD
                'OrdCndiTpCode': '0',       # �ֹ����Ǳ���: 0:����
            }
    
            response = await api.request('CSPAT00600', inputs)
            print(response)
            if not response:
                print(f'�ֹ���û ����: {api.last_message}')
            else:
                print(f'�ֹ���û ���: [{response.rsp_cd}] {response.rsp_msg}')
    
        elif �ֹ���û == '3' or �ֹ���û == '4':
            # ����/��� ���� �Է�
            try:
                �ֹ���ȣ = int(input(f'�ֹ���ȣ�� �Է��ϼ���:'))
                �������� = int(input(f'���������� �Է��ϼ���:') if �ֹ���û == '3' else 0)
            except :
                print("�Է¿���")
                break
        
            # �ֹ���ȣ ��ġ�ϴ� ��ü�᳻�� ��ȸ
            matched_unfill = next((x for x in unfills if x['�ֹ���ȣ'] == �ֹ���ȣ), None)
            if not matched_unfill:
                 print(f'�ֹ���ȣ {�ֹ���ȣ}�� ���� ��ü�᳻���� �����ϴ�.')
            else:
                if �ֹ���û == '3':
                    # ������û
                    inputs = {
                        'OrgOrdNo': �ֹ���ȣ,       # ���ֹ���ȣ
                        'AcntNo': acc.number,       # ���¹�ȣ
                        'InptPwd': pass_number,     # �Էº�й�ȣ
                        'IsuNo': 'A'+matched_unfill['�����ڵ�'],    # �����ڵ�
                        'OrdQty': matched_unfill['��ü���ܷ�'],     # �ֹ�����
                        'OrdprcPtnCode': '00',      # ȣ�������ڵ�: 00@������, 03@���尡 ...
                        'OrdCndiTpCode': '0',       # �ֹ����Ǳ���: 0:����, 1:IOC, 2:FOK
                        'OrdPrc': ��������,         # �ֹ���
                    }
                    response = await api.request('CSPAT00700', inputs)
                    if not response:
                        print(f'���� ��û����: {api.last_message}')
                    else:
                        print(f'���� ��û ���: {response.rsp_msg}')
                else:
                    # ��ҿ�û
                    inputs = {
                        'OrgOrdNo': �ֹ���ȣ,       # ���ֹ���ȣ
                        'AcntNo': acc.number,       # ���¹�ȣ
                        'InptPwd': pass_number,     # �Էº�й�ȣ
                        'IsuNo': 'A'+matched_unfill['�����ڵ�'],    # �����ڵ�
                        'OrdQty': matched_unfill['��ü���ܷ�'],     #
                    }
                    response = await api.request('CSPAT00800', inputs)
                    if not response:
                        print(f'��� ��û����: {api.last_message}')
                    else:
                        print(f'��� ��û ���: {response.rsp_msg}')

        else:
            print('�߸��� �Է��Դϴ�.')
            break
        
        await asyncio.sleep(1) # 1�� ��� �� �ݺ�
        pass

    print('�ܰ���� �ǽð� ����')
    for real_cd in ['SC0', 'SC1', 'SC2', 'SC3', 'SC4']:
        api.request_realtime(real_cd, '', False)


if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(lambda tr_cd, key, datas: print(f"on_realtime: {tr_cd}, {key}, {datas}"))
    run_loop(sample(api), forever=True) # ���ѷ����� ����

# Output:
'''
�ܰ���� �ǽð� ���
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    9     |      9       |  56408   | 56500  | -0.04  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  29791   |  005930  | �ż����� |    3     |  45000   |     3      | 56500  |   29484    | 12341714 |
|  27791   |  005930  |   �ż�   |    1     |  50000   |     1      | 56500  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):1
�����ڵ� 6�ڸ��� �Է��ϼ��� (ex �Ｚ������ ��� 005930):005930
�ֹ������� �Է��ϼ��� (00:������, 03:���尡):03
�ֹ������� �Է��ϼ���:1
CSPAT00600: [00040] �������� �ż��ֹ��� �Ϸ� �Ǿ����ϴ�.
CSPAT00600InBlock1, Fields = 10, Count = 1
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
|    AcntNo   | InptPwd |  IsuNo  |      OrdQty      |     OrdPrc    | BnsTpCode | OrdprcPtnCode | MgntrnCode | LoanDt | OrdCndiTpCode |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
| XXXXXXXXXXX |   0000  | A005930 | 0000000000000001 | 0000000000.00 |     2     |       03      |    000     |        |       0       |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
CSPAT00600OutBlock1, Fields = 26, Count = 1
+--------+-------------+---------+---------+--------+--------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
| RecCnt |    AcntNo   | InptPwd |  IsuNo  | OrdQty | OrdPrc | BnsTpCode | OrdprcPtnCode | PrgmOrdprcPtnCode | StslAbleYn | StslOrdprcTpCode | CommdaCode | MgntrnCode | LoanDt | MbrNo | OrdCndiTpCode | StrtgCode | GrpId | OrdSeqNo | PtflNo | BskNo | TrchNo | ItemNo |   OpDrtnNo   | LpYn | CvrgTpCode |
+--------+-------------+---------+---------+--------+--------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
|   1    | XXXXXXXXXXX |   0000  | A005930 |   1    |  0.0   |     2     |       03      |         00        |     0      |        0         |     41     |    000     |        |  000  |       0       |           |       |    0     |   0    |   0   |   0    |   0    | 000000000000 |  0   |     0      |
+--------+-------------+---------+---------+--------+--------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
CSPAT00600OutBlock2, Fields = 18, Count = 1
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
| RecCnt | OrdNo |  OrdTime  | OrdMktCode | OrdPtnCode | ShtnIsuNo | MgempNo | OrdAmt | SpareOrdNo | CvrgSeqno | RsvOrdNo | SpotOrdQty | RuseOrdQty | MnyOrdAmt | SubstOrdAmt | RuseOrdAmt | AcntNm |  IsuNm   |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
|   1    | 30161 | 124917831 |     40     |     03     |  A005930  |         | 69500  |     0      |     0     |    0     |     1      |     0      |     0     |      0      |     0      | ȫ�浿 | �Ｚ���� |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=9, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:49:17.648404 |
|       0:00:00.027589       |
+----------------------------+
�ֹ���û ���: [00040] �������� �ż��ֹ��� �Ϸ� �Ǿ����ϴ�.
on_realtime: SC0, , {'lineseq': 100124483, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124483', 'trid': '00124917826449', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 124917826, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '02', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '�Ｚ����', 'ordqty': 1, 'ordprice': 0, 'hogagb': '0', 'etfhogagb': '03', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30161, 'ordtm': '124917831', 'prntordno': 30161, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 0, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 0, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 9, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 9, 'sellableqty': 9, 'unercsellordqty': 1, 'avrpchsprc': 56408, 'pchsamt': 507675, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 19492}
on_realtime: SC1, , {'lineseq': 100124484, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124484', 'trid': '00124917826449', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 124917826, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '11', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': 'ȫ�浿', 'Isuno': 'KR7005930003', 'Isunm': '�Ｚ����', 'ordno': 30161, 'orgordno': 0, 'execno': 83445, 'ordqty': 1, 'ordprc': 0, 'execqty': 1, 'execprc': 56600, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '03', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 0, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 0, 'ordavrexecprc': 56600, 'ordamt': 0, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '124917000', 'rcptexectime': '124917000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 0, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 22072}
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    10    |      10      |  56427   | 56600  |  0.09  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  29791   |  005930  | �ż����� |    3     |  45000   |     3      | 56600  |   29484    | 12341714 |
|  27791   |  005930  |   �ż�   |    1     |  50000   |     1      | 56600  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):1
�����ڵ� 6�ڸ��� �Է��ϼ��� (ex �Ｚ������ ��� 005930):005930
�ֹ������� �Է��ϼ��� (00:������, 03:���尡):00
�ֹ������� �Է��ϼ���:40000
�ֹ������� �Է��ϼ���:2
CSPAT00600: [00040] �������� �ż��ֹ��� �Ϸ� �Ǿ����ϴ�.
CSPAT00600InBlock1, Fields = 10, Count = 1
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
|    AcntNo   | InptPwd |  IsuNo  |      OrdQty      |     OrdPrc    | BnsTpCode | OrdprcPtnCode | MgntrnCode | LoanDt | OrdCndiTpCode |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
| XXXXXXXXXXX |   0000  | A005930 | 0000000000000002 | 0000040000.00 |     2     |       00      |    000     |        |       0       |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
CSPAT00600OutBlock1, Fields = 26, Count = 1
+--------+-------------+---------+---------+--------+---------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
| RecCnt |    AcntNo   | InptPwd |  IsuNo  | OrdQty |  OrdPrc | BnsTpCode | OrdprcPtnCode | PrgmOrdprcPtnCode | StslAbleYn | StslOrdprcTpCode | CommdaCode | MgntrnCode | LoanDt | MbrNo | OrdCndiTpCode | StrtgCode | GrpId | OrdSeqNo | PtflNo | BskNo | TrchNo | ItemNo |   OpDrtnNo   | LpYn | CvrgTpCode |
+--------+-------------+---------+---------+--------+---------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
|   1    | XXXXXXXXXXX |   0000  | A005930 |   2    | 40000.0 |     2     |       00      |         00        |     0      |        0         |     41     |    000     |        |  000  |       0       |           |       |    0     |   0    |   0   |   0    |   0    | 000000000000 |  0   |     0      |
+--------+-------------+---------+---------+--------+---------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
CSPAT00600OutBlock2, Fields = 18, Count = 1
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
| RecCnt | OrdNo |  OrdTime  | OrdMktCode | OrdPtnCode | ShtnIsuNo | MgempNo | OrdAmt | SpareOrdNo | CvrgSeqno | RsvOrdNo | SpotOrdQty | RuseOrdQty | MnyOrdAmt | SubstOrdAmt | RuseOrdAmt | AcntNm |  IsuNm   |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
|   1    | 30221 | 125135851 |     40     |     00     |  A005930  |         | 80000  |     0      |     0     |    0     |     2      |     0      |     0     |      0      |     0      | ȫ�浿 | �Ｚ���� |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=14, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:51:35.667561 |
|       0:00:00.028281       |
+----------------------------+
�ֹ���û ���: [00040] �������� �ż��ֹ��� �Ϸ� �Ǿ����ϴ�.
on_realtime: SC0, , {'lineseq': 100124679, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124679', 'trid': '00125135846336', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125135846, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '02', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '�Ｚ����', 'ordqty': 2, 'ordprice': 40000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30221, 'ordtm': '125135851', 'prntordno': 30221, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 80000, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 80000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 2, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 6072}
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    10    |      10      |  56427   | 56500  | -0.08  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 3
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30221   |  005930  |   �ż�   |    2     |  40000   |     2      | 56500  |     0      | 12513585 |
|  29791   |  005930  | �ż����� |    3     |  45000   |     3      | 56500  |   29484    | 12341714 |
|  27791   |  005930  |   �ż�   |    1     |  50000   |     1      | 56500  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):3
�ֹ���ȣ�� �Է��ϼ���:30221
���������� �Է��ϼ���:45000
���� ��û ���: �������� �����ֹ��� �Ϸ� �Ǿ����ϴ�.
on_realtime: SC0, , {'lineseq': 100124893, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT001', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124893', 'trid': '00125305947967', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125305947, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '02', 'marketgb': '10', 'ordgb': '02', 'orgordno': 30221, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '�Ｚ����', 'ordqty': 2, 'ordprice': 45000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30288, 'ordtm': '125305953', 'prntordno': 30221, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 2, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 90000, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 90000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 2, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
on_realtime: SC2, , {'lineseq': 100124894, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124894', 'trid': '00125305947967', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125305947, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '12', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': 'ȫ�浿', 'Isuno': 'KR7005930003', 'Isunm': '�Ｚ����', 'ordno': 30288, 'orgordno': 30221, 'execno': 0, 'ordqty': 2, 'ordprc': 45000, 'execqty': 0, 'execprc': 0, 'mdfycnfqty': 2, 'mdfycnfprc': 45000, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '00', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 2, 'orgordunercqty': 0, 'orgordmdfyqty': 2, 'orgordcancqty': 0, 'ordavrexecprc': 0, 'ordamt': 90000, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125305000', 'rcptexectime': '125305000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 2, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    10    |      10      |  56427   | 56500  | -0.08  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 3
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | �ż����� |    2     |  45000   |     2      | 56500  |   30221    | 12530595 |
|  29791   |  005930  | �ż����� |    3     |  45000   |     3      | 56500  |   29484    | 12341714 |
|  27791   |  005930  |   �ż�   |    1     |  50000   |     1      | 56500  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):4
�ֹ���ȣ�� �Է��ϼ���:29791
��� ��û ���: �������� ����ֹ��� �Ϸ� �Ǿ����ϴ�.
on_realtime: SC0, , {'lineseq': 100125118, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT002', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125118', 'trid': '00125451053359', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125451053, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '03', 'marketgb': '10', 'ordgb': '02', 'orgordno': 29791, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '�Ｚ����', 'ordqty': 3, 'ordprice': 0, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30342, 'ordtm': '125451058', 'prntordno': 29484, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 3, 'nmcpysndno': 0, 'ordamt': 0, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 0, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 3, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
on_realtime: SC3, , {'lineseq': 100125119, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125119', 'trid': '00125451053359', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125451053, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '13', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': 'ȫ�浿', 'Isuno': 'KR7005930003', 'Isunm': '�Ｚ����', 'ordno': 30342, 'orgordno': 29791, 'execno': 0, 'ordqty': 3, 'ordprc': 0, 'execqty': 0, 'execprc': 0, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 3, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 3, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 3, 'ordavrexecprc': 0, 'ordamt': 0, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125451000', 'rcptexectime': '125451000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 3, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    10    |      10      |  56427   | 56400  | -0.25  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | �ż����� |    2     |  45000   |     2      | 56400  |   30221    | 12530595 |
|  27791   |  005930  |   �ż�   |    1     |  50000   |     1      | 56400  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):3
�ֹ���ȣ�� �Է��ϼ���:27791
���������� �Է��ϼ���:60000
���� ��û ���: �������� �����ֹ��� �Ϸ� �Ǿ����ϴ�.
on_realtime: SC0, , {'lineseq': 100125170, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT001', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125170', 'trid': '00125540332052', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125540332, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '02', 'marketgb': '10', 'ordgb': '02', 'orgordno': 27791, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '�Ｚ����', 'ordqty': 1, 'ordprice': 60000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30357, 'ordtm': '125540336', 'prntordno': 27791, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 1, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 60000, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 60000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 1, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 2072}
on_realtime: SC2, , {'lineseq': 100125171, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125171', 'trid': '00125540332052', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125540332, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '12', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': 'ȫ�浿', 'Isuno': 'KR7005930003', 'Isunm': '�Ｚ����', 'ordno': 30357, 'orgordno': 27791, 'execno': 0, 'ordqty': 1, 'ordprc': 60000, 'execqty': 0, 'execprc': 0, 'mdfycnfqty': 1, 'mdfycnfprc': 60000, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '00', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 1, 'orgordunercqty': 0, 'orgordmdfyqty': 1, 'orgordcancqty': 0, 'ordavrexecprc': 0, 'ordamt': 60000, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125540000', 'rcptexectime': '125540000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 1, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 2072}
on_realtime: SC1, , {'lineseq': 100125181, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125181', 'trid': '00125540332052', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125540332, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '11', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': 'ȫ�浿', 'Isuno': 'KR7005930003', 'Isunm': '�Ｚ����', 'ordno': 30357, 'orgordno': 27791, 'execno': 83857, 'ordqty': 1, 'ordprc': 60000, 'execqty': 1, 'execprc': 56400, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '00', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 0, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 0, 'ordavrexecprc': 56400, 'ordamt': 60000, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125542000', 'rcptexectime': '125542000', 'rmndLoanamt': 0, 'secbalqty': 11, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 11, 'sellableqty': 11, 'unercsellordqty': 0, 'avrpchsprc': 56425, 'pchsant': 620675, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 2072}
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    11    |      11      |  56425   | 56600  |  0.09  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 1
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | �ż����� |    2     |  45000   |     2      | 56600  |   30221    | 12530595 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):2
�����ڵ� 6�ڸ��� �Է��ϼ��� (ex �Ｚ������ ��� 005930):005930
�ֹ������� �Է��ϼ��� (00:������, 03:���尡):03
�ֹ������� �Է��ϼ���:1
CSPAT00600: [00039] �������� �ŵ��ֹ��� �Ϸ� �Ǿ����ϴ�.
CSPAT00600InBlock1, Fields = 10, Count = 1
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
|    AcntNo   | InptPwd |  IsuNo  |      OrdQty      |     OrdPrc    | BnsTpCode | OrdprcPtnCode | MgntrnCode | LoanDt | OrdCndiTpCode |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
| XXXXXXXXXXX |   0000  | A005930 | 0000000000000001 | 0000000000.00 |     1     |       03      |    000     |        |       0       |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
CSPAT00600OutBlock1, Fields = 26, Count = 1
+--------+-------------+---------+---------+--------+--------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
| RecCnt |    AcntNo   | InptPwd |  IsuNo  | OrdQty | OrdPrc | BnsTpCode | OrdprcPtnCode | PrgmOrdprcPtnCode | StslAbleYn | StslOrdprcTpCode | CommdaCode | MgntrnCode | LoanDt | MbrNo | OrdCndiTpCode | StrtgCode | GrpId | OrdSeqNo | PtflNo | BskNo | TrchNo | ItemNo |   OpDrtnNo   | LpYn | CvrgTpCode |
+--------+-------------+---------+---------+--------+--------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
|   1    | XXXXXXXXXXX |   0000  | A005930 |   1    |  0.0   |     1     |       03      |         00        |     0      |        0         |     41     |    000     |        |  000  |       0       |           |       |    0     |   0    |   0   |   0    |   0    | 000000000000 |  0   |     0      |
+--------+-------------+---------+---------+--------+--------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
CSPAT00600OutBlock2, Fields = 18, Count = 1
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
| RecCnt | OrdNo |  OrdTime  | OrdMktCode | OrdPtnCode | ShtnIsuNo | MgempNo | OrdAmt | SpareOrdNo | CvrgSeqno | RsvOrdNo | SpotOrdQty | RuseOrdQty | MnyOrdAmt | SubstOrdAmt | RuseOrdAmt | AcntNm |  IsuNm   |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
|   1    | 30415 | 125759387 |     40     |     03     |  A005930  |         |   0    |     0      |     0     |    0     |     1      |     0      |     0     |      0      |     0      | ȫ�浿 | �Ｚ���� |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=36, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:57:59.201879 |
|       0:00:00.026036       |
+----------------------------+
�ֹ���û ���: [00039] �������� �ŵ��ֹ��� �Ϸ� �Ǿ����ϴ�.
on_realtime: SC0, , {'lineseq': 100125346, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125346', 'trid': '00125759382676', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125759382, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '01', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '�Ｚ����', 'ordqty': 1, 'ordprice': 0, 'hogagb': '0', 'etfhogagb': '03', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30415, 'ordtm': '125759387', 'prntordno': 30415, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 0, 'bnstp': '1', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 0, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 11, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 11, 'sellableqty': 10, 'unercsellordqty': 1, 'avrpchsprc': 56425, 'pchsamt': 620675, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 2072}
on_realtime: SC1, , {'lineseq': 100125347, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125347', 'trid': '00125759382676', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125759382, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '11', 'ordmktcode': '10', 'ordptncode': '01', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': 'ȫ�浿', 'Isuno': 'KR7005930003', 'Isunm': '�Ｚ����', 'ordno': 30415, 'orgordno': 0, 'execno': 83950, 'ordqty': 1, 'ordprc': 0, 'execqty': 1, 'execprc': 56600, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '03', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 0, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 0, 'ordavrexecprc': 56600, 'ordamt': 0, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '1', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125759000', 'rcptexectime': '125759000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 0, 'avrpchsprc': 56425, 'pchsant': 564250, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 13262}
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    10    |      10      |  56425   | 56600  |  0.09  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 1
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | �ż����� |    2     |  45000   |     2      | 56600  |   30221    | 12530595 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):2
�����ڵ� 6�ڸ��� �Է��ϼ��� (ex �Ｚ������ ��� 005930):005930
�ֹ������� �Է��ϼ��� (00:������, 03:���尡):00
�ֹ������� �Է��ϼ���:60000
�ֹ������� �Է��ϼ���:4
CSPAT00600: [00039] �������� �ŵ��ֹ��� �Ϸ� �Ǿ����ϴ�.
CSPAT00600InBlock1, Fields = 10, Count = 1
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
|    AcntNo   | InptPwd |  IsuNo  |      OrdQty      |     OrdPrc    | BnsTpCode | OrdprcPtnCode | MgntrnCode | LoanDt | OrdCndiTpCode |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
| XXXXXXXXXXX |   0000  | A005930 | 0000000000000004 | 0000060000.00 |     1     |       00      |    000     |        |       0       |
+-------------+---------+---------+------------------+---------------+-----------+---------------+------------+--------+---------------+
CSPAT00600OutBlock1, Fields = 26, Count = 1
+--------+-------------+---------+---------+--------+---------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
| RecCnt |    AcntNo   | InptPwd |  IsuNo  | OrdQty |  OrdPrc | BnsTpCode | OrdprcPtnCode | PrgmOrdprcPtnCode | StslAbleYn | StslOrdprcTpCode | CommdaCode | MgntrnCode | LoanDt | MbrNo | OrdCndiTpCode | StrtgCode | GrpId | OrdSeqNo | PtflNo | BskNo | TrchNo | ItemNo |   OpDrtnNo   | LpYn | CvrgTpCode |
+--------+-------------+---------+---------+--------+---------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
|   1    | XXXXXXXXXXX |   0000  | A005930 |   4    | 60000.0 |     1     |       00      |         00        |     0      |        0         |     41     |    000     |        |  000  |       0       |           |       |    0     |   0    |   0   |   0    |   0    | 000000000000 |  0   |     0      |
+--------+-------------+---------+---------+--------+---------+-----------+---------------+-------------------+------------+------------------+------------+------------+--------+-------+---------------+-----------+-------+----------+--------+-------+--------+--------+--------------+------+------------+
CSPAT00600OutBlock2, Fields = 18, Count = 1
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
| RecCnt | OrdNo |  OrdTime  | OrdMktCode | OrdPtnCode | ShtnIsuNo | MgempNo | OrdAmt | SpareOrdNo | CvrgSeqno | RsvOrdNo | SpotOrdQty | RuseOrdQty | MnyOrdAmt | SubstOrdAmt | RuseOrdAmt | AcntNm |  IsuNm   |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
|   1    | 30449 | 125848706 |     40     |     00     |  A005930  |         | 240000 |     0      |     0     |    0     |     4      |     0      |     0     |      0      |     0      | ȫ�浿 | �Ｚ���� |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=41, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:58:48.518812 |
|       0:00:00.028306       |
+----------------------------+
�ֹ���û ���: [00039] �������� �ŵ��ֹ��� �Ϸ� �Ǿ����ϴ�.
on_realtime: SC0, , {'lineseq': 100125431, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125431', 'trid': '00125848701365', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125848701, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '01', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '�Ｚ����', 'ordqty': 4, 'ordprice': 60000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30449, 'ordtm': '125848706', 'prntordno': 30449, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 240000, 'bnstp': '1', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 240000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 6, 'unercsellordqty': 4, 'avrpchsprc': 56425, 'pchsamt': 564250, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 13262}
�ܰ���ȸ��...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| �����ڵ� |  �����  | �ܰ���� | �ŵ����ɼ��� | ��մܰ� | ���簡 | ������ |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | �Ｚ���� |    10    |      6       |  56425   | 56500  | -0.07  |
+----------+----------+----------+--------------+----------+--------+--------+
��ü����ȸ��...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| �ֹ���ȣ | �����ڵ� |   ����   | �ֹ����� | �ֹ����� | ��ü���ܷ� | ���簡 | ���ֹ���ȣ | �ֹ��ð� |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30449   |  005930  |   �ŵ�   |    4     |  60000   |     4      | 56500  |     0      | 12584870 |
|  30288   |  005930  | �ż����� |    2     |  45000   |     2      | 56500  |   30221    | 12530595 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
�ֹ��� �Է��ϼ��� (1:�ż�, 2:�ŵ�, 3:����, 4:���):
�ܰ���� �ǽð� ����
'''