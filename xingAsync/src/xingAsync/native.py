import ctypes

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

class RECV_FLAG:
    REQUEST_DATA: int = 1
    MESSAGE_DATA: int = 2
    SYSTEM_ERROR_DATA: int = 3
    RELEASE_DATA: int = 4

class RECV_PACKET(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("nRqID", ctypes.c_int),
        ("nDataLength", ctypes.c_int),
        ("nTotalDataBufferSize", ctypes.c_int),
        ("nElapsedTime", ctypes.c_int),
        ("nDataMode", ctypes.c_int),
        ("szTrCode", ctypes.c_char * 10),
        ("_szTrCode", ctypes.c_char),
        ("cCont", ctypes.c_char),
        ("szContKey", ctypes.c_char * 18),
        ("_szContKey", ctypes.c_char),
        ("szUserData", ctypes.c_char * 30),
        ("_szUserData", ctypes.c_char),
        ("szBlockName", ctypes.c_char * 16),
        ("_szBlockName", ctypes.c_char),
        ("lpData", ctypes.c_voidp)
    ]

class MSG_PACKET(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("nRqID", ctypes.c_int),
        ("nIsSystemError", ctypes.c_int),
        ("szMsgCode", ctypes.c_char * 5),
        ("_szMsgCode", ctypes.c_char),
        ("nMsgLength", ctypes.c_int),
        ("szMessageData", ctypes.c_voidp)
    ]

class REAL_RECV_PACKET(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("szTrCode", ctypes.c_char * 3),
        ("_szTrCode", ctypes.c_char),
        ("nKeyLength", ctypes.c_int),
        ("szKeyData", ctypes.c_char * 32),
        ("_szKeyData", ctypes.c_char),
        ("szRegKey", ctypes.c_char * 32),
        ("_szRegKey", ctypes.c_char),
        ("nDataLength", ctypes.c_int),
        ("pszData", ctypes.c_voidp)
    ]
