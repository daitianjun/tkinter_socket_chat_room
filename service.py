import json
import socket
import threading

class Service:
    sockets = []
    namelist = []
    lock = threading.Lock()
    def __init__(self, ip='0.0.0.0', port=8888):
        self.ip = ip
        self.port = port
        self.create()

    # 开始监听
    def create(self):
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        # 使用多线程建立多个客户端
        while 1:
            sock,addr = self.socket.accept()
            self.sockets.append(sock)
            print(sock,addr)
            t = threading.Thread(target=self.run,args=(sock,addr))
            t.start()

    # 处理每个客户请求
    def run(self,socket,addr):
        # 接收昵称
        data = socket.recv(1024)
        name = data.decode('gbk')
        with self.lock:
            self.namelist.append(name)
            print(self.namelist)
        socket.send(json.dumps(self.namelist).encode('gbk'))
        # 接收数据
        while 1:
            try:
                data = socket.recv(1024)
            except:
                return None
            message= data.decode('gbk')
            if message=='':
                continue
            # 向每个客户端发送信息
            with self.lock:
                i=0
                while i<len(self.sockets):
                    try:
                        self.sockets[i].send(json.dumps({"user":name,"message":message,"userlist":self.namelist}).encode('gbk'))
                    except:
                        # 统计断开的连接
                        self.sockets.remove(self.sockets[i])
                        self.namelist.pop(i)
                        i-=1
                    i+=1



if __name__=='__main__':
    Service()