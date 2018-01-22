# # -*- coding: utf-8 -*-
# # @Time    : 2018/1/5 17:38
# # @Author  : zhangxinhe
# # @File    : video_parser.py
import cv2
import os
import time
import tensorflow as tf

from managers.config_manager import ConfigManager
from managers.path_manager import PathManager
from modules.frame.frame import Frame
from libs.utils.frame_parser import parse_origin_video_frame
from libs.utils.frame_parser import item_detect
from managers.component_manager import ComponentManager
from multiprocessing import Queue, Pool
# import affinity

# class VideoParserProcess(threading.Thread):
#     def __init__(self, in_queue, detected_queue):
#         threading.Thread.__init__(self)
#         self.__video_name = 'Video' + str(ConfigManager.get_sources())

def worker(input_q, detect_q, update_q):
    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PathManager.get_ckpt_path(), 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    category_index = ComponentManager.get_category_index()
    width = ConfigManager.get_width()
    height = ConfigManager.get_height()

    t = time.time()
    n = 0
    while True:
        operation_id, frame_id, frame = input_q.get()
        # print "operation_id: ", operation_id, "frame_id: ", frame_id
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        now = time.time()
        n += 1
        if now - t > 1:
            print "hand FPS: ", n, " time: ", now - t,
            print " input_q: ", input_q.qsize(), " detect_q: ", detect_q.qsize()
            t = now
            n = 0

        updated_frame, score, classes, boxes = parse_origin_video_frame(frame_rgb,
                                                                        sess,
                                                                        detection_graph,
                                                                        category_index)

        items = item_detect(score, classes, boxes, category_index)
        if items:
            valid_frame = Frame(operation_id, frame_id)
            print "items: ",
            for item in items:
                print frame_id, item.get_id(), item.get_name(), item.get_score(), width - item.get_x(), height - item.get_y(),
                valid_frame.add_item(item)
            print " end"
            detect_q.put(valid_frame)

        # for imshow
        output_rgb = cv2.cvtColor(updated_frame, cv2.COLOR_RGB2BGR)
        update_q.put((frame_id, output_rgb))
        # output_rgb = cv2.cvtColor(updated_frame, cv2.COLOR_RGB2BGR)
        # cv2.imshow("video", output_rgb)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    sess.close()

class VideoParserProcess(object):
    def __init__(self, in_queue, detected_queue, update_queue):
        self.__video_name = 'Video' + str(ConfigManager.get_sources())
        self.__in_queue = in_queue
        self.__detected_queue = detected_queue
        self.__update_queue = update_queue

    def run(self):
        self.__pool = Pool(ConfigManager.get_worker_num(), worker, (self.__in_queue, self.__detected_queue, self.__update_queue))
        # self.__pool = Pool(1, worker, (self.__in_queue, self.__detected_queue, self.__update_queue, 4))

    def destory(self):
        self.__pool.terminate()

# class VideoParserProcess(multiprocessing.Process):
#     def __init__(self, in_queue, detected_queue):
#         super(VideoParserProcess, self).__init__()
#         self.__video_name = 'Video' + str(ConfigManager.get_sources())
