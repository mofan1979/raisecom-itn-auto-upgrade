from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog
import sys
import test


# 自定义类，继承自pyqt生成的Ui_MainWindow父类
class itn_auto_up(QMainWindow, test.Ui_MainWindow):
    def __init__(self):
        # 构造函数继承父类的构造函数
        # # 以下为传统写法
        # QMainWindow.__init__(self)
        # test.Ui_MainWindow.__init__(self)
        # 以下为新式写法
        super(itn_auto_up, self).__init__()
        self.setupUi(self)

    def get_rule(self):
        filename, ok = QFileDialog.getOpenFileName(self, '读取规则文件', 'c:/')
        if ok:
            print(filename)


if __name__ == '__main__':
    # 大概是启动qt绘图框架吧，套路
    app = QApplication(sys.argv)
    # 实例化自定义ui类
    ui = itn_auto_up()
    ui.show()
    sys.exit(app.exec_())
