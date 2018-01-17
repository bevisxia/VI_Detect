# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 17:56
# @Author  : zhangxinhe
# @File    : frame_manager.py
import threading

from modules.frame.item import DetectItem
from modules.gate.gate_status import Gate
from modules.gate.gate_status import GateOperationEnum
from managers.queue_manager import QueueManager
from modules.video.process_msg import *
from modules.comm.msg import *

class FrameManager(object):
    def __init__(self, width, height, msg_queue):
        self.__frames = {}
        self.__lock = threading.Lock()
        self.__width = width
        self.__height = height
        self.__detect_item = []
        self.__operation_id = 0
        self.__msg_queue = msg_queue
        self.__gate = Gate.get_instance()
        self.__gate.add_status_observer(GateOperationEnum.GATE_OPEN, self.__on_gate_open)
        self.__gate.add_status_observer(GateOperationEnum.GATE_CLOSE, self.__on_gate_close)

    def add_frame(self, frame):
        with self.__lock:
            operation_id = frame.get_operation_id()
            frame_lst = self.__frames.get(operation_id, [])
            self.__frames[operation_id] = self.__insert_frame(frame, frame_lst)

    def __on_gate_open(self):
        if self.__operation_id > 3:
            self.__operation_id = 0
        else:
            self.__operation_id += 1
        self.__msg_queue.put(GateOpenMsg(self.__operation_id))

    def __on_gate_close(self):
        self.__msg_queue.put(GateCloseMsg(self.__operation_id))
        threading._start_new_thread(self.__begin_parse, ('parse_frame', '111'))

    def __begin_parse(self, name, id):
        self.__parse_frame()
        self.__send_result()

    def __send_result(self):
        msg = MsgFactory.get_msg(MsgCodeEnum.MSG_REPORT_RESULT_REQ)
        msg.set_items(self.__detect_item)
        msg.send()

    def __insert_frame(self, insert_frame, frame_list):
        for i in range(len(frame_list)-1, -1, -1):
            cur_frame = frame_list[i]
            if insert_frame.get_frame_id() < cur_frame.get_frame_id():
                continue
            else:
                frame_list.insert(i+1, insert_frame)
                print "insert frame id: ", insert_frame.get_frame_id()
                break
        else:
            frame_list.insert(0, insert_frame)

        return frame_list

    def __get_all_categories(self, frames):
        categories = []
        for f in frames:
            categories.extend(f.get_item_names())
        return list(set(categories))

    def __add_detect_item(self, item):
        self.__detect_item.append(item)

    def __get_detect_item(self):
        return self.__detect_item

    def print_item(self):
        for item in self.__detect_item:
            print "id: ", item.get_id(), " name: ", item.get_name()

    def __parse_frame(self):
        self.__detect_item = []
        frame_keys = sorted(self.__frames.keys())
        frames = self.__frames.pop(frame_keys[0]) if frame_keys else []

        for category in self.__get_all_categories(frames):
            start_x = start_y = 0
            end_x = end_y = 0
            take_count = 0
            category_id = 0
            for frame in frames:
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

        # print "start (",
        for item in items:
            x_mid = self.__width - item.get_x()
            y_mid = self.__height - item.get_y()
            # print item.get_name(), item.get_score(), x_mid, y_mid
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
        # print ", count: ", count
        # print ") end"
        return count, start_x, start_y, end_x, end_y