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

def TagCard():
###############사용자 도서카드 읽어서 누구인지 확인하기#####################
    T = serial.Serial('COM6',9600)
    strTemp = ""

    while True:
        print('Tag your ID Card')
        strTemp = T.readline().decode('utf-8')
        strTemp = strTemp.replace("\n","").encode('utf-8')
        strTemp = str(strTemp)
        strTemp = strTemp[3:14]
        if(strTemp!=''):
            T.close()
            print(strTemp)
            return strTemp


#uid값을 get방식으로 보냄 >> spring으로부터 도서 분류번호를 리턴받음(ex.300)
def reqUser(strTemp):
    url = "http://localhost:8080/member/"
    response = requests.get(url+strTemp)
    result = response.json()
    url2 = "http://localhost:8080/user/borrow/"
    response2 = requests.get(url2+strTemp)
    result2 = response2.json()
    tmp = result.get('Name')
    tmp2 = result2.get('result')
    a = []
    
    if tmp != 'error' and tmp2 != 'error':
        for i in range(3):
            check = 'borrow'+str(i+1)
            if result2[check] != 'X':
                a.append(result2[check])
        return result['Name'],a

    elif tmp != 'error' and tmp2 == 'error':
        return '대출 현황을 불러올 수 없습니다.'
    
    elif tmp == 'error':
        return '회원이 아닙니다'

def reqUser2(strTemp):
    url2 = "http://localhost:8080/user/borrow/"
    response2 = requests.get(url2+strTemp)
    result2 = response2.json()
    tmp2 = result2.get('result')
    a = []
    
    if tmp2 != 'error':
        for i in range(3):
            check = 'borrow'+str(i+1)
            if result2[check] != 'X':
                a.append(result2[check])
        return a

    elif tmp2 == 'error':
        return '대출 현황을 불러올 수 없습니다.'

def reqLogin(id, pw):
    url = "http://localhost:8080/user/LoginSBC/"
    response = requests.get(url+id+'/'+pw)
    result = response.json()
    return result.get('result')

def reqLendList(bookUid):
    url = "http://localhost:8080/book/lendList/"
    response = requests.get(url+bookUid)
    result = response.json()
    return result['bookName'],result['cateNum']


def reqBookName(strTemp): 
    url = "http://localhost:8080/book/return/check/"
    response = requests.get(url+strTemp)
    result = response.json()
    return result['book']

def reqReturn(strTemp): #BookReturn
    url = "http://localhost:8080/book/return/"
    response = requests.get(url+strTemp)
    result = response.json()
    return result['book']


def conLed(n):
    T = serial.Serial('COM6',9600)
    T.write(n.encode())
    
    
    return 0


