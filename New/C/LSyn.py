import threading

import UdpSocket


def  sendHeartBeat():
    heart_beat = UdpSocket.UdpClient()
    heart_beat.sendHeartBeatPackage()

t1 = threading.Thread(target=sendHeartBeat)
t1.start()


