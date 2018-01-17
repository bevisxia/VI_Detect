class MsgCode:
    CODE_GATE_OPEN = 0
    CODE_GATE_CLOSE = 1
    CODE_EXIT = 999

class ProcessMsg(object):
    def __init__(self):
        self._msg_code = None
        self._kargs = {}

    def get_code(self):
        return self._msg_code

    def get_args(self, key=None):
        return self._kargs.get(key, None) if key else self._kargs

class GateOpenMsg(ProcessMsg):
    def __init__(self, operation_id):
        super(GateOpenMsg, self).__init__()
        self._msg_code = MsgCode.CODE_GATE_OPEN
        self._kargs = {'operation_id': operation_id}

class GateCloseMsg(ProcessMsg):
    def __init__(self, operation_id):
        super(GateCloseMsg, self).__init__()
        self._msg_code = MsgCode.CODE_GATE_CLOSE
        self._kargs = {'operation_id': operation_id}
