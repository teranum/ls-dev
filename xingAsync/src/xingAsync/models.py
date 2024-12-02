class AccountInfo:
    ''' 계좌정보 클래스 '''

    def __init__(self):

        self.number: str = ''
        ''' 계좌번호 (11자리 숫자) '''

        self.name: str = ''
        ''' 계좌명 '''

        self.detail_name: str = ''
        ''' 상세계좌명 ('선물옵션', '해외선물', ...) '''

        self.nick_name: str = ''
        ''' 닉네임 '''

    def __str__(self):
        return f'{self.number} {self.name} {self.nick_name} {self.detail_name}'

class ResponseData:
    ''' request 응답 클래스 '''

    def __init__(self):

        self.tr_cd = ''
        ''' TR 코드 '''

        self.cont_yn = False
        ''' 연속여부 '''

        self.cont_key = ''
        ''' 연속키 '''

        self.rsp_cd = ''
        ''' 응답코드 '''

        self.rsp_msg = ''
        ''' 응답메시지 '''

        self.body: dict[str, dict | list] = {}
        '''
        응답 데이터 (inblock 포함)
        배열이면 list, 아니면 dict
        '''

        self.id: int = 0
        ''' 요청 ID '''

        self.elapsed_ms: float = 0.0
        ''' 요청/응답 소요시간 (ms) '''

        self.res = None
        ''' 자원정보 '''


    def __getitem__(self, key: str, /) -> dict | list | None: 
        return self.body.get(key, None)

    def __str__(self) -> str:
        return f'tr_cd=\'{self.tr_cd}\'\ncont_yn={self.cont_yn}\ncont_key=\'{self.cont_key}\'\nrsp_cd=\'{self.rsp_cd}\'\nrsp_msg=\'{self.rsp_msg}\'\nbody={self.body}\nelapsed_ms={self.elapsed_ms}'
