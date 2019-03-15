import struct


class Load:
    def __init__(self, buff):

        self.buff = buff
        self.client = None

    def setClient(self, client):
        self.client = client

    # 发送信息
    def sendInfo(self, text):
        text = text.encode()
        text_length = len(text)
        self.client.send(struct.pack('i', text_length))
        self.client.send(struct.pack(str(text_length) + 's', text))

    # 接收信息
    def receiveInfo(self):

        text_length = self.client.recv(4)
        text_length = struct.unpack('i', text_length)[0]
        text = self.client.recv(text_length)
        text = struct.unpack(str(text_length) + 's', text)
        text = text[0]
        text = text.decode()
        return text
