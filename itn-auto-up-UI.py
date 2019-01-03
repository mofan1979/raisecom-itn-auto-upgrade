from PyQt5 import QtWidgets
import sys
import test


# 自定义类，继承自pyqt生成的Ui_MainWindow父类
class itn_auto_up(test.Ui_MainWindow):
    def __init__(self, MainWindow):
        # 构造函数继承父类的构造函数
        super().setupUi(MainWindow)


if __name__ == '__main__':
    # 大概是启动qt绘图框架吧
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # 实例化自定义ui类
    ui = itn_auto_up(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
