# encoding:utf-8
#图像识别完整的代码
import requests,base64
import re
import jieba
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
    # print("------")
    # print(wordlist)
    # 关键词垃圾查询
    

    ls=list(res.items())
    ls=sorted(ls,key = lambda x:x[1][0],reverse=True)
    print(ls)
    return ls
    # for i in response.json()['result']:
    #     strr=str(i)# 识别结果序列
    #     result_list = {}
    #     result_list['name'] = re.findall('\{\'score\': .*?, \'root\': .*?, \'keyword\': \'(.*?)\'}', strr)
    #     print(result_list['name'])
if __name__=="__main__":
    # BDident('D:\Program\Python\RaspberryPi\image.jpg')
    lajitype("牙膏")