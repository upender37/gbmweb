# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(332, 399)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 20, 331, 51))
        font = QFont()
        font.setPointSize(19)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 68, 61, 16))
        self.keyword_list_textedit = QTextEdit(self.centralwidget)
        self.keyword_list_textedit.setObjectName(u"keyword_list_textedit")
        self.keyword_list_textedit.setGeometry(QRect(20, 88, 291, 261))
        self.start_btn = QPushButton(self.centralwidget)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setGeometry(QRect(20, 360, 75, 31))
        self.stop_btn = QPushButton(self.centralwidget)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setGeometry(QRect(240, 360, 75, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GMB Data Extractor", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"GMB Data Extractor", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Keyword list", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_btn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi

