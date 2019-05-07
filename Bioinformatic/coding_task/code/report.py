# !/usr/bin/python
# -*- encoding: utf-8 -*-
##########################################################
# Creater       :  夜下凝月
# Created  date :  2019-03-18, 18:27:40
# Modiffed date :  2019-03-19, 22:39:31
##########################################################
import os
import sys


def serach (DIR):
    """Recursively find all FASTA files in a directory"""
    working_dir = os.listdir(DIR)
    for i in working_dir:
        # 如果是目录则递归，否则打开文件进行操作
        temp_dir = DIR + '/' + i
        if os.path.isdir(temp_dir):
            serach(temp_dir)
        elif i.split(".")[-1] == 'fas': # temp——dir  ->  ./a/b/a/text.fas
            over_300bp( temp_dir ) 
            longest_shortest(temp_dir)

def over_300bp(input_f_path):
    """Print name and lenth of the seq that length over 300 bp"""
    with open (input_f_path,'r',encoding='utf-8') as f:
        f = f.read()
    f = f.split("\n")
    lines_num = len(f)# 实际序列个数是它的一半
    report_str = ""
    # 回车拆分后，直接判断序列。但必须是FASTA格式
    i = 1
    j = 0 # 计数大于300bp的序列个数
    while( i < lines_num ):
        size = len(f[i])
        if size > 300:
            j += 1
        i += 2
    file_name = input_f_path.split("/")[-1]
    with open(OUTPUT_F_PATH+"/report_over_300.txt", 'a', encoding='utf-8') as rep:
        rep.write("nums:  {0:d}\t \t{1:<} \n".format(j,file_name))

def longest_shortest(input_f_name):
    """ Output the 10 longest seq and the 10 shortest seq with seq headers"""
    with open(input_f_name,'r',encoding='utf-8') as row_f:
        row_f = row_f.readlines()
        f = [x.rstrip('\n') for x in row_f]
    seq_nums = len(f) # 实际序列个数是它的一半
    temp_list =[] #  基因序列索引-序列长度 [(index, lenth),...]
    # 向列表添加元素
    i = 1
    while(i < seq_nums):
        temp_list.append((i,len(f[i])))
        i += 2
    lenth_list = len(temp_list)
    # 排序 长度：小 -> 大
    for i in range(lenth_list):
        for j in range(i+1, lenth_list):
            if temp_list[i][1] > temp_list[j][1]:
                temp_list[i], temp_list[j] = temp_list[j], temp_list[i]
    report_str = "" 
    # 添加最短的10条
    for i in temp_list[0:10]:
        report_str += f[i[0]-1] + "\n" + f[i[0]] + "\n"
    # 添加最长的10条
    for i in temp_list[-10:]:
        report_str += f[i[0]-1] + "\n" + f[i[0]] + "\n"
    with open(OUTPUT_F_PATH+"/longest_shortest.fasta",'a+',encoding='utf-8') as rep:
        rep.write(report_str)
    GC_and_N50(f, temp_list, input_f_name)

def GC_and_N50( f, sorted_list, input_f_name):
    """report the GC% and N50"""
    GC_num = 0
    GC = 0
    seq = "".join(f[1::2])
    # 计算该文件中序列总长度的一半
    half_seq_lenth  = len(seq)/2
    # 找出N50序列
    N50 = 1
    j = 0
    for i in sorted_list[::-1]:
        j += i[1]
        if j <= half_seq_lenth:
            N50 += 1
        else:
            break
    # 计算GC含量
    for i in seq:
        if i in "GC":
            GC_num += 1
    GC = GC_num / len(seq)
    file_name = input_f_name.split("/")[-1]
    with open(OUTPUT_F_PATH + "/GC_and_N50_report.txt",'a',encoding="utf-8") as of:
        of.write("GC%:  {0:.4%}\tN50 size: {1:d}\t file_name:  {2}\n".format(GC,N50,file_name))

if __name__ == '__main__':
    INPUT_F_PATH = sys.argv[1]
    try:
        OUTPUT_F_PATH = sys.argv[2]
        # 判断输出目录是否存在
        if os.path.exists(OUTPUT_F_PATH) :
            pass
        else:
            os.makedirs(OUTPUT_F_PATH)
    except:
        OUTPUT_F_PATH = "./"
    if len(os.listdir(OUTPUT_F_PATH)) != 0:
        os.makedirs(OUTPUT_F_PATH + '/report')
        OUTPUT_F_PATH += '/report'
    print("程序运行中")
    serach(INPUT_F_PATH)
    print("程序结束运行")
    sys.exit()

from bs4 import BeautifulSoup
from etree import xpath
Bea