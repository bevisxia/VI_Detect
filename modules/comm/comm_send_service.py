import threading
import time
from Queue import Queue

class CommSendService(threading.Thread):

    def __init__(self, thread_name, tcp_client):
        threading.Thread.__init__(self)
        self.__name = thread_name
        self.__tcp_client = tcp_client
        self.__alive = True
        self.__msg_queue = Queue(5)

    def stop(self):
        self.__alive = False

    def send_msg(self, msg):
        #msg must end with '\n'
        msg_buf = msg + '\n'
        print "send_msg: ", msg_buf
        self.__msg_queue.put(msg_buf)

    def run(self):
        while self.__alive:
            msg = self.__msg_queue.get()
            if msg:
                flag = self.__tcp_client.send(msg)





