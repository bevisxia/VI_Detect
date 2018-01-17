# -*- coding: utf-8 -*-
# @Time    : 2018/1/17 17:18
# @Author  : zhangxinhe
# @File    : video_capture.py
import time
import cv2
import multiprocessing
import threading
import thread
from modules.video.process_msg import MsgCode
from libs.utils.app_utils import FPS, WebcamVideoStream
from managers.config_manager import ConfigManager

class VideoCaptureProcess(multiprocessing.Process):
    def __init__(self,in_queue, out_queue, msg_queue):
        super(VideoCaptureProcess, self).__init__()
        self.__in_queue = in_queue
        self.__out_queue = out_queue
        self.__msg_queue = msg_queue
        self.__updated_frame_lst = []
        self.__frame_id = 0
        self.__operation_id = 0
        self.__gate_open = False

    def __insert_to_frame_lst(self, updated_frame):
        pass

    def __handle_pci_msg(self, msg):
        code = msg.get_code()
        if code == MsgCode.CODE_GATE_OPEN:
            self.__gate_open = True
            self.__frame_id = 0
            self.__operation_id = msg.get_args('operation_id')
        elif code == MsgCode.CODE_GATE_CLOSE:
            self.__gate_open = False

    def __recv_msg_from_main(self):
        while True:
            msg = self.__msg_queue.get()
            self.__handle_pci_msg(msg)

    def __get_out_queue(self):
        while True:
            updated_frame = self.__out_queue.get()
            self.__insert_to_frame_lst(updated_frame)


    def __get_im_frame(self):
        pass

    def run(self):
        thread.start_new_thread(self.__recv_msg_from_main,("recv_main_process", "11"))
        # thread.start_new_thread(self.__get_out_queue,("get_out_queue", "11"))

        video_capture = WebcamVideoStream(ConfigManager.get_sources(),
                                          ConfigManager.get_width(),
                                          ConfigManager.get_height()).start()
        fps = FPS().start()
        while True:
            if self.__gate_open:
                origin_frame = video_capture.read()
                time.sleep(0.1)
                # n += 1
                now = time.time()
                # if now - t > 1:
                #     print "read FPS: ", n, " time: ", now - t,
                #     print " input_q: ", self.__input_q.qsize(), " output_q: ", self.__output_q.qsize(),
                #     print " max_qsize: ", self.__queue_size
                #     t = now
                #     n = 0

                frame_rgb = cv2.cvtColor(origin_frame, cv2.COLOR_BGR2RGB)
                self.__in_queue.put((self.__operation_id, self.__frame_id, frame_rgb))
                self.__frame_id += 1
            else:
                time.sleep(0.1)

                # updated_frame = self.__get_im_frame()



