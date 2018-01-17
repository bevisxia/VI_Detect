
def coroutine(func):
    def start(*args, **kwargs):
        f = func(*args,**kwargs)
        next(f)
        return f
    return start

def except_caught(func):
    def except_handle(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            print "except_caught: ",e
            return False, None

    return except_handle