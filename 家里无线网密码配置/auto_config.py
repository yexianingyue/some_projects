from selenium import webdriver
import time
import sys
import os
print("\n\n密码不要超过横线， 不得短于小于号\n\n")
passwd = input("输入将要改变的密码:\n\n<<<<<<<<--------------------------------------------------------\n<<<<<<<<--------------------------------------------------------\r")
while( len(passwd) > 64 or len(passwd) < 8):
    os.system("cls")
    if len(passwd) < 8:
        print("密码长度较小")
    elif len(passwd) > 64:
        print("密码长度过长")
    passwd = input("\n\n重新输入密码:\n\n<<<<<<<<--------------------------------------------------------\n<<<<<<<<--------------------------------------------------------\r")
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
driver.find_element_by_id("WlanPassword_password").clear()#清空密码
driver.find_element_by_id("WlanPassword_password").send_keys(passwd)#填写密码
wifi_name = driver.find_element_by_xpath('//tr[@id="record_0"]/td[3]').text#获取wifi名称
driver.close()
driver.find_element_by_id('Save_button').click()#保存更改
os.system("cls")
print("\n\n\n\n\n===========================================================")
print("wifi名称："+wifi_name)
print("wifi密码："+passwd)
print("===========================================================")
input("自行关闭窗口")
