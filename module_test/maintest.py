# encoding:utf-8
#图像识别完整的代码
import requests,base64
import re
import jieba
import json
# import picamera
import time
def lajitype(name):
    TXmykey="9f24a5e1f94efda4a631bf1da207b002"
    url="http://api.tianapi.com/txapi/lajifenlei/index?key="+TXmykey+"&word="
    url+=name
    response=requests.post(url)
    if(response.status_code!=200):#出错
        return -1
    resJson=response.json()
    print(resJson)

def BDident(jpgfile):
    appid = '20248707'
    api_key = 'F5HqGj2qafe4S4XABw2rqX9K'
    secret_key = 'EsnxjFCnyZaZyUrFN3jorYlZKjzCWN1q'

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+secret_key
    response = requests.post(host)

    access_token = response.json()['access_token']

    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    # 二进制方式打开图片文件base64编码
    f = open(jpgfile, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}

    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    # if response:
    #      print (response.json())
    resJson=response.json()
    res={}
    lajiText=""
    if(resJson.get("result")):
        lajilist=resJson["result"]
        print(lajilist)
        for item in lajilist:
            lajiText+=","+item.get("keyword")
            res[item.get("keyword")]=(item.get("score"),-1)
    # 关键词分割
    wordlist=jieba.lcut(lajiText)
    words={}
    for word in wordlist:
        if len(word)>1:
            words[word]=words.get(word,0)+1
    wordlist=list(words.items())
    wordlist=sorted(wordlist,key = lambda x:x[1],reverse=True)
    print("------")
    print(wordlist)
    print(wordlist[0][0])
    return wordlist[0][0]

    # ls=list(res.items())
    # ls=sorted(ls,key = lambda x:x[1][0],reverse=True)
    # print(ls)
    # # return ls
    # for i in response.json()['result']:
    #     strr=str(i)# 识别结果序列
    #     result_list = {}
    #     result_list['name'] = re.findall('\{\'score\': .*?, \'root\': .*?, \'keyword\': \'(.*?)\'}', strr)
    #     print(result_list['name'])
data = [{}]
def updateUI(i,name,weight,price):
    
    data[i]['name'] = name
    data[i]['weight'] = weight
    data[i]['price'] = price
    url_json = 'http://127.0.0.1:8080'
    data_json = json.dumps(data)
    r_json = requests.post(url_json,data_json)
    print(data_json)
    print(r_json)
    print(r_json.text)
    print(r_json.content)

if __name__=="__main__":
    # Camera=picamera.PiCamera()
    # Camera.capture("image.jpg")
    time.sleep(1)
    name=BDident("image.jpg")
    updateUI(0,name,"0.3kg","3RMB")
    time.sleep(1)
    name=BDident("image.jpg")
    updateUI(1,name,"1kg","10RMB")