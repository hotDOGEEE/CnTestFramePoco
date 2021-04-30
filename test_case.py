#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/23 17:18
# @Author : hu xu
# @File : test_case.py
# @Software: longyuan
import pytest
import allure
import pathlib
import time
import os
import re
from poco.drivers.unity3d import UnityPoco
from common.cls_coclient.log import logger
from common.pytest_func import select_data
from common import adb_shell
from common.pytest_func import reading_data


al = adb_shell.AdbShell()
poco = UnityPoco()


file_path = pathlib.Path(__file__).parent

# 检测模块
config_data = reading_data.config_data()
Choice_moudle = config_data['测试用例模块']
Case_data = select_data(Choice_moudle)



@allure.step('执行测试用例')
def runner(case_data):
    """
    case_data的结构还需要自己定，定下来之后自己判断对应数据去做什么事情
    刘林写的这套沿用框架，里面具体实现的方法统统不要自己根据项目写
    :param case_data:
    :return:
    """
    def _chinese_operation(item):
        """
        传进来的是以excel中测试步骤行为单位的项，每一项对应一个操作
        :param item:
        :return:
        """

        event = item.split('"')[0]
        content = re.findall('.*?"(.*?)"$', item)[0]
        if '点击' in event:
            if 'poco' in content:
                exec(content+'.click()')
            elif ',' in content:
                poco.click(eval(content))
            else:
                poco(text=content).click()
        elif '滑动' in event:
            try:
                event_content = eval(content)
                al.swipe(event_content[0], event_content[1])
            except Exception:
                event_content = content.split("],[")
                al.swipe(event_content[0]+']', '['+event_content[1])
        elif '输入' in event:
            c = content.split(':')
            if 'poco' in content:
                exec(c[0]+'.set_text("'+c[1]+'")')
            else:
                poco(text=c[0]).parent().set_text(c[1])
        elif '长按' in event:
            if 'poco' in content:
                exec(content + '.long_click()')
            if ',' in content:
                poco.click(eval(content))
            else:
                poco(text=content).long_click()
        elif '出现' in event:
            if 'poco' in content:
                exec(content + '.wait_for_appearance()', )
            else:
                poco(text=content).wait_for_appearance()
        elif '消失' in event:
            if 'poco' in content:
                exec(content + '.wait_for_disappearance()')
            else:
                poco(text=content).wait_for_disappearance()
        elif '等待' in event:
            time.sleep(int(content))
        elif '不存在' in event:
            poco_instruct = content+'.exists()'
            code_str = f"""
exists_check_rst = {poco_instruct}
print(exists_check_rst)
assert exists_check_rst is False
            """
            if 'poco' in content:
                exec(code_str)
            else:
                exists_check_rst = poco(text=content).exists()
                assert exists_check_rst is False
        elif '存在' in event:
            poco_instruct = content + '.exists()'
            code_str = f"""
exists_check_rst = {poco_instruct}
print(exists_check_rst)
assert exists_check_rst is True
            """
            if 'poco' in content:
                exec(code_str)
            else:
                exists_check_rst = poco(text=content).exists()
                assert exists_check_rst is True
        elif '截屏' in event:
            snapname = content
            os.system(f'adb shell screencap -p /sdcard/{snapname}.png')
        elif '返回' == content:
            os.system('adb shell input keyevent 4')
            time.sleep(2)

    def _expect_check(ep):
        event = ep.split('"')[0]
        content = ep.split('"')[1]
        if '显示' == event:
            poco(text=content).wait_for_appearance()
        elif '消失' in event or '不显示' == event:
            poco(text=content).wait_for_disappearance()

    print('打印测试数据')
    print(case_data)
    allure.dynamic.title(case_data['id'])
    allure.dynamic.description(case_data['description'])
    logger.info(f'case_name: {case_data["id"]}, description: {case_data["description"]}')
    #执行用例部分
    for i in case_data['event_list']:
        _chinese_operation(i)
        time.sleep(1)
    #检查结果部分
    expect = case_data['expect']
    _expect_check(expect)



def back_home():
    for _ in range(100):
        if poco(text='大厅').exists():
            break
        elif poco(text='是否退出游戏').exists():
            poco(text='取消').click()
            if poco(text='大厅').exists():
                poco(text='大厅').click()
                break
            else:
                logger.info('进入到奇怪界面')
        else:
            os.system('adb shell input keyevent 4')
            time.sleep(1)


class TestChoice:

    """
    这是一个模块的检测，我们的setup和teardown，不是切换到对应模式
    启动关闭qt的过程，我们要的是，从大厅跳转到对应模块下，最后teardown回到大厅的过程
    """

    def setup_class(cls):
        pass

    def teardown_class(cls):
        back_home()

    @allure.feature(Choice_moudle)
    @pytest.mark.parametrize("case_data", Case_data)
    def test_warehouse(self, case_data):
        try:
            runner(case_data)
        except RuntimeError:
            print('用例报错，退回主界面')
        finally:
            back_home()

