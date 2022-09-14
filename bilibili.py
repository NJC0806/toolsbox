import re
import requests
import json
import subprocess
import time
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
import _thread

class Bilibili:
    #创建B站视频下载栏UI
    def __init__(self, tabwidget):
        #创建保持视频的文件夹
        if not os.path.exists('download/video'):
            os.mkdir('./download/video', 755)

        self.bilbil_tab = QtWidgets.QWidget()
        self.bilbil_tab.setObjectName("bilbil_tab")
        # 创建lable
        self.lable = QtWidgets.QLabel(self.bilbil_tab)
        self.lable.setGeometry(QtCore.QRect(20, 50, 200, 30))
        self.lable.setObjectName('bilbil_lable')
        self.lable.setText('B站视频链接')
        # 创建line edit
        self.line_edit = QtWidgets.QLineEdit(self.bilbil_tab)
        self.line_edit.setGeometry(QtCore.QRect(185, 50, 750, 30))
        self.line_edit.setObjectName('bilbil_line_edit')
        self.line_edit.setFont(QFont('Times new roman', 14))
        self.line_edit.setText('https://www.bilibili.com/video/BV1mB4y1G7d3')
        # 创建开始下载按钮
        self.start_button = QtWidgets.QPushButton(self.bilbil_tab)
        self.start_button.setGeometry(QtCore.QRect(380, 150, 130, 40))
        self.start_button.setObjectName("bilbil_start_button")
        self.start_button.setText("开始下载")
        self.start_button.clicked.connect(self.creat_thread)
        # 创建text edit用于输出日志
        self.text_edit = QtWidgets.QTextEdit(self.bilbil_tab)
        self.text_edit.setGeometry(QtCore.QRect(0, 250, 963, 443))
        self.text_edit.setObjectName("bilibili_text_edit")
        self.text_edit.setFont(QFont("times new roman", 14))

        self.save_path = 'download\\video\\'

        tabwidget.addTab(self.bilbil_tab, "B站视频下载")

    def creat_thread(self):
        self.text_edit.setText('开始输出日志')
        try:
            _thread.start_new_thread(self.download , ('download', 2,))
            self.out_log('线程已启动')
        except:
            self.out_log('无法启动线程')

    def download(self, name, count):
        self.start_button.setEnabled(False)
        video_info = self.get_video_info(self.line_edit.text())
        self.save_temp_file(video_info[0], video_info[1], video_info[2])
        self.merge_data(video_info[0])

    def get_response(self,html_url):
        headers = {
            # 加入一个防盗链，解决403问题
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
        }
        response = requests.get(url=html_url, headers=headers)
        return response

    def get_video_info(self,html_url):
        response = self.get_response(html_url)
        # 正则表达式匹配取出来的数据是列表
        title = re.findall('<h1 title="(.*?)" class="video-title tit">', response.text)[0]
        html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', response.text)[0]
        json_data = json.loads(html_data)
        self.out_log('开始获取视频信息')
        # 解析json数据
        audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
        video_url = json_data['data']['dash']['video'][0]['baseUrl']
        info = [title, audio_url, video_url]

        return info

    def save_temp_file(self,title, audio_url, video_url):
        # 保存音频二进制数据
        self.out_log('开始请求音频文件')
        audio_content = self.get_response(audio_url).content
        # 保存视频二进制数据
        self.out_log('开始请求视频文件')
        video_content = self.get_response(video_url).content
        with open(f'download\\video\\audio.mp3', mode='wb') as f:
            f.write(audio_content)
            self.out_log('正在保存音频文件')
        with open(f'download\\video\\video.mp4', mode='wb') as f:
            f.write(video_content)
            self.out_log('正在保存视频文件')
    def merge_data(self, title):
        #目的是把标题中的空格去掉，防止ffmpeg报错
        title = title.replace(" ", "")
        self.out_log('开始合并数据')
        cmd = f'.\\ffmpeg\\bin\\ffmpeg.exe -i  download\\video\\video.mp4 -i  download\\video\\audio.mp3 -c:v copy -c:a aac -strict experimental -y  download\\video\\{title}.mp4'
        print(cmd)
        proc = subprocess.Popen(cmd, shell=True)
        while True:
            if proc.poll() is None:
                self.out_log('正在合并数据，请稍后')
            else:
                self.out_log('合并完成，文件下载成功！！')
                self.out_log('文件保存路径为：' + os.getcwd() + '\\' + self.save_path + title + '.mp4')
                if os.path.exists('./download/video/video.mp4'):
                    os.remove('./download/video/video.mp4')
                if os.path.exists('./download/video/audio.mp3'):
                    os.remove('./download/video/audio.mp3')
                self.start_button.setEnabled(True)
                break
            time.sleep(3)

    def out_log(self, log):
        self.text_edit.append(log)
