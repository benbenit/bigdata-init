# -*- coding: utf-8 -*-

import re
import subprocess

# 步骤1：更新系统软件包
subprocess.call(["sudo", "yum", "update", "-y"])

# 步骤2：创建并编辑 MySQL Yum 存储库文件
mysql_repo = """
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=https://repo.mysql.com/yum/mysql-5.7-community/el/7/$basearch/
enabled=1
gpgcheck=0
"""

with open("/etc/yum.repos.d/mysql-community.repo", "w") as file:
    file.write(mysql_repo)

# 步骤3：安装 MySQL 5.7
subprocess.call(["sudo", "yum", "install", "-y", "mysql-community-server"])

# 步骤4：启动 MySQL 服务
subprocess.call(["sudo", "systemctl", "start", "mysqld"])

# 步骤5：检查 MySQL 服务状态
subprocess.call(["sudo", "systemctl", "status", "mysqld"])

# 步骤6: 提取临时密码
# 6.1 定义正则表达式模式来匹配临时密码行
password_pattern = r'A temporary password is generated for root@localhost: (\S+)'

# 6.2 读取日志文件
with open('/var/log/mysqld.log', 'r') as file:
    log_content = file.read()

# 6.3 查找最后一次出现的临时密码行
matches = re.findall(password_pattern, log_content)

print("============================================")
if not matches:
    print("未发现临时密码")
    exit(1)
else:
    temporary_password = matches[-1]
    print("请使用临时密码 {} 登陆mysql完成初始配置...".format(temporary_password))

    # 7. 进入 MySQL 进行配置
    prompt = """
    设置复杂密码: set password=password("Qps1024@mb");
    密码长度限制: set global validate_password_length=4;
    密码安全级别: set global validate_password_policy=0;
    设置简单密码: set password=password("hadoop");
    允许远程登录: update mysql.user set host="%" where user="root";
    刷新权限: flush privileges;
    退出: quit;
    若需修改默认字符集,请在 /etc/my.cnf -> [mysqld] 下添加以下配置,并重启mysql服务
    
    """
    print(prompt)

    mysql_login_command = ["mysql", "-uroot", "-p"]

    subprocess.call(mysql_login_command)
