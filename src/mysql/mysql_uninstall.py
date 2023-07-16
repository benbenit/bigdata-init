# -*- coding: utf-8 -*-

import subprocess

# 停止MySQL服务
subprocess.call(["sudo", "systemctl", "stop", "mysqld"])

# 卸载MySQL软件包
subprocess.call(["sudo", "yum", "remove", "-y", "mysql-community-server"])
subprocess.call(["sudo", "rpm", "-qa", "|", "grep", "mysql", "|", "xargs", "-n1", "sudo", "rpm",  "-e",  "--nodeps"])
subprocess.call(["sudo", "rpm", "-qa", "|", "grep", "mariadb", "|", "xargs", "-n1", "sudo", "rpm",  "-e",  "--nodeps"])

# 删除MySQL临时密码文件
subprocess.call(["sudo", "rm", "-rf", "/var/log/mysqld.log"])

# 删除MySQL数据目录
subprocess.call(["sudo", "rm", "-rf", "/var/lib/mysql"])

# 清理MySQL配置文件
subprocess.call(["sudo", "rm", "-f", "/etc/my.cnf"])

# 清理MySQL库
subprocess.call(["sudo", "rm", "-f", "/etc/yum.repos.d/mysql-community.repo"])
subprocess.call(["sudo", "yum", "clean", "all"])

print("MySQL已成功卸载")
