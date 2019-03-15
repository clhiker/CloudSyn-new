import threading
import time
import inspect
import ctypes

import UdpSocket

thread_list = []

# 模拟静态变量（python动态特性）
class FINISH(object):
     finish = False

def _async_raise(tid, exctype):
   tid = ctypes.c_long(tid)
   if not inspect.isclass(exctype):
      exctype = type(exctype)
   res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
   if res == 0:
      raise ValueError("invalid thread id")
   elif res != 1:
      ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
      raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
   _async_raise(thread.ident, SystemExit)

def myTest():
    while True:
        time.sleep(1)

# 主线程
class mainThread(threading.Thread):
    def run(self):
        t3 = threading.Thread(target=myTest)
        t3.start()
        thread_list.append(t3)
        while True:
            time.sleep(1)


# 心跳包线程
class breatThread(threading.Thread):
    def run(self):
        heart_beat = UdpSocket.UdpServer()
        FINISH.finish = heart_beat.begin()

if __name__ == "__main__":
    t1 = mainThread()
    t2 = breatThread()
    t1.start()
    t2.start()

    thread_list.append(t1)
    while not FINISH.finish:
        time.sleep(0.1)
    for item in thread_list:
        stop_thread(item)

    print('stoped')
    exit()


