# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 17:56
# @Author  : zhangxinhe
# @File    : frame_manager.py
import threading

from modules.frame.item import DetectItem

class FrameManager(object):
    def __init__(self, width, height):
        self.__frames = []
        self.__frame_id = 0
        self.__lock = threading.Lock()
        self.__width = width
        self.__height = height
        self.__detect_item = []

    def add_frame(self, frame):
        with self.__lock:
            frame.set_frame_id(self.__frame_id)
            self.__frame_id += 1
            self.__frames.append(frame)

    def __get_all_categories(self):
        categories = []
        for f in self.__frames:
            categories.extend(f.get_item_names())
        return list(set(categories))

    def __add_detect_item(self, item):
        self.__detect_item.append(item)

    def get_detect_item(self):
        return self.__detect_item

    def print_item(self):
        for item in self.__detect_item:
            print "id: ", item.get_id(), " name: ", item.get_name()

    def parse_frame(self):
        for category in self.__get_all_categories():
            start_x = start_y = 0
            end_x = end_y = 0
            take_count = 0
            category_id = 0
            for frame in self.__frames:
                items = frame.get_items_by_name(category)
                if category_id == 0:
                    category_id = 0
                count, start_x, start_y, end_x, end_y = self.__handle_item(items, start_x, start_y, end_x, end_y)
                if count == 1:
                    take_count += 1

            if start_x > self.__width/2:
                print category, " was not taked from inside!"
            else:
                if end_x > start_x:
                    if  end_x - start_x > self.__width/4:
                        print category, " has been taked!"
                        take_count += 1
                    else:
                        print category, " taked but put back!"
                else :
                    print category, " taked but put back!"
            if take_count > 0:
                print take_count, " ", category, " has been taked!"
                # add detect item
                detect_item = DetectItem(category_id, category, take_count)
                self.__add_detect_item(detect_item)

    def __handle_item(self, items, start_x, start_y, end_x, end_y):
        count = 0

        #print "start (",
        for item in items:
            x_mid = self.__width - item.get_x()
            y_mid = self.__height - item.get_y()
            print item.get_name(), item.get_score(), x_mid, y_mid
            if (start_x == 0) & (start_y == 0):
                start_x = x_mid
                start_y = y_mid
            else:
                # taked an other one
                if (x_mid < end_x) & (end_x - x_mid > self.__width / 3):
                    print item.get_name(), "has been taked one"
                    start_x = x_mid
                    start_y = y_mid
                    count += 1
                end_x = x_mid
                end_y = y_mid
        #print ", count: ", count
        #print ") end"
        return count, start_x, start_y, end_x, end_y