# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 16:00
# @Author  : zhangxinhe
# @File    : config_manager.py

class ConfigManager(object):
    __model_name = ''
    __num_classes = 0
    __queue_size = 0
    __width = 0
    __height = 0
    __workers = 0
    __sources = ''

    @classmethod
    def init(cls, args):
        cls.__model_name = args.model
        cls.__num_classes = args.classnum
        cls.__queue_size = args.queue_size
        cls.__width = args.width
        cls.__height = args.height
        cls.__workers = args.num_workers
        print "num workers: ", cls.__workers
        cls.__sources = args.video_source

    @classmethod
    def get_model_name(cls):
        return cls.__model_name

    @classmethod
    def get_num_classes(cls):
        return cls.__num_classes

    @classmethod
    def get_queue_size(cls):
        return cls.__queue_size

    @classmethod
    def get_width(cls):
        return cls.__width

    @classmethod
    def get_height(cls):
        return cls.__height

    @classmethod
    def get_worker_num(cls):
        return cls.__workers

    @classmethod
    def get_sources(cls):
        return cls.__sources