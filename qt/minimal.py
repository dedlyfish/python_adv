from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QWidget

class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(CentralWidget, self).__init__(*args, **kwargs)
        lay = QVBoxLayout()

        self.list = QListWidget()
        self.text = QLineEdit()
        self.send_btn = QPushButton('send')

        self.setLayout(lay)
        lay.addWidget(self.list)
        lay.addWidget(self.text)
        lay.addWidget(self.send_btn)

class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)
        self.wid = CentralWidget()
        self.setCentralWidget(self.wid)
        self.wid.send_btn.clicked.connect(self.send_chat)
        self.wid.text.returnPressed.connect(self.send_chat)

    def send_chat(self):
        self.wid.list.addItem(self.wid.text.text())
        self.wid.list.scrollToBottom()
        self.wid.text.setText('')