import os
import json
import subprocess
import time

ZipCatRunLoad = os.getcwd()  # ./ZipCat/bin/ 程序运行时位置

RootLoad = ZipCatRunLoad  # 程序运行的根目录

HashCatFiles = RootLoad + "\\hashcat\\"  # hashcat 储存不同版本hashcat的目录
SuffixList = []
HashCatLoad = []
HashCatVersion = []
data = {'path': '', 'Dictionary': []}
flag = 0
RunningList = {}
# 查找hashcat地址

for file in os.listdir(HashCatFiles):
    if "hashcat-" in file:
        HashCatLoad.append(HashCatFiles + file + '\\Hashcat.exe')
        HashCatVersion.append(file)

# 读取设置
with open(RootLoad + "\\data\\Setting.json", 'r') as f:
    data = json.load(f)
with open(RootLoad + "\\data\\RunningList.json", 'r') as file:
    RunningList = json.load(file)


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


def ReadingAttackMode():
    global RootLoad
    with open(RootLoad + '\\data\\AttackMode.json', 'r') as file:
        Dictionary = json.load(file)
    return Dictionary


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


# 删除历史记录
def ClearHistory(Load):
    HistoryLoad = Load + 'hashcat.potfile'
    with open(HistoryLoad, 'w') as file:
        pass
    return True


# 读取历史记录

def GetHistory(Load):
    HistoryList = []
    HistoryLoad = Load + 'hashcat.potfile'
    with open(HistoryLoad, 'r') as file:
        for elem in file.readlines():
            HistoryList.append(elem)
    return HistoryList


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


def GetRunList():
    global RunningList
    with open(RootLoad + "\\data\\RunningList.json", 'r') as file:
        RunningList = json.load(file)
    return RunningList


def UploadRunList(List):
    with open(RootLoad + "\\data\\RunningList.json", 'w') as file:
        json.dump(List, file)
    return True


# 自动匹配攻击类型

def CommandSet(form):
    form = str(form).split('.')[1]
    SuffixDictionary = {'7z': '7-Zip', 'hc22000': 'WPA-PBKDF2-PMKID+EAPOL'}
    Commands = ""
    try:
        Commands = SuffixDictionary[form]
    except:
        pass
    print(Commands, form)
    return Commands


# 存储结果
def SaveResult(Res):
    with open(RootLoad + '\\data\\Result\\%s' % time.strftime('%y_%m_%d_%H.txt', time.localtime()), 'a') as f:
        f.write(Res)
