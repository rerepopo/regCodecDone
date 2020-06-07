# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from regDecoder import Ui_Form
import sys

#ref: https://doc.qt.io/qt-5/qtablewidgetitem.html
#ref: https://www.regexpal.com/93640

def set_bit(value, bit):
    return value | (1 << bit)

def clear_bit(value, bit):
    return value & ~(1 << bit)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.buttonClicked)
        self.ui.pushButtonCleanSelection.clicked.connect(self.buttonCleanSelection)
        self.ui.tableWidget.itemDoubleClicked.connect(self.itemDoubleClickedToInverse)
        self.ui.tableWidget.itemSelectionChanged.connect(self.itemSelectionChangedSlot)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.inputIntValue = 0xFF

    def itemSelectionChangedSlot(self):
        # print('itemSelectionChangedSlot is ')
        indexList = []
        for item in self.ui.tableWidget.selectedItems():
            indexList.append([31 - item.column(), item.text()])
        if indexList == []:  # select nothing, take it as select all
            for columnIndex in range(0, 32):
                indexList.append([31 - columnIndex, self.ui.tableWidget.item(0, columnIndex).text()])
        indexList.sort()  # indexList.sort(reverse=True)
        # print(indexList)

        selectedValueText = ""
        for list in indexList:
            selectedValueText = list[1] + selectedValueText
        # print(selectedValueText)
        # show lineEditOutXXX
        self.ui.lineEditOutBin.setText("0b" + selectedValueText)
        self.ui.lineEditOutDec.setText(str(int(selectedValueText, base=2)))
        self.ui.lineEditOutHex.setText(hex(int(selectedValueText, base=2)).upper().replace("0X", "0x"))
        # show labelOutputResult
        indexList.sort(reverse=True)
        selectedIndexText = []
        for list in indexList:
            # print(str(list[0]))
            selectedIndexText.append(str(list[0]))
        if len(selectedIndexText) == 32:
            self.ui.labelOutputResult.setText("Output Result: ")
        else:
            self.ui.labelOutputResult.setText("partial Selection: [" + ', '.join(selectedIndexText) + "]")

    def itemDoubleClickedToInverse(self, item):
        print('item double click. item index is ' + str(31 - item.column()))
        itemIndex = 31 - item.column()
        if item.text() == "0":
            item.setText("1")
            self.inputIntValue = set_bit(self.inputIntValue, itemIndex)
        else:
            item.setText("0")
            self.inputIntValue = clear_bit(self.inputIntValue, itemIndex)
        self.buttonCleanSelection()

    def buttonCleanSelection(self):
        print('buttonCleanSelection: ')
        for item in self.ui.tableWidget.selectedItems():
            item.setSelected(False)

    def buttonClicked(self):
        text = self.ui.lineEdit.text()
        # ref https://vimsky.com/zh-tw/examples/detail/python-method-PyQt4.QtGui.QFont.html
        palettePass = QtGui.QPalette()
        palettePass.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
        fontPass = QtGui.QFont()
        fontPass.setPointSize(12)
        fontPass.setBold(False)
        paletteFail = QtGui.QPalette()
        paletteFail.setColor(QtGui.QPalette.Text, QtCore.Qt.red)
        fontFail = QtGui.QFont()
        fontFail.setPointSize(16)
        fontFail.setBold(True)
        print("buttonClicked: text is " + str(text))
        try:
            if text[0:2] == "0x":  # if hex
                intVal = int(text[2:], 16)
                binVal = bin(intVal)
            elif text[0:2] == "0b":  # if bin
                intVal = int(text[2:], 2)
                binVal = bin(intVal)
            else:  # if dec
                intVal = int(text, 10)
                binVal = bin(intVal)
            #print(" binVal is " + binVal)
            #print(" intVal is " + str(intVal))
            if intVal > (pow(2,32)-1):
                intVal = (pow(2,32)-1)
                binVal = bin(intVal)
                self.ui.lineEdit.setPalette(paletteFail)
                self.ui.lineEdit.setFont(fontFail)
                self.ui.labelInputCheckResult.setText(str(text) + ' is invalid input. Take it as 0xFFFFFFFF.  \nNOTE: Only Support 0~2^32-1.')
            elif intVal < 0:
                intVal = 0
                binVal = bin(intVal)
                self.ui.lineEdit.setPalette(paletteFail)
                self.ui.lineEdit.setFont(fontFail)
                self.ui.labelInputCheckResult.setText(str(text)+' is invalid input. Take it as 0. \nNOTE: Only Support 0~2^32-1.')
            else:
                self.ui.lineEdit.setPalette(palettePass)
                self.ui.lineEdit.setFont(fontPass)
                self.ui.labelInputCheckResult.setText("Input Check Result: PASS.")
                print("Input Check Result: PASS.")
            self.inputIntValue = intVal
        except:
            intVal = self.inputIntValue
            binVal = bin(intVal)
            self.inputIntValue = self.inputIntValue
            self.ui.lineEdit.setPalette(paletteFail)
            self.ui.lineEdit.setFont(fontFail)
            self.ui.labelInputCheckResult.setText(str(text)+' is invalid input. \nNOTE: "^0x[0-9A-Fa-f]+$" for hex. "^0b[0-1]+$" for binary. "^[0-9]+$" for decimal.')
                 #    /^       # start of string
                 #    0x       # 0x prefix
                 #    [0-9A-F] # a hex digit
                 #    $        # end of string
        # for used:
        index = -1
        while binVal[index] in ["1", "0"]:
            item = self.ui.tableWidget.item(0, 32 + index)
            item.setText(binVal[index])
            index = index - 1
        # for not used: make all zero
        while 32 + index >= 0:
            item = self.ui.tableWidget.item(0, 32 + index)
            item.setText("0")
            index = index - 1
        self.buttonCleanSelection()
        self.itemSelectionChangedSlot()

    def keyPressEvent(self, qKeyEvent):
        #print(qKeyEvent.key())
        if qKeyEvent.key() == QtCore.Qt.Key_Return or qKeyEvent.key() == QtCore.Qt.Key_Enter:
            self.buttonClicked()
            print('Enter pressed: ')
        else:
            super().keyPressEvent(qKeyEvent)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.setWindowTitle("regDecodec ver.20200607")

    brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
    brush.setStyle(QtCore.Qt.SolidPattern)
    for i in [0,16] :
        for j in range(0,8) :
            print(i+j)
            window.ui.tableWidget.item(0, i+j).setBackground(brush)


    window.show()
    sys.exit(app.exec_())


