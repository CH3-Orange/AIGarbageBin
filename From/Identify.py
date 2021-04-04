import requests,base64
import re
import jieba

def identify(_jpgfile):
    
    jpg = open(_jpgfile, "rb")
    mykey="9f24a5e1f94efda4a631bf1da207b002"
    jpg64 =  base64.b64encode(jpg.read())
    jpg.close()
    url = 'http://api.tianapi.com/txapi/imglajifenlei/'
    body = {
        "key": mykey,
        "img": jpg64.decode(),
    }
    # print(body)
    headers = {'content-type': "application/x-www-form-urlencoded"}
    response = requests.post(url,headers=headers, data=body )
    if(response.status_code!=200):#出错
        return -1
    resJson=response.json()
#     print(resJson)
    res={}
    if(resJson.get("newslist")):
        lajilist=resJson["newslist"]
        for item in lajilist:
            res[item.get("name")]=(item.get("trust"),item.get("lajitype"))

    # print(res)
    ls=list(res.items())
    ls=sorted(ls,key= lambda x:x[1],reverse=True)
    #print(ls)
    return ls

def lajitype(name):
    TXmykey="9f24a5e1f94efda4a631bf1da207b002"
    url="http://api.tianapi.com/txapi/lajifenlei/index?key="+TXmykey+"&word="
    url+=name
    response=requests.post(url)
    
    if(response.status_code!=200):#出错
        return -1
    resJson=response.json()
    print(resJson)
    if(resJson.get("code")==250):#出错
        return -1
    res={}
    if(resJson.get("newslist")):
        lajilist=resJson["newslist"]
        for item in lajilist:
            res[item.get("type")]=res.get(item.get("type"),0)+1

    # print(res)
    ls=list(res.items())#(垃圾类别编号，出现次数)
    type_to_name=["可回收","有害垃圾","湿垃圾","干垃圾"]
    # 0为可回收、1为有害、2为厨余(湿)、3为其他(干)
    ls=sorted(ls,key= lambda x:x[1],reverse=True)
    print(ls)
    return ls


def BDident(jpgfile):
    # appid = '20248707'
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
        # print(lajilist)
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
    print("---分词结果---")
    print(wordlist)
    print(wordlist[0][0])
    print("-------------")
    return wordlist[0][0]


def BDTXidentify(jpgfile):
    ljname= BDident(jpgfile)
    ljtype=lajitype(ljname)
    if ljtype==-1:
        return -1
    type_to_name=["可回收","有害垃圾","湿垃圾","干垃圾"]
    return (ljname,ljtype[0][0],type_to_name[ljtype[0][0]])
    


if __name__=="__main__":
    print(BDTXidentify(r'D:\Program\Python\RaspberryPi\AIGarbageBin\From\test.jpg'))