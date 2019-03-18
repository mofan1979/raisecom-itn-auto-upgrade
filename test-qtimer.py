from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QObject
import sys
# 注意 作为类来调用模块，需要继承QObject
# class AA(QObject):
#     def __init__(self):
#         super(QObject, self).__init__()
#         self.time = QTimer(self)
#         self.time.start(200)
#         self.time.timeout.connect(self.aa)

def work():
    print("3333333333")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # aa = AA()
    t = QTimer()
    t.start(200)
    t.timeout.connect(work)
    sys.exit(app.exec_())
