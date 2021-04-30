# -*- coding: utf-8 -*-
import logging
import pathlib
import sys
import os

log_file = pathlib.Path(__file__).parent.parent / 'test_report/result/test_log.log'


def clear():
    lf = str(log_file)
    try:
        os.remove(lf)
    except Exception:
        pass


clear()


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger()

# 指定logger输出格式
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s]: %(message)s')


file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8', delay=False)
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器

logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
# DEBUG，INFO，WARNING，ERROR，CRITICAL
logger.setLevel(logging.INFO)


