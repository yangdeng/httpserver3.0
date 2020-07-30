
from  socket import *
import json
from setting import *
from select import select
from urls import *

#应用累，处理某一方面的请求
class Application:
    def __init__(self):
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.socked = socket()
        self.socked.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        self.bind(frame_ip,frame_port)
        self.socked.listen(5)


    def start(self):
        self.rlist.append(self.socked)
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.socked:
                    connfd,addr = r.accept()
                    self.rlist.append(connfd)
                else:
                    self.handle(r)
                    self.rlist.remove(r)

    def handle(self,connfd):
        request = connfd.recv(1024).decode()
        request = json.loads(request)
        #print(request)
        if request['method'] == 'GET':
            if request['info'] == '/' or request['info'][-5:] == '.html':
                response = self.get_html(request['info'])
            else:
                response = self.get_data(request['info'])
        elif request['method'] == 'POST':
            pass

        response = json.dumps(response)
        connfd.send(response.encode())
        connfd.close()

    def get_html(self,info):
        if info == '/':
            filename = STATIC_DIR + "/index.html"
        else:
            filename = STATIC_DIR + info
        try:
            fd = open(filename)
        except Exception as e:
            fd = open(STATIC_DIR + '/404.html')
            return {'status':'404', 'data':fd.read()}
        else:
            return {'status':'200', 'data': fd.read()}


    def get_data(self,info):
        for url,func in urls:
            if url == info:
                return {'status':'200', 'data': func()}
        return {'status':'404', 'data': 'sorry.....'}




app = Application()
app.start()




