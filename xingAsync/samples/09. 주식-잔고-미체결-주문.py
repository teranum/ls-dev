# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd, acc_pwd_number # app_key.py 파일에 사용자 ID, 비번, 공증 비번, 계좌비번을 저장해두고 import

'''
1. 계좌 실시간 등록, 잔고 / 미체결 조회
2. 주문요청 : (매수, 매도, 정정, 취소), (시장가, 지정가)
'''

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    # 계좌번호 가져오기
    acc_name = "종합매매"
    acc = next((item for item in api.accounts if item.detail_name == acc_name), None)
    if not acc: return print(f"{acc_name} 계좌가 없습니다.")
    pass_number = "0000" if api.is_simulation else acc_pwd_number

    print('주식계좌 실시간 등록')
    for real_cd in ['SC0', 'SC1', 'SC2', 'SC3', 'SC4']: # SC0: 주식주문접수, SC1: 주식주문체결, SC2: 주식주문정정, SC3: 주식주문취소, SC4: 주식주문거부
        if not api.realtime(real_cd, '', True):
            return print(f'{real_cd} 실시간 등록실패: {api.last_message}')

    while True:
        # 잔고 표시
        print('잔고조회중...')
        inputs = {
            'accno': acc.number,    # 계좌번호
            'passwd': pass_number,  # 계좌비밀번호
            'prcgb': '1',           # 단가구분 : 1:평균단가, 2:BEP단가
            'chegb': '2',           # 체결구분 : 0: 결제기준잔고, 2: 체결기준잔고(잔고가 없는 종목은 제외)
            'dangb': '0',           # 단일가구분 : 0:정규장, 1:시간외 단일가
            'charge': '1',          # 제비용포함여부 : 0:미포함, 1:포함
            'cts_expcode': '',      # CTS종목번호 : 연속 조회시에 이전 조회한 OutBlock의 cts_expcode 값으로 설정
        }
        response = await api.request('t0424', inputs)
        if not response:
            print(f'잔고 요청실패: {api.last_message}')
            break
        # print(response)
        if not response['t0424OutBlock1']:
            print('잔고내역이 없습니다.')
        else:
            balances = [dict({
                '종목코드': x['expcode'],
                '종목명': x['hname'],
                '잔고수량': x['janqty'],
                '매도가능수량': x['mdposqt'],
                '평균단가': x['pamt'],
                '현재가': x['price'],
                '수익율': x['sunikrt'],
            }) for x in response['t0424OutBlock1']]
            print(balances)

        # 미체결 표시
        print('미체결조회중...')
        inputs = {
            'accno': acc.number,    # 계좌번호
            'passwd': pass_number,  # 계좌비밀번호
            'expcode': '',          # 종목코드
            'chegb': '2',           # 체결구분 : 0:전체, 1:체결, 2:미체결
            'medosu': '0',          # 매도수구분 : 0:전체, 1:매도, 2:매수
            'sortgb': '1',          # 정렬기준 : 1:주문번호 역순, 2:주문번호 순
            'cts_ordno': '',        # 연속조회키 : 연속조회시 사용
        }
        response = await api.request('t0425', inputs)
        if not response:
            print(f'미체결 요청실패: {api.last_message}')
            break
        # print(response)
        if not response['t0425OutBlock1']:
            print('미체결내역이 없습니다.')
        else:
            unfills = [dict({
                '주문번호': x['ordno'],
                '종목코드': x['expcode'],
                '구분': x['medosu'],
                '주문수량': x['qty'],
                '주문가격': x['price'],
                '미체결잔량': x['ordrem'],
                '현재가': x['price1'],
                '원주문번호': x['orgordno'],
                '주문시간': x['ordtime'],
            }) for x in response['t0425OutBlock1']]
            print(unfills)

        # 주문요청 입력
        주문요청 = input(f'주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):')
        if len(주문요청) == 0:
            break
        if 주문요청 == '1' or 주문요청 == '2':
            # 주문 정보 입력
            try:
                종목코드 = input(f'종목코드 6자리를 입력하세요 (ex 삼성전자인 경우 005930):')
                매매구분 = '2' if 주문요청 == '1' else '1'
                주문구분 = input(f'주문구분을 입력하세요 (00:지정가, 03:시장가):')
                주문가격 = int(0 if 주문구분 == '03' else input(f'주문가격을 입력하세요:'))
                주문수량 = int(input(f'주문수량을 입력하세요:'))
            except :
                print("입력오류")
                break
        
            # 신규주문 요청
            inputs = {
                'AcntNo': acc.number,       # 계좌번호
                'InptPwd': pass_number,     # 입력비밀번호
                'IsuNo': 'A'+종목코드,      # 종목코드: 주식/ETF : 종목코드 or A+종목코드(모의투자는 A+종목코드)
                'OrdQty': 주문수량,         # 주문수량
                'OrdPrc': 주문가격,         # 주문가
                'BnsTpCode': 매매구분,      # 매매구분: 1:매도 2:매수
                'OrdprcPtnCode': 주문구분,  # 호가유형코드: 00:지정가 03:시장가
                'MgntrnCode': '000',        # 신용거래코드: 000:보통
                'LoanDt': '',               # 대출일: YYYYMMDD
                'OrdCndiTpCode': '0',       # 주문조건구분: 0:없음
            }
    
            response = await api.request('CSPAT00600', inputs)
            print(response)
            if not response:
                print(f'주문요청 실패: {api.last_message}')
            else:
                print(f'주문요청 결과: [{response.rsp_cd}] {response.rsp_msg}')
    
        elif 주문요청 == '3' or 주문요청 == '4':
            # 정정/취소 정보 입력
            try:
                주문번호 = int(input(f'주문번호를 입력하세요:'))
                정정가격 = int(input(f'정정가격을 입력하세요:') if 주문요청 == '3' else 0)
            except :
                print("입력오류")
                break
        
            # 주문번호 일치하는 미체결내역 조회
            matched_unfill = next((x for x in unfills if x['주문번호'] == 주문번호), None)
            if not matched_unfill:
                 print(f'주문번호 {주문번호}에 대한 미체결내역이 없습니다.')
            else:
                if 주문요청 == '3':
                    # 정정요청
                    inputs = {
                        'OrgOrdNo': 주문번호,       # 원주문번호
                        'AcntNo': acc.number,       # 계좌번호
                        'InptPwd': pass_number,     # 입력비밀번호
                        'IsuNo': 'A'+matched_unfill['종목코드'],    # 종목코드
                        'OrdQty': matched_unfill['미체결잔량'],     # 주문수량
                        'OrdprcPtnCode': '00',      # 호가유형코드: 00@지정가, 03@시장가 ...
                        'OrdCndiTpCode': '0',       # 주문조건구분: 0:없음, 1:IOC, 2:FOK
                        'OrdPrc': 정정가격,         # 주문가
                    }
                    response = await api.request('CSPAT00700', inputs)
                    if not response:
                        print(f'정정 요청실패: {api.last_message}')
                    else:
                        print(f'정정 요청 결과: {response.rsp_msg}')
                else:
                    # 취소요청
                    inputs = {
                        'OrgOrdNo': 주문번호,       # 원주문번호
                        'AcntNo': acc.number,       # 계좌번호
                        'InptPwd': pass_number,     # 입력비밀번호
                        'IsuNo': 'A'+matched_unfill['종목코드'],    # 종목코드
                        'OrdQty': matched_unfill['미체결잔량'],     #
                    }
                    response = await api.request('CSPAT00800', inputs)
                    if not response:
                        print(f'취소 요청실패: {api.last_message}')
                    else:
                        print(f'취소 요청 결과: {response.rsp_msg}')

        else:
            print('잘못된 입력입니다.')
            break
        
        await asyncio.sleep(1) # 1초 대기 후 반복
        pass

    print('잔고관련 실시간 해지')
    for real_cd in ['SC0', 'SC1', 'SC2', 'SC3', 'SC4']:
        api.request_realtime(real_cd, '', False)


if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(lambda tr_cd, key, datas: print(f"on_realtime: {tr_cd}, {key}, {datas}"))
    run_loop(sample(api), forever=True) # 무한루프로 실행

# Output:
'''
잔고관련 실시간 등록
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    9     |      9       |  56408   | 56500  | -0.04  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  29791   |  005930  | 매수정정 |    3     |  45000   |     3      | 56500  |   29484    | 12341714 |
|  27791   |  005930  |   매수   |    1     |  50000   |     1      | 56500  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):1
종목코드 6자리를 입력하세요 (ex 삼성전자인 경우 005930):005930
주문구분을 입력하세요 (00:지정가, 03:시장가):03
주문수량을 입력하세요:1
CSPAT00600: [00040] 모의투자 매수주문이 완료 되었습니다.
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
|   1    | 30161 | 124917831 |     40     |     03     |  A005930  |         | 69500  |     0      |     0     |    0     |     1      |     0      |     0     |      0      |     0      | 홍길동 | 삼성전자 |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=9, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:49:17.648404 |
|       0:00:00.027589       |
+----------------------------+
주문요청 결과: [00040] 모의투자 매수주문이 완료 되었습니다.
on_realtime: SC0, , {'lineseq': 100124483, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124483', 'trid': '00124917826449', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 124917826, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '02', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '삼성전자', 'ordqty': 1, 'ordprice': 0, 'hogagb': '0', 'etfhogagb': '03', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30161, 'ordtm': '124917831', 'prntordno': 30161, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 0, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 0, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 9, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 9, 'sellableqty': 9, 'unercsellordqty': 1, 'avrpchsprc': 56408, 'pchsamt': 507675, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 19492}
on_realtime: SC1, , {'lineseq': 100124484, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124484', 'trid': '00124917826449', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 124917826, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '11', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': '홍길동', 'Isuno': 'KR7005930003', 'Isunm': '삼성전자', 'ordno': 30161, 'orgordno': 0, 'execno': 83445, 'ordqty': 1, 'ordprc': 0, 'execqty': 1, 'execprc': 56600, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '03', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 0, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 0, 'ordavrexecprc': 56600, 'ordamt': 0, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '124917000', 'rcptexectime': '124917000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 0, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 22072}
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    10    |      10      |  56427   | 56600  |  0.09  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  29791   |  005930  | 매수정정 |    3     |  45000   |     3      | 56600  |   29484    | 12341714 |
|  27791   |  005930  |   매수   |    1     |  50000   |     1      | 56600  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):1
종목코드 6자리를 입력하세요 (ex 삼성전자인 경우 005930):005930
주문구분을 입력하세요 (00:지정가, 03:시장가):00
주문가격을 입력하세요:40000
주문수량을 입력하세요:2
CSPAT00600: [00040] 모의투자 매수주문이 완료 되었습니다.
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
|   1    | 30221 | 125135851 |     40     |     00     |  A005930  |         | 80000  |     0      |     0     |    0     |     2      |     0      |     0     |      0      |     0      | 홍길동 | 삼성전자 |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=14, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:51:35.667561 |
|       0:00:00.028281       |
+----------------------------+
주문요청 결과: [00040] 모의투자 매수주문이 완료 되었습니다.
on_realtime: SC0, , {'lineseq': 100124679, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124679', 'trid': '00125135846336', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125135846, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '02', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '삼성전자', 'ordqty': 2, 'ordprice': 40000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30221, 'ordtm': '125135851', 'prntordno': 30221, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 80000, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 80000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 2, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 6072}
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    10    |      10      |  56427   | 56500  | -0.08  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 3
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30221   |  005930  |   매수   |    2     |  40000   |     2      | 56500  |     0      | 12513585 |
|  29791   |  005930  | 매수정정 |    3     |  45000   |     3      | 56500  |   29484    | 12341714 |
|  27791   |  005930  |   매수   |    1     |  50000   |     1      | 56500  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):3
주문번호를 입력하세요:30221
정정가격을 입력하세요:45000
정정 요청 결과: 모의투자 정정주문이 완료 되었습니다.
on_realtime: SC0, , {'lineseq': 100124893, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT001', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124893', 'trid': '00125305947967', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125305947, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '02', 'marketgb': '10', 'ordgb': '02', 'orgordno': 30221, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '삼성전자', 'ordqty': 2, 'ordprice': 45000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30288, 'ordtm': '125305953', 'prntordno': 30221, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 2, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 90000, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 90000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 2, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
on_realtime: SC2, , {'lineseq': 100124894, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000124894', 'trid': '00125305947967', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125305947, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '12', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': '홍길동', 'Isuno': 'KR7005930003', 'Isunm': '삼성전자', 'ordno': 30288, 'orgordno': 30221, 'execno': 0, 'ordqty': 2, 'ordprc': 45000, 'execqty': 0, 'execprc': 0, 'mdfycnfqty': 2, 'mdfycnfprc': 45000, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '00', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 2, 'orgordunercqty': 0, 'orgordmdfyqty': 2, 'orgordcancqty': 0, 'ordavrexecprc': 0, 'ordamt': 90000, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125305000', 'rcptexectime': '125305000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 2, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 172380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499827620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    10    |      10      |  56427   | 56500  | -0.08  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 3
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | 매수정정 |    2     |  45000   |     2      | 56500  |   30221    | 12530595 |
|  29791   |  005930  | 매수정정 |    3     |  45000   |     3      | 56500  |   29484    | 12341714 |
|  27791   |  005930  |   매수   |    1     |  50000   |     1      | 56500  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):4
주문번호를 입력하세요:29791
취소 요청 결과: 모의투자 취소주문이 완료 되었습니다.
on_realtime: SC0, , {'lineseq': 100125118, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT002', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125118', 'trid': '00125451053359', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125451053, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '03', 'marketgb': '10', 'ordgb': '02', 'orgordno': 29791, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '삼성전자', 'ordqty': 3, 'ordprice': 0, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30342, 'ordtm': '125451058', 'prntordno': 29484, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 3, 'nmcpysndno': 0, 'ordamt': 0, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 0, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 3, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
on_realtime: SC3, , {'lineseq': 100125119, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125119', 'trid': '00125451053359', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125451053, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '13', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': '홍길동', 'Isuno': 'KR7005930003', 'Isunm': '삼성전자', 'ordno': 30342, 'orgordno': 29791, 'execno': 0, 'ordqty': 3, 'ordprc': 0, 'execqty': 0, 'execprc': 0, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 3, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 3, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 3, 'ordavrexecprc': 0, 'ordamt': 0, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125451000', 'rcptexectime': '125451000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 3, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 4072}
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    10    |      10      |  56427   | 56400  | -0.25  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | 매수정정 |    2     |  45000   |     2      | 56400  |   30221    | 12530595 |
|  27791   |  005930  |   매수   |    1     |  50000   |     1      | 56400  |     0      | 11553394 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):3
주문번호를 입력하세요:27791
정정가격을 입력하세요:60000
정정 요청 결과: 모의투자 정정주문이 완료 되었습니다.
on_realtime: SC0, , {'lineseq': 100125170, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT001', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125170', 'trid': '00125540332052', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125540332, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '02', 'marketgb': '10', 'ordgb': '02', 'orgordno': 27791, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '삼성전자', 'ordqty': 1, 'ordprice': 60000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30357, 'ordtm': '125540336', 'prntordno': 27791, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 1, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 60000, 'bnstp': '2', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 60000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 1, 'avrpchsprc': 56428, 'pchsamt': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 2072}
on_realtime: SC2, , {'lineseq': 100125171, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125171', 'trid': '00125540332052', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125540332, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '12', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': '홍길동', 'Isuno': 'KR7005930003', 'Isunm': '삼성전자', 'ordno': 30357, 'orgordno': 27791, 'execno': 0, 'ordqty': 1, 'ordprc': 60000, 'execqty': 0, 'execprc': 0, 'mdfycnfqty': 1, 'mdfycnfprc': 60000, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '00', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 1, 'orgordunercqty': 0, 'orgordmdfyqty': 1, 'orgordcancqty': 0, 'ordavrexecprc': 0, 'ordamt': 60000, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125540000', 'rcptexectime': '125540000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 1, 'avrpchsprc': 56428, 'pchsant': 564275, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 145380, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499854620, 'ordablesubstamt': 0, 'ruseableamt': 2072}
on_realtime: SC1, , {'lineseq': 100125181, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125181', 'trid': '00125540332052', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125540332, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '11', 'ordmktcode': '10', 'ordptncode': '02', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': '홍길동', 'Isuno': 'KR7005930003', 'Isunm': '삼성전자', 'ordno': 30357, 'orgordno': 27791, 'execno': 83857, 'ordqty': 1, 'ordprc': 60000, 'execqty': 1, 'execprc': 56400, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '00', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 0, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 0, 'ordavrexecprc': 56400, 'ordamt': 60000, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '2', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125542000', 'rcptexectime': '125542000', 'rmndLoanamt': 0, 'secbalqty': 11, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 11, 'sellableqty': 11, 'unercsellordqty': 0, 'avrpchsprc': 56425, 'pchsant': 620675, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 2072}
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    11    |      11      |  56425   | 56600  |  0.09  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 1
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | 매수정정 |    2     |  45000   |     2      | 56600  |   30221    | 12530595 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):2
종목코드 6자리를 입력하세요 (ex 삼성전자인 경우 005930):005930
주문구분을 입력하세요 (00:지정가, 03:시장가):03
주문수량을 입력하세요:1
CSPAT00600: [00039] 모의투자 매도주문이 완료 되었습니다.
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
|   1    | 30415 | 125759387 |     40     |     03     |  A005930  |         |   0    |     0      |     0     |    0     |     1      |     0      |     0     |      0      |     0      | 홍길동 | 삼성전자 |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=36, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:57:59.201879 |
|       0:00:00.026036       |
+----------------------------+
주문요청 결과: [00039] 모의투자 매도주문이 완료 되었습니다.
on_realtime: SC0, , {'lineseq': 100125346, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125346', 'trid': '00125759382676', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125759382, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '01', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '삼성전자', 'ordqty': 1, 'ordprice': 0, 'hogagb': '0', 'etfhogagb': '03', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30415, 'ordtm': '125759387', 'prntordno': 30415, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 0, 'bnstp': '1', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 0, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 11, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 11, 'sellableqty': 10, 'unercsellordqty': 1, 'avrpchsprc': 56425, 'pchsamt': 620675, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 2072}
on_realtime: SC1, , {'lineseq': 100125347, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1294, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAS100', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125347', 'trid': '00125759382676', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125759382, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordxctptncode': '11', 'ordmktcode': '10', 'ordptncode': '01', 'mgmtbrnno': '', 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'acntnm': '홍길동', 'Isuno': 'KR7005930003', 'Isunm': '삼성전자', 'ordno': 30415, 'orgordno': 0, 'execno': 83950, 'ordqty': 1, 'ordprc': 0, 'execqty': 1, 'execprc': 56600, 'mdfycnfqty': 0, 'mdfycnfprc': 0, 'canccnfqty': 0, 'rjtqty': 0, 'ordtrxptncode': 0, 'mtiordseqno': 0, 'ordcndi': '0', 'ordprcptncode': '03', 'nsavtrdqty': 0, 'shtnIsuno': 'A005930', 'opdrtnno': '', 'cvrgordtp': '', 'unercqty': 0, 'orgordunercqty': 0, 'orgordmdfyqty': 0, 'orgordcancqty': 0, 'ordavrexecprc': 56600, 'ordamt': 0, 'stdIsuno': 'KR7005930003', 'bfstdIsuno': '', 'bnstp': '1', 'ordtrdptncode': '00', 'mgntrncode': '000', 'adduptp': '41', 'commdacode': '41', 'Loandt': '', 'mbrnmbrno': 0, 'ordacntno': 'XXXXXXXXXXX', 'agrgbrnno': '', 'mgempno': '', 'futsLnkbrnno': '', 'futsLnkacntno': '', 'futsmkttp': '', 'regmktcode': '', 'mnymgnrat': 20, 'substmgnrat': 0, 'mnyexecamt': 0, 'ubstexecamt': 0, 'cmsnamtexecamt': 0, 'crdtpldgexecamt': 0, 'crdtexecamt': 0, 'prdayruseexecval': 0, 'crdayruseexecval': 0, 'spotexecqty': 0, 'stslexecqty': 0, 'strtgcode': '', 'grpId': '00000000000000000000', 'ordseqno': 0, 'ptflno': 0, 'bskno': 0, 'trchno': 0, 'itemno': 0, 'orduserId': 'user1234', 'brwmgmtYn': 0, 'frgrunqno': '', 'trtzxLevytp': '', 'lptp': '', 'exectime': '125759000', 'rcptexectime': '125759000', 'rmndLoanamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 10, 'unercsellordqty': 0, 'avrpchsprc': 56425, 'pchsant': 564250, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 13262}
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    10    |      10      |  56425   | 56600  |  0.09  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 1
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30288   |  005930  | 매수정정 |    2     |  45000   |     2      | 56600  |   30221    | 12530595 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):2
종목코드 6자리를 입력하세요 (ex 삼성전자인 경우 005930):005930
주문구분을 입력하세요 (00:지정가, 03:시장가):00
주문가격을 입력하세요:60000
주문수량을 입력하세요:4
CSPAT00600: [00039] 모의투자 매도주문이 완료 되었습니다.
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
|   1    | 30449 | 125848706 |     40     |     00     |  A005930  |         | 240000 |     0      |     0     |    0     |     4      |     0      |     0     |      0      |     0      | 홍길동 | 삼성전자 |
+--------+-------+-----------+------------+------------+-----------+---------+--------+------------+-----------+----------+------------+------------+-----------+-------------+------------+--------+----------+
nRqID=41, cont_yn=False, cont_key=
+----------------------------+
|  request / elapsed times   |
+----------------------------+
| 2024-11-18 12:58:48.518812 |
|       0:00:00.028306       |
+----------------------------+
주문요청 결과: [00039] 모의투자 매도주문이 완료 되었습니다.
on_realtime: SC0, , {'lineseq': 100125431, 'accno': 'XXXXXXXXXXX', 'user': 'user1234', 'len': 1053, 'gubun': 'B', 'compress': '0', 'encrypt': '0', 'offset': 212, 'trcode': 'SONAT000', 'comid': '063', 'userid': 'user1234', 'media': 'HT', 'ifid': '000', 'seq': '000125431', 'trid': '00125848701365', 'pubip': '058120201069', 'prvip': '', 'pcbpno': '', 'bpno': '', 'termno': '', 'lang': 'K', 'proctm': 125848701, 'msgcode': '0000', 'outgu': '', 'compreq': '0', 'funckey': 'C', 'reqcnt': 0, 'filler': '', 'cont': 'N', 'contkey': '', 'varlen': 50, 'varhdlen': 0, 'varmsglen': 0, 'trsrc': 's', 'eventid': '0078', 'ifinfo': '', 'filler1': '', 'ordchegb': '01', 'marketgb': '10', 'ordgb': '01', 'orgordno': 0, 'accno1': 'XXXXXXXXXXX', 'accno2': '', 'passwd': '********', 'expcode': 'KR7005930003', 'shtcode': 'A005930', 'hname': '삼성전자', 'ordqty': 4, 'ordprice': 60000, 'hogagb': '0', 'etfhogagb': '00', 'pgmtype': 0, 'gmhogagb': 0, 'gmhogayn': 0, 'singb': '000', 'loandt': '', 'cvrgordtp': '', 'strtgcode': '', 'groupid': '', 'ordseqno': 0, 'prtno': 0, 'basketno': 0, 'trchno': 0, 'itemno': 0, 'brwmgmyn': 0, 'mbrno': 63, 'procgb': '', 'admbrchno': '', 'futaccno': '', 'futmarketgb': '', 'tongsingb': '41', 'lpgb': '', 'dummy': '', 'ordno': 30449, 'ordtm': '125848706', 'prntordno': 30449, 'mgempno': '', 'orgordundrqty': 0, 'orgordmdfyqty': 0, 'ordordcancelqty': 0, 'nmcpysndno': 0, 'ordamt': 240000, 'bnstp': '1', 'spareordno': 0, 'cvrgseqno': 0, 'rsvordno': 0, 'mtordseqno': 0, 'spareordqty': 0, 'orduserid': '', 'spotordqty': 0, 'ordruseqty': 0, 'mnyordamt': 240000, 'ordsubstamt': 0, 'ruseordamt': 0, 'ordcmsnamt': 0, 'crdtuseamt': 0, 'secbalqty': 10, 'spotordableqty': 0, 'ordableruseqty': 0, 'flctqty': 0, 'secbalqtyd2': 10, 'sellableqty': 6, 'unercsellordqty': 4, 'avrpchsprc': 56425, 'pchsamt': 564250, 'deposit': 500000000, 'substamt': 0, 'csgnmnymgn': 144660, 'csgnsubstmgn': 0, 'crdtpldgruseamt': 0, 'ordablemny': 499855340, 'ordablesubstamt': 0, 'ruseableamt': 13262}
잔고조회중...
Row Count = 1
+----------+----------+----------+--------------+----------+--------+--------+
| 종목코드 |  종목명  | 잔고수량 | 매도가능수량 | 평균단가 | 현재가 | 수익율 |
+----------+----------+----------+--------------+----------+--------+--------+
|  005930  | 삼성전자 |    10    |      6       |  56425   | 56500  | -0.07  |
+----------+----------+----------+--------------+----------+--------+--------+
미체결조회중...
Row Count = 2
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
| 주문번호 | 종목코드 |   구분   | 주문수량 | 주문가격 | 미체결잔량 | 현재가 | 원주문번호 | 주문시간 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
|  30449   |  005930  |   매도   |    4     |  60000   |     4      | 56500  |     0      | 12584870 |
|  30288   |  005930  | 매수정정 |    2     |  45000   |     2      | 56500  |   30221    | 12530595 |
+----------+----------+----------+----------+----------+------------+--------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):
잔고관련 실시간 해지
'''