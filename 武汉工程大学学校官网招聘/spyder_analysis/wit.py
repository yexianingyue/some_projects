#-*-encoding:utf-8-*-
import urllib.request
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import os
import sys
import time
class WuLiao():
    current_path = ""
    df=[]#存放公司信息
    times=1
    def __init__ (self):
        print("开始爬取数据\n")
        self.getPath()
        self.getData()
    def getPath(self):
        #当前文件路径
        WuLiao.current_path = os.getcwd()+r'\data'
    def getData(self):
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        self.content_url = "http://jyb.wit.edu.cn/module/getjobs?start=0&count=&keyword=&company_name=&city_name=&about_major=%E7%94%9F%E7%89%A9&degree_require=&type_id=-1&is_practice=0"
        self.content = urllib.request.Request(url=self.content_url,headers=self.headers)
        self.content = urllib.request.urlopen(self.content)
        self.content = BeautifulSoup(self.content,'lxml')
        self.content = self.content.p.get_text()
        self.content = json.loads(self.content)
        self.content = self.content["data"]
        self.companyMessage(self.content)



    #将每个公司的待遇分别提取出来
    def companyMessage(self,content):
        for digit in range(len(self.content)):
            sys.stdout.write("正在爬取,请稍后      \r")
            self.company_name = self.content[digit]["company_name"]#企业名称
            self.city_name = self.content[digit]["city_name"]#工作地点
            self.job_name = self.content[digit]["job_name"]#岗位名称
            self.salary = self.content[digit]["salary"]#岗位工资
            self.averageincome = self.averageIncome(self.salary)#平均工资
            self.about_major = self.content[digit]["about_major"]#相关专业
            self.degree_require = self.content[digit]["degree_require"]#学历要求
            self.treament = self.content[digit]["keywords"]#待遇
            self.every_company = (self.company_name,self.city_name,self.job_name,self.salary,self.averageincome,self.about_major,self.degree_require,self.treament)
#            self.process()
            WuLiao.df.append(self.every_company)
            sys.stdout.write("正在爬取,请稍后...\r")
        self.reserve(WuLiao.df)
    def process(self):
#        os.system("cls")
        sys.stdout.write("正在爬取,请稍后      \r")
        for a in range(1,7):
            sys.stdout.write("正在爬取,请稍后%s\r"%("."*a))
#                print("正在爬取,请稍后%s\r"%("."*a))
            sys.stdout.flush()
            time.sleep(0.0)



    #求平均工资
    def averageIncome(self,salary):
        #类似与3.4K-6.5K
        if "K" in self.salary:
            self.patten = re.compile("\d[.\d]*")
            self.digit = self.patten.findall(self.salary)#分离出工资范围
            #将工资转化成数值型
            if len(self.digit[0])==1 or ("." not in self.digit[0]):
                self.digit[0] = int(self.digit[0])
            elif  "." in self.digit[0]:
                self.digit[0] = int(self.digit[0].split(".")[0]) + int(self.digit[0].split(".")[1])*0.1
            if len(self.digit[1])==1 or ("." not in self.digit[1]):
                self.digit[1] = int(self.digit[1])
            else:
                self.digit[1] = int(self.digit[1].split(".")[0]) + int(self.digit[1].split(".")[1])*0.1
            self.digit = (self.digit[0]+self.digit[1])/2*1000
            return self.digit
        #对个别情况枚举
        elif "3000-5000" in self.salary:
            return 4000
        elif "4000-5000" in self.salary:
            return 4500
        elif "4000-8000" in self.salary:
            return 6000
        else:
            return 0

    def reserve(self,df):
        self.name = ["企业名称","工作地点","岗位名称","岗位工资","平均工资","相关专业","学历要求","待遇"]
        self.ultimate = pd.DataFrame(columns=self.name,data=WuLiao.df)
        self.ultimate.to_csv(WuLiao.current_path+r'\wit.csv',encoding='gbk',index=False)
        sys.stdout.write("爬取完毕                  \r\n资料已保存至%s\n"%(WuLiao.current_path+r'\wit.csv'))



def judge():
    #获取当前目录
    current_path = os.getcwd()
    #获取父目录
    father_path = os.path.abspath(os.path.dirname(current_path)+os.path.sep+".")
    #判断文件是否存在
    data_path = os.path.exists(father_path+r"\data\wit.csv") or os.path.exists(current_path+r"\data\wit.csv")
    if data_path:
        out()
    else:
        if os.path.exists(current_path+r"\data"):
            os.system("cls")
            go()
        else:
            os.system("cls")
            print("\n正在创建'\\data'目录\n")
            os.makedirs(current_path+r'\data')
            print("创建完毕\n")
            go()


def out():
    print("\n资料已存在,无需再次爬取\n")
    sys.exit()

def go():
    WuLiao()

if __name__ == "__main__":
    judge()
