import json
import requests
import string
from bs4 import BeautifulSoup

def checkTorConfig():
    url = "https://check.torproject.org/"
    proxies = globals()['proxies'] if 'proxies' in globals() else {} 
    headers = globals()['headers'] if 'headers' in globals() else {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
    response = requests.get(url, headers = headers, proxies = proxies)
    soup = BeautifulSoup(response.text, "html.parser")
    return {'ip': soup.find('strong').text, 'withTor': 'Congratulations' in soup.find('h1').text}
def requestsWithTor(url):
    proxies = globals()['proxies'] if 'proxies' in globals() else {} 
    headers = globals()['headers'] if 'headers' in globals() else {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
    return requests.get(url, headers = headers, proxies = proxies)
def getDictKey(dict, val):
    for key, value in dict.items():
         if val == value:
             return key
    return None

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

config = checkTorConfig()
if config['withTor']:
    print('In tor with IP ' + config['ip'])
    categories = {'課程類型':'SCH', '群別代碼':'GRP', '科別代碼':'DEP', '班群':'CLA', '課程類別':'CAT', '開課方式':'MOD', '科目屬性':'ATT1', '領域名稱':'FLD'}
    url = "https://k12ea.ssivs.chc.edu.tw/setCode.aspx?g=S"
    response = requestsWithTor(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text.replace('<BR/>', ' '), "html.parser")
    mapArray = soup.find('span', id='Label1').text.split()
    x = {}
    for i in range(0, len(mapArray)//2):
        x[mapArray[i * 2]] = mapArray[i * 2 + 1]
    with open('schoolCodeMap.json', 'w', encoding="utf-8") as outfile:
        #要有indent，輸出才會漂亮；ensure_ascii=False才可輸出中文，否則會輸出unicode
        json.dump(x, outfile, indent=4, ensure_ascii=False)
else:
    print('Not in tor with IP ' + config['ip'])
