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
from managers.comm_manager import CommManager
from modules.video.video_parser import VideoParser
from modules.comm.msg import MsgFactory
from modules.comm.msg_code_define import MsgCodeEnum
from modules.comm.comm_recv_service import CommRecvService

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

    video_parser = VideoParser()

def start_main():
    CommManager.start()
    comm_recv_thread = CommRecvService('comm_recv_service', CommManager.get_tcp_client())
    comm_recv_thread.start()

    # send register msg
    send_service = CommManager.get_comm_send_service()
    send_service.send_msg(MsgFactory.get_msg(MsgCodeEnum.MSG_REGISTER_REQ).get_body())

    while True:
        time.sleep(0.2)

def clear_project():
    CommManager.stop()

if __name__ == '__main__':
    init_project()
    start_main()
    clear_project()