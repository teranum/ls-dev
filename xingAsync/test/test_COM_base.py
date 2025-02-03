from xingAsync import XASession, XAQuery, XAReal
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

########################################################################################
# COM 객체 XASession, XAQuery, XAReal 테스트
# * asyncio를 사용하지 않음, asyncio 이용 어려울 경우 사용 (가능한 DLL 모드 XingApi 이용 권장)
# * Res파일 경로 설정 필요없음
# * OnLogin, OnReceiveData 이벤트 처리 필요없음, 실시간 데이터 수신시 OnReceiveRealData 이벤트 처리 필요
########################################################################################

def sample():
    # 로그인
    session = XASession()
    session.ConnectServer("api.ls-sec.co.kr", 20001)
    if not session.Login(user_id, user_pwd, cert_pwd, 0, 0):
        print(f"로그인 실패: {session.last_message}")
        return

    print(f"로그인 성공: {session.last_message}")

    # 보유계좌 표시
    acc_count = session.GetAccountListCount()
    print(f"Account List Count: {acc_count}")
    for i in range(acc_count):
        acc_num = session.GetAccountList(i)
        acc_name = session.GetAccountName(acc_num)
        acc_detail = session.GetAcctDetailName(acc_num)
        print(f"{acc_num} {acc_name} {acc_detail}")

    # 요청: 삼성전자("005930") 현재가 조회
    query = XAQuery("t1102")
    query.SetFieldData("t1102InBlock", "shcode", 0, "005930")
    ret = query.Request(False)
    if ret < 0:
        print(f"t1102 request failed: {query.last_message}")
        return

    # 요청 성공시, 조회된 데이터 확인
    print(f"t1102 request succeeded: {query.last_message}")
    price = query.GetFieldData('t1102OutBlock', 'price', 0)
    print(f"삼성전자 현재가: {price}")

    # 추가작업
    ...

    # 실시간 시세 요청/이벤트 처리
    real = XAReal("S3_")
    real.OnReceiveRealData = lambda code: print(f"RealData: {code}")
    real.SetFieldData("InBlock", "shcode", "005930")
    real.AdviseRealData()


if __name__ == "__main__":
    sample()
    # 실시간 데이터 수신시 메시지 루프 필요
    import pythoncom
    while True:
        pythoncom.PumpWaitingMessages()

# Output:
'''
로그인 성공: [0000] 로그인 성공
Account List Count: 3
XXXXXXXXXXX 홍길동 선물옵션
XXXXXXXXXXX 홍길동 해외선옵
XXXXXXXXXXX 홍길동 종합매매
t1102 request succeeded: [00000] 정상적으로 조회가 완료되었습니다.
삼성전자 현재가: 51000
RealData: S3_
RealData: S3_
RealData: S3_
...
'''