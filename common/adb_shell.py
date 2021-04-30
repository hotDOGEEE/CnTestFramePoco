import subprocess
import time


class AdbShell(object):

    def __init__(self, resolution=None):
        """
        :param resolution:  设备屏幕分辨率, 默认2340*1080
        """
        if resolution is None:
            resolution = [2340, 1080]
        self.resolution_x = resolution[0]
        self.resolution_y = resolution[1]

    def tap(self, pos):
        """
        :param pos:  airtest上获取到的pos数据
        :return:
        """
        x, y = int(pos[0] * self.resolution_x), int(pos[1] * self.resolution_y)
        subprocess.call(f'adb shell input tap {x} {y}', shell=True)
        time.sleep(0.6)

    def tap_org(self, pos):
        x, y = pos[0], pos[1]
        subprocess.call(f'adb shell input tap {x} {y}', shell=True)

    def swipe(self, pos1, pos2):
        """

        :param pos1:  原始的pos
        :param pos2:  需要移动到的pos
        :return:
        """
        x1, y1 = int(pos1[0] * self.resolution_x), int(pos1[1] * self.resolution_y)
        x2, y2 = int(pos2[0] * self.resolution_x), int(pos2[1] * self.resolution_y)
        subprocess.call(f'adb shell input swipe {x1} {y1} {x2} {y2} 350', shell=True)
        time.sleep(0.5)

    def screenrecord(self, filename, record_time=None):
        """

        :param filename:  录屏保存文件名
        :param record_time:  录屏时间, 默认180s
        :return:
        """
        if record_time:
            p = subprocess.Popen(r'adb shell screenrecord --time-limit {record_time} /sdcard/{filename}.mp4', shell=True)
            p.kill()
        else:
            p = subprocess.Popen(r'adb shell screenrecord /sdcard/{filename}.mp4', shell=True)
        return p


if __name__ == '__main__':

    m = AdbShell()
    m.swipe([0.73, 0.9], [0.35, 0.7])

