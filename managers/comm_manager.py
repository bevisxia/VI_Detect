from modules.comm.tcp_client import TcpClient
#from modules.comm.comm_recv_service import CommRecvService
from modules.comm.comm_send_service import CommSendService
from modules.gate.gate_status import Gate

class CommManager(object):
    __tcp_client = None
    #__comm_recv_thread = None
    __comm_send_thread = None
    __gate = None
    __addr = '127.0.0.1'
    __port = 18501

    @classmethod
    def init(cls):
        cls.__tcp_client = TcpClient(cls.__addr, cls.__port)
        #cls.__comm_recv_thread = CommRecvService('comm_recv_service', cls.__tcp_client)
        cls.__comm_send_thread = CommSendService('comm_send_service', cls.__tcp_client)
        cls.__gate = Gate.get_instance()

    @classmethod
    def start(cls):
        cls.__tcp_client.connect()
        #cls.__comm_recv_thread.start()
        cls.__comm_send_thread.start()

    @classmethod
    def stop(cls):
        #cls.__comm_recv_thread.stop()
        cls.__comm_send_thread.stop()

    @classmethod
    def get_tcp_client(cls):
        return cls.__tcp_client

    @classmethod
    def get_gate(cls):
        return cls.__gate

    #@classmethod
    #def get_comm_recv_service(cls):
    #    return cls.__comm_recv_thread

    @classmethod
    def get_comm_send_service(cls):
        return cls.__comm_send_thread

    @classmethod
    def set_gate_status(cls, status):
        cls.__gate.set_cur_gate_status(status)