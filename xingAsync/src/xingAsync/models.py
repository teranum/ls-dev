class AccountInfo:
    def __init__(self):
        self.number: str = ''
        ''' 계좌번호 (11자리 숫자) '''
        self.name: str = ''
        ''' 계좌명 '''
        self.detail_name: str = ''
        ''' 상세계좌명 ('선물옵션', '해외선물', ...) '''
        self.nick_name: str = ''
        ''' 닉네임 '''
        self.pass_number: str = ''
        ''' 비밀번호 (4자리 숫자: 주문시 필수 세팅)'''
    def __str__(self):
        return f'{self.number} {self.name} {self.detail_name}'

class ResponseData:
    '''
    RequestTrAsync 요청 응답 클래스
    '''
    def __init__(self):
        self.tr_cd = ''
        ''' TR 코드 '''
        self.nRqID: int = 0

        # 서버 응답 데이터
        self.cont_yn = False
        ''' 연속여부 '''
        self.cont_key = ''
        ''' 연속키 '''
        self.rsp_cd = ''
        ''' 응답코드 '''
        self.rsp_msg = ''
        ''' 응답메시지 '''
        self.body = {}
        ''' 응답 데이터 '''
