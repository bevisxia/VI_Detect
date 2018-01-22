import cv2
import multiprocessing
import time
from managers.config_manager import ConfigManager

class VideoShowProcess(multiprocessing.Process):
    def __init__(self, update_queue):
        super(VideoShowProcess, self).__init__()
        self.__update_queue = update_queue
        self.__video_name = 'Video' + str(ConfigManager.get_sources())

    def run(self):
        # file = open("/home/tensorflow/VI_Detect/frame_id.txt", "w")
        while True:
            time.sleep(0.1)
            frame_id, frame = self.__update_queue.get()
            # filename = "/home/tensorflow/VI_Detect/" + str(frame_id) + ".jpg"

            # cv2.imwrite(str(frame_id), frame)
            # print >> file, str(frame_id)
            #
            cv2.imshow(self.__video_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # params = []
            # params.append(cv.CV_IMWRITE_PXM_BINARY)
            # params.append(1)
            # cv2.imwrite(filename, frame)