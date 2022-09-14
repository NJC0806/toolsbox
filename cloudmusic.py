import time
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
import _thread
import requests
import re

class CloudMusic:
    #创建网易云音乐下载栏UI
    def __init__(self, tabwidget):
        #创建保持视频的文件夹
        if not os.path.exists('download/music'):
            os.mkdir('./download/music', 755)

        self.cloudmusic_tab = QtWidgets.QWidget()
        self.cloudmusic_tab.setObjectName("cloudmusic_tab")
        # 创建lable
        self.lable = QtWidgets.QLabel(self.cloudmusic_tab)
        self.lable.setGeometry(QtCore.QRect(20, 50, 200, 30))
        self.lable.setObjectName('cloudmusic_lable')
        self.lable.setText('网易云音乐链接')
        # 创建line edit
        self.line_edit = QtWidgets.QLineEdit(self.cloudmusic_tab)
        self.line_edit.setGeometry(QtCore.QRect(220, 50, 730, 30))
        self.line_edit.setObjectName('cloudmusic_line_edit')
        self.line_edit.setFont(QFont('Times new roman', 14))
        self.line_edit.setText('https://music.163.com/#/song?id=521416693')
        # 创建开始下载按钮
        self.start_button = QtWidgets.QPushButton(self.cloudmusic_tab)
        self.start_button.setGeometry(QtCore.QRect(380, 150, 130, 40))
        self.start_button.setObjectName('cloudmusicl_start_button')
        self.start_button.setText('开始下载')
        self.start_button.clicked.connect(self.creat_thread)
        # 创建text edit用于输出日志
        self.text_edit = QtWidgets.QTextEdit(self.cloudmusic_tab)
        self.text_edit.setGeometry(QtCore.QRect(0, 250, 963,443))
        self.text_edit.setObjectName('cloudmusic_text_edit')
        self.text_edit.setFont(QFont('times new roman', 14))

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