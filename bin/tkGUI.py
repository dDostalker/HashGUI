#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.filedialog
from core import HashCatVersion, HashCatLoad
import core, GetHashAttackMode
from threading import Thread
import time
import subprocess
import signal
import copy

HashMode = {}

MainWindows = [200, 200, '#1E1F22', "720x400", 0, False]  # 窗口x，窗口y，窗口颜色,窗口大小,#313233.窗口是否展开
MainWindowBoards = [["#1E1F22", '#3BBCD6'], ['white'], []]  # 窗口(颜色),关闭控件(颜色),按钮颜色
# 主窗口设置
MainWindow = tk.Tk()
MainWindow.title('ZipCat_GUI')  # 主窗口名称
MainWindow.geometry(MainWindows[3])  # 窗口大小+起始位置
MainWindow.resizable(True, False)  # 能否调整大小
MainWindow.config(background=MainWindows[2])  # 背景颜色
MainWindow.overrideredirect(True)  # 隐藏边框

ForceInt = tk.IntVar()
MachineInt = tk.IntVar()
ForceInt.set(core.ReadForce())
MachineInt.set(core.ReadMachine())

# 命令语句
Command_HashCat = " "
Command_AttackMode = " "
Command_HashMode = " "
Command_Dictionary = " "
Command_Aim = " "
Command_Mask1 = " "
Command_Mask2 = " "
Pids = -1

# 特例全局
DictionaryLabels = Label(MainWindow, text=Command_Dictionary, background=MainWindows[2],
                         foreground=MainWindowBoards[1][0])
DictionaryLabels.place(x=150, y=185)

AimLabels = Label(MainWindow, text=Command_Aim, background=MainWindows[2],
                  foreground=MainWindowBoards[1][0])
AimLabels.place(x=210, y=220)

HashModeLabels = Label(text=Command_HashMode, background=MainWindows[2], foreground=MainWindowBoards[1][0])

HashModeCombobox = ttk.Combobox()
# 暂存历史
MaskSet = {''}


def DictionaryLabel(value):
    DictionaryLabels.config(text=core.OutPutCut(value, 120), fg='white')


def DictionaryWarning():
    DictionaryLabels.config(text='请输入攻击模式', fg='red')


def AimLabelWarning():
    DictionaryLabels.config(text='无效的攻击路径', fg='red')


def AimLabel(value):
    if core.FileCheck(value):
        AimLabels.config(text=core.OutPutCut(value, 65), fg='white')
    else:
        AimLabelWarning()


def WordSet():
    Command = ""
    sets = ""
    if ForceInt.get():
        sets += '--force'
    if MachineInt.get():
        sets += ' --machine-readable '

    # 判断有无空栏
    if Command_HashCat.isspace():
        tkinter.messagebox.showerror('错误', '未选中hashcat')
        return 0
    elif Command_HashMode.isspace():
        tkinter.messagebox.showerror('错误', '未选中攻击模式')
        return 0
    elif Command_Aim.isspace():
        tkinter.messagebox.showerror('错误', '未选中攻击目标')
        return 0

    if '0' in Command_AttackMode:  # 单字典攻击
        if Command_Dictionary.isspace():
            tkinter.messagebox.showerror('错误', '未填入字典')
            return 0
        Command = "%s %s %s %s %s %s " % (
            Command_HashCat, sets, Command_HashMode, Command_AttackMode, Command_Aim, Command_Dictionary)

    elif '1' in Command_AttackMode:  # 多字典攻击
        if Command_Dictionary.isspace():
            tkinter.messagebox.showerror('错误', '未填入字典')
            return 0
        Command = "%s %s %s %s %s %s " % (
            Command_HashCat, sets, Command_HashMode, Command_AttackMode, Command_Aim, Command_Dictionary)

    elif '3' in Command_AttackMode:  # 掩码攻击
        if Command_Mask2.isspace():
            tkinter.messagebox.showerror('错误', '未填入掩码')
            return 0
        Command = "%s %s %s %s %s %s %s" % (
            Command_HashCat, sets, Command_HashMode, Command_AttackMode, Command_Mask1, Command_Aim, Command_Mask2)

    elif '6' in Command_AttackMode:  # 混合攻击1
        if Command_Mask2.isspace() or Command_Dictionary.isspace():
            tkinter.messagebox.showerror('错误', '未填入字典或掩码')
            return 0
        Command = "%s %s %s %s %s %s %s " % (
            Command_HashCat, sets, Command_HashMode, Command_AttackMode, Command_Aim, Command_Dictionary, Command_Mask2)

    elif '7' in Command_AttackMode:  # 混合攻击2
        if Command_Mask2.isspace() or Command_Dictionary.isspace():
            tkinter.messagebox.showerror('错误', '未填入字典或掩码')
            return 0
        Command = "%s %s %s %s %s %s %s " % (
            Command_HashCat, sets, Command_HashMode, Command_AttackMode, Command_Aim, Command_Mask2, Command_Dictionary)
    global ProcessList
    if Command in ProcessList:
        tkinter.messagebox.showwarning('警告', '重复设置代码')
        return 0
    ProcessList.append(Command)
    core.UploadRunList(ProcessList)


# 设置资源加载
# 边框是否加长标志


# 图片资源加载


# 子窗口
SonWindowFlag = 0
ProcessList = []


def OpenMenu(event):
    Menu = tk.Toplevel()
    local1 = -1
    StopButton = Button(Menu, text='停止运行')
    StartButton = Button(Menu, text='开始运行')
    ProcessLabel1 = Label(Menu, text='当前进度:')
    ProcessLabel2 = Label(Menu)
    ProcessReadyList = Listbox(Menu, width=140, height=25)
    RefreshFlag = 1
    ProcessListCheck = []
    flag = 0

    def _Refresh():
        nonlocal RefreshFlag
        if flag != 0:
            tkinter.messagebox.showwarning('警告', '关闭将停止当前运行，不保留进度')
            try:
                os.kill(Pids, signal.SIGTERM)
            except:
                pass
        RefreshFlag = 0
        if t1.is_alive():
            pass
        else:
            Menu.destroy()

    def Refresh():
        nonlocal local1, ProcessListCheck

        def UpgradeList():
            nonlocal local1

            try:
                local1 = ProcessList.index(ProcessReadyList.get(ProcessReadyList.curselection()))
            except:
                pass
            ProcessReadyList.delete(0, 'end')
            for item in ProcessList:
                ProcessReadyList.insert("end", core.OutPutCut(item, 150))
                if local1 == -1:
                    continue
                ProcessReadyList.select_set(local1)

        while RefreshFlag:
            time.sleep(0.5)

            if ProcessList == ProcessListCheck:
                pass
            else:
                ProcessListCheck = copy.copy(ProcessList)
                UpgradeList()

    def CommandStart():
        nonlocal flag
        global Pids
        ret = ""
        ret2 = ""
        ret3 = ""
        while True:
            if flag == 0:
                if len(ProcessList) == 0:
                    tkinter.messagebox.showwarning('完成', '已经全部运行完毕')
                    break
                try:
                    os.kill(Pids, signal.SIGTERM)
                except:
                    pass
                Command = ProcessList.pop(0)
                s = subprocess.Popen(
                    Command,
                    cwd=str(Command_HashCat[:-11]),  # cmd特定的查询空间的命令
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,  # 标准输入 键盘
                    encoding='gb2312'
                )

                core.UploadRunList(ProcessList)  # 同步一下文件
                Pids = s.pid
                flag = 1
                while True:
                    time.sleep(0.2)
                    if not ret2.isspace():
                        ret3 = ret2
                    if not ret.isspace():
                        ret2 = ret
                    ret = s.stdout.readline()

                    print(ret)
                    if flag == 0:
                        break
                    if 'Exhausted' in ret:
                        core.SaveResult('(%s) default to run hash\n' % Command)
                        ProcessLabel2.config(text='(%s) default to run hash' % Command)
                    elif 'Cracked' in ret:
                        core.SaveResult('(%s) hash value is (%s)\n' % (Command, ret3))
                        ProcessLabel2.config(text='(%s) hash value is (%s)' % (Command, ret3))
                    elif 'Use --show to display them' in ret:
                        tkinter.messagebox.showwarning('存在运行记录',
                                                       '%s 的目标在先前运行过，请查找历史记录' % (Command))
                    elif 'Stop' in ret:
                        flag = 0

                        break
            else:
                tkinter.messagebox.showwarning('警告', '存在运行中的hashcat')
        StartButton['state'] = 'normal'
        StopButton['state'] = 'disable'

    def Delete(event):
        try:
            local = ProcessReadyList.curselection()[0]
            ProcessReadyList.delete(local)
            ProcessList.pop(local)
            nonlocal local1
            local1 = -1
            core.UploadRunList(ProcessList)

        except:
            tkinter.messagebox.showwarning('警告', '没有选中任何值')
        return

    def ProcessListbox():

        def StopProcess(event):
            nonlocal flag
            global Pids
            StartButton['state'] = 'normal'
            StopButton['state'] = 'disable'
            os.kill(Pids, signal.SIGTERM)
            flag = 0
            Pids = 0
            return

        def StartProcess(event):
            StartButton['state'] = 'disable'
            StopButton['state'] = 'normal'
            t2 = threading.Thread(target=CommandStart)
            t2.start()
            return

        ProcessListBar = Scrollbar(Menu)
        ProcessListBar.config(command=ProcessReadyList.yview)
        ProcessListBar.pack(side="right", fill="y")
        for item in ProcessList:
            ProcessReadyList.insert("end", core.OutPutCut(item, 150))
        ProcessReadyList.pack()

        def Buttons():
            DeleteButton = Button(Menu, text='删除')
            StopButton.bind('<ButtonPress-1>', StopProcess)
            StartButton.bind('<ButtonPress-1>', StartProcess)
            DeleteButton.bind('<ButtonPress-1>', Delete)
            StopButton['state'] = 'disable'
            StartButton.pack(side="left")
            StopButton.pack(side="left")
            DeleteButton.pack(side="right")
            ProcessLabel1.pack(side="left")
            ProcessLabel2.pack(side="left")

            ProcessReadyList.config(yscrollcommand=ProcessListBar.set)

        return Buttons()

    Menu.geometry('1000x600')
    Menu.resizable(False, False)
    Menu.title('缓存hash值')
    ProcessListbox()

    t1 = Thread(target=Refresh)
    t1.start()
    Menu.protocol("WM_DELETE_WINDOW", _Refresh)
    Menu.mainloop()
    return


# 查看历史
def HistoryWindow():
    global SonWindowFlag
    if SonWindowFlag == 1:
        tkinter.messagebox.showwarning('存在打开的子窗口', '检查有无打开的窗口，请先完成上一个子窗口后再继续')
        return
    HistoryShowWindow = tk.Toplevel()
    SonWindowFlag = 1
    HistoryList = Listbox(HistoryShowWindow, width=70, height=25)

    def _HistoryWindow():
        global SonWindowFlag
        SonWindowFlag = 0
        HistoryShowWindow.destroy()

    def HistoryListbox():
        def ClearFunc(event):
            if core.ClearHistory(Command_HashCat[:-11]):
                HistoryList.delete(0, 'end')
                for item in core.GetHistory(Command_HashCat[:-11]):
                    HistoryList.insert("end", core.OutPutCut(item, 70))
                tkinter.messagebox.showwarning('通知', '清除成功')
            else:
                tkinter.messagebox.showerror('错误', '清除失败')

        HistoryListBar = Scrollbar(HistoryShowWindow)
        HistoryListBar.config(command=HistoryList.yview)
        HistoryListBar.pack(side="right", fill="y")
        for item in core.GetHistory(Command_HashCat[:-11]):
            HistoryList.insert("end", core.OutPutCut(item, 70))
        HistoryList.pack()
        ClearHistoryButton = Button(HistoryShowWindow, text='清除全部记录')
        ClearHistoryButton.bind('<ButtonPress-1>', ClearFunc)
        ClearHistoryButton.pack()
        HistoryList.config(yscrollcommand=HistoryListBar.set)

    HistoryShowWindow.geometry('600x500')
    HistoryShowWindow.resizable(False, False)
    HistoryShowWindow.title('历史hash')
    HistoryListbox()
    HistoryShowWindow.protocol("WM_DELETE_WINDOW", _HistoryWindow)
    HistoryShowWindow.mainloop()


# 混合攻击
def StartMix1(value):
    DictionaryLoad = ""

    global SonWindowFlag
    if SonWindowFlag == 1:
        tkinter.messagebox.showwarning('存在打开的子窗口', '检查有无打开的窗口，请先完成上一个子窗口后再继续')
        return
    SonWindowFlag = 1
    MixWindow = tk.Toplevel()
    if value == 0:
        title = "混合攻击1(掩码在后)"
    else:
        title = "混合攻击2(掩码在前)"
    MixWindow.title(title)
    MixWindow.geometry("600x400")
    MaskSet = tk.IntVar()
    MaskSet.set(0)

    def _StartMix1():
        global SonWindowFlag
        SonWindowFlag = 0
        MixWindow.destroy()

    def DictionaryChoose():
        def SelectPath(event):
            # 选择文件path_接收文件地址
            path_ = tkinter.filedialog.askopenfilename()
            if '.txt' not in path_:
                tkinter.messagebox.showerror('错误', '请使用txt格式字典')
                return
            nonlocal DictionaryLoad
            DictionaryLoad = path_
            Label2.config(text=core.OutPutCut(DictionaryLoad, 72))

        Label1 = Label(MixWindow, text="字典:")
        Label2 = Label(MixWindow, text=DictionaryLoad)
        DictionaryButton = Button(MixWindow, text="选择文件")
        DictionaryButton.bind('<ButtonPress-1>', SelectPath)
        Label1.place(x=10, y=10)
        Label2.place(x=120, y=10)
        DictionaryButton.place(x=50, y=8)

    MaskTextbox = Text(MixWindow, width=80, height=8)
    LengthSetSpin = Spinbox(MixWindow, from_=1, to=4096)

    maps = ['?l', '?u', '?d', '?h', '?H', '?s', '?a', '?f']

    def RadioButtons():
        text = ['英文小写', '英文大写', '数字小写', '数字', '小写16进制', '大写16进制', '符号', '全部可见字符']
        b = 10
        for i in range(0, 8):
            Radiobutton(MixWindow, text=text[i], variable=MaskSet, value=i).place(x=b, y=280)
            b += len(text[i]) * 10 + 30

    def SetLength():
        def Textbox():
            MaskTextbox.place(x=10, y=100)
            LengthSetLabel = Label(MixWindow, text='填充长度')

            LengthSetLabel.place(x=10, y=250)
            LengthSetSpin.place(x=100, y=250)

        return Textbox()

    # 掩码填充

    def SetCertainButton():
        def FillMask(event):
            MaskTextbox.insert("insert", maps[MaskSet.get()] * int(LengthSetSpin.get()))

        def UpLoad(event):
            global Command_Dictionary
            global Command_Mask2
            Command_Dictionary = DictionaryLoad
            Command_Mask2 = MaskTextbox.get('0.0', 'end')[:-1]
            if value == 0:
                DictionaryLabel(Command_Dictionary + ' ' + Command_Mask2)
            else:
                DictionaryLabel(Command_Mask2 + ' ' + Command_Dictionary)
            _StartMix1()

        FillButton = Button(MixWindow, text='填充')
        FillButton.bind("<ButtonPress-1>", FillMask)
        FillButton.place(x=500, y=350)
        CertainButton = Button(MixWindow, text='确认')
        CertainButton.bind("<ButtonPress-1>", UpLoad)
        CertainButton.place(x=550, y=350)

    SetLength()
    RadioButtons()
    DictionaryChoose()
    SetCertainButton()
    MixWindow.protocol("WM_DELETE_WINDOW", _StartMix1)
    MixWindow.mainloop()


# 目标选则
def StartChooseAimGUI(event):
    # 单选按钮共用变量
    Aim = ""
    global SonWindowFlag
    if SonWindowFlag == 1:
        tkinter.messagebox.showwarning('存在打开的子窗口', '检查有无打开的窗口，请先完成上一个子窗口后再继续')
        return
    SonWindowFlag = 1
    ChooseAimWindow = tk.Toplevel()
    v = tk.IntVar()
    v.set(2)
    AimLoadLabel = Label(ChooseAimWindow, text='目标路径：')
    Radiobutton(ChooseAimWindow, text='选择文件', variable=v, value=1).place(x=10, y=10)
    Radiobutton(ChooseAimWindow, text='直接输入hash值', variable=v, value=2).place(x=10, y=40)
    InputBoxText = Text(ChooseAimWindow, width=50, height=8)
    CommandAimButton = Button(ChooseAimWindow, text='确定')

    def _StartChooseAimGUI():
        global SonWindowFlag
        SonWindowFlag = 0
        ChooseAimWindow.destroy()

    def AutoChooseMode(Load):
        global Command_HashMode, Command_Aim
        AttackMode = core.CommandSet(Load)

        if AttackMode != '' and v.get() == 1:
            Command_HashMode = '-m ' + str(HashMode[AttackMode])
            HashModeCombobox.set(AttackMode)
            HashModeLabels.config(text=Command_HashMode)
            HashModeLabels.place(x=600, y=150)

    def SelectPath(event):
        # 选择文件path_接收文件地址
        path_ = tkinter.filedialog.askopenfilename()
        nonlocal Aim
        Aim = path_
        AimLoadLabel.config(text='目标路径：' + Aim)

    def Box():
        ChooseFile = Button(ChooseAimWindow, text='选择文件')
        ChooseFile.bind("<ButtonPress-1>", SelectPath)
        InputBoxText.place(x=10, y=75)
        ChooseFile.place(x=100, y=10)

    def UpLoadAim(event):
        global Command_Aim
        if v.get() == 1:
            Command_Aim = Aim
            AutoChooseMode(Command_Aim)
        elif v.get() == 2:
            Command_Aim = InputBoxText.get('0.0', 'end')[:-1]

        AimLabel(Command_Aim)

        CommandAimButton['command'] = _StartChooseAimGUI

    ChooseAimWindow.geometry('600x200')
    ChooseAimWindow.resizable(False, False)  # 能否调整大小
    ChooseAimWindow.title('输入hash值或选择文件')
    AimLoadLabel.place(x=165, y=15)
    Box()
    CommandAimButton.place(x=550, y=160)
    CommandAimButton.bind("<ButtonPress-1>", UpLoadAim)
    ChooseAimWindow.protocol("WM_DELETE_WINDOW", _StartChooseAimGUI)
    ChooseAimWindow.mainloop()
    return


# 掩码攻击
def MaskAttack():
    MaskSet = tk.IntVar()
    MaskSet.set(0)
    global SonWindowFlag
    if SonWindowFlag == 1:
        tkinter.messagebox.showwarning('存在打开的子窗口', '检查有无打开的窗口，请先完成上一个子窗口后再继续')
        return
    SonWindowFlag = 1
    MaskAttackWindow = tk.Toplevel()
    MaskTextbox = Text(MaskAttackWindow, width=80, height=8)
    LengthSetSpin = Spinbox(MaskAttackWindow, from_=1, to=4096)
    MinSpin = Spinbox(MaskAttackWindow, from_=1, to=4096)
    MaxSpin = Spinbox(MaskAttackWindow, from_=1, to=4096)
    maps = ['?l', '?u', '?d', '?h', '?H', '?s', '?a', '?f']

    def _MaskAttack():
        global SonWindowFlag
        SonWindowFlag = 0
        MaskAttackWindow.destroy()

    def RadioButtons():
        text = ['英文小写', '英文大写', '数字', '小写16进制', '大写16进制', '符号', '全部可见字符', '全部字符']
        b = 10
        for i in range(0, 8):
            Radiobutton(MaskAttackWindow, text=text[i], variable=MaskSet, value=i).place(x=b, y=280)
            b += len(text[i]) * 10 + 30

    def SetLength():
        Label(MaskAttackWindow, text='最小长度').place(x=10, y=10)
        Label(MaskAttackWindow, text='最大长度').place(x=10, y=30)

        def Textbox():
            MaskTextbox.place(x=10, y=100)
            LengthSetLabel = Label(MaskAttackWindow, text='填充长度')

            LengthSetLabel.place(x=10, y=250)
            LengthSetSpin.place(x=100, y=250)
            MinSpin.place(x=80, y=10)
            MaxSpin.place(x=80, y=30)

        return Textbox()

    # 掩码填充
    def FillMask(event):
        MaskTextbox.insert("insert", maps[MaskSet.get()] * int(LengthSetSpin.get()))

    # 传递掩码
    def UpLoad(event):
        global Command_Mask1
        global Command_Mask2
        if int(MinSpin.get()) > int(MaxSpin.get()):
            tkinter.messagebox.showerror('错误', '最大值必须大于等于最小值')
            return 0

        Command_Mask1 = '--increment --increment-min ' + MinSpin.get() + ' --increment-max ' + MaxSpin.get()
        Command_Mask2 = MaskTextbox.get('0.0', 'end')[:-1]
        if int(MinSpin.get()) > len(Command_Mask2) / 2:
            tkinter.messagebox.showerror('错误', '掩码个数过少')
            return
        elif int(MaxSpin.get()) < len(Command_Mask2) / 2:
            tkinter.messagebox.showerror('错误', '掩码个数过多')
            return
        DictionaryLabel(Command_Mask2)
        _MaskAttack()

    # 确认键
    def SetCertainButton():
        FillButton = Button(MaskAttackWindow, text='填充')
        FillButton.bind("<ButtonPress-1>", FillMask)
        FillButton.place(x=500, y=350)
        CertainButton = Button(MaskAttackWindow, text='确认')
        CertainButton.bind("<ButtonPress-1>", UpLoad)
        CertainButton.place(x=550, y=350)

    MaskAttackWindow.geometry('600x400')
    MaskAttackWindow.title('掩码设置')
    MaskAttackWindow.resizable(False, False)
    SetCertainButton()
    RadioButtons()
    SetLength()
    MaskAttackWindow.protocol('WM_DELETE_WINDOW', _MaskAttack)
    MaskAttackWindow.mainloop()


# 字典设置
def ChooseDictionary(mode):
    DictionaryLoad = " "
    DictionaryLoad2 = " "
    global SonWindowFlag
    if SonWindowFlag == 1:
        tkinter.messagebox.showwarning('存在打开的子窗口', '检查有无打开的窗口，请先完成上一个子窗口后再继续')
        return
    SonWindowFlag = 1
    ChooseDictionaryWindow = tk.Toplevel()
    DictionaryFLoadLabel = Label(ChooseDictionaryWindow, text=core.OutPutCut(DictionaryLoad, 68))
    DictionarySLoadLabel = Label(ChooseDictionaryWindow, text=core.OutPutCut(DictionaryLoad2, 68))
    CertainButton = Button(ChooseDictionaryWindow, text='确定')
    ChooseDictionarySButton = Button(ChooseDictionaryWindow, text='选择字典2')
    ChooseDictionaryFButton = Button(ChooseDictionaryWindow, text='选择字典1')
    DictionaryMidText = Text(ChooseDictionaryWindow, width=70, height=1)

    def _ChooseDictionary():
        global SonWindowFlag
        SonWindowFlag = 0
        ChooseDictionaryWindow.destroy()

    def DictionLabel():

        DictionaryMidLabel = Label(ChooseDictionaryWindow, text='衔接内容:')
        DictionaryFLabel = Label(ChooseDictionaryWindow, text='字典1:')
        DictionarySLabel = Label(ChooseDictionaryWindow, text='字典2:')

        DictionaryFLabel.place(x=10, y=10)
        DictionarySLabel.place(x=10, y=120)
        DictionaryMidLabel.place(x=10, y=70)

    def SelectPath(event):
        # 选择文件path_接收文件地址
        path_ = tkinter.filedialog.askopenfilename()
        if '.txt' not in path_:
            tkinter.messagebox.showerror('错误', '请使用txt格式字典')
            return

        nonlocal DictionaryLoad
        DictionaryLoad = path_
        DictionaryFLoadLabel.config(text=core.OutPutCut(DictionaryLoad, 68))

    def SelectPath2(event):
        # 选择文件path_接收文件地址
        path_ = tkinter.filedialog.askopenfilename()
        if '.txt' not in path_:
            tkinter.messagebox.showerror('错误', '请使用txt格式字典')
            return
        nonlocal DictionaryLoad2
        DictionaryLoad2 = path_
        DictionarySLoadLabel.config(text=core.OutPutCut(DictionaryLoad2, 68))

    def Send(event):
        global Command_Dictionary
        if mode == 0:
            Command_Dictionary = DictionaryLoad
        elif (mode == 1) and (DictionaryMidText.get('0.0', 'end') != '\n'):
            Command_Dictionary = DictionaryLoad + ' -j \'$' + DictionaryMidText.get('0.0', 'end')[
                                                              :-1] + '\' ' + DictionaryLoad2
        else:
            Command_Dictionary = DictionaryLoad + ' ' + DictionaryLoad2
        DictionaryLabel(Command_Dictionary)
        CertainButton['command'] = _ChooseDictionary

    def ChooseDictionarys():
        ChooseDictionaryFButton.bind("<ButtonPress-1>", SelectPath)
        ChooseDictionaryFButton.place(x=75, y=7)
        CertainButton.bind("<ButtonPress-1>", Send)
        CertainButton.place(x=550, y=160)
        DictionaryFLoadLabel.place(x=140, y=10)

        ChooseDictionarySButton.bind("<ButtonPress-1>", SelectPath2)
        ChooseDictionarySButton.place(x=75, y=120)
        DictionarySLoadLabel.place(x=140, y=120)

    ChooseDictionarySButton['state'] = 'normal'
    DictionaryMidText['state'] = 'normal'
    if mode == 0:
        ChooseDictionarySButton['state'] = 'disable'
        DictionaryMidText['state'] = 'disable'

    ChooseDictionaryWindow.title('字典选择')
    ChooseDictionaryWindow.geometry('600x200')
    ChooseDictionaryWindow.resizable(False, False)  # 能否调整大小
    DictionLabel()
    ChooseDictionarys()
    DictionaryMidText.place(x=75, y=70)
    ChooseDictionaryWindow.protocol('WM_DELETE_WINDOW', _ChooseDictionary)
    ChooseDictionaryWindow.mainloop()
    return


# 主窗口
def MainWindowBoard():
    # 设置下拉框格式
    ComboStyle = tkinter.ttk.Style()
    ComboStyle.theme_create('Main', parent='alt',
                            settings={'TCombobox':
                                {'configure':
                                    {
                                        'foreground': 'white',
                                        'selectbackground': '#3BBCD6',  # 选择后的背景颜色
                                        'fieldbackground': '#363636',  # 下拉框颜色
                                        'background': '#363636',  # 背景颜色
                                        "font": 10,  # 字体大小
                                        "font-weight": "bold",

                                    }}}
                            )
    ComboStyle.theme_use('Main')

    # 任务栏
    def TitleMap():

        def MoveButtonFun():
            def drag_start(event):
                # 记录鼠标按下的坐标
                event.widget.start_x = event.x
                event.widget.start_y = event.y

            def drag_motion(event):
                # 计算鼠标的偏移量
                x = event.widget.winfo_x() - event.widget.start_x + event.x
                y = event.widget.winfo_y() - event.widget.start_y + event.y
                MainWindows[0] += x
                MainWindows[1] += y
                # 移动窗口部件到新的位置
                MainWindow.geometry('+%s+%s' % (MainWindows[0], MainWindows[1]))

            # 拖动栏
            MoveButton = Canvas(MainWindow, bg=MainWindowBoards[0][0], width=MainWindows[3].split('x')[0],
                                height=27)  # 使用截取，截前半部分的屏幕长度
            MoveTitle = Canvas(MainWindow, bg=MainWindowBoards[0][1], width=MainWindows[3].split('x')[0] + str(50),
                               height=1)
            SplitBar = Canvas(MainWindow, bg=MainWindowBoards[0][1], width=1, height=400)
            MoveTitle.config(highlightthickness=False)
            SplitBar.config(highlightthickness=False)
            MoveButton.config(highlightthickness=False)  # 取消边框
            MoveButton.bind("<ButtonPress-1>", drag_start)  # 按下处理
            MoveButton.bind("<B1-Motion>", drag_motion)  # 移动处理
            SplitBar.place(x=720, y=27)
            MoveButton.place(x=0, y=0)
            MoveTitle.place(x=0, y=27)

        def CloseButtonFun():
            # 关闭按钮
            def func():
                try:
                    os.kill(Pids, signal.SIGTERM)
                except:
                    pass
                MainWindow.destroy()

            def CloseMainWindow():
                CloseButton['command'] = func

            CloseButton = Button(MainWindow, bg=MainWindowBoards[0][0], text='X', fg=MainWindowBoards[1][0], width=3)
            CloseButton.config(borderwidth=0)
            CloseButton.place(x=int(MainWindows[3].split('x')[0]) - 28)
            CloseButton.bind("<Button-1>", CloseMainWindow())

        def ChangeWindows():
            def func():
                global MainWindows
                x = int(MainWindows[3].split('x')[0])
                if MainWindows[4] == 0:
                    x += 200
                    MainWindows[4] = 1
                    CloseButton.config(text='<')
                else:
                    x -= 200
                    MainWindows[4] = 0
                    CloseButton.config(text='>')

                MainWindows[3] = str(x) + 'x400'
                MainWindow.geometry(MainWindows[3])

            def CloseMainWindow():
                CloseButton['command'] = func

            CloseButton = Button(MainWindow, bg=MainWindowBoards[0][0], text='>', fg=MainWindowBoards[1][0], width=3)
            CloseButton.config(borderwidth=0)
            CloseButton.place(x=int(MainWindows[3].split('x')[0]) - 60)
            CloseButton.bind("<Button-1>", CloseMainWindow())

        return MoveButtonFun(), CloseButtonFun(), ChangeWindows()

    # 选择hashcat的路径
    def ChooseHashCatVersion():
        global Command_HashCat, HashMode
        value = Command_HashCat
        if len(value) > 50:
            value = value[:50] + '...'
        GHashCatVersionLabel = Label(text=value, background=MainWindows[2],
                                     foreground=MainWindowBoards[1][0])

        # 显示并同步上一次的路径
        def SavedPath():
            global Command_HashCat
            Command_HashCat = core.SearChHashCatLoad()
            if Command_HashCat:
                HashCatVersionLabels()

        # 选择HashCat版本模块
        def ChooseHashCatVersionLabels():

            HashCatVersionLabel = Label(text="选择HashCat", background=MainWindows[2],
                                        foreground=MainWindowBoards[1][0])
            HashCatVersionLabel.place(x=50, y=28)

        # 刷新hashcat路径所在文本
        def HashCatVersionLabels():
            value = Command_HashCat
            if len(value) > 60:
                value = value[:60] + '...'
            GHashCatVersionLabel.config(text=value)
            GHashCatVersionLabel.place(x=245, y=50)

        def selectPath():
            # 选择文件path_接收文件地址
            path_ = tkinter.filedialog.askopenfilename()
            global Command_HashCat, HashMode
            Command_HashCat = path_
            HashCatVersionLabels()

            core.SaveHashCatLoad(path_)

        # 设置hashcat位置
        def SetHashCatVersion(event):
            for file in HashCatLoad:
                if HashCatVersionCombox.get() in file:
                    global Command_HashCat
                    Command_HashCat = file
                    HashCatVersionLabels()
                    return

        def ChooseHashCatLoadButton():
            HashCatLoadButton = Button(text='...', command=selectPath, bg=MainWindows[2], fg=MainWindowBoards[0][1],
                                       font=('Helvetica', 15))
            HashCatLoadButton.configure(borderwidth=0)
            HashCatLoadButton.place(x=215, y=40)

        HashCatVersionCombox = ttk.Combobox()
        HashCatVersionCombox['value'] = HashCatVersion
        HashCatVersionCombox.config(background=MainWindowBoards[0][0])
        HashCatVersionCombox.place(x=50, y=50)
        HashCatVersionCombox.bind("<<ComboboxSelected>>", SetHashCatVersion)

        return SavedPath(), ChooseHashCatVersionLabels(), ChooseHashCatLoadButton(),

    # 设置攻击方式
    def ChooseAttackMode():
        SetAttackModes = {'字典攻击': 0, '组合攻击': 1, '掩码攻击': 3, '混合攻击1': 6, '混合攻击2': 7}
        AttackModeLabel = Label(text=Command_AttackMode, background=MainWindows[2],
                                foreground=MainWindowBoards[1][0])

        def SetAttackMode(event):
            global Command_AttackMode
            global Command_Mask1, Command_Mask2, Command_Dictionary
            Command_Mask1 = ""
            Command_Mask2 = ""
            Command_Dictionary = ""
            DictionaryLabel(Command_Mask1)
            Command_AttackMode = '-a ' + str(SetAttackModes[AttackModeCombobox.get()])

            return ShowAttackModeLabel()

        def SetAttackModeLabel():
            AttackModeLabel = Label(text="攻击模式", background=MainWindows[2], foreground=MainWindowBoards[1][0])
            AttackModeLabel.place(x=50, y=75)

        def ShowAttackModeLabel():
            AttackModeLabel.config(text=Command_AttackMode)
            AttackModeLabel.place(x=220, y=100)

        AttackModeCombobox = ttk.Combobox(MainWindow)
        AttackModeCombobox['value'] = list(SetAttackModes.keys())
        AttackModeCombobox.config(background=MainWindowBoards[0][0])
        AttackModeCombobox.place(x=50, y=100)
        AttackModeCombobox.bind("<<ComboboxSelected>>", SetAttackMode)

        return SetAttackModeLabel()

    # 哈希类型
    def ChooseHashMode():

        def ShowHashCatModeLabel():
            HashModeLabels.config(text=Command_HashMode)
            HashModeLabels.place(x=600, y=150)

        def ChooseHashModeLabel():
            HashModeLabel = Label(text="hash类型", background=MainWindows[2], foreground=MainWindowBoards[1][0])
            HashModeLabel.place(x=50, y=125)

        def SetHashModeLabel(event):
            global Command_HashMode
            Command_HashMode = '-m ' + str(HashMode[HashModeCombobox.get()])
            return ShowHashCatModeLabel()

        HashModeCombobox['value'] = list(HashMode.keys())
        HashModeCombobox.config(background=MainWindowBoards[0][0], width=72)
        HashModeCombobox.place(x=50, y=150)
        HashModeCombobox.bind("<<ComboboxSelected>>", SetHashModeLabel)
        return ChooseHashModeLabel()

    # 设置掩码
    def ChooseMaskMode():

        # 判断攻击模式
        def Mode(event):
            if '0' in Command_AttackMode:
                return ChooseDictionary(0)
            elif '3' in Command_AttackMode:
                return MaskAttack()
            elif '1' in Command_AttackMode:
                return ChooseDictionary(1)
            elif '6' in Command_AttackMode:
                return StartMix1(0)
            elif '7' in Command_AttackMode:
                return StartMix1(1)
            else:
                return DictionaryWarning()

        OpenNewMaskUI = Button(text='掩码/字典设置', bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
        OpenNewMaskUI.config(highlightthickness=False, borderwidth=0)
        OpenNewMaskUI.place(x=50, y=185)
        OpenNewMaskUI.bind("<Button-1>", Mode)

    def ChooseAimButton():
        AimButton = Button(text='目标文件', bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
        AimButton.config(highlightthickness=False, borderwidth=0)
        AimButton.bind("<Button-1>", StartChooseAimGUI)
        AimButton.place(x=50, y=220)

    # 展开边框
    def Sidebar():
        def History():
            def StartHistoryWindow(event):
                HistoryWindow()

            OpenHistoryButton = Button(text='历史记录', bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
            OpenHistoryButton.config(highlightthickness=False, borderwidth=0)
            OpenHistoryButton.bind("<Button-1>", StartHistoryWindow)
            OpenHistoryButton.place(x=800, y=40)

        def CheckCudaLabel():
            if MainWindows[5]:
                Cuda = "检测到Cuda"
                Color = 'green'
            else:
                Cuda = "未检测到Cuda"
                Color = 'red'
            CudaLabel = Label(MainWindow, text=Cuda, background=MainWindows[2],
                              foreground=Color)
            CudaLabel.place(x=730, y=90)

        def UploadHashCatMode():
            def Upload(event):
                if GetHashAttackMode.UploadFun():
                    tkinter.messagebox.showwarning('更新完毕')
                else:
                    tkinter.messagebox.showerror('错误', '更新失败，请检查网络或联系开发者')

            UploadButton = Button(text='更新hashcat掩码攻击方式', bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
            UploadButton.config(highlightthickness=False, borderwidth=0)
            UploadButton.place(x=730, y=140)
            UploadButton.bind("<Button-1>", Upload)

        def SetForce():
            ForceSetButton = Checkbutton(text='忽略警告', variable=ForceInt)
            MachineSetButton = Checkbutton(text='简单输出模式', variable=MachineInt)
            ForceSetButton.config(bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
            ForceSetButton.bind("<Button-1>", lambda event: core.SetForce(not ForceInt.get()))
            MachineSetButton.config(bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
            MachineSetButton.bind("<Button-1>", lambda event: core.SetMachine(not MachineInt.get()))

            ForceSetButton.place(x=730, y=180)
            MachineSetButton.place(x=730, y=220)
            # 测试速度

        def ClearData():

            def ClearDataCommand(event):
                core.RunCommand(Command_HashCat[:-11], Command_HashCat + ' -b')

            ClearDataButton = Button(text='测试速度', bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
            ClearDataButton.config(highlightthickness=False, borderwidth=0)
            ClearDataButton.place(x=730, y=40)
            ClearDataButton.bind("<Button-1>", ClearDataCommand)

        return ClearData(), CheckCudaLabel(), History(), UploadHashCatMode(), SetForce()

    def LowerRight():
        def GUIStartButton():
            def StartRunCommand(event):
                WordSet()

            StartButton = Button(text='-运行-', bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
            StartButton.config(highlightthickness=False, borderwidth=0)
            StartButton.bind("<Button-1>", StartRunCommand)
            StartButton.place(x=600, y=350)

            MenuHashCatButton = Button(text='运行目录', bg=MainWindowBoards[0][0], fg=MainWindowBoards[0][1])
            MenuHashCatButton.config(highlightthickness=False, borderwidth=0)
            MenuHashCatButton.bind("<Button-1>", OpenMenu)
            MenuHashCatButton.place(x=650, y=350)

        return GUIStartButton()

    return (TitleMap(), ChooseHashCatVersion(), ChooseAttackMode(), ChooseHashMode(), ChooseMaskMode(), Sidebar(),
            ChooseAimButton(), LowerRight())


if __name__ == '__main__':
    if core.CudaTest() == 0:
        pass
    else:
        MainWindows[5] = False
        tkinter.messagebox.showwarning("警告", "没有找到cuda，hashcat将使用cpu运算，无法达到最高性能")
    HashMode = core.ReadingAttackMode()
    ProcessList = list(core.GetRunList())
    MainWindows[5] = True
    MainWindowBoard()
    # 窗口运行
    MainWindow.mainloop()
