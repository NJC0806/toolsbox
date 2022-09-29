import time
import _thread
from PyQt5.QtGui import QImage
from PyQt5 import QtWidgets, QtGui
import datetime

class FakeScreen():

    def __init__(self, tabwidget):
        # 创建一个fakescreen的tabwidget
        self. fake_screen_tab = QtWidgets.QWidget()
        self. fake_screen_tab.setObjectName("fake_screen_tab")

        # 创建开始显示按钮
        self.start_button = QtWidgets.QPushButton(self.fake_screen_tab)
        self.start_button.setObjectName("fake_screen_button")
        self.start_button.setText("开始显示")
        self.start_button.clicked.connect(self.create_thread)

        # 创建水平布局用于管理开始下载按钮以及添加弹簧
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        # 在开始下载按钮左右添加两个弹簧
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_1.addItem(spacerItem1)
        self.horizontalLayout_1.addWidget(self.start_button)
        self.horizontalLayout_1.addItem(spacerItem2)

        # 创建label用于显示图像
        self.image = QImage()
        self.label = QtWidgets.QLabel(self.fake_screen_tab)
        self.label.setObjectName('fake_screen_lable')
        # 创建水平布局用于管理开始下载按钮以及添加弹簧
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # 在开始下载按钮左右添加两个弹簧
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout_2.addItem(spacerItem4)


        # 垂直布局
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout")
        self.verticalLayout_1.addLayout(self.horizontalLayout_1)
        self.verticalLayout_1.addLayout(self.horizontalLayout_2)

        # 创建一个水平布局，用于水平分布所有已经经过组件，这样的目的是为了让各个组件全屏到bilibili_tab中
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.fake_screen_tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.addLayout(self.verticalLayout_1)

        # 最后创建一个垂直分布，目的是为了让bilibili_tab全屏分布到QtWidget中
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tabwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addWidget(self.fake_screen_tab)
        tabwidget.addTab(self.fake_screen_tab, QtGui.QIcon('xx.png'), "虚拟屏")

    def create_thread(self):
        try:
            _thread.start_new_thread(self.show_image , ('download', 2,))
            print('线程已启动')
        except:
            print('无法启动线程')
            
    def show_image(self, name, count):
        for index in range(100,999):
            print("time1"+str(datetime.datetime.now()))
            QImage.load(self.image, f'./output/frame-0{index}.jpg', format='jpg')
            self.label.setPixmap(QtGui.QPixmap(self.image))
            time.sleep(40*0.001)
            print("time2"+str(datetime.datetime.now()))
'''
import av
import sys
import _thread
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
def h264ToJpg_demo():
    inputFileName = "input.h264"
    container = av.open(inputFileName)
    print("container:", container)
    print("container.streams:", container.streams)
    print("container.format:", container.format)
    #img = QImage()
    #lable = QtWidgets.QLabel()
    for frame in container.decode(video=0):
        print("process frame: %04d (width: %d, height: %d)" % (frame.index, frame.width, frame.height))
        frame.to_image().save("output/frame-%04d.jpg" % frame.index)
        # QImage.load(img, f'output/frame-{frame.index}.jpg', format='jpg')
        # lable.setPixmap(QPixmap(img))

def main():
    h264ToJpg_demo()


if __name__ == "__main__":
    sys.exit(main())
'''