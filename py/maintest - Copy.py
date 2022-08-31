import requests
import json
import serial
import time
import pymysql
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtCore
from PyQt5 import uic
import os
from PyQt5 import QtCore, QtGui, QtWidgets

import usercardTest


form_mainWindow = uic.loadUiType("mainWindow.ui")[0]

class mainWindow(QDialog,QWidget, form_mainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.returnB.setEnabled(True)
        self.resize(400,300)
        self.returnB.clicked.connect(self.returnBtn)

    def returnBtn(self):
        uid = usercardTest.TagCard()
        nameA = usercardTest.reqUser(uid) 
        self.hide()
        self.second = loginWindow(nameA)  
        self.second.exec()
        self.show()

            
form_loginWindow = uic.loadUiType("thirdWindow.ui")[0]

class loginWindow(QDialog,QWidget, form_loginWindow):
    def __init__(self,nameA):
        super(loginWindow,self).__init__()
        self.setupUi(self)
        self.label_13.setText(nameA[0]+"님")
        self.returnBt.clicked.connect(self.returnBt_Clicked)
        self.closeBt.clicked.connect(self.closeBt_Clicked)
        self.resize(400,300)
        
##        lendList = []
##        for i in range(len(nameA[1])):
##            data = usercardTest.reqLendList(nameA[1][i])
##            lendList.append(data)
##        print(lendList)
##        
##        q=0
##        p=0
##        for i in range((len(lendList))*2):
##            self.tableWidget.setItem(q, p, QTableWidgetItem(lendList[q][p]))
##            p+=1
##            if(p>1):
##                q+=1
##                p=0

    def returnBt_Clicked(self):
        uid = usercardTest.TagCard()
        bookTitle = usercardTest.reqBookName(uid)
        self.third = lastWindow(bookTitle,uid)
        self.third.exec_()
        
    def closeBt_Clicked(self):
        self.close()
    
form_lastWindow = uic.loadUiType("lastWindow.ui")[0]

class lastWindow(QDialog,QWidget, form_lastWindow):
    def __init__(self,bookTitle,uid):
        super(lastWindow,self).__init__()
        self.setupUi(self)
        self.initUI()
        self.textEdit.setText(bookTitle)
        self.requestB.clicked.connect(lambda: self.request_Clicked(uid))
        
    def initUI(self):
        self.resize(800,600)
        self.cancelB.clicked.connect(self.cancel_Clicked)
        
    def request_Clicked(self,uid):
        #z = self.textEdit.toPlainText()
        z = usercardTest.reqReturn(uid)
        result = usercardTest.conLed(z)
        self.close()

    def cancel_Clicked(self):
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    w = mainWindow()
    w.show()
    #w.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())

