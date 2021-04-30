#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/13 10:13
# @Author : hu xu
# @File : runner.py
# @Software: longyuan
import os
import argparse
import pathlib
from common import cls_coclient
from common.pytest_func import utlis, reading_data

file_path = pathlib.Path(__file__).parent
config_data = reading_data.config_data()
curPath = os.path.abspath(os.path.dirname(__file__))
parse = argparse.ArgumentParser(description='运行参数')
parse.add_argument('--pagpath', type=str, default=config_data['apk路径'])
parse.add_argument('--server', type=str, default=config_data['连接服务器'])
parse.add_argument('--test_module', type=str, default=config_data['测试用例模块'])
args = parse.parse_args()
pagpath = args.pagpath
server = args.server

test_module = args.test_module
if config_data['apk路径']:
    cls_coclient.entrance.run(pag_path=pagpath, game_server=server)

# 运行测试
if test_module != 'All':
    os.system(f'pytest {curPath}/test_case.py::TestChoice --alluredir {curPath}/resource/temp --clean-alluredir')
else:
    os.system(f'pytest {curPath}/test_case.py --alluredir {curPath}/resource/temp --clean-alluredir')
os.system(f'allure generate {curPath}/resource/temp -o {curPath}/report --clean')

print('报告查看地址(本地):'+curPath+r'\report\index.html')
report_path = config_data['测试报告访问地址']
