import sys
from PyQt5.QtWidgets import QApplication
from minimal import AppWindow

if __name__=='__main__':
    app = QApplication(sys.argv)
    wid = AppWindow()
    wid.show()
    sys.exit(app.exec_())