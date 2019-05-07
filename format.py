#  !/usr/bin/python
#  -*- encoding:utf-8 -*-
import sys
import os
from typing import Optional
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QTextEdit, QLineEdit)

class opt_DNA_Seq():
    """
    test = opt_DNA_Seq( sequence ) return the seq only include "ATCG"
    test.reverse ,  return the reverse sequence
    test.complementary ,    return the complementary sequence
    test.reverse_and_complementary ,    return the reverse and complementary sequence
    """
    def __init__(self, dna_seq: str):
        self.DNA_seq = dna_seq.upper()#  字符串大写以后利于后面的操作
        self.DNA_seq = self.__format(self.DNA_seq)#  格式化后的序列,方法中，复制后进行操作

    #  选取其中的正确碱基返回处理后的字符串
    def __format(self, DNA_seq: str) -> Optional[str]:
        """The private function to select "ATCG" from DNA_seq"""
        temp = []
        self.DNA_seq = DNA_seq
        for x in self.DNA_seq:
            if x in "ATCG":
                temp.append(x)
        return "".join(temp)

    #  完成反向链设置关键字默认参数，便于后面调用
    def reverse(self) -> Optional[str]:
        """Return the reverse string of  DNA_seq"""
        #  print("in reverse")
        return self.DNA_seq[::-1]

    #  完成互补链
    def complementary(self) -> Optional[str]:
        """Return complementary string of DNA_seq"""
        #  print("_"*30)
        #  print("in complrmrntary")
        temp = []
        for x in self.DNA_seq:
            if   x == "A": x="T"
            elif x == "T": x="A"
            elif x == "C": x="G"
            elif x == "G": x="C"
            temp.append(x)
        return "".join(temp)

    #  完成反向互补链
    def reverse_and_complementary(self) -> Optional[str]:
        """Return the anticomplementary string of DNA_seq"""
        #  print("_"*30)
        #  print("in reverse_and_completementary")
        result = []
        temp = self.DNA_seq[::-1]
        for x in temp:
            if   x == "A": x="T"
            elif x == "T": x="A"
            elif x == "C": x="G"
            elif x == "G": x="C"
            result.append(x)
        return "".join(result)

class GUI(QWidget):
    """show the result of processed"""
    def __init__(self):
        super().__init__()
        self.initGUI()
    def initGUI(self):
        LINE_NUM = 1 #  控制UI行标签位置 每用一次就加一
        #  ROW_NUMS = 0 #  控制UI列标签位置
        
        #  define label name
        seq_name = QLabel("序列名称")
        origin_data = QLabel("输入DNA")
        cleared_data = QLabel("处理后的")
        revers_data = QLabel("反义序列")
        comple_data = QLabel("互补序列")
        rev_com_data = QLabel("反向互补")


        #  define label's type
        self.seq_nameEdit = QLineEdit()
        self.originEdit = QTextEdit()
        self.clearedEdit = QTextEdit()
        self.reversEdit = QTextEdit()
        self.compleEdit  = QTextEdit()
        self.rev_comEdit  = QTextEdit()

        #  define some buttons
        process_btn = QPushButton("处理")
        self.export_btn_5 = QPushButton("一键导出")

        #  set the gap between 'QTextEdit()'
        grid = QGridLayout()
        grid.setSpacing(10)


#       grid.addWidget( 要显示的标签，第几行，第几列 )

#  1st line
        grid.addWidget(seq_name, LINE_NUM, 0)
        grid.addWidget(self.seq_nameEdit,LINE_NUM,1)

#  2nd line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(origin_data, LINE_NUM, 0)
        grid.addWidget(self.originEdit, LINE_NUM, 1)
        #add button to process DNA seq
        grid.addWidget(process_btn, LINE_NUM, 2)
        process_btn.clicked.connect(self.__processDNA)

#  3rd line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(cleared_data, LINE_NUM, 0)
        grid.addWidget(self.clearedEdit, LINE_NUM, 1)

#  4s line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(revers_data, LINE_NUM, 0)
        grid.addWidget(self.reversEdit, LINE_NUM, 1)

#  5s line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(comple_data, LINE_NUM, 0)
        grid.addWidget(self.compleEdit, LINE_NUM, 1)

#  6s line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(rev_com_data, LINE_NUM, 0)
        grid.addWidget(self.rev_comEdit, LINE_NUM, 1)
        grid.addWidget(self.export_btn_5,LINE_NUM,2)
        self.export_btn_5.clicked.connect(self.__export)

        self.setLayout(grid)
        
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle("处理DNA")
        self.show()

#  process input seq
    def __processDNA(self):
        """function from process_btn"""
        dna = self.originEdit.toPlainText()# 读取文本框的内容 -> dna
        DNA = opt_DNA_Seq(dna)# 实例化
        cleared_seq = DNA.DNA_seq# 选出ATCG正确的碱基
        self.clearedEdit.setPlainText(cleared_seq)
        #  self.clearedEdit.setHtml("<font color='red' size=6><red>"+cleared_seq+"</font>")

        revers_seq = DNA.reverse()
        self.reversEdit.setPlainText(revers_seq)

        comple_seq = DNA.complementary()
        self.compleEdit.setPlainText(comple_seq)

        rev_com_seq = DNA.reverse_and_complementary()
        self.rev_comEdit.setPlainText(rev_com_seq)

#  export three DNA seq
    def __export(self):
        """
        导出处理后的序列，如果序列名未定义
        __________________________________________
        目  录：./导出的序列/
        __________________________________________
        文件名                      含义
        __________________________________________
        raw_.seq                处理后的原生序列
        revers_.seq             反义序列
        complementary_.seq      互补序列
        rev_com_.seq            反向互补序列
        __________________________________________
        """
        filename = self.seq_nameEdit.text()
    #  filename
        row_name = './导出的序列/raw_' + filename + '.seq'
        revers_name = './导出的序列/revers_' + filename + '.seq'
        complementary_name = './导出的序列/complementary_' + filename + '.seq'
        revers_complementary_name = './导出的序列/rev_com_' + filename + '.seq'
    #  seq
        row_seq = self.clearedEdit.toPlainText()
        revers_seq = self.reversEdit.toPlainText()
        complementary_seq = self.compleEdit.toPlainText()
        revers_complementary_seq = self.rev_comEdit.toPlainText()

        dicname = os.getcwd() + r'/导出的序列/'
        if not os.path.exists(dicname):
            os.makedirs(dicname)
        with open( row_name, 'w', encoding='utf-8' ) as f:
            f.write(row_seq)
        with open( revers_name, 'w', encoding='utf-8' ) as f:
            f.write(revers_seq)
        with open( complementary_name, 'w', encoding='utf-8' ) as f:
            f.write(complementary_seq)
        with open( revers_complementary_name, 'w', encoding='utf-8' ) as f:
            f.write(revers_complementary_seq)
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    g = GUI()
    sys.exit(app.exec_())
