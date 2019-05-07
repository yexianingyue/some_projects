#-*-encoding:utf-8 -*-
from selenium import webdriver
import time
from tkinter import *
from tkinter.messagebox import *
import json
def auto_config(name,passwd):
    name=name
    passwd=passwd
    option = webdriver.ChromeOptions()#启动前设置
    option.add_argument('disable-infobars')#不显示浏览器正在受控制
    driver = webdriver.Chrome(chrome_options=option)
    driver.maximize_window()#最大化窗口
    url = "http://192.168.1.1"
    driver.get(url)
    driver.find_element_by_id('txt_Username').send_keys('user')
    driver.find_element_by_id('txt_Password').send_keys('icd2d')
    driver.find_element_by_id('btnSubmit').click()
    driver.find_element_by_xpath('//a[text()="网络"]').click()
    driver.find_element_by_xpath('//a[text()="WLAN网络配置"]').click()
    driver.switch_to_frame('frameContent')#重新获取页面元素
    driver.find_element_by_id("WlanSsid_text").clear()#清空用户名
    driver.find_element_by_id("WlanSsid_text").send_keys(name)
    driver.find_element_by_id("WlanPassword_password").clear()#清空密码
    driver.find_element_by_id("WlanPassword_password").send_keys(passwd)#填写密码
    driver.close()
    driver.find_element_by_id('Save_button').click()#保存更改

def checkinfo():
    name = wifi_name.get()
    passwd = wifi_passwd.get()
    judge=2
    if name != '':
        if name.split('-')[0] == 'CMCC' and len(name)>5:
            name_tip['text']=''
            judge-=0
        else:
            name_tip['text']='起始名称必须为CMCC-'
            name_tip['fg']='red'
            judge-=1
    if passwd != '':
        if len(passwd) > 7 and len(passwd) < 65:
            passwd_tip['text']=''
            judge-=0
        else:
            passwd_tip['text']="密码长度在8-64"
            passwd_tip['fg']='red'
            judge-=1
    if judge==2:
        getinfo(name,passwd)
    else:
        confirm
def space(row,window):
    space = Label(window,text='')
    space.grid(row=row)
def getinfo(name,passwd):
    name=name
    passwd=passwd
    auto_config(name,passwd)
    #保存信息
    setting={}
    setting['name']=name
    setting['passwd']=passwd
    setting = json.dumps(setting,ensure_ascii=False)
    with open(r"D:/zy/无线网密码配置/config.json",'w',encoding='utf-8') as cg:
        cg.write(setting)
    #显示信息
    result = Tk(className='配置结果')
    result.geometry('300x150')
    space(0,result)
    #wifi名称
    wifi_name_ = Label(result,text="   wifi名称:   "+name)
    wifi_name_.grid(row=1,sticky=W)
    space(2,result)
    #wifi密码
    wifi_passwd_ = Label(result,text="   wifi密码:   "+passwd)
    wifi_passwd_.grid(row=3,sticky=W)
    mainloop()

#=================================================================
#读取配置信息
try:
    config = open(r"D:/zy/无线网密码配置/config.json",'r',encoding="utf-8")
    setting = json.load(config)
    setting_name = setting['name']
    setting_passwd = setting['passwd']
    config.close()
except:
    setting_name = 'CMCC-yxny'
    setting_passwd = 'sdlksjasdf354'
#主界面===========================================================
configure = Tk(className="无线网络配置")
configure.geometry("400x200")
space(0,configure)
#用户名信息提示
name_tip = Label(configure,text='')
name_tip.grid(row=1,column=3)
#wifi名称第三行显示
wifi_name_ = Label(configure,text="   wifi名称:")
wifi_name_.grid(row=2,sticky=W)
wifi_name = Entry(configure)
wifi_name.insert(END,setting_name)
wifi_name.grid(row=2,column=3,sticky=E)
space(3,configure)
#密码信息提示
passwd_tip=Label(configure,text='')
passwd_tip.grid(row=4,column=3)
#wifi密码
wifi_passwd_ = Label(configure,text="   wifi密码:")
wifi_passwd_.grid(row=5,sticky=W)
wifi_passwd = Entry(configure)
wifi_passwd.insert(END,setting_passwd)
wifi_passwd.grid(row=5,column=3,sticky=E)
space(6,configure)
#主界面按钮
#确定
Label(configure)
confirm=Button(text='完成',command = checkinfo)
confirm.grid(row=7,column=2,sticky=E)
#取消
Label(configure)
cancel = Button(text="退出",command=configure.quit)
cancel.grid(row=7,column=3,sticky=E)
mainloop()

