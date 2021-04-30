#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/23 17:23
# @Author : liu lin
# @File : data.py
# @Software: longyuan
"""
1.处理用例数据
2.生成测试套件
3.游戏模式切换
"""
import re
import json
import pathlib
import allure
from common.pytest_func import case_header, Excel
file_path = pathlib.Path(__file__).parent.parent



def data_to_dict(data):
    """
    :param data:
    :return:
    """
    head = []
    list_dict_data = []
    for d in data[0]:
        d = case_header.get(d, d)
        head.append(d)
    for b in data[1:]:
        dict_data = {}
        for i in range(len(head)):
            if isinstance(b[i], str):
                dict_data[head[i]] = b[i].strip()
            else:
                dict_data[head[i]] = b[i]
        list_dict_data.append(dict_data)
    return list_dict_data


def case_orders(case_order):
    """处理case_order.xlsx文件中的用例命令"""
    if '{' in case_order:
        case_order = re.findall('{(.*?)}', case_order)
        order_list = list()
        for c in case_order:
            c = "{" + c + "}"
            c = eval(c)
            order_list.append(c)
        return order_list
    else:
        case_order = case_order.split('\n')
        return case_order


def dict_to_suite(data):
    """

    :param chess_id:
    :param data: dict_data
    :return:
    """
    test_suite = dict()
    for d in data:
        if d['execute'] == 'pass':
            continue
        test_case = {'id': d['id'], 'description': d['description'],
                     'event_list': case_orders(d['step']), 'expect': d['expect']}
        moudle_name = test_case['id'].split('_')[0]
        if moudle_name not in test_suite.keys():
            test_suite[moudle_name] = []
            test_suite[moudle_name].append(test_case)
        else:
            test_suite[moudle_name].append(test_case)
    return test_suite




@allure.step('切换检测模块')
def change_mode(mode):
    """模式切换"""
    file1 = open(file_path.parent / "test/run/work/QT.json", "w")
    file2 = open(file_path.parent / "test/Datas/QT.json", "w")
    data = {
      "Hread-Field": "Network Configuration",
      "Pack-Field": {
        "GameMode": mode,
        "PlayerCount": 8
      }
    }
    file1.write(json.dumps(data))
    file2.write(json.dumps(data))
    file1.close()
    file2.close()


def select_data(moudle='All'):
    m = Excel(file_path.parent / 'case/cases.xlsx')
    m.read('case_sheet')
    data_dict = data_to_dict(m.list_data)
    test_suite = dict_to_suite(data_dict)
    if moudle == 'All':
        all_case_data = list()
        for t in test_suite:
            t_data = test_suite[t]
            all_case_data = all_case_data+t_data
        return all_case_data
    else:
        try:
            return test_suite[moudle]
        except Exception:
            return None


def config_data():
    m = Excel(file_path.parent / 'case/cases.xlsx')
    m.read('config_sheet')
    m.dic = dict()
    for i in m.list_data:
        m.dic[i[0]] = i[1]
    return m.dic


if __name__ == '__main__':
    print(select_data(moudle='Home'))
