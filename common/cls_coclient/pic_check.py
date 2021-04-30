# -*- encoding=utf8 -*-
import aircv as ac
import os
import cv2
import numpy as np
import pathlib
from common import adb_shell

# 调用不复杂，就每次调用截图一张，再去找就行了，需要传入待对比图像地址

file = pathlib.Path(__file__).parent.parent.parent / 'environment'


class Similar(object):

    def __init__(self, pixel_difference=10):
        """
        :return
        """
        self.pixel_difference = pixel_difference

    def _normalize(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (10, 10))
        return image

    def _compute_similar(self, image1, image2):
        image1 = self._normalize(image1)
        image2 = self._normalize(image2)
        image = np.abs(image1 - image2)
        res = np.where(image > 10, 0, 1)
        return np.sum(res)

    def __call__(self, image1, image2):
        if isinstance(image1, str):
            image1 = cv2.imread(image1)
        if isinstance(image2, str):
            image2 = cv2.imread(image2)
        if not isinstance(image1, np.ndarray) or not isinstance(image2, np.ndarray):
            raise ValueError("The image must be ndarray!")
        if int(self._compute_similar(image1, image2)) == 100:
            return False
        else:
            return True


def tmpl_test(target_img=str(file)+r'\target1.png'):
    al = adb_shell.AdbShell()
    os.system(r'adb shell screencap -p /sdcard/screen.png')
    os.system(r'adb pull /sdcard/screen.png ' + str(file))
    t1 = ac.imread(str(file)+r'\screen.png')
    t2 = ac.imread(target_img)
    try:
        pos = ac.find_template(t1, t2)['result']
        al.tap_org(pos)
    except Exception as e:
        print(e)


if __name__ == '__main__':

    Similar = Similar()
    print(Similar.__call__(r'E:\untitled\source1.png', r'E:\untitled\source2.png'))
