from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,QMessageBox
import sys
import test
import telnetlib  # 调用telnet方法需要的库
from datetime import datetime
from multiprocessing import Pool
from time import sleep


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
        f1, ok = QFileDialog.getOpenFileName(self, '读取规则文件', '', '*.csv')
        if ok:
            # print(f1)
            self.rule_confirm.setText(f1)
        # 判断所有必填项已经填写，开放升级按钮
        self.get_ready()

    def get_ip(self):
        f2, ok = QFileDialog.getOpenFileName(self, '读取ip列表文件', '', '*.txt')
        if ok:
            # print(f2)
            with open(f2, 'r') as f:
                # 读取文件
                my_ip_hosts = f.read()
            self.hosts.setPlainText(my_ip_hosts)
        # 判断所有必填项已经填写，开放升级按钮
        self.get_ready()

    def get_res_dir(self):
        f3 = QFileDialog.getExistingDirectory(self, '设置结果保存目录', '.')
        self.res_dir.setText(f3)
        # 判断所有必填项已经填写，开放升级按钮
        self.get_ready()

    def get_ready(self):
        # 判断所有必填项已经填写，开放升级按钮
        if self.hosts.toPlainText() != '' and self.res_dir.toPlainText() != '' and self.rule_confirm.toPlainText() != '' and self.setpool.text() != '':
            self.pushButton_3.setEnabled(True)
        else:
            self.pushButton_3.setEnabled(False)

    def update_itn185_331(self, ip, rule):
        # 定义执行升级函数，需要传入参数为设备ip，规则列表矩阵
        # 尝试发起telnet连接
        t90 = datetime.now()
        try:
            tn = telnetlib.Telnet(ip.encode(), port=23, timeout=3)
            # 登陆交互
            tn.write('\n'.encode())
            tn.read_until(b'Login:')
            tn.write('raisecom\n'.encode())
            tn.read_until(b'Password:')
            tn.write('raisecom\n'.encode())
            tn.read_until(b'>')
            tn.write('enable\n'.encode())
            tn.read_until(b'Password:')
            tn.write('raisecom\n'.encode())
            tn.read_until(b'#')
            tn.write('show version\n'.encode())  # 读取设备版本
            devinfo = tn.read_until(b'#').decode()  # 解码成Unicode格式以供比对
            # print(devinfo)
            # 逐行比对升级规则
            for r in rule:
                ftp_host = r[9]
                ftp_user = r[10]
                ftp_pw = r[11]
                if devinfo.find('Product Name: %s' % r[0]) >= 0 and devinfo.find('Hardware Version: %s' % r[1]) >= 0:
                    # 匹配设备型号和硬件版本成功
                    devtype = r[0] + ':' + r[1]
                    print(ip, '升级的设备类型是', devtype)
                    # print(devinfo.find(r[3]))
                    if devinfo.find(r[3]) >= 0:
                        print(ip, '恭喜，设备system版本已经是最新，无需升级')
                        return '%s,成功,无需升级\n' % ip
                    # 下载升级包
                    try:
                        # 记录开始时间
                        t0 = datetime.now()
                        # 备份startup配置
                        if r[8] == 'yes':
                            cmd_line = 'write\n'
                            print('[', t0, ']', ip, devtype, '执行', cmd_line)
                            tn.write(cmd_line.encode())
                            tn.read_until(b'#')
                            ft0 = t0.strftime('%Y%m%d_%H%M%S')
                            cmd_line = 'upload startup-config ftp %s %s %s %s-%s.conf\n' % (
                                ftp_host, ftp_user, ftp_pw, ip, ft0)
                            print('[', datetime.now(), ']', ip, devtype, '执行', cmd_line)
                            tn.write(cmd_line.encode())
                            flag = tn.read_until(b'#').decode().find(' success')
                            # 备份不成功则报错退出，成功则继续
                            if flag < 0:
                                # 确认telnet会话是否存活
                                try:
                                    tn.close()
                                    print('[', datetime.now(), ']', '%s,失败,备份startup-config失败' % ip)
                                    return '%s,失败,备份startup-config失败\n' % ip
                                except:
                                    print('[', datetime.now(), ']', '%s,失败,备份startup-config过程中telnet连接中断' % ip)
                                    return '%s,失败,telnet连接中断\n' % ip
                            print('[', datetime.now(), ']', ip, devtype, '备份startup-config成功')
                        # 清理前次升级失败冗余的镜像文件
                        if r[6] != '':
                            tn.write('dir\n'.encode())  # 显示flash文件列表
                            flag = tn.read_until(b'#').decode().find(r[6])
                            # print(flag)
                            if flag >= 0:
                                t60 = datetime.now()
                                cmd_line = 'erase flash/core/%s\n' % r[6]
                                print('[', t60, ']', ip, devtype, '执行', cmd_line)
                                tn.write(cmd_line.encode())
                                tmp = tn.read_until(b"Please input 'yes' to confirm:").decode()
                                # print(tmp)
                                cmd_line1 = 'yes\n'
                                tn.write(cmd_line1.encode())
                                # print(cmd_line1)
                                result = tn.read_until(b'#', timeout=600).decode()
                                print(result.find(' success'))
                                t61 = datetime.now()
                                if result.find(' success') >= 0:
                                    print('[', t61, ']', ip, devtype, cmd_line, '执行成功，耗时：', t61 - t60)
                                else:
                                    print('[', t61, ']', ip, devtype, cmd_line, '执行失败，耗时：', t61 - t60)
                                    # return  '%s,失败,%s出错\n' % ip %cmd_line
                                    # 此处失败不影响后续操作
                        # 下面开始判断升级bootrom
                        t2 = datetime.now()
                        if r[2] != '' and devinfo.find('Bootrom Version: %s' % r[2]) < 0:
                            cmd_line = 'download bootstrap ftp %s %s %s %s\n' % (ftp_host, ftp_user, ftp_pw, r[4])
                            print('[', t2, ']', ip, devtype, '执行', cmd_line)
                            tn.write(cmd_line.encode())
                            result1 = tn.read_until(b'#', timeout=180).decode()  # 获取bootrom升级结果
                            # print(result1)
                            t3 = datetime.now()
                            if result1.find(' success') >= 0:
                                print('[', t3, ']', ip, devtype, 'BOOTROM下载成功，共耗时 ', t3 - t2)
                            # bootrom升级失败则报错退出
                            else:
                                # 判断telnet会话存活
                                try:
                                    tn.close()
                                    print('[', t3, ']', ip, devtype, 'BOOTROM升级异常或超时，共耗时 ', t3 - t2)
                                    return '%s,失败,下载bootrom出错\n' % ip
                                except:
                                    print('[', datetime.now(), ']', '%s,失败,bootrom升级过程中telnet连接中断' % ip)
                                    return '%s,失败,telnet连接中断\n' % ip
                        # 下面开始升级system
                        tn.write('dir\n'.encode())
                        dirlist = tn.read_until(b'#').decode()
                        flag = dirlist.find(r[5])  # 判断是否有已存在的文件，为后面二次确认做准备
                        # print(flag)
                        cmd_line = 'download system ftp %s %s %s %s\n' % (ftp_host, ftp_user, ftp_pw, r[5])
                        t4 = datetime.now()
                        print('[', t4, ']', ip, devtype, 'bootrom版本满足，开始执行', cmd_line)
                        tn.write(cmd_line.encode())
                        # 如果已经有存在的文件，确认覆盖升级
                        if flag >= 0:
                            sleep(3)
                            tn.write('yes\n'.encode())  # 等待3秒后输入yes二次确认
                        # 获取命令结果
                        result1 = tn.read_until(b'#', timeout=2700).decode()
                        # print(result1)
                        t5 = datetime.now()
                        # 判断返回，如果含有download system success，则成功，超时抛出失败
                        if result1.find(' success') >= 0:  # 注意success前有空格，以便区分unsuccessful和successful
                            # 指定启动文件
                            cmd_line = 'boot next-startup %s \n' % r[5]
                            print('[', t5, ']', ip, devtype, 'system下载成功，耗时', t5 - t4, '，正在执行', cmd_line)
                            tn.write(cmd_line.encode())
                            result3 = tn.read_until(b'#', timeout=300).decode()
                            t6 = datetime.now()
                            # 判断boot next-startup是否成功
                            if result3.find(' success') >= 0:
                                print('[', t6, ']', ip, devtype, cmd_line, '执行成功，耗时', t6 - t5)
                                # 判断是否需要擦除旧的镜像文件
                                if r[7] != '':
                                    # 将r[7]单元格所列文件名按分隔符/切片
                                    eraselist = r[7].split('/')
                                    # 迭代比较列表中文件名
                                    for e in eraselist:
                                        # 假如存在该文件名则擦除
                                        if dirlist.find(e) >= 0:
                                            t6 = datetime.now()
                                            cmd_line = 'erase flash/core/%s\n' % e
                                            print('[', t6, ']', ip, devtype, '执行', cmd_line)
                                            tn.write(cmd_line.encode())
                                            sleep(2)
                                            cmd_line2 = 'yes\n'
                                            tn.write(cmd_line2.encode())
                                            # print(cmd_line)
                                            tmp = tn.read_until(b'#').decode()
                                            # print(tmp)
                                            t7 = datetime.now()
                                            # 此处擦除成功与否不影响升级结果
                                            if tmp.find(' success') >= 0:
                                                print('[', t7, ']', ip, devtype, '执行', cmd_line, '成功，耗时：', t7 - t6)
                                            else:
                                                print('[', t7, ']', ip, devtype, '执行', cmd_line, '失败，耗时：', t7 - t6)
                                # 判断是否需要重启激活，只有填写yes才重启，其他值均不重启。注意r[12]作为行尾带有换行符'\n'
                                if r[12].find('yes') >= 0:
                                    cmd_line = 'write\n'
                                    tn.write(cmd_line.encode())
                                    tn.read_until(b'#')
                                    cmd_line = 'reboot now\n'
                                    print('[', datetime.now(), ']', ip, devtype, '执行', cmd_line)
                                    tn.write(cmd_line.encode())
                                    return '%s,成功,升级systemboot成功，并重启激活\n' % ip
                                # 如果不需要重启激活
                                else:
                                    # 判断telnet会话存活
                                    try:
                                        tn.close()
                                        print('[', t6, ']', ip, devtype, '等待重启激活')
                                        return '%s,成功,升级systemboot成功，等待重启激活\n' % ip
                                    except:
                                        print('[', datetime.now(), ']', '%s,失败,指定启动文件过程中telnet连接中断' % ip)
                                        return '%s,失败,telnet连接中断\n' % ip
                            # boot next-startup执行错误处理
                            else:
                                # 判断telnet会话存活
                                try:
                                    tn.close()
                                    print('[', t6, ']', ip, devtype, '执行', cmd_line, '失败，耗时', t6 - t5)
                                    return '%s,失败,指定boot next-startup文件失败\n' % ip
                                except:
                                    print('[', datetime.now(), ']', '%s,失败,指定启动文件过程中telnet连接中断' % ip)
                                    return '%s,失败,telnet连接中断\n' % ip
                        # 如果system下载失败
                        else:
                            try:
                                # 确认telnet会话是否存活
                                tn.close()
                                print('[', t5, ']', ip, devtype, cmd_line, '执行异常或超时，耗时 ', t5 - t4)
                                return '%s,失败,下载system出错\n' % ip
                            except:
                                print('[', t5, ']', ip, devtype, '升级system过程telnet连接中断，耗时 ', t5 - t4)
                                return '%s,失败,telnet连接中断\n' % ip
                    # 升级过程异常处理
                    except:
                        t8 = datetime.now()
                        try:
                            # 确认telnet会话是否存活
                            tn.close()
                            print('[', t8, ']', ip, devtype, '升级异常，其他未知原因，共耗时 ', t8 - t0)
                            return '%s,失败,其他未知原因\n' % ip
                        except:
                            print('[', t8, ']', ip, devtype, '升级异常，telnet连接中断，共耗时 ', t8 - t0)
                            return '%s,失败,telnet连接中断\n' % ip
            # 遍历规则无匹配的处理
            t91 = datetime.now()
            try:
                # 确认telnet会话是否存活
                tn.close()
                print('%s，失败，不支持的设备类型' % ip)
                return '%s,失败,不支持的设备类型\n' % ip
            except:
                print('[', t91, ']', ip, '比对型号版本过程异常，telnet连接中断，共耗时 ', t91 - t90)
                return '%s,失败,telnet连接中断\n' % ip
        # telnet异常错误处理
        except:
            print('%s telnet连接失败，非RC设备或设备离线' % ip)
            return '%s,失败,非RC设备或设备离线\n' % ip

    def multiprocess_update(self):
        # 从rule_confirm控件中取出文件名
        f1 = self.rule_confirm.toPlainText()
        print(f1)
        if f1 == '':
            QMessageBox.information(self,"error",)
        # 逐行取出规则，放到列表rule[]中
        rule = []
        try:
            with open(f1, mode='r') as f:
                for line in f:
                    rule.append(line.split(','))
        # 规则文件读取错误处理
        except:
            print('错误，升级规则文件%s不存在或路径错误' % f1)
            exit()
        # 剔除首行抬头说明行
        rule.pop(0)
        # 校验每行升级规则是否符合规范
        for r in rule:
            index = rule.index(r) + 2
            # 必填字段缺失错误处理
            if r[0] == '' or r[1] == '' or r[3] == '' or r[5] == '':
                print('错误！升级规则表第%d行中必填字段未填写！' % index)
                exit()
            # bootrom镜像文件缺失错误处理
            if r[2] != '' and r[4] == '':
                print('错误！升级规则表第%d行中定义了bootrom目标版本，未定义bootrom升级文件' % index)
                exit()
        # 读取hosts文本框的内容切片成设备列表，移除空行
        ip_list = self.hosts.toPlainText().split()
        for i in ip_list:
            if i == '':
                ip_list.remove(i)
        start_time = datetime.now()
        # 结果日志存路径，文件名为格式化日期_时间.csv
        my_dir = self.res_dir.toPlainText()
        logfile = '%s/result%s.csv' % (my_dir, start_time.strftime('%Y%m%d_%H%M%S'))
        try:
            log = open(logfile, mode='a')
        # 日志文件操作错误处理
        except:
            print('错误，结果日志文件存放路径/result不存在')
            exit()
        # 从setpool文本框控件取出线程数值
        pool_num = self.setpool.text()
        # 创建进程池
        p = Pool(pool_num)
        # 开启多进程异步升级，回调函数记录结果到log文件
        for ip in ip_list:
            p.apply_async(self.update_itn185_331, args=(ip, rule,), callback=log.write)
        p.close()
        p.join()
        log.close()
        end_time = datetime.now()
        print(end_time, '批量升级执行完成，共耗时', end_time - start_time)


if __name__ == '__main__':
    # 大概是启动qt绘图框架吧，套路
    app = QApplication(sys.argv)
    # 实例化自定义ui类
    ui = itn_auto_up()
    ui.show()
    sys.exit(app.exec_())
