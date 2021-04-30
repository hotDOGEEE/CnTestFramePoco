#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/23 17:23  
# @Author : liu lin
# @File : utlis.py
# @Software: longyuan
"""
1.读取测试用例
"""
import xlrd


class Excel:

    def __init__(self, file_name):
        # 打开文件
        self.wb = xlrd.open_workbook(file_name)
        self.sh = self.wb.sheet_names()
        # 装载所有数据的list
        self.list_data = []
        # 将测试数据内调用的方法，改编成自定义里面的变量
        self.dict_data = {}

    def read(self, target_sheet=None):
        # 循环编辑
        if not target_sheet:
            for sheet_name in self.sh:
                # 通过每个sheetname获取到每个页的内容
                sheet = self.wb.sheet_by_name(sheet_name)
                # 获取总行数
                rosw = sheet.nrows
                # 根据总行数进行读取
                for i in range(0, rosw):
                    rowvalues = sheet.row_values(i)
                    # 讲每一行的内容添加进去
                    self.list_data.append(rowvalues)
        else:
            sheet = self.wb.sheet_by_name(target_sheet)
            # 获取总行数
            rosw = sheet.nrows
            # 根据总行数进行读取
            for i in range(0, rosw):
                rowvalues = sheet.row_values(i)
                # 讲每一行的内容添加进去
                self.list_data.append(rowvalues)