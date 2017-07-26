#! /usr/bin/env python
#  -*- coding: utf-8-*-
import pickle
import re
import sys
from datetime import datetime

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

with open('data.pickle', 'rb') as f:
    data = pickle.load(f)

    # Use if you deleted dump file and don't want to add new contacts manualy

# data = OrderedDict(
#     [('Name', ['Dmitriy Polyvyan', 'Anastas i Volochkova', 'Bill Tucker']),
#      ('Phone Number', ['+79117069852', '+7 925 385 72', '8 999 203 56 27']), ('Date Of Birth', ['08.01.1995', '07.12.1972', '06.05.1964'])])
# with open('data.pickle', 'wb') as f:
#     pickle.dump(data, f)

global name_regex, date_regex, number_regex
name_regex = re.compile('[a-zA-Z\s.]+')
number_regex = re.compile('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
date_regex = re.compile('([0-2]\d|3[01])\.(0\d|1[012])\.(\d{4})')


# Table class. It initializes table, shows messege boxes and also works with data and checks input
class MyTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setmydata()
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def SaveData(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)

    def AddToData(self, row, item):
        if (row == 'Name'):
            names = data['Name']
            names.append(str(item))
            data.update({'Name': names})
        elif (row == 'Number'):
            numbers = data['Phone Number']
            numbers.append(str(item))
            data.update({'Phone Number': numbers})
        elif (row == 'Date'):
            dates = data['Date Of Birth']
            dates.append(str(item))
            data.update({'Date Of Birth': dates})

    def EditData(self, row, item):
        if (row == 'Name'):
            names = data['Name']
            names.insert(rowNumber, str(item))
            del names[rowNumber + 1]
            data.update({'Name': names})
        elif (row == 'Number'):
            numbers = data['Phone Number']
            numbers.insert(rowNumber, str(item))
            del numbers[rowNumber + 1]
            data.update({'Phone Number': numbers})
        elif (row == 'Date'):
            dates = data['Date Of Birth']
            dates.insert(rowNumber, str(item))
            del dates[rowNumber + 1]
            data.update({'Date Of Birth': dates})

    def setmydata(self):
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
            self.setHorizontalHeaderLabels(horHeaders)

    def MessageBox(self, title, text, info_text):
        msgbox = QtGui.QMessageBox(self)
        msgbox.setWindowTitle(title)
        msgbox.setIcon(QtGui.QMessageBox.Information)
        msgbox.setText(text)
        msgbox.setInformativeText(info_text)
        msgbox.addButton(QtGui.QMessageBox.Yes)
        ret = msgbox.exec_()

    def InputCheck(self, name, number, date):
        if (not re.match(name_regex, name) or len(str(name).replace(' ',''))==0):
            MyTable.MessageBox(self, 'Error', 'Wrong name format', '')
            return False

        if (not re.match(number_regex, number) or len(str(number).replace(' ',''))==0):
            MyTable.MessageBox(self, 'Error', 'Wrong number format', '')
            return False

        if (not re.match(date_regex, date)):
            MyTable.MessageBox(self, 'Error', 'Wrong date format', '')
            return False
        try:
            checkDate = datetime.strptime(str(date), "%d.%m.%Y")
        except:
            MyTable.MessageBox(self, 'Error', 'Wrong date format', '')
            return False
        if (checkDate > datetime.now()):
            MyTable.MessageBox(self, 'Error', 'Wrong date format', '')
            return False
        return True


# This class initializes main window

class GridLayout2(QtGui.QWidget):
    def __init__(self, parent=None):
        global contactTable
        
        QtGui.QWidget.__init__(self, parent)
        contactTable = MyTable(data, len(data['Name']), 3)
        tabelLabel = QtGui.QLabel('List of contacts:')

        AddRow = QtGui.QPushButton(QtGui.QIcon('new.png'), '', self)
        AddRow.setFixedWidth(30)
        AddRow.setToolTip('Add new contact')

        EditRow = QtGui.QPushButton(QtGui.QIcon('write.png'), '', self)
        EditRow.setFixedWidth(30)
        EditRow.setToolTip('Edit contact')

        Count = QtGui.QPushButton(QtGui.QIcon('count.png'), '', self)
        Count.setFixedWidth(30)
        Count.setToolTip('Delete selected contact')

        ClearAll = QtGui.QPushButton(QtGui.QIcon('clear.png'), '', self)
        ClearAll.setFixedWidth(30)
        ClearAll.setToolTip('Delete all contacts')

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(AddRow)
        vbox.addWidget(EditRow)
        vbox.addWidget(Count)
        vbox.addWidget(ClearAll)

        # Setting

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(tabelLabel, 0, 0)
        grid.addWidget(contactTable, 1, 0)
        grid.addLayout(vbox, 1, 1)

        self.setWindowTitle('Notebook')
        self.setWindowIcon(QtGui.QIcon('details.png'))
        self.setFixedSize(400, 300)
        self.setLayout(grid)
        self.resize(700, 300)
        self.connect(EditRow, QtCore.SIGNAL('clicked()'), self.EdtRow)
        self.connect(ClearAll, QtCore.SIGNAL('clicked()'), self.Clear)
        self.connect(AddRow, QtCore.SIGNAL('clicked()'), self.AddRw)
        self.connect(Count, QtCore.SIGNAL('clicked()'), self.DeleteRow)

    def EdtRow(self):
        lastRow = contactTable.rowCount()
        if (lastRow == 0):
            MyTable.MessageBox(contactTable, 'Error', 'There is no contacts to edit!', 'Please, add some contacts to edit them!')
        else:
            self.dialogTextBrowser = ModuleEditRow()
            self.dialogTextBrowser.show()

    def Clear(self):
        rows = contactTable.rowCount();
        while rows >= 0:
            contactTable.removeRow(rows)
            rows -= 1
        data['Name'] = []
        data['Phone Number'] = []
        data['Date Of Birth'] = []
        MyTable.SaveData(contactTable)
        contactTable.clearContents()

    def DeleteRow(self):
        indexes = contactTable.selectionModel().selectedIndexes()
        for index in sorted(indexes):
            contactTable.removeRow(index.row())
            del data['Name'][index.row()]
            del data['Phone Number'][index.row()]
            del data['Date Of Birth'][index.row()]
            MyTable.SaveData(contactTable)

    def AddRw(self):
        self.dialogTextBrowser = ModuleAddRow()
        self.dialogTextBrowser.show()

    def CheckForBirthday(self):
        for x in range(len(data['Date Of Birth'])):
            date = datetime.strptime(data['Date Of Birth'][x], "%d.%m.%Y")
            if (date.month == datetime.now().month and date.day == datetime.now().day):
                MyTable.MessageBox(contactTable, 'Birthday Reminder',
                                   'Today is the birthday of ' + str(data['Name'][x]),
                                   "Don't forget to congratulate him/her!")


# Class adds new contact
class ModuleAddRow(GridLayout2):
    def __init__(self, parent=None):

        global numberEdited
        global nameEdited
        global dateOfBirthEdited
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('Add new contact')
        self.setWindowIcon(QtGui.QIcon('details.png'))

        name = QtGui.QLabel('Name')
        number = QtGui.QLabel('Phone Number')
        date = QtGui.QLabel('Date of Birth')

        ExitAndSave = QtGui.QPushButton(QtGui.QIcon('save.png'), '', self)
        ExitAndSave.setFixedWidth(125)
        Exit = QtGui.QPushButton(QtGui.QIcon('exit.png'), '', self)

        nameEdited = QtGui.QLineEdit()
        nameEdited.setFixedWidth(100)
        nameEdited.setMaxLength(30)
        nameEdited.setValidator(QRegExpValidator(QRegExp('[a-zA-Z\s.]+')))

        numberEdited = QtGui.QLineEdit()
        numberEdited.setFixedWidth(100)
        numberEdited.setMaxLength(16)
        numberEdited.setValidator(QRegExpValidator(QRegExp('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')))
        dateOfBirthEdited = QtGui.QLineEdit()
        dateOfBirthEdited.setFixedWidth(100)
        dateOfBirthEdited.setMaxLength(10)
        dateOfBirthEdited.setValidator(QRegExpValidator(QRegExp('([0-2]\d|3[01])\.(0\d|1[012])\.(\d{4})')))

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(name, 1, 0)
        grid.addWidget(nameEdited, 1, 1)

        grid.addWidget(number, 2, 0)
        grid.addWidget(numberEdited, 2, 1)

        grid.addWidget(date, 3, 0)
        grid.addWidget(dateOfBirthEdited, 3, 1)

        grid.addWidget(ExitAndSave, 6, 0)
        grid.addWidget(Exit, 6, 1)

        self.setLayout(grid)
        self.resize(350, 300)
        self.connect(ExitAndSave, QtCore.SIGNAL('clicked()'), self.ExtAndSv)
        self.connect(Exit, QtCore.SIGNAL('clicked()'), self.Ext)

    def ExtAndSv(self):
        NumRows = contactTable.rowCount()
        if (MyTable.InputCheck(contactTable, nameEdited.text(), numberEdited.text(), dateOfBirthEdited.text())):
            MyTable.AddToData(contactTable, 'Name', nameEdited.text())
            MyTable.AddToData(contactTable, 'Number', numberEdited.text())
            MyTable.AddToData(contactTable, 'Date', dateOfBirthEdited.text())
            contactTable.insertRow(NumRows)
            MyTable.setmydata(contactTable)
            MyTable.SaveData(contactTable)
            self.close()

    def Ext(self):
        self.close()


# Class edits contacts
class ModuleEditRow(ModuleAddRow):
    def __init__(self, parent=None):

        global rowNumber
        global nameEdited
        global numberEdited
        global dateOfBirthEdited
        global lastRow
        QtGui.QWidget.__init__(self, parent)

        rowNumber = contactTable.rowCount() - 1
        lastRow = contactTable.rowCount()
        contactTable.selectRow(lastRow - 1)

        self.setWindowTitle('Edit contact')
        self.setWindowIcon(QtGui.QIcon('details.png'))

        editNameLabel = QtGui.QLabel('Edit name')
        editPhoneLabel = QtGui.QLabel('Edit phone ')
        editDateOfBirth = QtGui.QLabel('Edit Date of Birth ')

        ExitAndSave = QtGui.QPushButton(QtGui.QIcon('save.png'), '', self)
        ExitAndSave.setFixedWidth(125)
        Exit = QtGui.QPushButton(QtGui.QIcon('exit.png'), '', self)

        Up = QtGui.QPushButton(QtGui.QIcon('up.png'), '', self)
        Up.setFixedWidth(35)
        SupUp = QtGui.QPushButton(QtGui.QIcon('SupUp.png'), '', self)

        Down = QtGui.QPushButton(QtGui.QIcon('down.png'), '', self)
        SupDown = QtGui.QPushButton(QtGui.QIcon('SupDown.png'), '', self)

        text = QTableWidgetItem(contactTable.item(lastRow - 1, 0))
        nameEdited = QtGui.QLineEdit()
        nameEdited.insert(text.text())
        nameEdited.setFixedWidth(100)
        nameEdited.setMaxLength(30)
        nameEdited.setValidator(QRegExpValidator(QRegExp('[a-zA-Z\s.]+')))

        text = QTableWidgetItem(contactTable.item(lastRow - 1, 1))
        numberEdited = QtGui.QLineEdit()
        numberEdited.setFixedWidth(100)
        numberEdited.setMaxLength(16)
        numberEdited.insert(text.text())
        numberEdited.setValidator(QRegExpValidator(QRegExp('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')))

        text = QTableWidgetItem(contactTable.item(lastRow - 1, 2))
        dateOfBirthEdited = QtGui.QLineEdit()
        dateOfBirthEdited.setFixedWidth(100)
        dateOfBirthEdited.setMaxLength(10)
        dateOfBirthEdited.insert(text.text())
        dateOfBirthEdited.setValidator(QRegExpValidator(QRegExp('([0-2]\d|3[01])\.(0\d|1[012])\.(\d{4})')))

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(editNameLabel, 1, 0)
        grid.addWidget(nameEdited, 1, 1)
        grid.addWidget(editPhoneLabel, 2, 0)
        grid.addWidget(numberEdited, 2, 1)
        grid.addWidget(SupUp, 1, 3)
        grid.addWidget(editDateOfBirth, 3, 0)
        grid.addWidget(dateOfBirthEdited, 3, 1)
        grid.addWidget(Up, 2, 3)
        grid.addWidget(Down, 3, 3)
        grid.addWidget(SupDown, 4, 3)
        grid.addWidget(ExitAndSave, 4, 0)
        grid.addWidget(Exit, 4, 1)

        self.setLayout(grid)
        self.resize(350, 300)
        self.connect(ExitAndSave, QtCore.SIGNAL('clicked()'), self.ExtAndSvAd)
        self.connect(Exit, QtCore.SIGNAL('clicked()'), self.ExtAd)
        self.connect(SupUp, QtCore.SIGNAL('clicked()'), self.SpUp)
        self.connect(Up, QtCore.SIGNAL('clicked()'), self.UpM)
        self.connect(Down, QtCore.SIGNAL('clicked()'), self.DownM)
        self.connect(SupDown, QtCore.SIGNAL('clicked()'), self.SpDown)

    def ExtAndSvAd(self):
        if (MyTable.InputCheck(contactTable, nameEdited.text(), numberEdited.text(), dateOfBirthEdited.text())):
            MyTable.EditData(contactTable, 'Name', nameEdited.text())
            MyTable.EditData(contactTable, 'Number', numberEdited.text())
            MyTable.EditData(contactTable, 'Date', dateOfBirthEdited.text())
            MyTable.SaveData(contactTable)
            MyTable.setmydata(contactTable)

    def ExtAd(self):
        self.close()

    def SpUp(self):
        global rowNumber
        rowNumber = 0
        contactTable.selectRow(rowNumber)
        text = QTableWidgetItem(contactTable.item(rowNumber, 0))
        nameEdited.setText(text.text())
        text = QTableWidgetItem(contactTable.item(rowNumber, 1))
        numberEdited.setText(text.text())
        text = QTableWidgetItem(contactTable.item(rowNumber, 2))
        dateOfBirthEdited.setText(text.text())

    def SpDown(self):
        global rowNumber
        contactTable.selectRow(lastRow - 1)
        text = QTableWidgetItem(contactTable.item(lastRow - 1, 0))
        nameEdited.setText(text.text())
        text = QTableWidgetItem(contactTable.item(lastRow - 1, 1))
        numberEdited.setText(text.text())
        text = QTableWidgetItem(contactTable.item(lastRow - 1, 2))
        dateOfBirthEdited.setText(text.text())
        rowNumber = lastRow - 1

    def UpM(self):
        global rowNumber
        if (rowNumber == 0):
            self.SpDown()
        else:
            rowNumber = rowNumber - 1
            contactTable.selectRow(rowNumber)
            text = QTableWidgetItem(contactTable.item(rowNumber, 0))
            nameEdited.setText(text.text())
            text = QTableWidgetItem(contactTable.item(rowNumber, 1))
            numberEdited.setText(text.text())
            text = QTableWidgetItem(contactTable.item(rowNumber, 2))
            dateOfBirthEdited.setText(text.text())

    def DownM(self):
        global rowNumber
        if (rowNumber == contactTable.rowCount() - 1):
            self.SpUp()
        else:
            rowNumber = rowNumber + 1
            contactTable.selectRow(rowNumber)
            text = QTableWidgetItem(contactTable.item(rowNumber, 0))
            nameEdited.setText(text.text())
            text = QTableWidgetItem(contactTable.item(rowNumber, 1))
            numberEdited.setText(text.text())
            text = QTableWidgetItem(contactTable.item(rowNumber, 2))
            dateOfBirthEdited.setText(text.text())


def main(args):
    app = QApplication(args)
    qb = GridLayout2()
    qb.CheckForBirthday()
    qb.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
