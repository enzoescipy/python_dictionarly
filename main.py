import sys
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
import os
import copy
from googletrans import Translator
from pynput import keyboard
from pynput.mouse import Controller as Controller_mouse
from pynput.keyboard import Controller as Controller_keyboard
from pynput.mouse import Button  




def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("dialog.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.dict = []
        self.mouse = Controller_mouse()
        self.keyboard = Controller_keyboard()
        with open('korean.p', 'rb') as file:
            self.korean = pickle.load(file)
        with open('english.p', 'rb') as file:
            self.english = pickle.load(file)


        self.setupUi(self)

        self.translator = Translator()
        self.testnum = 0

        self.setWindowTitle('빠르고 강력한 한국-영어 단어장! 빠강단!')
        self.setWindowIcon(QIcon("book-24px.svg"))

        self.langAlt()

        self.go.clicked.connect(self.saveitem)
        self.dell.clicked.connect(self.dellitem)
        #self.TypeEng.textChanged.connect(self.osusumegogoeng)
        self.TypeEng.returnPressed.connect(self.convertToKor)
        self.TypeEng.returnPressed.connect(self.langAlt)
        #self.TypeKor.textChanged.connect(self.osusumegogokor)
        self.TypeKor.returnPressed.connect(self.saveitem)
        self.TypeKor.returnPressed.connect(self.convertToEng)
        self.TypeKor.returnPressed.connect(self.langAlt)

        #self.osusumeeng.activated.connect(self.osusumechangeeng)
        #self.osusumekor.activated.connect(self.osusumechangekor)

        self.Save.clicked.connect(self.store)
        self.Load.clicked.connect(self.load)

        self.test.clicked.connect(self.makecsv)

        self.pluscount.clicked.connect(self.plu_count)
        self.minuscount.clicked.connect(self.min_count)

        self.temptest.clicked.connect(self.tempteststart)

        self.filename.setText("selfeng-first-1") #set title.
    
    def closeEvent(self, event):
        choice = QMessageBox.question(self, '종료',
                                            "저장하지 않은 단어 및 파일은 완전히 손실됩니다. \n 이대로 종료하시겠습니까?",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass


    def store(self):
        if self.Save.text() == '정말 저장?':
            s = self.filename.text()
            try:
                with open(s + '.p', 'wb') as file:
                    pickle.dump(self.dict, file)
                self.Save.setText('저장')
                self.Load.setText('불러오기')
                self.Load.clicked.connect(self.load)
                self.Load.clicked.disconnect(self.get)
            except:
                self.filename.setText('cannot find file.')
                self.Save.setText('저장')
                self.Load.setText('불러오기')
                self.Load.clicked.connect(self.load)
                self.Load.clicked.disconnect(self.get)
        else:
            self.Save.setText('정말 저장?')
            self.Load.setText('취소!')
            self.Load.clicked.disconnect(self.load)
            self.Load.clicked.connect(self.get)
    def get(self):
        self.Save.setText('저장')
        self.Load.setText('불러오기')
        self.Load.clicked.connect(self.load)
        self.Load.clicked.disconnect(self.get)



    def load(self):
        s = self.filename.text()
        try:
            with open(s + '.p', 'rb') as file:
                self.dict = pickle.load(file)
            self.dict.sort(reverse=True, key=lambda table : table[3])
            self.DictList.setRowCount(len(self.dict))
            for i in range(len(self.dict)):
                for j in range(len(self.dict[i])):
                    self.DictList.setItem(i, j, QTableWidgetItem(str(self.dict[i][j])))
        except:
            self.filename.setText('cannot find file.')
    
    def langAlt(self):
        self.keyboard.press(keyboard.KeyCode.from_vk(21))
        self.keyboard.release(keyboard.KeyCode.from_vk(21))

    def convertToEng(self):
        #get and set the Eng mouse position.
        parent_stack = [self.TypeEng]
        parent_pos = [self.TypeEng.pos()]
        i = 0
        while True:
            parent = parent_stack[i].parentWidget()
            if parent == None:
                break
            parent_stack.append(parent)
            parent_pos.append(parent.pos())
            i += 1
        xsum = 0
        ysum = 0
        for pos in parent_pos:
            xsum += pos.x()
            ysum += pos.y()

        icon = self.iconSize()
        self.mouse.position = (xsum + 10, ysum + icon.height() + 10)

        #click raising
        self.mouse.click(Button.left, 1)

    def convertToKor(self):
        #get and set the Kor mouse position.
        parent_stack = [self.TypeKor]
        parent_pos = [self.TypeKor.pos()]
        i = 0
        while True:
            parent = parent_stack[i].parentWidget()
            if parent == None:
                break
            parent_stack.append(parent)
            parent_pos.append(parent.pos())
            i += 1
        xsum = 0
        ysum = 0
        for pos in parent_pos:
            xsum += pos.x()
            ysum += pos.y()

        icon = self.iconSize()
        self.mouse.position = (xsum + 10, ysum + icon.height() + 10)

        #click raising
        self.mouse.click(Button.left, 1)


    def saveitem(self):
        do = [self.TypeEng.text(), self.TypeKor.text(), self.TypeMemo.text(), 5]  #
        self.TypeEng.clear()
        self.TypeKor.clear()
        if do not in self.dict:
            self.dict.append(do)
            self.DictList.setRowCount(self.DictList.rowCount() + 1)
            self.DictList.setItem(self.DictList.rowCount() - 1, 0, QTableWidgetItem(do[0]))
            self.DictList.setItem(self.DictList.rowCount() - 1, 1, QTableWidgetItem(do[1]))
            self.DictList.setItem(self.DictList.rowCount() - 1, 2, QTableWidgetItem(do[2]))
            self.DictList.setItem(self.DictList.rowCount() - 1, 3, QTableWidgetItem(str(do[3])))

    def dellitem(self):
        if self.DictList.currentColumn() == 0:
            if self.DictList.currentItem() != None:
                item = self.DictList.currentItem().text()
                index = self.DictList.currentRow()
                self.DictList.removeRow(index)

                hahadict = copy.deepcopy(self.dict)

                for i in range(len(hahadict)):
                    for j in range(len(hahadict[i])):
                        if hahadict[i][j] == item:
                            self.dict.pop(i)

    def min_count(self):
        if self.DictList.currentColumn() == 0:
            if self.DictList.currentItem() != None:
                item = self.DictList.currentItem().text()
                index = self.DictList.currentRow()
                hahadict = copy.deepcopy(self.dict)

                for i in range(len(hahadict)):
                    for j in range(len(hahadict[i])):
                        if hahadict[i][j] == item:
                            self.dict[i][3] -= 1
                            self.DictList.setItem(i, 3, QTableWidgetItem(str(self.dict[i][3])))
                            if self.dict[i][3] == 0:
                                self.dellitem()
                
                self.DictList.setCurrentCell(index + 1, self.DictList.currentColumn())
    def plu_count(self):
        if self.DictList.currentColumn() == 0:
            if self.DictList.currentItem() != None:
                item = self.DictList.currentItem().text()
                index = self.DictList.currentRow()
                hahadict = copy.deepcopy(self.dict)

                for i in range(len(hahadict)):
                    for j in range(len(hahadict[i])):
                        if hahadict[i][j] == item:
                            self.dict[i][3] += 1
                            self.DictList.setItem(i, 3, QTableWidgetItem(str(self.dict[i][3])))
                            
                self.DictList.setCurrentCell(index + 1, self.DictList.currentColumn())


    def makecsv(self):
        pd.DataFrame(map(lambda x : x[0:2],self.dict), columns=['영어','한글']).to_csv('testpaper.csv',encoding='utf-8-sig')
        print('done!')


    def osusumechangeeng(self,index):
        self.TypeEng.setText(self.osusumeeng.currentText())
    def osusumechangekor(self):
        self.TypeKor.setText(self.osusumekor.currentText())

    def osusumegogoeng(self):
        typo = self.TypeEng.text()
        startlist = []
        if typo == '':
            return
        else:
            for word in self.english:
                if word.find(typo) == 0:
                    startlist.append(word)
        self.osusumeeng.clear()
        for word in startlist:
            self.osusumeeng.addItem(word)

        #self.TypeKor.setText(trans)
    def osusumegogokor(self):
        typo = self.TypeKor.text()
        startlist = []
        if typo == '':
            return
        else:
            for word in self.korean:
                if word.find(typo) == 0:
                    startlist.append(word)
        self.osusumekor.clear()
        for word in startlist:
            self.osusumekor.addItem(word)
    def transengtokor(self):
        typo = self.TypeEng.text()
        try:
            trans = self.translator.translate(typo, dest='ko')
            self.TypeKor.setText(trans.text)
        except AttributeError as err :
            print(err)
    def transkortoeng(self):
        typo = self.TypeKor.text()
        try :
            trans = self.translator.translate(typo, dest='en')
            self.TypeEng.setText(trans.text)
        except AttributeError as err :
            print(err)
        
    def tempteststart(self):
        self.temptest.setText('다음')
        self.test.setText('시험 끝내기')

        self.temptest.clicked.connect(self.temptestgo)
        self.test.clicked.connect(self.temptestend)

        self.test.clicked.disconnect(self.makecsv)
        self.temptest.clicked.disconnect(self.tempteststart)
    def temptestgo(self):
        self.reload()
        for i in range(self.testnum,len(self.dict),1):
            self.DictList.setItem(i, 1, QTableWidgetItem('????'))
        self.testnum += 1
    def temptestend(self):
        self.reload()
        self.testnum = 0

        self.temptest.setText('간이 시험')
        self.test.setText('시험 파일 제작')

        self.temptest.clicked.connect(self.tempteststart)
        self.test.clicked.connect(self.makecsv)

        self.temptest.clicked.disconnect(self.temptestgo)
        self.test.clicked.disconnect(self.temptestend)
    def reload(self):
        self.dict.sort(reverse=True, key=lambda table : table[3])
        self.DictList.setRowCount(len(self.dict))
        for i in range(len(self.dict)):
            for j in range(len(self.dict[i])):
                self.DictList.setItem(i, j, QTableWidgetItem(str(self.dict[i][j])))


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()