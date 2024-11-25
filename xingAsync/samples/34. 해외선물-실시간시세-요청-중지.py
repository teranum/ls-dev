# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"로그인 실패: {api.last_message}")

    real_code = "OVC"   # 실시간 코드: (OVC: 해외선물 체결, OVH: 해외선물 호가, ...)
    key = "HSIX24"      # 실시간 Key/종목코드: (HSIX24: Hang Seng(2024.11), ...)
    advise = True       # True 이면 실시간 시작, False 이면 실시간 중지

    if api.realtime(real_code, key, advise):
        print(f"요청 성공: {real_code}, {key}, {advise}")
    else:
        print(f"요청 실패: {api.last_message}")

if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(lambda tr_cd, key, datas: print(f"on_realtime: {tr_cd}, {key}, {datas}"))
    run_loop(sample(api), forever=True) # 무한루프로 실행

# Output:
'''
요청 성공: OVC, HSIX24, True
on_realtime: OVC, HSIX24, {'symbol': 'HSIX24', 'ovsdate': '20241121', 'kordate': '20241121', 'trdtm': '175933', 'kortm': '185933', 'curpr': 19540.0, 'ydiffpr': 49.0, 'ydiffSign': '5', 'open': 19588.0, 'high': 19592.0, 'low': 19496.0, 'chgrate': -0.25, 'trdq': 1, 'totq': '1415', 'cgubun': '-', 'mdvolume': '', 'msvolume': '', 'ovsmkend': '20241122'}
on_realtime: OVC, HSIX24, {'symbol': 'HSIX24', 'ovsdate': '20241121', 'kordate': '20241121', 'trdtm': '175933', 'kortm': '185933', 'curpr': 19540.0, 'ydiffpr': 49.0, 'ydiffSign': '5', 'open': 19588.0, 'high': 19592.0, 'low': 19496.0, 'chgrate': -0.25, 'trdq': 1, 'totq': '1416', 'cgubun': '-', 'mdvolume': '', 'msvolume': '', 'ovsmkend': '20241122'}
on_realtime: OVC, HSIX24, {'symbol': 'HSIX24', 'ovsdate': '20241121', 'kordate': '20241121', 'trdtm': '175935', 'kortm': '185935', 'curpr': 19539.0, 'ydiffpr': 50.0, 'ydiffSign': '5', 'open': 19588.0, 'high': 19592.0, 'low': 19496.0, 'chgrate': -0.26, 'trdq': 1, 'totq': '1417', 'cgubun': '-', 'mdvolume': '', 'msvolume': '', 'ovsmkend': '20241122'}
on_realtime: OVC, HSIX24, {'symbol': 'HSIX24', 'ovsdate': '20241121', 'kordate': '20241121', 'trdtm': '175939', 'kortm': '185939', 'curpr': 19540.0, 'ydiffpr': 49.0, 'ydiffSign': '5', 'open': 19588.0, 'high': 19592.0, 'low': 19496.0, 'chgrate': -0.25, 'trdq': 1, 'totq': '1418', 'cgubun': '+', 'mdvolume': '', 'msvolume': '', 'ovsmkend': '20241122'}
on_realtime: OVC, HSIX24, {'symbol': 'HSIX24', 'ovsdate': '20241121', 'kordate': '20241121', 'trdtm': '175940', 'kortm': '185940', 'curpr': 19540.0, 'ydiffpr': 49.0, 'ydiffSign': '5', 'open': 19588.0, 'high': 19592.0, 'low': 19496.0, 'chgrate': -0.25, 'trdq': 1, 'totq': '1419', 'cgubun': '+', 'mdvolume': '', 'msvolume': '', 'ovsmkend': '20241122'}
'''