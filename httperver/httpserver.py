"""
HTTPSERVER主程序

"""
from  socket import *
import sys
from threading import Thread
from config import *
import re
import json

ADDR = (HOST,PORT)

#和webframe通信的函数
def connect_frame(env):
    s = socket()
    try:
        s.connect((frame_ip,frame_port))
    except Exception as e:
        print(e)
        return
    #讲字典转换为json格式
    data = json.dumps(env)
    # 将解析后请求发送给webframe
    s.send(data.encode())
    # 接受来自webframe的数据
    data = s.recv(4096 * 100).decode()
    # print(json.loads(data)) #转换为字典
    return json.loads(data)


class HTTPServer:
    def __init__(self):
        self.address = ADDR
        self.create_socket()#浏览器交互
        #self.connect_socket()#链接webtframe
        self.bind()

    def create_socket(self):
        self.socked = socket()
        self.socked.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)

    # def connect_socket(self):
    #     self.connect_socked = socket()
    #     frame_addr = (frame_ip,frame_port)
    #     try:
    #         self.connect_socked.connect(frame_addr)
    #     except Exception as e:
    #         print(e)
    #         sys.exit()

    def bind(self):
        self.socked.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    def handle(self,connfd):
        request = connfd.recv(4096).decode()
        print(request)
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            env = re.match(pattern,request).groupdict()
        except:
            connfd.close()
            return
        else:
            data = connect_frame(env)
            if data:
                self.response(connfd,data)
            # #讲字典转换为json格式
            # data = json.dumps(env)
            # #将解析后请求发送给webframe
            # self.connect_socked.send(data.encode())
            # #接受来自webframe的数据
            # data = self.connect_socked.recv(4096*100).decode()
            # #print(json.loads(data)) #转换为字典
            # self.response(connfd,json.loads(data))

        #给浏览器发送数据
    def response(self,connfd,data):
        if data['status'] == '200':
            responsHeaders = "HTTP/1.1 200 OK\r\n"
            responsHeaders+= "Content-Type:text/html\r\n"
            responsHeaders+="\r\n"
            responsBody = data['data']
        elif data['status'] == '404':
            responsHeaders = "HTTP/1.1 404 not found\r\n"
            responsHeaders += "Content-Type:text/html\r\n"
            responsHeaders += "\r\n"
            responsBody = data['data']
        else:
            pass

        response_data = responsHeaders + responsBody
        connfd.send(response_data.encode())



    def server_forever(self):
        self.socked.listen(5)
        print("Listen the port %d"% self.port)
        while True:
            connfd,addr = self.socked.accept()
            print("connect form", addr)
            client = Thread(target=self.handle,args=(connfd,))
            client.start()





http = HTTPServer()
http.server_forever()










