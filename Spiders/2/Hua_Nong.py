"""
为了整理华农的招聘信息,更为直观的阅读信息
"""
# !/usr/bin/python
# -*- encoding: utf-8 -*-
##########################################################
# Creater       :  夜下凝月
# Created  date :  2019-03-31, 08:28:33
# Modiffed date :  2019-03-31, 09:10:33
##########################################################

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import os

class HuaNongSpyder():
    """To get the job info from HuaNong """
    df = []#保存所有公司的招聘信息
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
        self.index_url = "http://hzau.91wllm.com/largefairs/view/id/731/domain/hzau"
        self.get_index_link()


    def get_index_link(self):
        """Get the link of every company"""
        index_content = urllib.request.Request(url=self.index_url, headers=self.headers)
        index_content = urllib.request.urlopen(index_content)
        index_content = index_content.read().decode('utf-8')
        index_content = BeautifulSoup(index_content, 'lxml')
        index_content = index_content.find('table',{"class":"standmap"})
        company_link  = index_content.find_all('a',{"target":"_blank"})
        #对提取出来的公司连接进行下一步操作
        for i in company_link:
            company_name = i.get_text()
            company_url = i.attrs['href']
            self.get_every_company_info(company_name, company_url)
        self.__judge_dir()


    def get_every_company_info(self, name, url):
        """Get the info of every company  (The style of info is table)"""
        print(name)
        base_url = "http://hzau.91wllm.com"
        url = base_url + url
        company = urllib.request.Request(url=url, headers=self.headers)
        company = urllib.request.urlopen(company)
        company = BeautifulSoup(company.read().decode('utf-8'),'lxml')
        introduction = company.find('table')
        introduction = introduction.find_all('tr')
        for i in introduction:
            j = i.td.get_text()
            if j == "简历接收邮箱":
                email = i.find_all('td')[1].get_text()
            elif i.td.get_text() == "岗位":
                carre = introduction.index(i) + 1  #获取”岗位“标签索引，+1后就是岗位信息内容
        for i in introduction[carre:]:
            job_content = i.findAll("td")# 最后一行是投递简历的操作
            job = job_content[0].get_text()
            major = job_content[1].get_text()
            num = job_content[2].get_text()
            salary = job_content[3].get_text()
            edu_bg = job_content[4].get_text()
            job_category = job_content[5].get_text()
            else_needs = job_content[6].get_text()
            info = (name, job, major, num, salary, edu_bg, job_category, else_needs , email)
            HuaNongSpyder.df.append(info)

    
    def __judge_dir(self):
        """Judge whether file"""
        current_dir = os.listdir("./")
        file_name = "HuaNong_data.csv"
        if file_name in current_dir:
            whether_cover = input("{0}已存在，是否覆盖（输入数字1覆盖）:".format(file_name))
            if 1 != int(whether_cover):
                file_name = input("请输入文件基名：")
        info_header = ["企业名称", "岗位", "专业", "数量", "薪资", "学历", "工作性质", "其他需求", "邮箱"]
        data = pd.DataFrame(columns=info_header, data=HuaNongSpyder.df)
        data.to_csv("./{0}.csv".format(file_name), encoding='utf_8_sig', index=False)
        print("Finish")

                
if __name__ == "__main__":
    HuaNongSpyder()
