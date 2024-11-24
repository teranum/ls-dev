# -*- coding: euc-kr -*-
from xingAsync import *
from common import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py ���Ͽ� ����� ID, ���, ���� ����� �����صΰ� import

async def sample(api: XingApi):
    if api.logined:
        print("�̹� �α��� �Ǿ����ϴ�.")
        print(api.accounts, "��������")
        return

    print("�α��� ��û��...")
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")
    print(f"�α��� ����: {"��������" if api.is_simulation else "������"}")

    print(api.accounts, "��������")


if __name__ == "__main__":
    api = XingApi()
    run_loop(sample(api), True) # ���� ����, �Ǵ� �Ʒ��� ���� ����
