from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import requests as r
import re
from urllib.request import urlopen
import os
from youtube_dl import YoutubeDL
import ctypes

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 308)
        self.centralwidget = QtWidgets.QWidget(Frame)
        self.centralwidget.setObjectName("centralwidget")
        Frame.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Frame)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Frame.setMenuBar(self.menubar)
        self.about = self.menubar.addMenu("About")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(120, 40, 161, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.pushButton = QtWidgets.QPushButton(Frame)
        self.pushButton.setGeometry(QtCore.QRect(160, 200, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(Frame)
        self.progressBar.setGeometry(QtCore.QRect(90, 250, 231, 23))
        self.progressBar.setMouseTracking(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(180, 130, 121, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(75)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAutoFillBackground(False)
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Frame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 160, 241, 21))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "KNLoad"))
        self.radioButton.setText(_translate("Frame", "Facebook"))
        self.radioButton_2.setText(_translate("Frame", "YouTube"))
        self.pushButton.setText(_translate("Frame", "Download"))
        self.label.setText(_translate("Frame", "URL : "))
        self.pushButton.clicked.connect(lambda : self.click(self.radioButton.isChecked(),self.radioButton_2.isChecked(),self.lineEdit,self.progressBar))
        self.act = self.about.addAction("About")
        self.act.triggered.connect(self.about_m)

    def about_m(self):
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'KNLoad - Video Download Program(Facebook and YouTube)\n\n\nYou can contact me at : \nInstagram : k4mran_abdullazade \nTelegram : @Kamran_Abdullazade\n\n\nDeveloper : Kamran Abdullazade\nVersion : 1.0', 'About', 0)
    def click(self,radioButton,radioButton_2,lineEdit,progressBar):

        if radioButton:
            url = lineEdit.text()
            html = r.get(url)
            #print("START") #Test
            video_url = re.search('hd_src:"(.+?)"', html.text).group(1)
            u = urlopen(video_url)
            file_size = int(u.headers['content-length'])
            #print(file_size) #Test

            f = open(os.path.join(os.getcwd(), "video_fb.mp4"), 'wb')

            downloaded_bytes = 0
            block_size = 1024 * 8
            while True:
                buffer = u.read(block_size)
                if not buffer:
                    break

                f.write(buffer)
                downloaded_bytes += block_size
                #print(downloaded_bytes) #Test
                self.setProgress(float(downloaded_bytes) / file_size * 100)

            f.close()
            #print("STOP") #Test


        elif radioButton_2:
            url = lineEdit.text()
            #print("START") #Test
            y = YoutubeDL({
                'format': 'mp4',
            })
            b = y.extract_info(url, download=False)
            yt_url = b['url']
            u = urlopen(yt_url)
            file_size = int(u.headers['content-length'])
            #print(file_size) #Test

            f = open(os.path.join(os.getcwd(), "video_yt.mp4"), 'wb')

            downloaded_bytes = 0
            block_size = 1024 * 8
            while True:
                buffer = u.read(block_size)
                if not buffer:
                    break

                f.write(buffer)
                downloaded_bytes += block_size
                #print(downloaded_bytes) #Test
                self.setProgress(float(downloaded_bytes) / file_size * 100)

            f.close()
            #print("STOP") #Test

    def setProgress(self, value):
        if value > 100:
            value = 100
        self.progressBar.setValue(value)

    def closeEvent(self, event):
        os._exit(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QMainWindow()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
