# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 16:49
# @Author  : zhangxinhe
# @File    : gate_status.py
import threading

class GateStatusEnum(object):
    OPEN = 0
    CLOSE = 1
    UNKNOW = 999

class GateOperationEnum(object):
    GATE_OPEN = 0
    GATE_CLOSE = 1

class Gate(object):
    _instance = None
    __lock = threading.Lock()
    __last_gate_status = GateStatusEnum.CLOSE
    __cur_gate_status = GateStatusEnum.CLOSE
    __gate_operation_observer = {GateOperationEnum.GATE_OPEN:[],
                                 GateOperationEnum.GATE_CLOSE:[]}

    def __new__(cls, *args, **kwargs):
        if Gate._instance is None:
            Gate._instance = object.__new__(cls, *args, **kwargs)

        return Gate._instance

    @classmethod
    def get_instance(cls):
        with cls.__lock:
            if cls._instance is None:
                cls._instance = Gate()

        return cls._instance

    def init(self):
        pass

    def set_cur_gate_status(self, status):
        if status in (GateStatusEnum.OPEN, GateStatusEnum.CLOSE):
            self.__last_gate_status = self.__cur_gate_status
            self.__cur_gate_status = status
            self.__on_gate_status_changed()

    def get_cur_gate_status(self):
        return self.__cur_gate_status

    def add_status_observer(self, status, callback):
        if status not in self.__gate_operation_observer:
            return False
        else:
            self.__gate_operation_observer[status].append(callback)
            return True

    def remove_status_observer(self, status, callback):
        if status not in self.__gate_operation_observer or \
           callback not in self.__gate_operation_observer[status]:
            return False
        else:
            self.__gate_operation_observer[status].remove(callback)
            return True

    def __on_gate_status_changed(self):
        if self.__last_gate_status == GateStatusEnum.CLOSE and \
           self.__cur_gate_status == GateStatusEnum.OPEN:
            self.__on_gate_operation_begin(GateOperationEnum.GATE_OPEN)
        elif self.__last_gate_status == GateStatusEnum.OPEN and \
             self.__cur_gate_status == GateStatusEnum.CLOSE:
            self.__on_gate_operation_begin(GateOperationEnum.GATE_CLOSE)
        else:
            # wrong status, should log to file and report to admin
            pass

    def __on_gate_operation_begin(self, operation):
        callback_lst = self.__gate_operation_observer.get(operation, [])
        for callback in callback_lst:
            callback()

