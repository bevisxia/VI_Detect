import time
import threading
import json
from modules.comm.msg import MsgFactory

class FrameService(threading.Thread):

    def __init__(self, frame_manager, detected_queue):
        threading.Thread.__init__(self)
        self.__detected_queue = detected_queue
        self.__frame_manager = frame_manager


    def run(self):
        while True:
            frame = self.__detected_queue.get()
            self.__frame_manager.add_frame(frame)

