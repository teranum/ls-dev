# -*- coding: euc-kr -*-
from builtins import print as original_print, input as original_input
from prettytable import *

from xingAsync import ResponseData


def run_loop(coro, forever = False):
    '''
    asyncio 루프를 실행하는 함수
    :param coro: 실행할 코루틴
    :param forever: 무한루프 여부
    '''
    import asyncio
    from qasync import QApplication
    from qasync import QEventLoop
    app = QApplication.instance()
    if app is not None:
        raise Exception("QApplication instance already exists. use exist event loop")
    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(coro)
        if forever: # 무한루프
            loop.run_forever()

ext_print = None
ext_input = None
def set_ext_func(print_func, input_func):
    global ext_print
    global ext_input
    ext_print = print_func
    ext_input = input_func

def input(prompt: str = "") -> str:
    if ext_input is not None:
        return ext_input(prompt)
    return original_input(prompt)

# prettytable을 사용하여 데이터를 표로 이쁘게 출력하는 함수
# 표준 print 함수를 대체하여 사용
def print(data, title=None):
    print_func = ext_print if ext_print is not None else original_print
    if data is None: return
    if isinstance(data, str):
        print_func(data)
    elif isinstance(data, dict):
        table = PrettyTable(['key','value'])
        fields = data.items();
        table.add_rows([list(x) for x in fields])
        print_func(f'Field Count = {len(fields)}')
        print_func(table)
    elif isinstance(data, list):
        if len(data) == 0:
            print_func('[]')
            return
        if isinstance(data[0], dict):
            table = PrettyTable()
            table.field_names = data[0]
            table.add_rows([x.values() for x in data])
            print_func(f'Row Count = {len(data)}')
            print_func(table)
        else:
            title = title if title is not None else 'value'
            table = PrettyTable([title])
            table.add_rows([[x] for x in data])
            print_func(f'Row Count = {len(data)}')
            print_func(table)
    elif isinstance(data, ResponseData):
        print_func(f'{data.tr_cd}: [{data.rsp_cd}] {data.rsp_msg}')
        keys = data.body.keys()
        for key in keys:
            print_func(key)
            print_func(data.body[key])
        print_func(f'nRqID={data.nRqID}, cont_yn={data.cont_yn}, cont_key={data.cont_key}')
