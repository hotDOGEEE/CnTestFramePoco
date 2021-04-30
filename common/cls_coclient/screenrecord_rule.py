# -*- encoding=utf8 -*-

import subprocess
import time
import os
import pathlib
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


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


def at():
    ScreenRecordRule().abnormal_termination()


class ScreenRecordRule(object):

    def __init__(self):
        self.poco = AndroidUiautomationPoco(use_airtest_input=False, screenshot_each_action=False)

    def app_start(self):
        """
        启动录屏软件到出现悬浮窗的方法，这个之前都是手动起的，其实也可以设置成每次运行时自动打开的过程
        :return:
        """
        os.system(r'adb shell am force-stop com.kimcy929.screenrecorder')
        os.system(r'adb shell am start -W -n com.kimcy929.screenrecorder/com.kimcy929.screenrecorder.activity.MainActivity')
        self.poco("com.kimcy929.screenrecorder:id/fab").click()

    def stop_record(self):
        os.system(r'adb shell service call statusbar 2')
        self.poco("com.kimcy929.screenrecorder:id/btnStopRecording").click()

    def comparison(self):
        """
        对比图片的，等怀彪有了方法调用

        :return:
        """

    def abnormal_termination(self):
        """
        检测到游戏闪退，进程不在了的情况下终止录屏
        :return:
        """
        srr = ScreenRecordRule()

        def _active_listen():
            while True:
                a = subprocess.call(r'adb shell ps|findstr autochess', shell=True)
                if a == 0:
                    time.sleep(1)
                elif a == 1:
                    break

        _active_listen()
        print('游戏进程未存活')
        srr.stop_record()
        srr.get_video_after()

    def complate_game(self, state):
        """
        自然对局结束停止录屏
        :return:
        """
        srr = ScreenRecordRule()
        if state == 1 or state == 2:
            srr.stop_record()
            image_start = pathlib.Path(__file__).parent.parent.parent / "common/cls_coclient/image_start.py"
            os.system(str(image_start))
            srr.get_video_after()

    def get_video_after(self):
        """
        当点击停止按钮，我们拿到了一个录制完毕的视频，应该去做些什么

        这里划分下来，应该分为：对视频的拷贝 删除 到ai算法的调用

        逻辑代码：
        获取录屏目录下所有文件
        将文件全部考入log_data中的screenrecord下面进行保存
        保存完毕后调用白块检测方法，检测视频中的UI异常信息情况
        删除手机中原本储存的录屏文件（手机的存储空间还挺精贵的。。。）
        :return:
        """

        file_in = pathlib.Path(__file__).parent.parent.parent / 'log_datas/screenrecord'
        print(file_in)
        with os.popen(r'adb shell ls /sdcard/Screenrecord', 'r') as f:
            text = f.read().splitlines()
        print(text)  # 打印cmd输出结果
        os.system(r'adb pull /sdcard/Screenrecord/' + text[-1] + ' ' + str(file_in))
        os.system(r'adb shell rm /sdcard/Screenrecord/' + text[0])
        return True


if __name__ == '__main__':

    sr = ScreenRecordRule()
    sr.get_video_after()

