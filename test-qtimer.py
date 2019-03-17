'''ITN185_331批量升级后台服务v1.0说明
编写人：莫凡 500264@qq.com
版本日期：20190316
说明：
1、本脚本用于台式IPRAN设备的自动一键升级，用户不需检查待升级设备类型，脚本会自动搜索匹配升级规则，
如果匹配不到规则，会报错并继续匹配下一台;
2、升级规则通过e:/python/upgrade_rule.csv定制。包括匹配设备类型、硬件版本、指定目标bootrom版本和文件、
指定目标system版本和文件、是否备份配置、ftp下载账号、是否重启激活等。每种设备一行，详见具体文件。
3、程序运行后定时轮询所有设备，自动升级
4、升级时一定要保证itn设备FLASH内存空间足够，否则异常!
5、升级设备ip列表放在e:/python/u_ip_list.txt供程序读取设备ip，每行一条ip
6、升级结果日志放在e:/python/result/目录下，文件名为“日期_时间.csv”
7、程序为多进程并行升级，需根据PC性能配置决定并发进程池大小Pool（），数量过多会影响稳定性，ftp服务端
程序需要支持高并发下载，推荐使用FileZilla server服务器程序。
8、升级规则可以指定升级前、升级成功后擦除旧版本文件，当然新版本文件名不能用同样的名字，否则会被误擦除！
'''

import telnetlib  # 调用telnet方法需要的库
from datetime import datetime
from multiprocessing import Pool
from PyQt5.QtCore import *


class test(QTimer):
    def __init__(self, parent=None):
        super(test, self).__init__(parent)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.work)

    def work(self):
        print('现在时间是', datetime.now())


if __name__ == '__main__':
    t = test()
