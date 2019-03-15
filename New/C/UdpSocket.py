#!/usr/bin/python
# encoding=utf-8

import socket
import configparser
import time

# 客户端
class UdpClient:
    def __init__(self):
        self.address = ()
        self.buff = 1024
        self.getConfig()
        # 连接选项
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.connect(self.address)


    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'udp_port'))
        self.address = (ip, port)

        self.buff = int(config.get('spilt', 'buff'))


    def sendHeartBeatPackage(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
        heart_beat_time_stamp = int(config.get('config', 'heart_beat_time_stamp'))

        old_time = time.time()
        while True:
            new_time = time.time()
            if new_time - old_time > heart_beat_time_stamp:
                self.client_socket.send('1'.encode())
                old_time = time.time()
            time.sleep(0.1)

if __name__ == '__main__':
    UdpClient().sendHeartBeatPackage()