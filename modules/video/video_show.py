import cv2
import threading
from managers.config_manager import ConfigManager

class VideoShowProcess(threading.Thread):
    def __init__(self, update_queue):
        threading.Thread.__init__(self)
        self.__update_queue = update_queue
        self.__video_name = 'Video' + str(ConfigManager.get_sources())

    def run(self):
        while True:
            frame_id, frame = self.__update_queue.get()
            output_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imshow(self.__video_name, output_rgb)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break