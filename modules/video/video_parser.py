# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 17:38
# @Author  : zhangxinhe
# @File    : video_parser.py
import sys
import cv2
import time
import tensorflow as tf
import threading
import thread
import multiprocessing
from multiprocessing import Queue, Pool, Process

from managers.config_manager import ConfigManager
from modules.comm.msg import MsgFactory
from modules.comm.msg_code_define import MsgCodeEnum
from managers.path_manager import PathManager
from modules.gate.gate_status import Gate
from modules.gate.gate_status import GateOperationEnum
from modules.frame.frame_manager import FrameManager
from modules.frame.frame import Frame
from libs.utils.frame_parser import parse_origin_video_frame
from libs.utils.frame_parser import item_detect
from libs.utils.app_utils import FPS, WebcamVideoStream
from libs.utils.decorator import coroutine

from managers.component_manager import ComponentManager

class VideoParser(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.__video_name = 'Video' + str(ConfigManager.get_sources())
        self.__queue_size = ConfigManager.get_queue_size()
        self.__input_q = Queue(maxsize=self.__queue_size)
        self.__output_q = Queue(maxsize=self.__queue_size)
        self.__width = ConfigManager.get_width()
        self.__height = ConfigManager.get_height()
        self.__gate = Gate.get_instance()
        self.__gate.add_status_observer(GateOperationEnum.GATE_OPEN, self.__on_gate_begin_open)
        self.__gate.add_status_observer(GateOperationEnum.GATE_CLOSE, self.__on_gate_begin_close)
        # self.__video_stream = WebcamVideoStream(ConfigManager.get_sources(),
        #                                         ConfigManager.get_width(),
        #                                         ConfigManager.get_height()).start()
        # self.__fps = self.__video_stream.stream.get(cv2.CAP_PROP_FPS)
        # self.__expose = self.__video_stream.stream.get(cv2.CAP_PROP_EXPOSURE)
        # print "fps: ", self.__fps
        # print "expose_value: ", self.__expose
        # self.__video_stream.stream.set(cv2.CAP_PROP_EXPOSURE, -6)
        # print "expose_value: ", self.__video_stream.stream.get(cv2.CAP_PROP_EXPOSURE)
        #
        self.__detection_graph = tf.Graph()
        self.__init_session()
        self.__gate_opened = False
        self.__cur_frame_manager = None
        # self.__co_thread = None
        self.__frame_sn = 0

    def __init_session(self):
        with self.__detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PathManager.get_ckpt_path(), 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.__session = tf.Session(graph=self.__detection_graph)

    def __send_result(self, detect_item):
        msg = MsgFactory.get_msg(MsgCodeEnum.MSG_REPORT_RESULT_REQ)
        msg.set_items(detect_item)
        msg.send()

    def __read_frame_thread_handle(self, name, id):
        video_capture = WebcamVideoStream(ConfigManager.get_sources(),
                                          ConfigManager.get_width(),
                                          ConfigManager.get_height()).start()
        fps = FPS().start()

        t = time.time()
        n = 0
        number = 0
        while self.__gate_opened:
            origin_frame = video_capture.read()
            time.sleep(0.1)
            n += 1
            number += 1
            now = time.time()
            if now - t > 1:
                print "read FPS: ", n, " time: ", now - t,
                print " input_q: ", self.__input_q.qsize(), " output_q: ", self.__output_q.qsize(),
                print " max_qsize: ", self.__queue_size
                t = now
                n = 0

            frame_rgb = cv2.cvtColor(origin_frame, cv2.COLOR_BGR2RGB)
            self.__input_q.put(frame_rgb)
            # img_name = "output" + str(number) + ".png"
            # cv2.imwrite(img_name, origin_frame)

            # frame_rgb = cv2.cvtColor(origin_frame, cv2.COLOR_BGR2RGB)
            # category_index = ComponentManager.get_category_index()
            # updated_frame, score, classes, boxes = parse_origin_video_frame(frame_rgb,
            #                                                                 self.__session,
            #                                                                 self.__detection_graph,
            #                                                                 category_index)
            # items = item_detect(score, classes, boxes, category_index)
            # if items:
            #     valid_frame = Frame()
            #     #print "items: ",
            #     for item in items:
            #     #    print item.get_id(), item.get_name(), item.get_score(), self.__width - item.get_x(), self.__height - item.get_y(),
            #         valid_frame.add_item(item)
            #     #print " end"
            #     self.__cur_frame_manager.add_frame(valid_frame)
            #
            # output_rgb = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            # cv2.imshow(self.__video_name, output_rgb)
            #
            # fps.update()
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        fps.stop()
        video_capture.stop()

    def __handle_frame_thread_handle(self, name, id):
        # parse_frame = self.__parse_origin_frame()
        # self.__read_frame(parse_frame)
        t = time.time()
        n = 0
        number = 0
        while True:
            frame = self.__input_q.get()
            n += 1
            number += 1
            now = time.time()
            if now - t > 1:
                print "handle FPS: ", n, " time: ", now - t,
                print " input_q: ", self.__input_q.qsize(), " output_q: ", self.__output_q.qsize(),
                print " max_qsize: ", self.__queue_size
                t = now
                n = 0

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            category_index = ComponentManager.get_category_index()
            updated_frame, score, classes, boxes = parse_origin_video_frame(frame_rgb,
                                                                            self.__session,
                                                                            self.__detection_graph,
                                                                            category_index)
            items = item_detect(score, classes, boxes, category_index)
            if items:
                valid_frame = Frame()
                # print "items: ",
                for item in items:
                    # print item.get_id(), item.get_name(), item.get_score(), self.__width - item.get_x(), self.__height - item.get_y(),
                    valid_frame.add_item(item)
                # print " end"
                self.__cur_frame_manager.add_frame(valid_frame)

            # self.__output_q.put(updated_frame)
            output_rgb = cv2.cvtColor(updated_frame, cv2.COLOR_RGB2BGR)
            cv2.imshow(self.__video_name, output_rgb)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.__cur_frame_manager.parse_frame()
        self.__send_result(self.__cur_frame_manager.get_detect_item())
        self.__cur_frame_manager = None

    def __on_gate_begin_open(self):
        with self.__lock:
            print "gate opened. started a thread!"
            print "width: ", self.__width, " height: ", self.__height
            self.__gate_opened = True
            self.__cur_frame_manager = FrameManager(ConfigManager.get_width(), ConfigManager.get_height())
            self.__frame_sn = 0
        # self.__read_frame_thread = Process(target = self.__read_frame_thread_handle, args = ("read_frame_thread", "1"))
        # self.__handle_frame_thread = Process(target = self.__handle_frame_thread_handle, args = (self.__input_q, self.__output_q))
        self.__read_frame_thread = thread.start_new_thread(self.__read_frame_thread_handle, ("read_frame_thread", "1"))
        self.__handle_frame_thread = thread.start_new_thread(self.__handle_frame_thread_handle, ("handle_frame_thread", "2"))

    def __on_gate_begin_close(self):
        print "gate closed"
        self.__gate_opened = False

    def __read_frame(self, target):
        t = time.time()
        n = 0
        while self.__gate_opened:
            n += 1
            now = time.time()
            if now - t > 1:
                print "hand FPS: ", n, " time: ", now - t,
                print " input_q: ", self.__input_q.qsize(), " output_q: ", self.__output_q.qsize(),
                print " max_qsize: ", self.__queue_size
                t = now
                n = 0
            frame = self.__input_q.get()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            target.send(frame_rgb)
        else:
            target.close()

    @coroutine
    def __parse_origin_frame(self):
        try:
            while True:
                frame = (yield)
                if frame is None:
                    continue

                category_index = ComponentManager.get_category_index()
                updated_frame, score, classes,boxes = parse_origin_video_frame(frame,
                                                                               self.__session,
                                                                               self.__detection_graph,
                                                                               category_index)
                items = item_detect(score, classes, boxes, category_index)
                if items:
                    valid_frame = Frame()
                    # print "items: ",
                    for item in items:
                        # print item.get_id(), item.get_name(), item.get_score(), self.__width - item.get_x(), self.__height - item.get_y(),
                        valid_frame.add_item(item)
                    # print " end"
                    self.__cur_frame_manager.add_frame(valid_frame)

                self.__output_q.put(updated_frame)
        except GeneratorExit:
            with self.__lock:
                self.__cur_frame_manager.parse_frame()
                self.__send_result(self.__cur_frame_manager.get_detect_item())
                self.__cur_frame_manager = None
