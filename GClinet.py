import pickle
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from socket import *

import GPacket
from HandleProcess import *
from GPacket import *
from GUser import *


class client:
    def __init__(self):
        # 登陆与注册界面需要用的组件
        self.top = Tk()  # 端口
        self.top.geometry('1600x900')

        self.fm1 = Frame(self.top)  # 登陆页面
        self.fm2 = Frame(self.top)  # 注册页面
        self.fm3 = Frame(self.top)  # 登录后的显示页面
        self.opera = 'l'
        self.authority = 0  # 权限等级，会根据用户的选择而改变，登陆时需核对
        self.name = ''  # 用户名输入框，登陆时需核对
        self.ps = ''  # 密码输入框，登陆时需核对

        HOST = gethostname()  # 使用的时候修改成服务器对应的名称
        PORT = 8888

        self.ADDR = (HOST, PORT)
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)

    def set_user_name(self, n):
        self.name = n

    def set_password(self, ps):
        self.ps = ps

    def get_user_name(self):
        return self.name

    def Log_check(self):

        try:
            self.tcpCliSock.connect(self.ADDR)
        except:
            messagebox.askokcancel(title='提示', message='连接失败，请检查你的网络')
            self.top.destroy()
        else:
            self.Login()

    def Login(self):

        ''' 选择权限，输入用户名和密码'''

        self.top.title('python分组管理系统')
        canvas_root = Canvas(self.fm1, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()

        self.fm1.pack()

        # 权限选择
        M = StringVar(self.fm1)
        M.set('权限')
        om = ttk.Combobox(self.fm1, textvariable=M, values=['一般用户', '组长', '教师'], state='readonly')
        om.bind('<<ComboboxSelected>>', lambda event: self.Change_Authority(event, om.get()))
        om.place(x=625, y=200)

        # 用户输入框
        name_E = Entry(self.fm1)
        name_M = Message(self.fm1)
        name_M['text'] = '用户'
        name_M.place(x=600, y=250)
        name_E.place(x=650, y=250)

        # 密码输入框
        ps_E = Entry(self.fm1, show='*')
        ps_M = Message(self.fm1)
        ps_M['text'] = '密码'
        ps_M.place(x=600, y=300)
        ps_E.place(x=650, y=300)
        bt = Button(self.fm1, text='确定', command=lambda: self.View(name_E.get(), ps_E.get()))

        bt.place(x=675, y=350)

        btR = Button(self.fm1, text='没有账号？点这里创建！', command=self.Regist).place(x=625, y=400)

        self.top.mainloop()
        pass

    def Regist(self):
        '''注册页面，目前还需要一个完善信息的页面，等待设计'''

        self.fm1.pack_forget()

        canvas_root = Canvas(self.fm2, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()

        self.fm2.pack()
        name_E = Entry(self.fm2)  # 姓名输入框
        stu_E = Entry(self.fm2)  # 学号输入框
        ps_E = Entry(self.fm2, show='*')  # 密码输入框
        authority = 0

        M = StringVar(self.fm2)
        M.set('权限')
        om = ttk.Combobox(self.fm1, textvariable=M, values=['一般用户', '组长', '教师'], state='readonly')
        om.bind('<<ComboboxSelected>>', lambda event: self.Change_Authority(event, om.get()))
        om.place(x=625, y=200)

        name_M = Message(self.fm2, text='用户名')
        stu_M = Message(self.fm2, text='学号/工号')
        ps_M = Message(self.fm2, text='密码')

        name_E.place(x=650, y=250)
        stu_E.place(x=650, y=300)
        ps_E.place(x=650, y=350)
        name_M.place(x=600, y=250)
        stu_M.place(x=585, y=300)
        ps_M.place(x=600, y=350)
        Button(self.fm2, text='确定',
               command=lambda: self.Regist_check(name_E.get(), stu_E.get(), ps_E.get())).place(x=650, y=400)
        Button(self.fm2, text='取消', command=self.Login).place(x=725, y=400)
        self.top.mainloop()

    def View(self, name_g, ps_g):

        """判断权限，根据权限执行不同的内容，显示不同的页面
        """

        self.set_user_name(name_g)
        self.set_password(ps_g)

        if not name_g or not ps_g:
            messagebox.askokcancel(title='提示', message='用户名与密码不能为空')
            self.top.destroy()
            return
        GM = GUser.GroupMember()
        GM.setUser_name(self.name)
        GM.setPassword(self.ps)
        GM.setUser_type(self.authority)
        operator = GM

        packet1 = Packet_login()  # 登陆请求
        packet1.setOperator(GM)
        packet2 = Packet_search_info()  # 查询请求
        packet2.setOperator(GM)
        res1 = self.communicate(packet1)

        if not res1:
            print(res1)
            messagebox.askokcancel(title='提示', message='找不到对象')
            self.top.destroy()

        self.fm1.pack_forget()
        self.fm2.pack_forget()
        self.fm3.pack()

        canvas_root = Canvas(self.fm3, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()

        wel = Message(self.fm3, foreground='green', text='欢迎使用python用户管理系统', aspect=800)
        name_M = Message(self.fm3, text='姓名:')
        stu_M = Message(self.fm3, text='学号:')

        # result=[]
        res2 = self.communicate(packet2)

        for itm in res2:
            if itm['user_name'] == self.name and itm['password'] == self.ps:
                information = itm
                break
        name = Message(self.fm3, text=information['name'])
        stu = Message(self.fm3, text=information['student_number'], aspect=800)

        wel.place(x=650, y=50)
        name_M.place(x=500, y=200)
        name.place(x=700, y=200)
        stu_M.place(x=500, y=300)
        stu.place(x=700, y=300)

        M_N = ToggledFrame(self.fm3, text='管理结果', width=200, height=30)

        M_N.place(x=450, y=550)
        tree = ttk.Treeview(M_N.sub_frame, columns=(
            'name', 'sex', 'student_number', 'group_number', 'qq_number', 'user_type', 'password', 'username'),
                            show="headings", displaycolumns="#all")

        if self.authority == 1:
            '''普通组员'''
            ssbj = Message(self.fm3, text='所属班级')
            ssxz = Message(self.fm3, text='所属小组')
            ssbj_M = Message(self.fm3, text='2020211317')
            ssxz_M = Message(self.fm3, text=information['group_number'])

            ssbj.place(x=500, y=400)
            ssxz.place(x=500, y=500)
            ssbj_M.place(x=700, y=400)
            ssxz_M.place(x=700, y=500)
        if self.authority == 2:
            '''组长'''
            ssbj = Message(self.fm3, text='所属班级')
            glxz = Message(self.fm3, text='管理小组')
            glxz_M = Message(self.fm3, text=information['group_number'])
            ssbj_M = Message(self.fm3, text='2020211317')
            ssbj.place(x=500, y=400)
            glxz.place(x=500, y=500)
            ssbj_M.place(x=700, y=400)
            glxz_M.place(x=700, y=500)
        if self.authority >= 3:
            '''授课老师'''
            glbj = Message(self.fm3, text='管理班级')
            glbj_M = Message(self.fm3, text='2020211317')
            glbj.place(x=500, y=400)
            glbj_M.place(x=700, y=400)
            yjdr = Button(self.fm3, text='一键导入', command=lambda: self.Import('person.csv', tree))
            yjdr.place(x=0, y=0)

            zstp=Button(self.fm3,text='展示图片',command= self.show_graph)
            zstp.place(x=100,y=0)

        tree.column('name', width=80)
        tree.column('sex', width=50)
        tree.column('student_number', width=100)
        tree.column('group_number', width=100)
        tree.column('qq_number', width=100)
        tree.column('user_type', width=50)
        tree.column('password', width=100)
        tree.column('username', width=100)

        tree.heading('name', text="姓名", anchor=W)
        tree.heading('sex', text="性别", anchor=W)
        tree.heading('student_number', text="学号", anchor=W)
        tree.heading('group_number', text="小组编号", anchor=W)
        tree.heading('qq_number', text="QQ号", anchor=W)
        tree.heading('user_type', text="用户等级", anchor=W)
        tree.heading('password', text="密码", anchor=W)
        tree.heading('username', text="用户名", anchor=W)

        def deljob():
            '''view界面的删除命令'''
            iid = tree.selection()
            packet = Packet_delete_info()
            packet.setOperator(operator)

            d = tree.item(tree.focus())
            d = d['values']
            delee = GUser.GroupMember()

            delee.setStudent_number(d[2])
            print(d[2])
            packet.setDelete_info(delee)
            self.communicate(packet)

            tree.delete(iid)

        def addjob():
            '''view界面的增加命令'''
            add = Tk()
            name_M = Message(add, text='姓名')
            name = Entry(add)
            sex_M = Message(add, text='性别')
            sex = ttk.Combobox(add, values=['M', 'F'], state='readonly')
            name_M.grid(row=0, column=0)
            name.grid(row=0, column=1)
            sex_M.grid(row=1, column=0)
            sex.grid(row=1, column=1)

            stu_M = Message(add, text='学号')
            stu = Entry(add)
            gro_M = Message(add, text='所属小组')
            gro = Entry(add)
            stu_M.grid(row=2, column=0)
            stu.grid(row=2, column=1)
            gro_M.grid(row=3, column=0)
            gro.grid(row=3, column=1)

            ut_M = Message(add, text='用户等级')
            ut = ttk.Combobox(add, values=['一般用户', '组长', '教师'], state='readonly')
            ps_M = Message(add, text='密码')
            ps = Entry(add)
            ut_M.grid(row=4, column=0)
            ut.grid(row=4, column=1)
            ps_M.grid(row=5, column=0)
            ps.grid(row=5, column=1)

            qq_M = Message(add, text='QQ号')
            qq = Entry(add)
            user_M = Message(add, text='用户名')
            user = Entry(add)
            qq_M.grid(row=6, column=0)
            qq.grid(row=6, column=1)
            user_M.grid(row=7, column=0)
            user.grid(row=7, column=1)

            addB = Button(add, text='确定', command=lambda: adding(
                {'name': name.get(), 'sex': sex.get(), 'student_number': stu.get(), 'group_number': gro.get(),
                 'qq_number': qq.get(), 'user_type': ut.get(), 'password': ps.get(), 'username': user.get()}, add))
            addB.grid(row=8, column=1)

        def adding(get, add):
            """向服务器发送增加请求，并在收到回复后，进行增加"""
            if get['user_type'] == '一般用户':
                get['user_type'] = 1
            elif get['user_type'] == '组长':
                get['user_type'] = 2
            else:
                get['user_type'] = 3
            packet = Packet_add_info()
            packet.setOperator(operator)
            addMember = GUser.GroupMember()

            addMember.setName(get['name'])
            addMember.setSex(get['sex'])
            addMember.setPassword(get['password'])
            addMember.setUser_type(get['user_type'])
            addMember.setUser_name(get['username'])
            addMember.setGroup_number(get['group_number'])
            addMember.setStudent_number(get['student_number'])
            addMember.setQQ_number(get['qq_number'])

            packet.setAdd_information(addMember)
            if self.communicate(packet):
                con = []
                for key in get:
                    con.append(get[key])
            tree.insert('', END, values=con)
            add.destroy()

        for itm in res2:
            itm=tuple(itm.values())
            tree.insert("", END, values=itm)
        tree.pack(fill=BOTH, expand=True)

        if self.authority > 1:
            delete = Button(M_N.sub_frame, text='删除', command=deljob)
            add = Button(M_N.sub_frame, text='增加', command=addjob)
            delete.pack(side='right')
            add.pack(side='left')
        self.top.mainloop()
    def show_graph(self):
        fm=Frame(self.top)
        fm3,pack_forget()
        fm.pack()

        canvas_root = Canvas(fm, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()

        img_gif=PhotoImage(file='sinc.png')
        label_img=Label(fm,image=img_gif)
        label_img.place(x=300,y=100)
        
    def Regist_check(self, name, un, ps):  # 用户名，学号，密码
        """向服务器发送注册请求"""
        GM = GUser.GroupMember()
        GM.setUser_name(name)
        GM.setStudent_number(un)
        GM.setPassword(ps)
        GM.setUser_type(self.authority)

        self.fm2.pack_forget()
        fm4 = Frame(self.top)

        canvas_root = Canvas(fm4, width=1600, height=900)
        im_root = HP.get_img('bj.png', 1600, 900)
        canvas_root.create_image(800, 450, image=im_root)
        canvas_root.pack()
        wel = Message(fm4, foreground='green', text='请输入补充信息', aspect=800)
        name_M = Message(fm4, text='姓名')
        sex_M = Message(fm4, text='性别')
        group_M = Message(fm4, text='所属小组')
        QQ_M = Message(fm4, text='QQ号')
        group_now = []

        name = Entry(fm4)
        sex = ttk.Combobox(fm4, values=['M', 'F'], state='readonly')
        group = ttk.Combobox(fm4, textvariable='请选择你的小组', values=group_now, state='readonly')  # group_now待定，为现有小组
        QQ = Entry(fm4)
        Bqd = Button(fm4, text='确定', command=lambda: check(name.get(), sex.get(), group.get(), QQ.get()))
        Bqx = Button(fm4, text='取消', command=self.Regist)
        wel.place(x=650, y=50)

        name_M.place(x=500, y=200)
        name.place(x=700, y=200)

        sex_M.place(x=500, y=300)
        sex.place(x=700, y=300)

        group_M.place(x=500, y=400)
        group.place(x=700, y=400)

        QQ_M.place(x=500, y=500)
        QQ.place(x=700, y=500)

        Bqd.place(x=600, y=750)
        Bqx.place(x=800, y=750)
        fm4.pack()
        self.top.mainloop()

        def check(name, sex, group, QQ):
            GM.setName(name)
            GM.setSex(sex)
            GM.setGroup_number(group)
            GM.setQQ_number(QQ)
            operator = Packet_add_info()
            operator.setAdd_information(GM)

            if self.communicate(operator):
                self.view(un, ps)
            else:

                m = messagebox.askokcancel(title='提示', message='注册失败，请重新注册')

    def Import(self, path, tree):

        import pandas as pd

        packet = GPacket.Packet_add_info()
        data = pd.read_csv(path)
        member_list = data.values.tolist()
        for i, j, k, l in member_list:
            add_context = GUser.GroupMember()
            add_context.setGroup_number(i)
            add_context.setName(j)
            add_context.setStudent_number(k)
            if l == 'N':
                l = 1
                add_context.setUser_type(1)
            else:
                l = 2
                add_context.setUser_type(2)
            add_context.setQQ_number('10110')
            add_context.setSex('F')
            add_context.setUser_name('root')
            add_context.setPassword('123456')
            packet.setAdd_information(add_context)
            if self.communicate(packet):
                tree.insert('', END, values=[j, 'F', k, i, '10110', l, '123456', 'root'])

    def Change_Authority(self, event, n):
        """注册时用来改变权限"""
        if n == '一般用户':
            self.authority = 1
        elif n == '组长':
            self.authority = 2
        elif n == '教师':
            self.authority = 3

    def communicate(self, packet):
        """通讯函数，负责与服务器进行沟通，
           ip与端口在创建类时进行指定，
           st表示要传输的内容"""

        bp = pickle.dumps(packet)
        data1 = bp
        self.tcpCliSock.send(data1)

        data = self.tcpCliSock.recv(1024)
        res = pickle.loads(data)
        result = None

        if type(res) == type(GPacket.Packet_response_login()):
            result = res.getPasswordSignal()
        elif type(res) == type(GPacket.Packet_response_is_successful()):
            result = res.getOperate_result()
        elif type(res) == type(GPacket.Packet_response_data()):
            allData = []
            while res.getData()['user_name'] != 's':
                allData.append(res.getData())
                data = self.tcpCliSock.recv(1024)
                res = pickle.loads(data)
            result = allData

        return result


c = client()
c.Log_check()
