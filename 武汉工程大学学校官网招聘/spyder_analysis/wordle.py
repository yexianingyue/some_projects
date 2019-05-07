#-*-encoding:utf-8-*-
import pandas as pd
import re
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
path = r'G:\创业就业指导\data\wit.csv'
content = open(path)
content = pd.read_csv(content)

def wC(picture,dic):
    #获取当前文件目录
    current_path = os.getcwd()
    #获取父目录
    father_path = os.path.abspath(os.path.dirname(current_path)+os.path.sep+".")
    # 读取背景图片
    color_mask = imread(father_path+r'\data'+picture)
    cloud = WordCloud(
#        relative_scaling = 0.5,
        #设置字体，不指定就会出现乱码
        font_path=father_path+r'\data\simfang.ttf',
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=100,
        min_font_size = 5,#显示的最小的字体大小
        #缩放
        scale=5.0
        )
    word_cloud = cloud.generate_from_frequencies(dic) #产生词云
    data_path = os.path.exists(father_path+r"\result")
    if  not(data_path):
        os.makedirs(father_path+r'\result')
    picture = picture.split(".")[0]
    word_cloud.to_file(father_path+r"\result"+picture+".png") #保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

#需要列表
def Dictory(every,picture):
    dic = {}
    picture = picture#此处无用,只是中间传递参数
    patten = set(every)
    patten = list(patten)
    for x in patten:
        for y in every:
            if x not in dic:
                if x==y:
                    dic[x] = 1
            elif x==y:
                dic[x] += 1
    wC(picture,dic)



def processCity_name():
    city_name = content["工作地点"]#空格隔开
    city_name = " ".join(city_name)
    city_name = city_name.replace(" ",",")
    city_name = city_name.replace("、",",")
    city_name = city_name.replace("，",",")
    city_name = re.sub("市","",city_name)
    city_name = city_name.split(",")
    Dictory(city_name,r'\city_name.jpg')






#

def processAbout_major():
    about_major = content["相关专业"]#原型是中文逗号隔开
    about_major = " ".join(about_major)
    about_major = about_major.replace(" ",",")
    about_major = about_major.replace("、",",")
    about_major = about_major.replace("，",",")
    about_major = about_major.replace("/",",")
    about_major = about_major.replace("或",",")
    about_major = re.sub("相关专业","",about_major)
    about_major = about_major.split(",")#列表
    Dictory(about_major,r'\about_major.jpg')

def processJob_name():
    job_name = content["岗位名称"]
    job_name = " ".join(job_name)
    job_name = job_name.replace(" ",",")
    job_name = job_name.split(",")#列表
    Dictory(job_name,r'\job_name.jpg')

if __name__ == "__main__":
    processCity_name()
    processAbout_major()
    processJob_name()