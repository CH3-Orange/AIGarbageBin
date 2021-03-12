import requests
import json

def updateUI():
    data = [{}]
    data[0]['name'] = '商品名'
    data[0]['weight'] = '重量'
    data[0]['price'] = '价格'
    url_json = 'http://127.0.0.1:8080'
    data_json = json.dumps(data)
    r_json = requests.post(url_json,data_json)
    print(data_json)
    print(r_json)
    print(r_json.text)
    print(r_json.content)
