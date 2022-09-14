import sys
import tabwidget
import bilibili
import cloudmusic
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    #创建保存下载文件的文件夹
    if not os.path.exists('download'):
        os.mkdir('./download', 755)

    w = tabwidget.TabWidget()
    #创建一个Bilibili下载栏
    b = bilibili.Bilibili(w)
    # 创建一个网易云音乐下载栏
    c = cloudmusic.CloudMusic(w)

    #设置窗口相关属性
    w.setWindowTitle("toolsbox")
    w.setWindowIcon(QIcon('./icons/红色蜘蛛.png'))
    w.resize(1200, 700)
    w.show()
    sys.exit(app.exec_())

