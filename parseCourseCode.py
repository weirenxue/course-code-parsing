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
    url = "https://course.tchcvs.tc.edu.tw/QueryCode.asp?T="
    x = {}
    for key, value in categories.items():
        x[key] = {}
        print(key, value)
        response = requestsWithTor(url + value)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        allTr = soup.find('table').find_all('tr')
        for tr in allTr:
            allTd = tr.find_all('td')
            if allTd != []:
                x[key][allTd[0].text] = allTd[1].text.replace('\r','').replace('\n','')
                
    key = '科目名稱代碼'
    x[key] = {}
    response = requestsWithTor(url + 'CATATT')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    allTr = soup.find('table').find_all('tr')
    for tr in allTr:
        allTd = tr.find_all('td')
        if allTd != []:
            x[key][allTd[3].text] = x[key][allTd[3].text] if allTd[3].text in x[key] else []
            x[key][allTd[3].text].append({
                '課程類別': getDictKey(x['課程類別'], allTd[0].text),
                '科目屬性': getDictKey(x['科目屬性'], allTd[1].text),
                '領域名稱': allTd[2].text,
                'Desc': allTd[4].text
            })
    
    with open('codeMap.json', 'w', encoding="utf-8") as outfile:
        #要有indent，輸出才會漂亮；ensure_ascii=False才可輸出中文，否則會輸出unicode
        json.dump(x, outfile, indent=4, ensure_ascii=False)
else:
    print('Not in tor with IP ' + config['ip'])
