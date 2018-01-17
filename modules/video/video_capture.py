# -*- coding: utf-8 -*-
# @Time    : 2018/1/17 17:18
# @Author  : zhangxinhe
# @File    : video_capture.py
import multiprocessing
import threading
import thread

class VideoCaptureProcess(multiprocessing.Process):
    def __init__(self,in_queue, out_queue):
        super(VideoCaptureProcess, self).__init__()
        self.__in_queue = in_queue
        self.__out_queue = out_queue

