import asyncio
from xingAsync import *
from app_key import user_id, user_pwd, cert_pwd # app_key.py 파일에 사용자 ID, 비번, 공증 비번을 저장해두고 import

async def sample(api: XingApi):
    if not await api.login(user_id, user_pwd, cert_pwd):
        print(f'로그인 실패: {api.last_message}')
        return

    # 실시간 요청
    codes = ['005930', '000660'] # 삼성전자, SK하이닉스 실시간 체결 수신
    if not api.realtime('S3_', codes, True):
        return print(f'실시간 요청 실패: {api.last_message}')

    print('실시간 요청 성공, 60초동안 실시간 수신...')
    await asyncio.sleep(60)

    # 실시간 해지
    api.realtime('', '', False) # 실시간 해지

def on_realtime(code: str, key: str, datas: dict):
    print(f'{code}, {key} => {datas}')

if __name__ == "__main__":
    api = XingApi()
    api.on_realtime.connect(on_realtime)
    run_loop(sample(api))
