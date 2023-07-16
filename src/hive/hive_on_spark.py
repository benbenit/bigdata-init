# -*- coding: utf-8 -*-
import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../util")
from xml_conf import update_config_file

hive_home = '/home/benbenit/apps/hive'
spark_home = '/home/benbenit/apps/spark'
hive_conf_dir = "{}/conf".format(hive_home)
hive_lib_dir = "{}/lib".format(hive_home)
spark_jars_dir = '{}/jars'.format(spark_home)
hive_site = "{}/hive-site.xml".format(hive_conf_dir)

configs = {
    'hive-site.xml': {
        'spark.yarn.jars': 'hdfs://node02:8020/spark-jars/*',
        'hive.execution.engine': 'spark',
        'hive.spark.client.connect.timeout': '10000ms'
    }
}


def hdfs_put_jars():
    mkdir_jar_cmd = ['hdfs', 'dfs', '-mkdir', '/spark-jars']
    process = subprocess.Popen(mkdir_jar_cmd)
    process.wait()
    os.system('hdfs dfs -put /home/benbenit/apps/spark/jars/* /spark-jars')
    put_log4j_api_cmd = ['hdfs', 'dfs', '-put', '/home/benbenit/apps/hive/lib/log4j-api-2.10.0.jar', '/spark-jars']
    subprocess.call(put_log4j_api_cmd)
    put_log4j_core_cmd = ['hdfs', 'dfs', '-put', '/home/benbenit/apps/hive/lib/log4j-core-2.10.0.jar', '/spark-jars']
    subprocess.call(put_log4j_core_cmd)


def cp_sparkjar_to_hivelib():
    if not os.path.exists('{}/scala-library-2.12.10.jar'.format(hive_lib_dir)):
        cp_scala_lib_cmd = ['cp', '{}/scala-library-2.12.10.jar'.format(spark_jars_dir), hive_lib_dir]
        subprocess.call(cp_scala_lib_cmd)
    print('复制 {} 到 {}'.format('scala-library-2.12.10.jar', hive_lib_dir))
    if not os.path.exists('{}/spark-core_2.12-3.1.3.jar'.format(hive_lib_dir)):
        cp_scala_lib_cmd = ['cp', '{}/spark-core_2.12-3.1.3.jar'.format(spark_jars_dir), hive_lib_dir]
        subprocess.call(cp_scala_lib_cmd)
        print('复制 {} 到 {}'.format('spark-core_2.12-3.1.3.jar', hive_lib_dir))
    if not os.path.exists('{}/spark-network-common_2.12-3.1.3.jar'.format(hive_lib_dir)):
        cp_scala_lib_cmd = ['cp', '{}/spark-network-common_2.12-3.1.3.jar'.format(spark_jars_dir), hive_lib_dir]
        subprocess.call(cp_scala_lib_cmd)
        print('复制 {} 到 {}'.format('park-network-common_2.12-3.1.3.jar', hive_lib_dir))


# 检查hdfs是否在运行,创建spark执行日志路径,历史日志路径,jar路径
def check_and_put_jars():
    if os.system("ps -ef | grep namenode | grep -v grep | awk '{print $2}'") != '':
        # 执行hdfs dfs -test命令检查路径是否存在
        check_command = ['hdfs', 'dfs', '-test', '-d', '/spark-jars']
        return_code = subprocess.call(check_command)
        if return_code == 0:
            rm_jar_cmd = ['hdfs', 'dfs', '-rm', '-r', '/spark-jars']
            rm_process = subprocess.Popen(rm_jar_cmd)
            rm_process.wait()
            hdfs_put_jars()
        else:
            hdfs_put_jars()
    else:
        print("请先启动hdfs")
        exit()


def configure_hive_on_spark(configurations):
    for config_file, config_props in configurations.items():
        update_config_file(hive_site, config_props)


configure_hive_on_spark(configs)
cp_sparkjar_to_hivelib()
check_and_put_jars()

