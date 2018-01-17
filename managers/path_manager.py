# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 15:45
# @Author  : zhangxinhe
# @File    : path_manager.py
import os

class PathManager(object):
    __root_path = ''
    __py_path = ''
    __tf_path = ''
    __slim_path = ''
    __ckpt_path = ''
    __label_path = ''

    @classmethod
    def init(cls, root_path, model_name):
        cls.__root_path = root_path
        cls.__py_path = os.path.join(cls.__root_path, 'libs')
        cls.__tf_path = os.path.join(cls.__root_path, 'libs')
        cls.__slim_path = os.path.join(cls.__root_path, 'libs', 'slim')
        cls.__ckpt_path = os.path.join(cls.__root_path, 'sd_model', model_name, 'frozen_inference_graph.pb')
        cls.__label_path = os.path.join(cls.__root_path, 'sd_model', model_name, 'pascal_label_map.pbtxt')

    @classmethod
    def get_python_path(cls):
        return cls.__py_path

    @classmethod
    def get_tf_path(cls):
        return cls.__tf_path

    @classmethod
    def get_slim_path(cls):
        return cls.__slim_path

    @classmethod
    def get_ckpt_path(cls):
        return cls.__ckpt_path

    @classmethod
    def get_label_path(cls):
        return cls.__label_path