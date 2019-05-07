#-*-encoding:utf-8-*-
#-*-encoding:utf-8-*-
from urllib.request import urlopen,quote
import json
import pandas as pd
import os

def getContent():
    path = r'G:\创业就业指导\data\wit.csv'
    content = open(path)
    content = pd.read_csv(content)
    price = content["平均工资"]
    company = content["企业名称"]
    company_dic={}
    for x in range(len(company)):
        if company[x] not in company_dic:
            price[x]=int(price[x])/1000*8
            company_dic[company[x]]=price[x]
    splitCompany(company_dic)

def getAdress(address):
  map_url = 'http://api.map.baidu.com/geocoder/v2/'
  output = 'json'
  ak = 'Your_BaiDu_ak'
  add = quote(address)#查询地点进行转码
  uri = map_url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
  req = urlopen(uri)
  res = req.read().decode()
  temp = json.loads(res)
  return temp

address_result = []
def splitCompany(company_dic):
    for x in company_dic:
        company_name = x
        print(company_name)
        company_price = company_dic[x]
        reserch = getAdress(company_name)
        if reserch['status'] == 0 :
            reserch['result']['location']['count'] = str(company_price)
            address_result.append(reserch['result']['location'])
    reserve(address_result)

def reserve(sddress_result):
    with open(os.getcwd()+r'\coordinate.txt','w',encoding = 'utf-8') as cd:
        cd.write(str(address_result))
        cd.close()

if __name__ == "__main__":
    getContent()



