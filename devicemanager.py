import _thread
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets, QtGui
from serial.tools.list_ports import comports

class DeviceManager:
    # devicemanager栏UI
    def __init__(self, tabwidget):
        # 创建一个devicemanager的tabwidget
        self.devicemanager_tab = QtWidgets.QWidget()
        self.devicemanager_tab.setObjectName("devicemanager_tab")

        # 创建开始下载按钮
        self.refresh_button = QtWidgets.QPushButton(self.devicemanager_tab)
        self.refresh_button.setObjectName("devicemanager_refresh_button")
        self.refresh_button.setText("刷新")
        self.refresh_button.clicked.connect(self.create_thread)

        # 创建水平布局用于管理刷新按钮以及添加弹簧
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        # 在刷新按钮左右添加两个弹簧
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_1.addItem(spacerItem1)
        self.horizontalLayout_1.addWidget(self.refresh_button)
        self.horizontalLayout_1.addItem(spacerItem2)

        # 创建text edit用于输出日志
        self.text_edit = QtWidgets.QTextEdit(self.devicemanager_tab)
        self.text_edit.setObjectName("bilibili_text_edit")
        self.text_edit.setFont(QFont("times new roman", 14))

        # 创建一个垂直布局，用于垂直分布的两个已经水平分布的布局以及一个日志输出窗口
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem3)
        self.verticalLayout_1.addLayout(self.horizontalLayout_1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_1.addItem(spacerItem4)
        self.verticalLayout_1.addWidget(self.text_edit)

        # 创建一个水平布局，用于水平分布所有已经经过组件，这样的目的是为了让各个组件全屏到devicemanager_tab中
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.devicemanager_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.addLayout(self.verticalLayout_1)

        # 最后创建一个垂直分布，目的是为了让devicemanager_tab全屏分布到QtWidget中
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tabwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addWidget(self.devicemanager_tab)

        tabwidget.addTab(self.devicemanager_tab, QtGui.QIcon('xx.png'), "设备管理器")

        # 默认获取一次
        self.refresh_button.click()

    def create_thread(self):
        try:
            _thread.start_new_thread(self.get_serial_info, ('get_serial_info', 2,))
        except:
            self.out_log('无法启动线程')

    def get_serial_info(self, name, count):
        serials = comports()
        for serial in serials:
            self.out_log(serial[1])

    def out_log(self, log):
        self.text_edit.append(log)


