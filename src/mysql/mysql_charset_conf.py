# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../util")
from my_cnf import modify_my_cnf

config_file = '/etc/my.cnf'  # 指定 my.cnf 文件的路径
modify_charset = {
    'character-set-server': 'utf8mb4',
    'collation-server': 'utf8mb4_unicode_ci'
}

success = modify_my_cnf(config_file, modify_charset)
if success:
    print('my.cnf 文件修改成功！')
    os.system('sudo systemctl restart mysqld')
else:
    print('my.cnf 文件修改失败。')
