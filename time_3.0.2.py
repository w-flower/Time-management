import json
import os
import threading
import time
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
import requests
import re
import webbrowser

# 全局变量
add_cishu = 0
start_cishu = 0
start_start_time_cishu = 0
lst = []
lst_even = []


def starting(name, *args):
    '''将函数打包进线程'''
    print('创建线程: ', name)
    t = threading.Thread(target=name, args=args) if args is not None else threading.Thread(target=name)
    t.setDaemon(True)
    t.start()
    


def messagebox_showinfo(text):
    '''新建线程来提醒'''
    def messagebox_showinfo_temp(ttext: str):
        messagebox.showinfo('提示', ttext)

    starting(messagebox_showinfo_temp, text)


def think(input_ttime, typ):
    '''内制判断方法'''
    for input_ttime_temp in input_ttime:
        try:
            input_ttime_temp = input_ttime_temp.split(':')
        except:
            return False
        if len(input_ttime_temp) >= 3:
            return False
        try:
            h = int(input_ttime_temp[0])
            m = int(input_ttime_temp[1])
            if len(str(h)) >= 3 or len(str(m)) >= 3:
                return False
        except:
            return False
        if h > 23 or h < 0 or m < 0 or m > 59:
            return False


def add_input():
    '''多线程接受输入'''
    global lst
    global lst_even
    # global separator
    lst.append('')
    lst_even.append('')
    print(lst)
    print(lst_even)
    input_add_len = len(lst)
    input_add_len_enven = len(lst_even)
    separator = LabelFrame(root, text='第{}项'.format(input_add_len))
    separator.pack(fill="x", padx=18, pady=5)

    labelhhello = Label(separator, text='时间  ')
    labelhhello.grid(row=0, column=0, padx=5)
    time_input = '00:00'

    def go(*args):
        global lst
        get = comboxlist.get()
        getone = comboxlistone.get()
        if len(get) == 2:
            if len(getone) == 2:
                time_input = get + ':' + getone
            elif len(getone) == 0:
                time_input = get + ':' + '0' + '0' + getone
            else:
                time_input = get + ':' + '0' + getone
        else:
            if len(getone) == 2:
                time_input = '0' + get + ':' + getone
            elif len(getone) == 0:
                time_input = '0' + get + ':' + '0' + '0' + getone
            else:
                time_input = '0' + get + ':' + '0' + getone
        lst[input_add_len - 1] = time_input

    comvalue = StringVar()  # 窗体自带的文本，新建一个值
    comboxlist = Combobox(separator, textvariable=comvalue, width=5)  # 初始化
    comboxlist["values"] = [i for i in range(0, 24)]
    comboxlist.current(int(time.strftime("%H")))  # 选择第n个
    comboxlist.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
    comboxlist.grid(row=0, column=1, sticky=W)

    Label(separator, text=':').place(x=115, y=0)

    comvalueone = StringVar()  # 窗体自带的文本，新建一个值
    comboxlistone = Combobox(separator,
                             textvariable=comvalueone,
                             width=5)  # 初始化
    comboxlistone["values"] = [i for i in range(0, 60)]
    comboxlistone.current(0)
    comboxlistone.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
    comboxlistone.grid(row=0, column=1, sticky=E)

    labelhhello = Label(separator, text='事件  ')
    labelhhello.grid(row=1, column=0)

    evenentry = Entry(separator, show=None)
    evenentry.grid(row=1, column=1)
    while True:
        # 实时接收数据
        try:
            lst_even[input_add_len_enven - 1] = evenentry.get()
            go()
            time.sleep(0.2)
        except:
            time.sleep(2)


def add():
    '''接受输入'''
    global add_cishu
    # 测试用户是否输入正确
    if add_cishu != 0:
        if think(lst, 'lst') == False:
            messagebox.showinfo("提示", "某个数据有错哦")
            return False
    add_cishu += 1
    starting(add_input)


def start():
    '''开始'''
    global root
    global start_start_time_cishu
    global lst
    if start_start_time_cishu >= 1:
        messagebox_showinfo("ok,到时间后会提醒你的,不要关闭这个界面哦,否则你录入的所有东西都会一洗而空")
        return None
    if think(lst, 'lst') == False:
        messagebox.showinfo('提示', '你的输入有错误哦')
        print('删除线程:start')
        return False
    start_start_time_cishu += 1
    messagebox_showinfo("ok,到时间后会提醒你的,不要关闭这个界面哦,否则你录入的所有东西都会一洗而空")
    print(lst)
    print(lst_even)
    slp = time.strftime("%S")
    if int(slp) < 30:
        slp = 30 - int(slp)
    else:
        slp = 60 - int(slp)
    try:
        time.sleep(slp)
    except:
        try:
            time.sleep(60 - int(slp))
        except:
            pass
    try:
        count = 0
        while True:
            '''重复判断并接收'''
            st = set(lst)
            lenlst = len(lst)
            if think(lst, 'lst') == False:
                time.sleep(2)
                print(st, 'false think')
                continue

            if count >= len(lst):
                messagebox.showinfo('提示', '计时停止')
                start_start_time_cishu = 0
                print('stop')
                break

            print(time.strftime('%H:%M'))

            if time.strftime('%H:%M') in st:
                count += 1
                showinfo_even = lst_even[lst.index(
                    time.strftime('%H:%M'))]  #寻找事件
                messagebox_showinfo("提示:{}".format(showinfo_even))
                st = set(lst)
                print(st)
                slp = time.strftime('%S')
                print('sleep: {}'.format(60 - slp))
                time.sleep(slp)
                continue
            else:
                slp = time.strftime("%S")  # 转换成新的时间格式(20)
                st = set(lst)
                time.sleep(10)
    # 错误收集
    except Exception as result:
        messagebox.showinfo(
            "提示", "请汇报给作者信息,已经出现bug,错误信息:in start: {}".format(result))


def start_thread():
    print('创建线程:开始')
    t = threading.Thread(target=start)
    t.setDaemon(True)
    t.start()


def menu():
    '''顶部菜单'''
    global root

    def set_up():
        '''设置'''
        global root
        # 创建新的窗口
        set_up = Tk()
        set_up.title('设置')
        set_up.geometry('250x400')
        set_up.attributes("-alpha", 0.83)  # 窗口透明度13 %
        set_up.attributes("-topmost", True)

        labelhello = Label(set_up, text='基本')
        labelhello.grid(row=1, column=0)

        # 透明度
        def change_setup(*args):
            root.attributes("-alpha", s2.get())
            set_up.attributes("-alpha", s2.get())

        def change_before_touming_by_first():
            root.attributes("-alpha", 0.83)
            set_up.attributes("-alpha", 0.83)

        labelhello = Label(set_up, text='透明度')
        labelhello.grid(row=2, column=0)
        s2 = Scale(set_up,
                   from_=0.5,
                   to=1,
                   orient=HORIZONTAL,
                   command=change_setup)  # orient=HORIZONTAL设置水平方向显示
        s2.grid(row=2, column=1)
        Button(set_up, text='还原默认设置',
               command=change_before_touming_by_first).grid(row=2, column=2)
        # 置顶设置

        Label(set_up, text='置顶').grid(row=4, column=0)
        zhiding = IntVar()

        def oon_user_True():  # 置顶
            root.attributes("-topmost", True)

        def oon_user_False():  # 取消置顶
            root.attributes("-topmost", False)

        radio1 = Radiobutton(set_up,
                             text="是",
                             variable=zhiding,
                             value=True,
                             command=oon_user_True)
        radio1.grid(row=4, column=1)
        radio2 = Radiobutton(set_up,
                             text="否",
                             variable=zhiding,
                             value=False,
                             command=oon_user_False)
        radio2.grid(row=4, column=2)

    def export():
        '''导出'''
        global lst
        global lst_even
        file = filedialog.askdirectory()
        print(file)
        if think(lst, 'lst') == False:
            messagebox.showinfo('你输入的时间有错误哦~')
            return False
        try:
            if file == '':
                messagebox.showinfo('提示', '导出失败')
                return False
            # 防止文件重复
            date = time.strftime('%Y%H%S%M')
            for i in range(3):
                date += str(int(date) << 2)[2:-1]
            date = date[20:-1]
            print(date)
            with open(file + '\\time{}.time_data'.format(date), 'w') as f:
                json.dump(lst, f)
                f.write('\n')
                json.dump(lst_even, f)
            messagebox.showinfo('提示', '导出成功!')
        except:
            messagebox.showinfo('提示', '导出失败')

    def un_export():
        '''导入'''
        global lst
        global lst_even
        file = filedialog.askopenfilename(title=u'选择导入文件')
        try:
            if file == '':
                messagebox.showinfo('提示', '导入失败')
                return False
            with open(file, 'r') as f:
                un_export_read = f.read()
                un_export_read = un_export_read.split('\n')
                lst = json.loads(un_export_read[0])
                lst_even = json.loads(un_export_read[1])
                if think(lst, 'lst') == False:
                    messagebox.showinfo('提示', '检测到该列表不正确,如果是我们导出的话,请报告给作者')
                messagebox.showinfo('提示', '导入成功')
        except:
            messagebox.showinfo(
                '提示', '导入失败,请导入后缀名time_data并且格式正确的文件,如果是我们导出的话,请报告给作者')

    menu_one = Menu(root)
    root['menu'] = menu_one
    f1 = Menu(menu_one, tearoff=False)  # 创建子菜单
    f1.add_command(label='设置', command=set_up)  # 子菜单栏
    f1.add_command(label='导出时间表', command=export)
    f1.add_command(label='导入时间表', command=un_export)
    menu_one.add_cascade(label='选项', menu=f1)

    def time_about_this():
        '''当前软件信息'''
        global root
        # 创建新的窗口
        time_tk = Tk()
        time_tk.title('软件信息')
        time_tk.geometry('250x400')
        time_tk.attributes("-alpha", 0.83)  # 窗口透明度13 %
        time_tk.attributes("-topmost", True)
        # 作者
        zuozhe = LabelFrame(time_tk, text='作者')
        zuozhe.pack(fill='x')
        Label(zuozhe, text='这一季 冬花凋落').pack(side=LEFT)

        # 软件
        ruanjian = LabelFrame(time_tk, text='软件')
        ruanjian.pack(fill='x')
        Label(ruanjian, text='版本号: 3.0.0内测版').grid(row=0, column=0)
        Label(ruanjian, text='编程软件: VScode  ').grid(row=1, column=0)
        Label(ruanjian, text='编程语言: python  ').grid(row=2, column=0)
        Label(ruanjian, text='参考资料: 百度&必应').grid(row=3, column=0)

        def gengxinrizhi():
            '''更新日志'''
            def gengxinrizhi_temp():
                name = time.strftime('%Y%H%S%M')
                for i in range(3):
                    name += str(int(name) << 2)[2:-1]
                name = name[20:-1]
                with open('更新日志time{}.txt'.format(name), 'w') as f:
                    f.write('''时间管理内测3.0.0更新日志
                ---------看完后我们就会删掉的~-------------
        
                时间管理内测3.0.0更新日志

                更新:
                2020.4.14
                界面全新更改
                添加菜单
                增加导出课程表和导入课程表
                2020.4.17
                整体优化,算法优化,常规维护
                2020.4.18
                添加软件信息
                常规维护,简化代码
                紧急维护,修复重大bug-->已修复
                2020.4.19
                发现bug打开日志出错
                2020.4.21
                变成公测版, 开启更新功能一代!
                同时他可以联网了,只不过只有在更新的时候可以连
                2020.4.22
                将更新更换成浏览器下载更新
                修复bug
                2020.4.23
                将更新下载方式设置为可选

                已知bug(已修复):
                无

                未修复:
                更新时候提示语出错(0.0,0.1)
                更新太慢了..............都怪作者不会多线程下载
                界面太长-->设置翻页,需要立刻更改<--
                导入后无法更改-->翻页
                ''')
                file = os.getcwd()
                os.system('notepad {}\\{}{}.txt'.format(
                    file, '更新日志time', name))
                try:
                    os.remove('更新日志time{}.txt'.format(name))
                except:
                    messagebox.showinfo('提示', '删除失败')

            starting(gengxinrizhi_temp)

        Button(ruanjian, text='更新日志', command=gengxinrizhi).grid(row=4,
                                                                 column=0)


    def update():
        '''更新'''
        def update_thread():
            try:
                ret = requests.get(
                    'https://github.com/feilong-hello/time_-/releases')
                ret = ret.text
                getnew = re.findall('time_3\.(.*?\..*?)\.exe', ret)
                flag = False
                len_ = 0

                # 倒序,获取最新版本
                getnew.reverse()
                for i in getnew:
                    if float(i) > 0.2:
                        flag = True
                        getnew = i
                        break
                    len_ += 1
                
                if flag:
                    if messagebox.askokcancel("提示",
                                              '发现新版本3.{},是否更新?'.format(getnew)):
                        getnewone = re.findall(
                            'href="(/feilong-hello/time_-/.*?/time_3\..*?\..*?\.exe)"',
                            ret)
                        getnewone.reverse()
                        print(getnewone)
                        print(len_)
                        getone = getnewone[len_ - 1]
                        print('http://github.com' + getone)
                        if messagebox.askokcancel('提示', '打开浏览器下载(快)or软件自身下载(慢)?\n确定:打开浏览器下载\n取消:打开软件自身下载'):

                            messagebox.showinfo('提示', '我们将会打开浏览器,并且自动下载最新版')
                            wangzhi = 'http://github.com' + getone
                            print(wangzhi)
                            webbrowser.open(wangzhi)
                        else:
                            if messagebox.askokcancel('提示', '确定更新吗?'):
                                headers = {
                                'User-Agent':
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4115.0 Safari/537.36 Edg/84.0.488.1'
                                }
                            
                                wangzhi = 'http://github.com' + getone
                                print(wangzhi)
                                for i in range(5):
                                    try:
                                        ggetdown = requests.get('https://github.com' + getone,
                                                            headers=headers, stream=True)
                                    except:
                                        messagebox_showinfo('第{}次访问失败'.format(i))
                                    else:
                                        break
                                
                                messagebox.showinfo('提示', '可能会有点慢哦,请稍等~')
                                print('open and write')
                                file = os.getcwd() + '\\'
                                with open(file+'临时任务夹请勿删除', 'a') as f:
                                    pass
                                return False
                                with open(file + '临时任务夹请勿删除' + 'time_3.{}beta.exe'.format(getnew), 'wb') as f:
                                    for chunk in ggetdown.iter_content(chunk_size=1024):
                                        if chunk:
                                            f.write(chunk)

                                # f.write(ggetdown.content)

                                messagebox.showinfo('提示', '下载完成')
                else:
                    messagebox.showinfo('提示', '未检测到新版本')

            except Exception as ex:
                messagebox.showinfo('提示', '检查更新失败')
                print(ex)

        starting(update_thread)

    menu_two = Menu(root)
    f2 = Menu(menu_two, tearoff=False)  # 创建子菜单
    f2.add_command(label='软件信息', command=time_about_this)  # 子菜单栏
    f2.add_command(label='检查更新', command=update)
    menu_one.add_cascade(label='关于', menu=f2)


def root_main():  # 初始化
    root.title('时间管理')
    root.geometry('250x400')
    root.attributes("-alpha", 0.83)  # 窗口透明度13 %
    root.attributes("-topmost", True)  # 窗口置顶
    root.resizable(0, 1)
    # 输入文本
    labelhello = Label(root, text='输入你的时间吧~不需要输入秒')
    labelhello.pack()

    labelhello = Label(root, text='24小时制,例如:(9:00):')
    labelhello.pack()

    # 分割线
    separator = Frame(relief="sunken")
    separator.pack(fill="x", padx=5, pady=5)
    # 添加按钮
    Button(root, text="添加信息", command=add).pack()
    Button(root, text='start', command=start_thread).pack(side='bottom')
    # Button(ui, text='删除信息',command=del_time).pack()
    menu()
    


if __name__ == '__main__':
    root = Tk()
    root_main()
    root.mainloop()