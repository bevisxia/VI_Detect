import time
import threading
import json
from modules.comm.msg import MsgFactory
from modules.comm.msg_code_define import MsgCodeEnum
from managers.comm_manager import CommManager

class CommRecvService(threading.Thread):

    def __init__(self, thread_name, tcp_client):
        threading.Thread.__init__(self)
        self.__name = thread_name
        self.__tcp_client = tcp_client
        self.__alive = True

    def stop(self):
        self.__alive = False

    def run(self):
        registered = False
        send_service = CommManager.get_comm_send_service()

        while self.__alive:
            if registered == False:
                # send register msg
                send_service.send_msg(MsgFactory.get_msg(MsgCodeEnum.MSG_REGISTER_REQ).get_body())
                registered = True

            flag, msg_buf = self.__tcp_client.recv(512)
            print "recv: ", msg_buf
            if not msg_buf:
                #self.__alive = False
                print "tcp_client try reconnect!"
                self.__tcp_client.reconnect()
                registered = False
                time.sleep(1)
            else:
                # buf end with '\n', we must remove first before parse it
                buf_dict = self.__parse_buf(msg_buf[0:len(msg_buf)])
                if buf_dict:
                    msg = MsgFactory.get_msg(buf_dict.get('ID'))
                    if msg:
                        msg.set_body(buf_dict)
                        msg.execute()
        print "recv process exit"

    def __parse_buf(self, buf):
        try:
            buf_dict = json.loads(buf)
        except ValueError:
            print "invalid msg!"
            return None
        return buf_dict

