#/usr/bin/python
#-*- encoding:utf-8 -*-
import sys
import time
import pyperclip
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGridLayout, 
                             QTextEdit, QLineEdit)

class GUI (QWidget):
    def __init__(self):
        super().__init__()
        self.initGUI()
    def initGUI(self):
        LINE_NUM = 1
        grid = QGridLayout()
        grid.setSpacing(10)

        self.start_name = QLabel("起始")
        self.end_name = QLabel("结尾")
        self.mark_name = QLabel("启动子位置")
        self.seq_name = QLabel("处理文本")
        self.process_info = QLabel("提示信息：")

        self.start_Edit = QLineEdit()
        self.end_Edit = QLineEdit()
        self.mark_Edit = QLineEdit()
        self.info_Edit = QLineEdit()
        self.seq_Edit = QTextEdit()

        cut_btn = QPushButton("截取")
        pro_btn = QPushButton("高亮")

#  1st line
        grid.addWidget(self.start_name, LINE_NUM, 0)
        grid.addWidget(self.start_Edit, LINE_NUM, 1)
        grid.addWidget(self.end_name, LINE_NUM, 2)
        grid.addWidget(self.end_Edit, LINE_NUM, 3)
        grid.addWidget(cut_btn, LINE_NUM, 4)
        cut_btn.clicked.connect(self.__cut)

#  2nd line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(self.mark_name, LINE_NUM, 0)
        grid.addWidget(self.mark_Edit, LINE_NUM, 1)
        grid.addWidget(pro_btn, LINE_NUM, 4)
        pro_btn.clicked.connect(self.__mark)

#  3rd line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(self.process_info, LINE_NUM, 0)
        grid.addWidget(self.info_Edit, LINE_NUM, 1)

#  4th line
        LINE_NUM = LINE_NUM + 1
        grid.addWidget(self.seq_name, LINE_NUM, 0)
        grid.addWidget(self.seq_Edit, LINE_NUM, 1, 5, 3)

        self.setLayout(grid)

        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle("寻找DNA片段")
        self.show()

    def __cut(self):
        """从全长中切片CDs"""
        self.info_Edit.setText("处理中...")
        raw_seq = self.seq_Edit.toPlainText()
        seq = self.__format(raw_seq.upper())
        # 先判断范围是否有效
        if self.start_Edit.text() and self.end_Edit.text():
            start = int(self.start_Edit.text())
            end = int(self.end_Edit.text())
            if  start>0 and end>0 and end>start:
                cut_seq = seq[start:end]
                self.seq_Edit.setPlainText( cut_seq )
                self.info_Edit.setText("序列长度：{}".format(len(cut_seq)))
            else:
                self.info_Edit.setText("范围错误，重新输入")
        else:
            self.info_Edit.setText("范围错误，重新输入")


    def __mark(self):
        """寻找启动子"""
        self.info_Edit.setText("处理中...")
        mark = int(self.mark_Edit.text()) - 1
        seq = self.seq_Edit.toPlainText().upper()
        seq = self.__format(seq)
        seq = list(seq)
        seq[mark] = "<font color='red' size=6>" + seq[mark] + "</font>"
        seq = "".join(seq)
        self.seq_Edit.setHtml(seq)
        lenth = len(seq)
        self.info_Edit.setText("序列长度：{}".format(lenth))


    def __format(self,seq):
        """The private function to select "ATCG" from DNA_seq"""
        temp = []
        self.DNA_seq = seq
        for x in self.DNA_seq:
            if x in "ATCG":
                temp.append(x)
        return "".join(temp)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    g = GUI()
    sys.exit(app.exec_())


