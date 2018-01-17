import time

"""
This file is just for function test, ignore it!
"""

def g1(n, target):
    while n > 0:
        target.send(n)
        n -= 1
    print 'g1 stopped'
    target.close()

def g2(target):
    try:
        while True:
            rsp = yield
            # time.sleep(5)
            print 'g2 result is %s'%rsp
            target.send(rsp)
    except GeneratorExit:
        print  'g2 stopped'
        target.close()

def g3():
    try:
        while True:
            result = yield
            # time.sleep(1)
            print 'g3 result is %s'%result
    except GeneratorExit:
        print 'g3 stopped'


if __name__ == '__main__':
    f3 = g3()
    next(f3)
    f2 = g2(f3)
    next(f2)
    f1 = g1(10000,f2)

