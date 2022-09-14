import time
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
import _thread
import requests
import re
'''
布局介绍
horizontalLayout_1 用于水平布局网易云音乐链接lable和用于输入url的line eidt;
horizontalLayout_2 用于水平布局开始下载按钮及左右个一个弹簧
verticalLayout_1   用于垂直布局horizontalLayout_1、horizontalLayout_2及日志输入窗口
horizontalLayout_3 创建一个水平布局，用于水平分布所有已经经过组件，这样的目的是为了让各个组件全屏到bilibili_tab中
verticalLayout_2   最后创建一个垂直分布，目的是为了让bilibili_tab全屏分布到QtWidget中
'''
class CloudMusic:
    #创建网易云音乐下载栏UI
    def __init__(self, tabwidget):
        #创建保持视频的文件夹
        if not os.path.exists('download/music'):
            os.mkdir('./download/music', 755)
        # 创建一个bilibili的tabwidget
        self.cloudmusic_tab = QtWidgets.QWidget()
        self.cloudmusic_tab.setObjectName("cloudmusic_tab")

        # 第一层
        # 创建网易云音乐链接lable
        self.lable = QtWidgets.QLabel(self.cloudmusic_tab)
        self.lable.setObjectName('cloudmusic_lable')
        self.lable.setText('网易云音乐链接')
        # 创建输入url的line edit
        self.line_edit = QtWidgets.QLineEdit(self.cloudmusic_tab)
        self.line_edit.setObjectName('cloudmusic_line_edit')
        self.line_edit.setFont(QFont('Times new roman', 14))
        self.line_edit.setText('https://music.163.com/#/song?id=521416693')

        # 创建水平布局用于管理网易云音乐链接lable和用于输入url的line edit
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.horizontalLayout_1.addWidget(self.lable)
        self.horizontalLayout_1.addWidget(self.line_edit)

        # 第二层
        # 创建开始下载按钮
        self.start_button = QtWidgets.QPushButton(self.cloudmusic_tab)
        self.start_button.setObjectName('cloudmusicl_start_button')
        self.start_button.setText('开始下载')
        self.start_button.clicked.connect(self.creat_thread)

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
        self.text_edit = QtWidgets.QTextEdit(self.cloudmusic_tab)
        self.text_edit.setObjectName('cloudmusic_text_edit')
        self.text_edit.setFont(QFont('times new roman', 14))

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

        # 创建一个水平布局，用于水平分布所有已经经过组件，这样的目的是为了让各个组件全屏到bilibili_tab中
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.cloudmusic_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.addLayout(self.verticalLayout_1)

        # 最后创建一个垂直分布，目的是为了让bilibili_tab全屏分布到QtWidget中
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tabwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addWidget(self.cloudmusic_tab)

        self.save_path = 'download\\music\\'

        tabwidget.addTab(self.cloudmusic_tab, '网易云音乐下载')

    def creat_thread(self):
        self.text_edit.setText('开始输出日志')
        try:
            _thread.start_new_thread(self.download, ())
            self.out_log('线程已启动')
        except:
            self.out_log('无法启动线程')

    def download(self):
        self.start_button.setEnabled(False)

    def get_response(self,url):
        # 请求头，就是用来伪装python代码，把代码伪装为浏览器去访问服务器
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        # 获取服务器响应
        response = requests.get(url=url, headers=headers)

        return response

    def download(self):

        id = re.findall('id=(\d+)', self.line_edit.text())
        self.out_log(f'歌曲id：{id[0]}')
        download_url = "https://link.hhtjim.com/163/" + id[0] + ".mp3"
        music_url = "http://music.163.com/song?id=" + id[0]
        song = requests.get(download_url).content
        song_info = requests.get(music_url).text
        song_name = re.findall('<em class="f-ff2">.*</em>', song_info)[0].lstrip('<em class="f-ff2">').rstrip('</em>')
        self.out_log(f'歌曲名：{song_name}')
        with open(self.save_path + song_name + '.mp3', 'wb') as f:
            f.write(song)
            self.out_log('文件保存路径为：' + os.getcwd() + '\\' + self.save_path + song_name + '.mp3')

    def out_log(self, log):
            self.text_edit.append(log)