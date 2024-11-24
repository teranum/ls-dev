# -*- coding: euc-kr -*-


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
