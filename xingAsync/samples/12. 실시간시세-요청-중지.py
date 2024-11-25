# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py ���Ͽ� ����� ID, ���, ���� ����� �����صΰ� import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")

    real_code = "S3_"   # �ǽð� �ڵ�: (S3_: KOSPIü��, H1_: KOSPIȣ���ܷ�, DH1: KOSPI�ð��ܴ��ϰ�ȣ���ܷ�, ...)
    key = "005930"      # �ǽð� Key/�����ڵ�: (005930: �Ｚ����, ...)
    advise = True       # True �̸� �ǽð� ����, False �̸� �ǽð� ����

    if api.realtime(real_code, key, advise):
        print(f"��û ����: {real_code}, {key}, {advise}")
    else:
        print(f"��û ����: {api.last_message}")

if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(lambda tr_cd, key, datas: print(f"on_realtime: {tr_cd}, {key}, {datas}"))
    run_loop(sample(api), forever=True) # ���ѷ����� ����

# Output:
'''
��û ����: S3_, 005930, True
'''