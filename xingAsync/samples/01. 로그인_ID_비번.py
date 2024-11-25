# -*- coding: euc-kr -*-
from xingAsync import *

async def sample(api: XingApi):
    if api.logined:
        print("�̹� �α��� �Ǿ����ϴ�.")
        for x in api.accounts: print(x)
        return

    user_id = input("����� ���̵�:")
    user_pwd = input("����� �н�����:")
    cert_pwd = input("�������� �н����� (���Է½� �������ڷ� �α���):")

    print("�α��� ��û��...")
    if not await api.login(user_id, user_pwd, cert_pwd):
        return print(f"�α��� ����: {api.last_message}")
    print(f"�α��� ����: {"��������" if api.is_simulation else "������"}")

    for x in api.accounts: print(x)


if __name__ == "__main__":
    api = XingApi()
    from qasync import QApplication, QEventLoop
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(sample(api))
