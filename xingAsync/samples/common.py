# -*- coding: euc-kr -*-


def run_loop(coro, forever = False):
    '''
    asyncio ������ �����ϴ� �Լ�
    :param coro: ������ �ڷ�ƾ
    :param forever: ���ѷ��� ����
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
        if forever: # ���ѷ���
            loop.run_forever()
