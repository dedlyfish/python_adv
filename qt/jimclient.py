import sys
from messenger import *
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Messenger()
        self.ui.setupUi(self)

        self.__status('Started app')

        self.ui.contactView.addItem('JohnDoe')
        self.ui.contactView.addItem('Smith')
        self.ui.contactView.addItem('Mary')
        self.ui.serverEdit.setText('127.0.0.1')
        self.ui.portEdit.setText('7777')

        self.ui.connectButton.clicked.connect(self.connect_server)
        self.ui.sendButton.clicked.connect(self.send_to_chat)
        self.ui.inputEdit.returnPressed.connect(self.send_to_chat)
        self.ui.contactButton.clicked.connect(self.add_contact)
        self.ui.contactView.doubleClicked.connect(self.contact_clicked)
        self.ui.checkBox.stateChanged.connect(self.toggle_guest)

    def __status(self, str):
        self.ui.stateView.addItem(str)
        self.ui.stateView.scrollToBottom()

    def connect_server(self):
        self.__status('Connecting to server')

    def send_to_chat(self):
        self.__status('Sending to chat')
        self.ui.chatView.addItem(self.ui.inputEdit.text())
        self.ui.chatView.scrollToBottom()
        self.ui.inputEdit.setText('')

    def add_contact(self):
        self.__status('Open contact dialog')
        account, ok_pressed = QtWidgets.QInputDialog.getText(self, 'Add contact', 'Contact name:',
                                                             QtWidgets.QLineEdit.Normal, '')
        if ok_pressed:
            self.__status('Add contact')
            self.ui.contactView.addItem(account)

    def contact_clicked(self, contact):
        self.ui.inputEdit.setText('{}: '.format(self.ui.contactView.currentItem().text()))

    def toggle_guest(self):
        self.__status('Checkbox toggled')
        if self.ui.checkBox.isChecked():
            state = True
        else:
            state = False
        self.ui.accountEdit.setDisabled(state)
        self.ui.passwordEdit.setDisabled(state)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
