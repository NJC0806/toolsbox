import sys
import tabwidget
import bilbili
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
    #创建一个Bilbil下载栏
    b = bilbili.Bilibili(w)
    c = cloudmusic.CloudMusic(w)
    w.setWindowTitle("toolsbox")
    w.setWindowIcon(QIcon('./icons/红色蜘蛛.png'))
    w.setFixedSize(1200, 700)
    w.show()

    sys.exit(app.exec_())

