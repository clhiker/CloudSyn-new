# -*- coding: utf-8 -*-
import socket
import time
import configparser
import threading

import load

class UdpServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = ()
        self.buff = 1024
        self.client = None

        self.time_out = False
        self.finish = False
        self.begin_signal = False

        # 读取配置文件
        self.readConfig()

        # 绑定地址
        self.server_socket.bind(self.address)


    # 读取配置信息
    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('remote.ini')
        ip = config.get('socket_config', 'ip')
        port = config.get('socket_config', 'udp_port')
        self.address = (ip, int(port))
        self.buff = int(config.get('socket_config', 'buff'))

    # 心跳包接收器
    def heartBeatReceive(self,):
        while True:
            heart_beat, address = self.server_socket.recvfrom(self.buff)
            heart_beat = heart_beat.decode()
            self.begin_signal = True
            if heart_beat == '1':
                self.time_out = False

    # 计时器
    def timeCount(self):
        config = configparser.ConfigParser()
        config.read('remote.ini')
        longest_heart_beat_time_stamp = int(config.get('socket_config', 'longest_heart_beat_time_stamp'))

        old_time = time.time()
        while True:
            new_time = time.time()
            if not self.time_out:
                old_time = time.time()
                self.time_out = True
            if new_time - old_time > longest_heart_beat_time_stamp and self.begin_signal:
                self.finish = True
                return
            time.sleep(0.01)

    def begin(self):
        t1 = threading.Thread(target = self.heartBeatReceive)
        t1.start()
        t2 = threading.Thread(target=self.timeCount)
        t2.start()
        while True:
            if self.finish:
                return True
            time.sleep(0.01)

