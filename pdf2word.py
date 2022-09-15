import re,os
import  _thread
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QFont
from pdf2docx import Converter
class Pdf2Word:
    def __init__(self, tabwidget):
        if os.path.exists('./convert_process.text'):
            os.remove('./convert_process.text')

        # 创建一个bilibili的tabwidget
        self.pdf2word_tab = QtWidgets.QWidget()
        self.pdf2word_tab.setObjectName("pdf2word_tab")

        # 第一层
        # 创建显示选择文件的路径的line edit
        self.path_line_edit = QtWidgets.QLineEdit(self.pdf2word_tab)
        self.path_line_edit.setObjectName("pdf2word_line_edit")
        self.path_line_edit.setFont(QFont('Times new roman', 14))

        # 创建选择文件按钮
        self.select_button = QtWidgets.QPushButton(self.pdf2word_tab)
        self.select_button.setObjectName("pdf2word_select_button")
        self.select_button.setText("选择目录")
        self.select_button.clicked.connect(self.select_files)

        # 第一层布局 创建水平布局用于管理B站视频链接lable和用于输入url的line edit
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.horizontalLayout_1.addWidget(self.path_line_edit)
        self.horizontalLayout_1.addWidget(self.select_button)

        # 第二层
        # 创建开始转换按钮
        self.start_button = QtWidgets.QPushButton(self.pdf2word_tab)
        self.start_button.setObjectName("pdf2word_start_button")
        self.start_button.setText("开始转换")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.create_thread)

        # 创建水平布局用于管理开始下载按钮以及添加弹簧
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # 在开始下载按钮左右添加两个弹簧
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.start_button)
        self.horizontalLayout_2.addItem(spacerItem2)

        # 第三层
        # 创建text edit用于输出日志
        self.text_edit = QtWidgets.QTextEdit(self.pdf2word_tab)
        self.text_edit.setObjectName("pdf2word_text_edit")
        self.text_edit.setFont(QFont("times new roman", 14))

        # 创建一个垂直布局，用于垂直分布的两个已经水平分布的布局以及一个日志输出窗口
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout")
        self.verticalLayout_1.addLayout(self.horizontalLayout_1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem3)
        self.verticalLayout_1.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem4)
        self.verticalLayout_1.addWidget(self.text_edit)

        # 目的是将所有组件全屏到pdf2word_tab中
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.pdf2word_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.addLayout(self.verticalLayout_1)

        # 最后创建一个垂直分布，目的是为了让pdf2word_tab全屏分布到QtWidget中
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tabwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addWidget(self.pdf2word_tab)

        tabwidget.addTab(self.pdf2word_tab, QtGui.QIcon('xx.png'), 'PDF转Word')

        # 用于保存文件绝对路径的列表
        self.files_path = []

    # 选择文件按钮的槽函数
    def select_files(self):
        try:
            self.files_path,_ = QFileDialog.getOpenFileNames(None, '选择一个或多个pdf文件', 'D:\\', 'Text Files (*.pdf);;All Files (*)')
            if len(self.files_path) == 1:
                self.path_line_edit.setText(self.files_path[0])
            else:
                content = ''
                for file_path in self.files_path:
                    content += file_path + '   '
                self.path_line_edit.setText(content)
        except Exception as e:
            self.out_log(f'选择文件路径异常{e}')
        self.start_button.setEnabled(True)

    def create_thread(self):
        self.text_edit.setText('开始输出日志')
        try:
            _thread.start_new_thread(self.pdf_2_word, ('pdf_2_word', 2,))
            self.out_log('线程已启动')
        except:
            self.out_log('无法启动线程')

    def pdf_2_word(self, name, count):
        self.start_button.setEnabled(False)

        self.out_log(f'{len(self.files_path)}个待转换文件，文件路径如下:')
        for file_path in self.files_path:
            path, name = os.path.split(file_path)
            self.out_log(f'《{name}》')
        self.out_log('============================================================================')
        for file_path in self.files_path:
            path, name = os.path.split(file_path)
            self.out_log(f'开始转换《{name}》,请耐心等待！')

            doc_name = file_path.split('.')[0]
            doc_file = f'{doc_name}.docx'
            converter = Converter(file_path)
            converter.convert(doc_file, start=0, end=None)
            converter.close()
            self.out_log('转换完成！存放路径如下(源文件夹下):')
            self.out_log(f'{doc_file}')
            self.out_log('============================================================================')
        self.out_log('全部文件已转换完成！')
        self.start_button.setEnabled(True)

    def out_log(self, log):
        self.text_edit.append(log)
