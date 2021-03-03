import pytest
import logging


LOG_DEFAULT_LEVEL = logging.DEBUG


@pytest.fixture(scope="session", autouse=True)
def set_up(request):
    '''Test package setup'''
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=LOG_DEFAULT_LEVEL,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='pytest.log',
                        filemode='w')
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(LOG_DEFAULT_LEVEL)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #################################################################################################
    # logging.debug('This is debug message')
    # logging.info('This is info message')
    # logging.warning('This is warning message')


def tear_down():
    '''Test package teardown'''