- ITN185_331批量升级工具v1.5说明
- 编写人：莫凡 500264@qq.com
- 鸣谢：冀文超 提供源代码思路
- 版本日期：20190725
- 说明：
1. 本脚本用于台式IPRAN设备的自动一键升级，用户不需检查待升级设备类型，脚本会自动搜索匹配升级规则，如果匹配不到规则，会报错并继续匹配下一台;
2. 升级规则通过/upgrade_rule.csv定制。包括匹配设备类型、硬件版本、指定目标bootrom版本和文件、指定目标system版本和文件、是否备份配置、ftp下载账号、是否重启激活等。每种设备一行，详见具体文件。
3. upgrade_rule.csv、u_ip_list.txt必须和程序文件放在同一目录下，且不能改名。
4. 升级时一定要保证itn设备FLASH内存空间足够，否则异常!
5. 升级设备ip列表放在/u_ip_list.txt供程序读取设备ip，每行一条ip
6. 升级结果日志放在/result子目录下，文件名为“日期_时间.csv”，如果/result目录不存在，自动创建
7. 程序为多进程并行升级，需根据PC性能配置决定并发进程数，数量过多会影响稳定性，ftp服务端程序需要支持高并发下载，推荐使用FileZilla server服务器程序。
8. 升级规则可以指定升级前、升级成功后擦除旧版本文件，当然新版本文件名不能用同样的名字，否则会被误擦除！
9. 目前不支持paf文件升级
10. 命令行使用“upgrade_iTN185_331_multiprocess.exe -p P_NUM”可实现无人值守静默升级，P_NUM为并发进程数，P_NUM必须大于等于1小于等于99。  
11. 设备登录用户名密码为出厂默认。暂不支持用户自定义用户名密码。
12. 如果windows环境运行提示缺少API-MS-Win-Core-Console-L1-1-0.dll运行库，请下载安装[微软常用运行库合集](http://baoku.360.cn/soft/show/appid/104698064)

20190420更新V1.3版本，修复一些telnet会话挂死bug，提升稳定性。  
20190724更新V1.4版本，修复擦除flash遗留镜像文件时误报失败的bug。  
20190725更新V1.5版本，修复boot next误报失败的bug。  

- 测试64进程并发升级170台iTN331设备只需要28分钟左右。
![效率演示](https://github.com/mofan1979/raisecom-itn-auto-upgrade/blob/master/%E5%8D%87%E7%BA%A7170%E5%8F%B0%E8%AE%BE%E5%A4%87%E8%80%97%E6%97%B6%E6%A0%B7%E4%BE%8B.jpg?raw=true)

- 结果由列表文件显示，直观方便统计和后续处理。

![结果演示](https://github.com/mofan1979/raisecom-itn-auto-upgrade/blob/master/170%E5%8F%B0%E5%8D%87%E7%BA%A7%E7%BB%93%E6%9E%9C%E6%A0%B7%E4%BE%8B.jpg?raw=true)
