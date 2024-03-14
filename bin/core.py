import os
import json
import subprocess
import signal
from threading import Thread


ZipCatRunLoad = os.getcwd()  # ./ZipCat/bin/ 程序运行时位置

RootLoad = ZipCatRunLoad[:-3]  # 程序运行的根目录

HashCatFiles = RootLoad + "hashcat\\"  # hashcat 储存不同版本hashcat的目录
SuffixList = []
HashCatLoad = []
HashCatVersion = []
data = {'path': '', 'Dictionary': []}
flag = 0
# 查找hashcat地址
for file in os.listdir(HashCatFiles):
    if "hashcat-" in file:
        HashCatLoad.append(HashCatFiles + file + '\\Hashcat.exe')
        HashCatVersion.append(file)
# 读取设置
with open(RootLoad + "\\data\\Setting.json", 'r') as f:
    data = json.load(f)


# 保存Hashcat路径
def SaveHashCatLoad(path):
    data['path'] = path
    with open(RootLoad + "\\data\\Setting.json", 'w') as file:
        json.dump(data, file)


# 保存Dictionary路径
def SaveDictionaryLoad(path):
    if path is not None:
        data['Dictionary'].append(path)
    with open(RootLoad + "\\data\\Setting.json", 'w') as file:
        json.dump(data, file)


# 读取hashcat路径
def SearChHashCatLoad():
    return data['path']


# 读取字典路径
def SearchDictionaryLoad():
    return data['Dictionary']


# 检测选择文件是否格式合理
def FileCheck(FileLoad):
    if '.' in FileLoad:
        suffix = str(FileLoad).split('.')[1]
        if suffix in SuffixList:
            return 0
    return 1


PidList1 = 0


def RunCommand(Load, HashCommands):
    global PidList1
    print(HashCommands)
    print(Load)
    if len(HashCommands) > 3:
        KillCommand()
        s = subprocess.Popen(
            HashCommands,
            cwd=str(Load),  # cmd特定的查询空间的命令
            stdin=None,  # 标准输入 键盘
            encoding='gb2312'
        )
        PidList1 = s.pid
    else:
        return -1


def ReadingAttackMode():
    global RootLoad
    with open(RootLoad + 'data\\AttackMode.json', 'r') as file:
        Dictionary = json.load(file)
    return Dictionary


def KillCommand():
    global PidList1
    if PidList1 != 0:
        try:
            os.kill(PidList1, signal.SIGTERM)
            PidList1 = 0
        except:
            PidList1 = 0
            return -1
    else:
        return -1


# 运行
# 检测cuda环境
def CudaTest():
    CudaRet = subprocess.Popen(
        'nvcc -V',  # cmd特定的查询空间的命令
        stdin=None,  # 标准输入 键盘
        encoding='gb2312',
        stdout=subprocess.DEVNULL
    )
    if 'NVIDIA (R) Cuda' in str(CudaRet.communicate()[0]):
        return 1
    else:
        return 0


# 读取记录
def ReadHistory(Load):
    HistoryLoad = Load + 'hashcat.potfile'
    HistoryList = []
    with open(HistoryLoad, 'r') as file:
        for line in file.readlines():
            HistoryList.append(line.strip('\n'))

        return HistoryList


def ClearHistory(Load):
    HistoryLoad = Load + 'hashcat.potfile'
    with open(HistoryLoad, 'w') as file:
        pass
    return True


# 防止词过长
def OutPutCut(words, lens):
    value = words
    if len(value) > lens:
        value = value[:lens] + '...'
    return value


def SetForce(value):
    with open(RootLoad + "\\data\\Setting.json", 'w') as file:
        data['Force'] = value
        json.dump(data, file)
    return


def ReadForce():
    return data['Force']


def SetMachine(value):
    with open(RootLoad + "\\data\\Setting.json", 'w') as file:
        data['Machine'] = value
        json.dump(data, file)
    return


def ReadMachine():
    return data['Machine']


def CommandSet(form):
    form = str(form).split('.')[1]
    SuffixDictionary = {'7z': '7-Zip', 'hc22000': 'WPA-PBKDF2-PMKID+EAPOL'}
    Commands = ""
    CommandAim = ""
    try:
        Commands = SuffixDictionary[form]
    except:
        pass
    print(Commands,form)
    return Commands


# 测试

if __name__ == '__main__':
    print(ReadHistory('D:\\tools\\ZipCat_GUI\\hashcat\\hashcat-6.2.6\\'))
