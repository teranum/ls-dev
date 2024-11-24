
class XING_MSG:
    """ 서버메시지 """

    XM_DISCONNECT: int = 1
    """ 서버와의 연결이 끊어졌을 경우 발생 """

    XM_RECEIVE_DATA: int = 3
    """ RequestData로 요청한 데이터가 서버로부터 받았을 때 발생 """

    XM_RECEIVE_REAL_DATA: int = 4
    """ AdviseData로 요청한 데이터가 서버로부터 받았을 때 발생 """

    XM_LOGIN: int = 5
    """ 서버로부터 로그인 결과 받았을때 발생 """

    XM_LOGOUT: int = 6
    """ 서버로부터 로그아웃 결과 받았을때 발생 """

    XM_TIMEOUT_DATA: int = 7
    """ RequestData로 요청한 데이터가 Timeout 이 발생했을때 """

    XM_RECEIVE_LINK_DATA: int = 8
    """ HTS 에서 연동 데이터가 발생했을 때 """

    XM_RECEIVE_REAL_DATA_CHART: int = 10
    """ 실시간 자동 등록한 후 차트 조회 시, 지표실시간 데이터를 받았을 때 """

    XM_RECEIVE_REAL_DATA_SEARCH: int = 11
    """ 종목검색 실시간 데이터를 받았을 때 """

    XM_LAST: int = 12
