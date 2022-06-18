import datetime
import json
import tkinter as tk
import tkinter.messagebox as msg
import socket
import threading
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self, name, client):
        super(Main, self).__init__()
        self.name = name
        self.tcp_client_socket = client
        self.create()
        # 发送昵称
        self.tcp_client_socket.send(self.name.encode('gbk'))
        data = self.tcp_client_socket.recv(1024)
        message = data.decode('gbk')
        data = json.loads(message)
        for i in set(data):
            self.listbox.insert(tk.END, i)
        # 接收消息线程
        t = threading.Thread(target=self.rev)
        t.start()
        self.mainloop()

    # 页面布局
    def create(self):
        self.geometry('800x500+300+100')
        self.title('多人聊天室')
        # 文本框
        self.area = tk.Text(self,state=tk.DISABLED)
        self.area.tag_configure("even",
                                foreground="blue")
        self.area.tag_configure("odd", foreground="black")
        # 滚动条
        self.vsb = tk.Scrollbar(self,command=self.area.yview,orient=tk.VERTICAL)
        self.area.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=tk.RIGHT,fill=tk.Y)
        self.area.pack(side=tk.RIGHT,fill=tk.Y)
        # 我的昵称
        myname = tk.Label(self,text='我的昵称:'+self.name)
        myname.place(relx=0.02,rely=0.78)
        # 输入框
        self.conent = ttk.Entry(self)
        self.conent.place(relx=0.02,rely=0.85)
        self.btn_send = ttk.Button(self, text='发送',
                                  command=self.send_message)
        self.btn_send.place(relx=0.02,rely=0.9)
        self.conent.bind('<Return>', self.send_message)
        # 在线用户
        u = tk.Label(self,text='在线用户:')
        u.place(relx=0.02,rely=0.05)

        self.listbox = tk.Listbox(self)
        self.listbox.place(relx=0.02,rely=0.15)
    # 点击发送按钮
    def send_message(self,event):
        message = self.conent.get()
        self.conent.delete(0, tk.END)
        self.tcp_client_socket.send(message.encode('gbk'))


    def rev(self):
        while 1:
            # 设置颜色状态
            tag = "odd"
            data = self.tcp_client_socket.recv(1024)
            message = data.decode('gbk')
            data = json.loads(message)
            #内容
            content = data.get('message')
            # 姓名
            name = data.get('user')
            if name==self.name:
                name="我"
            # 用户列表
            userlist = data.get('userlist')
            # 文本框插入
            try:
                # 设置可编辑
                self.area.config(state=tk.NORMAL)
                self.area.insert(tk.END,
                                 datetime.datetime.now().strftime(
                                     '%Y-%m-%d %H:%M:%S')+'\t'
                                 + name + '>>' + '\n',tag
                                 )
                tag = "even" if tag == "odd" else "odd"
                self.area.insert(tk.END,content + '\n',tag)
                # 设置不可编辑
                self.area.config(state=tk.DISABLED)
                self.listbox.delete(0,tk.END)
                for i in userlist:
                    self.listbox.insert(tk.END,i)
            except Exception as e:
                print(e)
                return None






#登录页
class Login(tk.Tk):
    def __init__(self):
        super(Login, self).__init__()

        self.create()
        self.mainloop()

    def create(self):
        self.geometry('500x300+200+150')
        self.title('用户登录')
        label = tk.Label(self, text='请输入聊天昵称:')
        label.grid(row=1, column=1,padx=20,pady=100)
        self.name = ttk.Entry(self)
        self.name.bind('<Return>', self.check)
        self.name.grid(row=1, column=2)

        btn = ttk.Button(self, text='登录', command=self.check)
        btn.grid(row=1, column=3)

    def check(self,event):
        name = self.name.get()
        if name == '':
            msg.showerror('错误', '昵称不能为空!')
            return None
        # 创建socket
        self.tcp_client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)
        try:
            # self.tcp_client_socket.connect(
            #     ('101.42.93.7',9999))
            self.tcp_client_socket.connect(
                ('127.0.0.1', 8888))
            self.destroy()
            Main(name, self.tcp_client_socket)
        except:
            msg.showerror('错误', '连接失败!')
            return None


if __name__ == '__main__':
    Login()
