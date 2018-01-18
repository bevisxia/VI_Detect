# -*- coding: utf-8 -*-
# @Time    : 2018/1/17 17:48
# @Author  : zhangxinhe
# @File    : queue_manager.py

from multiprocessing import Queue

class QueueManager(object):
    __origin_frame_queue = None
    __updated_frame_queue = None
    __detected_frame_queue = None
    __msg_queue = None

    @classmethod
    def init(cls, q_size):
        cls.__origin_frame_queue = Queue(q_size)
        cls.__updated_frame_queue = Queue(q_size)
        cls.__detected_frame_queue = Queue(q_size)
        cls.__msg_queue = Queue()

    @classmethod
    def get_origin_frame_queue(cls):
        return cls.__origin_frame_queue

    @classmethod
    def get_updated_frame_queue(cls):
        return cls.__updated_frame_queue

    @classmethod
    def get_detected_frame_queue(cls):
        return cls.__detected_frame_queue

    @classmethod
    def get_msg_queue(cls):
        return cls.__msg_queue

    @classmethod
    def is_round_over(cls):
        return cls.__origin_frame_queue.empty() and cls.__detected_frame_queue.empty()



