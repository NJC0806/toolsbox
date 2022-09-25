import os
import sys
import tabwidget
import bilibili
import cloudmusic
import pdf2word
import csdn
import devicemanager
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(tabwidget.ProxyStyle())

    # 创建保存下载文件的文件夹
    if not os.path.exists('download'):
        os.mkdir('./download', 755)

    w = tabwidget.TabWidget()

    # 创建CSDN下载栏
    csdn = csdn.CSDN(w)
    # 创建获取设备管理器的工具栏
    device = devicemanager.DeviceManager(w)
    # 创建pdf转word功能栏
    p2w = pdf2word.Pdf2Word(w)
    # 创建一个Bilibili下载栏
    b =bilibili.Bilibili(w)
    # 创建一个网易云音乐下载栏
    c = cloudmusic.CloudMusic(w)



    #设置窗口相关属性
    w.setWindowTitle("ToolsBox")
    w.setWindowIcon(QIcon('./icons/红色蜘蛛.png'))
    w.resize(1200, 700)
    w.show()
    sys.exit(app.exec_())

