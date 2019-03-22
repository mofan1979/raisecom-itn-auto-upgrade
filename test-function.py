from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QObject
import sys,os
from datetime import datetime
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
    # app = QApplication(sys.argv)
    # # aa = AA()
    # t = QTimer()
    # t.start(200)
    # t.timeout.connect(work)
    # sys.exit(app.exec_())
    # # print(sys.argv)
    # home = os.getcwd()
    # f3 = os.path.join(home, 'result')
    # if not os.path.exists(f3):
    #     os.makedirs(f3)
    # print(f3)
    # start_time = datetime.now()
    # logfile = os.path.join(f3,'%s.csv') % start_time.strftime('%Y%m%d_%H%M%S')
    # print(logfile)

    while True:
        # 接收控制台输入，input方法获取的是字符串，需要转成整数
        p_num = int(input('请输入并发进程数，推荐为CPU数量的整数倍：'))
        if 0 < p_num < 100:
            break
        print("非法数值，请从新输入1到99之间的整数")
    print(p_num)