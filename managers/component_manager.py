# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 18:11
# @Author  : zhangxinhe
# @File    : component_manager.py
from libs.object_detection.utils import label_map_util
#from modules.video.video_parser import VideoParser

class ComponentManager(object):
    __label_map = None
    __categories = None
    __category_index = None

    @classmethod
    def init(cls, label_path, num_classes):
        cls.__label_map = label_map_util.load_labelmap(label_path)
        cls.__categories = label_map_util.convert_label_map_to_categories(cls.__label_map,
                                                                          max_num_classes=num_classes,
                                                                          use_display_name=True)
        cls.__category_index = label_map_util.create_category_index(cls.__categories)

    @classmethod
    def get_label_map(cls):
        return cls.__label_map

    @classmethod
    def get_categories(cls):
        return cls.__categories

    @classmethod
    def get_category_index(cls):
        return cls.__category_index

