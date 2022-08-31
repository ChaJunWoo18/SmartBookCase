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


form_firstWindow = uic.loadUiType("C:\Users\LEE\tmp\git-init\ui\firstWindow.ui")[0]
form_secondWindow = uic.loadUiType("C:\Users\LEE\tmp\git-init\ui\secondWindow.ui")[0]
noBook = uic.loadUiType("C:\Users\LEE\tmp\git-init\ui\nobook.ui")[0]
form_loginWindow = uic.loadUiType("C:\Users\LEE\tmp\git-init\ui\loginWindow.ui")[0]
form_thirdWindow = uic.loadUiType("C:\Users\LEE\tmp\git-init\ui\thirdWindow.ui")[0]
form_fourthWindow = uic.loadUiType("C:\Users\LEE\tmp\git-init\ui\fourthWindow.ui")[0]

class firstWindow(QDialog,QWidget, form_firstWindow):
    def __init__(self):
        super(firstWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.pushButton.clicked.connect(self.startBtn)

    def startBtn(self):
        self.hide()
        second = secondWindow()
        second.exec()
        self.show()

class secondWindow(QDialog,QWidget, form_secondWindow):
    def __init__(self):
        super(secondWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.showMaximized()
        self.pushButton.clicked.connect(self.loginBtn)
        self.pushButton_2.clicked.connect(self.cardBtn)

    def loginBtn(self):
        self.second = loginWindow()
        self.second.exec()
        
    def cardBtn(self):
        uid = usercardTest.TagCard()
        nameA = usercardTest.reqUser(uid)
        if not nameA[1]:
            self.second = noBook(nameA)

        else:
            self.second = thirdWindow(nameA,uid)
            self.close()
        self.second.exec()


class noBook(QDialog,QWidget, noBook):
    def __init__(self,nameA):
        super(noBook,self).__init__()
        self.setupUi(self)
        self.resize(600,400)
        self.label.setText(nameA[0]+"님, 대출중인 도서가 없습니다.")
        
        self.pushButton.clicked.connect(self.closeBt_Clicked)

    def closeBt_Clicked(self):
        self.close()

class loginWindow(QDialog,QWidget, form_loginWindow):
    def __init__(self):
        super(loginWindow,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.login_Clicked)
        self.pushButton_2.clicked.connect(self.closeBt_Clicked)

    def login_Clicked(self):
        userId = self.textEdit.toPlainText()
        userPw = self.textEdit_2.toPlainText()
        loginCheck = usercardTest.reqLogin(userId, userPw)
        if loginCheck == 'pwError':
            self.textEdit_3.setText("비밀번호를 확인해주세요")
            self.textEdit_2.setText("")
        elif loginCheck == 'noMember':
            self.textEdit_3.setText("먼저 홈페이지에서 회원가입을 해주세요")
            self.textEdit_2.setText("")
            self.textEdit.setText("")
        else:
            nameA = usercardTest.reqUser(loginCheck)
            if not nameA[1]:
                self.second = noBook(nameA)
            else:
                self.second = thirdWindow(nameA,loginCheck)
            self.close() 
            self.second.exec()
            
            
    def closeBt_Clicked(self):
        self.close()            


class thirdWindow(QDialog,QWidget, form_thirdWindow):
    def __init__(self,nameA,uid):
        super(thirdWindow,self).__init__()
        self.setupUi(self)
        self.showMaximized()
        self.label.setText(nameA[0]+"님")
        self.pushButton.clicked.connect(lambda: self.returnBt_Clicked(uid))
        self.pushButton_2.clicked.connect(self.closeBt_Clicked)

        lendList = []
        for i in range(len(nameA[1])):
            data = usercardTest.reqLendList(nameA[1][i])
            lendList.append(data)

        if len(lendList) ==1:
            self.title_1.setText(lendList[0][0])
            self.num_1.setText(lendList[0][1])
        if len(lendList) ==2:
            self.title_1.setText(lendList[0][0])
            self.num_1.setText(lendList[0][1])
            self.title_2.setText(lendList[1][0])
            self.num_2.setText(lendList[1][1])
        if len(lendList) ==3:
            self.title_1.setText(lendList[0][0])
            self.num_1.setText(lendList[0][1])
            self.title_2.setText(lendList[1][0])
            self.num_2.setText(lendList[1][1])
            self.title_3.setText(lendList[2][0])
            self.num_3.setText(lendList[2][1])

        self.pushButton_3.clicked.connect(lambda: self.repaint_Clicked(nameA,uid))
        
    def returnBt_Clicked(self,userUid):
        uid = usercardTest.TagCard()
        bookTitle = usercardTest.reqBookName(uid)
        self.third = fourthWindow(bookTitle,uid,userUid)
        self.third.exec_()
        
    def closeBt_Clicked(self):
        self.close()

    def repaint_Clicked(self,nameA,uid):
        name = self.label.text()[:-1]
        if nameA[0] == name:
            tmp = usercardTest.reqUser2(uid)
        
        lendList = []
        for i in range(len(tmp)):
            data = usercardTest.reqLendList(tmp[i])
            lendList.append(data)
        
        self.title_1.setText('')
        self.num_1.setText('')
        self.title_2.setText('')
        self.num_2.setText('')
        self.title_3.setText('')
        self.num_3.setText('')
        if len(lendList) ==1:
            self.title_1.setText(lendList[0][0])
            self.num_1.setText(lendList[0][1])
        if len(lendList) ==2:
            self.title_1.setText(lendList[0][0])
            self.num_1.setText(lendList[0][1])
            self.title_2.setText(lendList[1][0])
            self.num_2.setText(lendList[1][1])
        if len(lendList) ==3:
            self.title_1.setText(lendList[0][0])
            self.num_1.setText(lendList[0][1])
            self.title_2.setText(lendList[1][0])
            self.num_2.setText(lendList[1][1])
            self.title_3.setText(lendList[2][0])
            self.num_3.setText(lendList[2][1])
        

class fourthWindow(QDialog,QWidget, form_fourthWindow):
    def __init__(self,bookTitle,uid,userUid):
        super(fourthWindow,self).__init__()
        self.setupUi(self)
        self.initUI()
        self.label.setText(bookTitle)
        self.pushButton.clicked.connect(lambda: self.request_Clicked(uid,userUid))
        
    def initUI(self):
        self.pushButton_2.clicked.connect(self.cancel_Clicked)
        
    def request_Clicked(self,uid,userUid):
        z = usercardTest.reqReturn(uid)
        result = usercardTest.conLed(z)
        self.label.setText('')
        self.label.setText(str(z)+'번에 반납해주세요')
        time.sleep(7)
        self.close()

    def cancel_Clicked(self):
        self.close()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    w = firstWindow()
    w.showMaximized()
    #w.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())

