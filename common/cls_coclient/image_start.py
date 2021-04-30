# -*- encoding=utf8 -*-

from airtest.core.api import *
from airtest.cli.parser import cli_setup


def get_devices():

    # popen返回文件对象，跟open操作一样
    with os.popen(r'adb devices', 'r') as f:
        text = f.read()
    print(text)  # 打印cmd输出结果

    # 输出结果字符串处理
    s = text.split("\n")  # 切割换行
    result = [x for x in s if x != '']  # 列生成式去掉空
    print(result)

    # 可能有多个手机设备
    devices = []  # 获取设备名称
    for i in result:
        dev = i.split("\tdevice")
        if len(dev) >= 2:
            devices.append(dev[0])

    if not devices:
        print('当前设备未连接上')
    else:
        print('当前连接设备：%s' % devices)
    return devices


def start_record():
    if not cli_setup():
        dvi = get_devices()
        auto_setup(__file__, logdir=False, devices=[
            "Android://127.0.0.1:5037/" + dvi[0] + "?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=ADBTOUCH",
        ])
    touch(Template(r"E:\AirtestIDE_2019-09-11_py3_win64\untitled.air\tpl1601196704168.png",
                   record_pos=(-0.269, -0.053), resolution=(1080, 2248)))


start_record()
