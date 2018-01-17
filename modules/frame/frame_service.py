import time
import threading

class FrameService(threading.Thread):

    def __init__(self, frame_manager, detected_queue):
        threading.Thread.__init__(self)
        self.__detected_queue = detected_queue
        self.__frame_manager = frame_manager

    def run(self):
        n = 0
        t = time.time()
        while True:
            frame = self.__detected_queue.get()

            n += 1
            now = time.time()
            if now - t > 1:
                print "detect queue FPS: ", n, " time: ", now - t,
                print " __detected_queue: ", self.__detected_queue.qsize()
                t = now
                n = 0

            self.__frame_manager.add_frame(frame)

