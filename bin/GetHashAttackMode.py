import random
from bs4 import BeautifulSoup
import re
import requests
import json
import core

list_num = []
list_name = []
s = {}
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']

url = 'https://hashcat.net/wiki/doku.php'  # hashcat格式存放处
params = {'id': 'example_hashes'}


def UploadFun():
    head = {"User-Agent": user_agent_list[int(random.uniform(0, 9))]}
    try:
        response = requests.get(url, params=params, headers=head)
        soup = BeautifulSoup(response.text, "html.parser")
        for i in soup.body.find_all('tr'):

            HTML_body = str(i)
            # 正则表达
            Ruler_num = re.search(r'<td class="col0"> (\d{0,10}) <', HTML_body)
            Ruler_name = re.search(r'<td class="col1"> ([^<]*) <', HTML_body)
            try:
                s[Ruler_name.group(1)] = Ruler_num.group(1)
            except:
                continue
    except IOError as e:
        print(e.errno)
        return False
    with open(core.RootLoad + 'data\\AttackMode.json', "w") as f:
        json.dump(s, f)
    return True
