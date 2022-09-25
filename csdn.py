import re
import os
import _thread
import parsel
import requests
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont

class CSDN:
    # 创建B站视频下载栏UI
    def __init__(self, tabwidget):
        # 创建保持视频的文件夹
        if not os.path.exists('download/csdn'):
            os.mkdir('./download/csdn', 755)

        # 创建一个csdn的tabwidget
        self.csdn_tab = QtWidgets.QWidget()
        self.csdn_tab.setObjectName("csdn_tab")

        # 第一层
        # 创建CDSN链接lable
        self.lable = QtWidgets.QLabel(self.csdn_tab)
        self.lable.setObjectName('csdn_lable')
        self.lable.setFont(QFont("times new roman", 14))
        self.lable.setText('CSDN链接')

        # 创建输入url的line edit
        self.line_edit = QtWidgets.QLineEdit(self.csdn_tab)
        self.line_edit.setObjectName('csdn_line_edit')
        self.line_edit.setFont(QFont('Times new roman', 14))
        self.line_edit.setText('https://blog.csdn.net/weixin_45983581/article/details/104605215')

        # 创建水平布局用于管理csdn链接lable和用于输入url的line edit
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.horizontalLayout_1.addWidget(self.lable)
        self.horizontalLayout_1.addWidget(self.line_edit)

        # 第二层
        # 创建开始下载按钮
        self.start_button = QtWidgets.QPushButton(self.csdn_tab)
        self.start_button.setObjectName("csdn_start_button")
        self.start_button.setText("开始下载")
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
        self.text_edit = QtWidgets.QTextEdit(self.csdn_tab)
        self.text_edit.setObjectName("bilibili_text_edit")
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

        # 创建一个水平布局，用于水平分布所有已经经过组件，这样的目的是为了让各个组件全屏到csdn_tab中
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.csdn_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.addLayout(self.verticalLayout_1)

        # 最后创建一个垂直分布，目的是为了让csdn_tab全屏分布到QtWidget中
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tabwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addWidget(self.csdn_tab)

        self.save_path = 'download\\csnd\\'

        tabwidget.addTab(self.csdn_tab, QtGui.QIcon('xx.png'), "CSDN下载")

    def create_thread(self):
        self.text_edit.setText('开始输出日志')
        try:
            _thread.start_new_thread(self.download_html, ('download_html', 2,))
            self.out_log('线程已启动')
        except:
            self.out_log('无法启动线程')

    def download_html(self, name, count):
        # 一个网页的模板{article}是我们要填写的内容
        html_template = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <ment charset="UTF-8">
                    <title>Document</title>
                </head>
                <body>
                    {article}
                </body>
            </html>
            '''
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'
        }
        response = requests.get(url=self.line_edit.text(), headers=headers)
        # 解析网站
        selector = parsel.Selector(response.text)
        # 通过网页元素找到文章内容，#表示网页属性是id .表示是class
        content = selector.css('#content_views').get()
        # 获取文章标题
        title = selector.css('#articleContentId::text').get()
        # 替换文章标题中的特殊字符
        filename = re.sub(r'[\/:*?"<>|]+', '-', title)
        # 保存为hrml文件
        self.out_log(f'开始保存{title}')
        html = html_template.format(article=content)
        with open(f'download\\csdn\\{filename}.html', mode='w', encoding='utf-8') as f:
            f.write(html)
        self.out_log('保存完成，文件路径为：' + os.getcwd() + '\\' + f'download\\csdn\\{filename}.html')

    def out_log(self, log):
        self.text_edit.append(log)


