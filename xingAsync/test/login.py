# -*- coding: euc-kr -*-
from xingAsync import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py ���Ͽ� ����� ID, ���, ���� ����� �����صΰ� import

async def sample(api: XingApi):
    print('�α��� ��û��...')

    if not await api.login(user_id, user_pwd, cert_pwd):
        print(f'�α��� ����: {api.last_message}')
        return

    print(f'�α��� ����: {'��������' if api.is_simulation else '������'}')

    # �������� ǥ��
    for x in api.accounts:
        print(x)

    # �Ｚ���� ���簡 ��ȸ
    response = await api.request('t1102', '005930') # 005930: �Ｚ����
    if not response:
        print(f'��û����: {api.last_message}')
        return

    price = response['t1102OutBlock'][0]['price']
    print(f'�Ｚ���� ���簡: {price}')


if __name__ == "__main__":
    api = XingApi()
    from qasync import QApplication, QEventLoop
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(sample(api))

