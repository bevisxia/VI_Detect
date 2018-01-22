# -*- coding: utf-8 -*-
# @Time    : 2018/1/5 15:27
# @Author  : zhangxinhe
# @File    : project.py
import os
import signal
import time
# import cv2
import argparse
import multiprocessing
from multiprocessing import Queue, Pool
# from libs.utils.app_utils import FPS, WebcamVideoStream
from managers.path_manager import PathManager
from managers.config_manager import ConfigManager
from managers.component_manager import ComponentManager
from managers.queue_manager import QueueManager
from managers.comm_manager import CommManager
from modules.video.video_parser import VideoParserProcess
# from modules.comm.msg import MsgFactory
# from modules.comm.msg_code_define import MsgCodeEnum
from modules.comm.comm_recv_service import CommRecvService
from modules.frame.frame_manager import FrameManager
from modules.frame.frame_service import FrameService
from modules.video.video_capture import VideoCaptureProcess
from modules.video.video_parser import VideoParserProcess
from modules.video.video_show import VideoShowProcess
import thread
# import affinity
# import psutil

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cn', '--classnum', dest='classnum', type=int,
                        default=90, help='Classes num of the model.')
    parser.add_argument('-model', '--model', dest='model', type=str,
                        default='ssd_mobilenet_v1_coco_11_06_2017', help='the model name you want to run.')
    parser.add_argument('-src', '--source', dest='video_source', type=int,
                        default=0, help='Device index of the camera.')
    parser.add_argument('-wd', '--width', dest='width', type=int,
                        default=480, help='Width of the frames in the video stream.')
    parser.add_argument('-ht', '--height', dest='height', type=int,
                        default=360, help='Height of the frames in the video stream.')
    parser.add_argument('-num-w', '--num-workers', dest='num_workers', type=int,
                        default=2, help='Number of workers.')
    parser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
                        default=5, help='Size of the queue.')
    return parser.parse_args()

def init_project():
    root_path = os.getcwd()
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)

    ConfigManager.init(_parse_args())
    PathManager.init(root_path, ConfigManager.get_model_name())
    ComponentManager.init(PathManager.get_label_path(), ConfigManager.get_num_classes())
    CommManager.init()
    QueueManager.init(ConfigManager.get_queue_size())

    global frame_manager
    frame_manager = FrameManager(ConfigManager.get_width(),
                                 ConfigManager.get_height(),
                                 QueueManager.get_msg_queue())

def start_main():
    CommManager.start()
    comm_recv_thread = CommRecvService('comm_recv_service', CommManager.get_tcp_client())
    comm_recv_thread.start()

    # start frame_manager service
    global frame_manager
    frame_service = FrameService(frame_manager, QueueManager.get_detected_frame_queue())
    frame_service.start()

    # start video parser process pool
    # video_parser = VideoParserProcess(QueueManager.get_origin_frame_queue(),
    #                                   QueueManager.get_detected_frame_queue())
    # video_parser.start()
    video_parser = VideoParserProcess(QueueManager.get_origin_frame_queue(),
                                      QueueManager.get_detected_frame_queue(),
                                      QueueManager.get_updated_frame_queue())
    video_parser.run()

    # start video show thread
    # video_show = VideoShowProcess(QueueManager.get_updated_frame_queue())
    # video_show.start()

    # set affinity
    # p = psutil.Process()
    # pro_info = p.as_dict(attrs=['pid', 'name', 'username'])
    # print psutil.cpu_count()
    # print "pid: ", os.getpid()
    # affinity.set_process_affinity_mask(os.getpid(),2L)
    # print "run on cpu", affinity.get_process_affinity_mask(os.getpid())

    # start video capture
    video_capture = VideoCaptureProcess(QueueManager.get_origin_frame_queue(),
                        QueueManager.get_updated_frame_queue(),
                        QueueManager.get_msg_queue())
    # video_capture.start()
    video_capture.run()

def clear_project():
    CommManager.stop()

frame_manager = None
if __name__ == '__main__':
    init_project()
    start_main()
    clear_project()