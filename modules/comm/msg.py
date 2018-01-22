# -*- coding: utf-8 -*-

import json
import time
from modules.comm.msg_code_define import *
from managers.comm_manager import CommManager
from managers.config_manager import ConfigManager
from modules.gate.gate_status import GateStatusEnum
from modules.frame.item import DetectItem

class Msg(object):
    def __init__(self):
        self._code = None
        self._body = {}

    def get_body(self):
        return json.dumps(self._body)

    def set_body(self, body):
        self._body = body

    def execute(self):
        pass

class EchoRequest(Msg):
    def __init__(self):
        super(EchoRequest, self).__init__()
        self._code = MsgCodeEnum.MSG_ECHO_REQ

class EchoResponse(Msg):
    def __init__(self):
        super(EchoResponse, self).__init__()
        self._code = MsgCodeEnum.MSG_ECHO_RSP
    pass

class RegisterRequest(Msg):
    def __init__(self):
        super(RegisterRequest, self).__init__()
        self._code = MsgCodeEnum.MSG_REGISTER_REQ
        client_key = "SdVI" + str(ConfigManager.get_sources())
        self._body = {'ID':str(self._code), 'ClientKey':client_key}
        print "2. body: ", self._body

    def get_body(self):
        print "body: ", self._body
        return json.dumps(self._body)

class RegisterResponse(Msg):
    def __init__(self):
        super(RegisterResponse, self).__init__()
        self._code = MsgCodeEnum.MSG_REGISTER_RSP

    def execute(self):
        if self._body.get('Status') in ('0', False):
            time.sleep(1)
            add_msg(MsgCodeEnum.MSG_REGISTER_REQ)

class StartDetectRequest(Msg):
    def __init__(self):
        super(StartDetectRequest, self).__init__()
        self._code = MsgCodeEnum.MSG_START_DETECT_REQ

    def execute(self):
        add_msg(MsgCodeEnum.MSG_START_DETECT_RSP, self._body)
        CommManager.set_gate_status(GateStatusEnum.OPEN)

class StartDetectResponse(Msg):
    def __init__(self):
        super(StartDetectResponse, self).__init__()
        self._code = MsgCodeEnum.MSG_START_DETECT_RSP

    def get_body(self):
        return json.dumps(self._body)

    def set_body(self, body):
        self._body = body
        self._body['ID'] = str(self._code)
        self._body['Status'] = '1'

class StopDetectRequest(Msg):
    def __init__(self):
        super(StopDetectRequest, self).__init__()
        self._code = MsgCodeEnum.MSG_STOP_DETECT_REQ

    def execute(self):
        add_msg(MsgCodeEnum.MSG_STOP_DETECT_RSP, self._body)
        CommManager.set_gate_status(GateStatusEnum.CLOSE)

class StopDetectResponse(Msg):
    def __init__(self):
        super(StopDetectResponse, self).__init__()
        self._code = MsgCodeEnum.MSG_STOP_DETECT_RSP

    def set_body(self, body):
        self._body = body
        self._body['ID'] = str(self._code)
        self._body['Status'] = '1'

class ReportResultRequest(Msg):
    def __init__(self):
        super(ReportResultRequest, self).__init__()
        self._code = MsgCodeEnum.MSG_REPORT_RESULT_REQ
        self._detect_item = []

    def set_items(self, item):
        self._detect_item = item

    def set_body(self, body):
        self._body = body

    def get_body(self):
        return json.dumps(self._body)

    def send(self):
        rsp_dict = {}
        rsp_dict['ID'] = str(self._code)
        products = "["
        for item in self._detect_item:
            id = item.get_id()
            name = item.get_name()
            count = item.get_count()
            print "id: ", id, "name: ", name, "count: ", count
            value = "{\"Id\": " + "\"" + str(id) + "\"" + "," + "\"Name\": " + "\"" + name + "\"" + "," + "\"Number\":" + "\"" + str(count) + "\"" + "}"
            #value = "{Name: " + "\"" + item.get_name() + "\"" + "," + "\"Number\":" + str(item.get_count()) + "}"
            products += value
            #products.join(value)
            #products.join(",")
            products += ","
        products1 = products[0:len(products)-1]
        products = products1 + "]"
        #products.join("]")
        print products
        rsp_dict['Products'] = products
        self.set_body(rsp_dict)
        CommManager.get_comm_send_service().send_msg(self.get_body())

class ReportResultResponse(Msg):
    def __init__(self):
        super(ReportResultResponse, self).__init__()
        self._code = MsgCodeEnum.MSG_REPORT_RESULT_RSP
    pass

def add_msg(code, body=None):
    msg = MsgFactory.get_msg(code)
    if body:
        msg.set_body(body)
    CommManager.get_comm_send_service().send_msg(msg.get_body())

class MsgFactory(object):
    __msg_clz_map = {
        MsgCodeEnum.MSG_ECHO_REQ: EchoRequest,
        MsgCodeEnum.MSG_ECHO_RSP: EchoResponse,
        MsgCodeEnum.MSG_REGISTER_REQ: RegisterRequest,
        MsgCodeEnum.MSG_REGISTER_RSP: RegisterResponse,
        MsgCodeEnum.MSG_START_DETECT_REQ: StartDetectRequest,
        MsgCodeEnum.MSG_START_DETECT_RSP: StartDetectResponse,
        MsgCodeEnum.MSG_STOP_DETECT_REQ: StopDetectRequest,
        MsgCodeEnum.MSG_STOP_DETECT_RSP: StopDetectResponse,
        MsgCodeEnum.MSG_REPORT_RESULT_REQ: ReportResultRequest,
        MsgCodeEnum.MSG_REPORT_RESULT_RSP: RegisterResponse
    }

    @classmethod
    def get_msg(cls, code):
        #msg_dict = json.loads(rsp_msg)
        msg_clz = cls.__msg_clz_map.get(int(code), None)
        return msg_clz() if msg_clz else None