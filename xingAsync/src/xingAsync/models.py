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
    '''
    request 응답 클래스
    '''
    def __init__(self):
        self.tr_cd = ''
        ''' TR 코드 '''
        self.id: int = 0
        ''' 요청 ID '''

        # 서버 응답 데이터
        self.cont_yn = False
        ''' 연속여부 '''
        self.cont_key = ''
        ''' 연속키 '''
        self.rsp_cd = ''
        ''' 응답코드 '''
        self.rsp_msg = ''
        ''' 응답메시지 '''
        self.body: dict[str, list | dict] = {}
        ''' 응답 데이터 '''

        self.tag = None
        ''' 자원정보 '''
        # self.times: list = []
        # ''' 요청/응답시간 '''

        self.ticks: list[int] = []

    def __getitem__(self, key: str, /) -> list | None: 
        result = self.body.get(key, None)
        if result is not None:
            return result
        if key.endswith('.fields'):
            key = key.replace('.fields', '')
            # tag에서 찾기
            if self.tag is not None:
                for block in self.tag.in_blocks:
                    if block.name == key:
                        return block.fields
                for block in self.tag.out_blocks:
                    if block.name == key:
                        return block.fields
        return None
