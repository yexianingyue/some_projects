# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:33:34 2018
Theme   BiliBIli_Cartoon
@author: yexia
"""
from selenium import webdriver
from urllib import request
from lxml import etree
import time

imgList=[]   #每添加一张漫画就加进去hash(imgSrc),若bun在列表中，则下一个
num = [0] #储存漫画的名称
repairNum=[]
count = 0 #重复的图片指针
temp_repair_count = []
option = webdriver.ChromeOptions()
option.add_argument("disable-infobars")
driver = webdriver.Chrome(chrome_options=option)
driver.get("https://www.bilibili.com/b6ca8c70-4335-4ad5-be90-a697d78ecb6e#up")
           
#记录每幅图重复的次数
def repairCount():
    """若count=5,不在辅助列表中，则添加"""
    if num[0] not in temp_repair_count:
        temp_repair_count.append(num[0])
    '''获得参数在列表中位置，时间复杂度为 n'''
    count = temp_repair_count.index(num[0])
    '''根据位置，判断是不是新元素，如果是，则添加，否则就+1'''
    if count not in repairNum:
        repairNum.append(1)
    elif  count not in repairNum:
        repairNum[count] +=1
        
#储存照片
def nextimg():
    time.sleep(0.5)
    driver.find_element_by_class_name("change-img-btn").click()
    html = driver.page_source
    html = etree.HTML(html)
    content = html.xpath('/html/body/div[@class="error-container"]/div[@class="error-manga"]/img/@src')
    imgSrc = 'https:'+content[0]  #获得图片真实地址
    print(imgSrc)
    hashImg = hash(imgSrc)
    if hashImg not in imgList:
        print(num)
        request.urlretrieve(imgSrc,'./img/'+str(num)+'.png')
        imgList.append(hashImg)
        num[0] += 1
    else:
        repairCount()
    
while(1):
    nextimg()
    if 20 in repairNum:
        print("一共有图片",end=" ")
        print(len(imgList))
        driver.close()
        exit(0)
    
