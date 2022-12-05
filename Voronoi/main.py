# $LAN=PYTHON$
# Python 3.10.7
# 中山大學資訊工程所 M113040019 余承叡
# 執行方法: 在虛擬環境下安裝pyqt5，並在虛擬環境中執行 python main.py

from PyQt5 import QtWidgets
from MainWidget import MainWidget


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())
