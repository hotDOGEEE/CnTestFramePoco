#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/23 17:22  
# @Author : liu lin
# @File : config.py
# @Software: longyuan
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

case_header = {
    '用例编号': 'id',
    '用例描述': 'description',
    '用例状态': 'state',
    '游戏模式': 'mode',
    '测试步骤': 'step',
    '预期结果': 'expect',
    '数据校验': 'assert',
    '是否执行': 'execute'
}
