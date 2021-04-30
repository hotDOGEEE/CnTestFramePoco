#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-09-01 11:29:16
# @Author : Huai Biao Zhang
# @Site : longyuan
# @File : findcolorblock.py
# @Software: Hifive

from cv2 import cv2
import numpy as np
import os
from abc import ABC, abstractmethod
import multiprocessing
from multiprocessing import Process, Value
from threading import Thread, Event
from PIL import Image

"""
检查opencv版本
"""
version = [int(v) for v in cv2.__version__.split('.')]
version_ = [4, 0, 0]
for i, v in enumerate(version):
    if version[i] < version_[i]:
        raise EnvironmentError("opencv version must >= 4.0.0!")


class FindColorBlock(ABC):

    def __init__(self, bgr_rate, area_limit):
        self.bgr_rate = bgr_rate
        self.area_limit = area_limit
        self.image = None
        self.gray = None

    @abstractmethod
    def _img2gray(self):
        """
        初始化gray
        """
        pass

    def _find_contours(self):
        # 从黑白图中寻找色块
        if self.gray is None:
            print("must init gray first!")
            return
        self.contours = []
        contours = cv2.findContours(self.gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        for contour in contours:
            if self._screen_contour(contour):
                self.contours.append(contour)

    def _screen_contour(self, contour: list) -> bool:
        """
        筛选色块
        :param contour: 色块
        :return : 通过True 不通过False
        """
        contour_area = cv2.contourArea(contour)
        if contour_area > self.area_limit:
            # 色块面积大于最小面积
            return True
        return False

    def draw_contours(self, color=(0, 0, 255), thickness=3):
        """
        绘制色块边框
        :param color: 边框颜色
        :param thickness: 边框粗细
        :return :
        """
        img = self.image.copy()
        return cv2.drawContours(img, self.contours, -1, color=color, thickness=thickness)

    def show(self, color=(0, 0, 255), thickness=3):
        """
        显示结果
        :param color: 边框颜色
        :param thickness: 边框粗细
        :return :
        """
        cv2.imshow("Color Block", self.draw_contours(color=color, thickness=thickness))
        cv2.waitKey()
        cv2.destroyWindow("Color Block")

    def save_result(self, savepath: str, color=(0, 0, 255), thickness=3):
        """
        保存结果
        :param savepath: 保存路径
        :param color: 边框颜色
        :param thickness: 边框粗细
        :return :
        """
        if not savepath:
            print("savepath is null, will not save!")
            return
        dirname = os.path.dirname(savepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        cv2.imwrite(savepath, self.draw_contours(color=color, thickness=thickness))

    def __call__(self, image, save=False, savepath="", color=(0, 0, 255), thickness=2) -> bool:
        """
        查找色块
        :param image: 图片路径 or 已经读取的图片array
        :param save: 是否保存检测结果, 如果检测到色块则保存，未检测到不保存
        :param savepath: 保存路径
        :param color: 边框颜色
        :param thickness: 边框粗细
        :return : 发现色块True 未发现 False
        """
        if isinstance(image, str):
            if not os.path.isfile(image):
                raise FileNotFoundError(f"Image {image} not exists!")
            image = Image.open(image)
            image = np.array(image)
            self.image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if isinstance(image, np.ndarray):
            self.image = image
        if self.image is None:
            raise TypeError(f"Image type error! current image type is {type(image)}")
        self._img2gray()
        self._find_contours()
        if len(self.contours) == 0:
            return False
        if save:
            self.save_result(savepath, color=color, thickness=thickness)
        return True


class FindPurpleBlock(FindColorBlock):

    def __init__(self, bgr_rate=(210, 40, 210), area_limit=20):
        super(FindPurpleBlock, self).__init__(bgr_rate, area_limit)

    def _img2gray(self):
        b, g, r = cv2.split(self.image)
        b = np.where(b >= self.bgr_rate[0], 1, 0)
        g = np.where(g <= self.bgr_rate[1], 1, 0)
        r = np.where(r >= self.bgr_rate[2], 1, 0)
        gray = b + g + r
        self.gray = np.where(gray == 3, 255, 0).astype(np.uint8)


class FindWhiteBlock(FindColorBlock):

    def __init__(self, bgr_rate=(255, 255, 255), simliar_rate=0.8, hw_rate=0.4, circumference_limit=10, area_limit=20):
        """
        :param bgr_rate: 接近纯白色的程度 255为纯白色
        :param simliar_rate: 检测白块接近矩形的程度
        :param hw_rate: 白块偏离正方形的程度
        :param circumference_limit: 白块最小周长限制
        :param area_limit: 白块最小面积限制
        :return
        """
        assert 0 < simliar_rate <= 1
        self.simliar_rate = simliar_rate
        self.hw_rate = hw_rate
        self.circumference_limit = circumference_limit
        super(FindWhiteBlock, self).__init__(bgr_rate, area_limit)

    def _img2gray(self):
        b, g, r = cv2.split(self.image)
        b = np.where(b >= self.bgr_rate[0], 1, 0)
        g = np.where(g >= self.bgr_rate[1], 1, 0)
        r = np.where(r >= self.bgr_rate[2], 1, 0)
        gray = b + g + r
        self.gray = np.where(gray == 3, 255, 0).astype(np.uint8)

    def _screen_contour(self, contour):
        # 筛选符合要求的白块
        if (contour.shape[0] < self.circumference_limit):
            return False
        width = np.max(contour[:, :, 0]) - np.min(contour[:, :, 0])
        height = np.max(contour[:, :, 1]) - np.min(contour[:, :, 1])
        max, min = (width, height) if width > height else (height, width)
        if min / max < self.hw_rate:
            return False
        block_area = width * height
        contour_area = cv2.contourArea(contour)
        if contour_area < self.area_limit:
            return False
        try:
            slimier = cv2.contourArea(contour) / block_area
        except ZeroDivisionError:
            return False
        if slimier > self.simliar_rate:
            return True
        return False


def _printProcess(frame_count, count, detect_stop):
    while not detect_stop.is_set():
        print("\r进度:{:.2f}%".format(count.value / frame_count * 100), end="")
        if count.value >= frame_count:
            print("\r检测完成\t\t")
            detect_stop.set()
            break


def _createWaterMark(image, current_frame, msec, frame_count):
    time = msec // 1000
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    return cv2.putText(image,
                       f"{int(h)}:{int(m)}:{int(s)} {int(frame_count)}/{current_frame}",
                       (10, 30),
                       cv2.FONT_HERSHEY_COMPLEX,
                       1,
                       (255, 255, 255))


def _findVideo(videopath, detector, savepath, frame_start, frame_stop, count, block_count):
    video = cv2.VideoCapture(videopath)
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    while True:
        if frame_start > frame_stop:
            break
        succ, frame = video.read()
        if succ:
            with count.get_lock():
                count.value += 1
            if detector(frame):
                with block_count.get_lock():
                    block_count.value += 1
                image = detector.draw_contours()
                msec = video.get(cv2.CAP_PROP_POS_MSEC)
                image = _createWaterMark(image, i, msec, frame_count)
                cv2.imwrite(f"{savepath}/{frame_start}.jpg", image)
        else:
            break
        frame_start += 1
    if frame_start <= frame_stop:
        print(f"->警告:获取第{frame_start}帧视频失败！")
    video.release()


def findVideo(videopath, detector, savepath, block_videopath=""):
    return findVideoMultProcessing(videopath, detector, savepath, block_videopath="", process_count=1)


def findVideoMultProcessing(videopath, detector, savepath, block_videopath="", process_count=0):
    """
    多进程视频检测
    :param videopath: 视频路径
    :param detector: 检测器
    :param savepath: 检测到色块帧保存路径
    :param block_videopath: (仅支持avi格式)色块视频保存地址, 默认地址为视频同路径视频名后加_block, avi格式
    :param process_count: 进程数量，<=0 则进程数量与cpu数量相同
    :return :
    """
    os.makedirs(savepath, exist_ok=True)
    count = Value('i', 0)  # 用于统计已检测帧数目，以显示进度
    block_count = Value('i', 0)  # 用于统计检测到的色块
    detect_stop = Event()
    video = cv2.VideoCapture(videopath)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video.release()
    if process_count <= 0:
        process_count = multiprocessing.cpu_count()
    else:
        process_count = min(multiprocessing.cpu_count(), process_count)
    if frame_count < 1000:
        # 小于1000帧不开启多进程
        process_count = 1
    processes = []
    step = int(frame_count // process_count)
    tp = Thread(target=_printProcess, args=(frame_count, count, detect_stop), daemon=True)
    tp.start()
    for i in range(process_count):
        frame_start = i * step
        frame_stop = frame_start + step - 1
        if i == process_count - 1:
            frame_stop = frame_count - 1
        processes.append(Process(target=_findVideo,
                                 args=(videopath, detector, savepath, frame_start, frame_stop, count, block_count),
                                 daemon=True))
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    if not detect_stop.is_set():
        detect_stop.set()
        print(f"\n警告：共有{frame_count - count.value}帧检测失败！")

    if 0 == block_count.value:
        print("未检测到色块")
        return block_count

    print("生成视频")
    if block_videopath == "":
        videoname = os.path.basename(videopath).split('.')[0]
        basedir = os.path.dirname(videopath)
        block_videopath = os.path.join(basedir, f"{videoname}_block.avi")
    else:
        _block_videopath = block_videopath.split('.')
        if len(_block_videopath) == 1:
            _block_videopath.append('.avi')
        if _block_videopath[-1] != 'avi':
            print("视频格式不支持，保存为avi格式！")
            _block_videopath.pop()
            _block_videopath.append('.avi')
        block_videopath = ".".join(_block_videopath) + '.avi'
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video_write = cv2.VideoWriter(block_videopath, fourcc, fps, size)
    images = os.listdir(savepath)
    images = sorted(images, key=lambda filename: int(filename.split('.')[0]))
    for filename in images:
        image = cv2.imread(os.path.join(savepath, filename))
        video_write.write(image)
    return block_count.value

def run(videopath,result_path):
    detector = FindWhiteBlock()
    findVideoMultProcessing(videopath, detector, result_path)


if __name__ == "__main__":
    # 查找紫块并显示结果
    find_purple_block = FindPurpleBlock()
    if find_purple_block("test.png"):
        find_purple_block.show()

    # 查找白块并保存结果
    find_white_block = FindWhiteBlock()
    find_white_block("test.png", save=True, savepath="result.jpg", color=(255, 255, 0), thickness=2)

    # 查找白块并保存结果
    find_white_block = FindWhiteBlock()
    if find_white_block("test.png"):
        find_white_block.save_result("result.jpg")

    # 从numpy array 中查找
    image = cv2.imread("test.png")
    find_purple_block = FindPurpleBlock()
    if find_purple_block(image):
        find_purple_block.show()

    # 视频检测多进程
    videopath = "C:/Users/longyuan/Desktop/SVID_20200902_153449_1.mp4"
    detector = FindWhiteBlock()
    findVideoMultProcessing(videopath, detector, "white")

    # 视频检测单进程
    videopath = "C:/Users/longyuan/Desktop/SVID_20200902_153449_1.mp4"
    detector = FindWhiteBlock()
    findVideoMultProcessing(videopath, detector, "white")
