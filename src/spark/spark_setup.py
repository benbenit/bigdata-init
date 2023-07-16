# -*- coding: utf-8 -*-
import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../util")
from xml_conf import update_config_file
from properties_conf import update_properties_file

hadoop_home = '/home/benbenit/apps/hadoop'
hadoop_conf_dir = '{}/etc/hadoop'.format(hadoop_home)
spark_home = '/home/benbenit/apps/spark'
spark_jar_dir = '{}/jars'.format(spark_home)
spark_conf_dir = '{}/conf'.format(spark_home)
spark_env_temp = '{}/spark-env.sh.template'.format(spark_conf_dir)
spark_env_custom = '{}/spark-env.sh'.format(spark_conf_dir)
spark_default_conf_temp = '{}/spark-defaults.conf.template'.format(spark_conf_dir)
spark_default_conf_custom = '{}/spark-defaults.conf'.format(spark_conf_dir)

if not os.path.exists(spark_env_custom):
    cp_env_cmd = ['cp', spark_env_temp, spark_env_custom]
    subprocess.call(cp_env_cmd)

if not os.path.exists(spark_default_conf_custom):
    cp_spark_conf_cmd = ['cp', spark_default_conf_temp, spark_default_conf_custom]
    subprocess.call(cp_spark_conf_cmd)

# 因为使用的是spark-without-hadoop 的二进制文件,所以依赖包需要自己拷贝
# if not os.path.exists('{}/')


# 检查hdfs是否在运行,创建spark执行日志路径,历史日志路径,jar路径
hadoop_namenode_pid = os.system("ps -ef | grep namenode | grep -v grep | awk '{print $2}'")
if hadoop_namenode_pid != '':
    mkdir_eventlog_cmd = ['hdfs', 'dfs', '-mkdir', '/spark-eventlogs']
    subprocess.call(mkdir_eventlog_cmd)
    mkdir_history_cmd = ['hdfs', 'dfs', '-mkdir', '/spark-history']
    subprocess.call(mkdir_history_cmd)


configurations = {
    'spark-env.sh': {
        'YARN_CONF_DIR': '/home/benbenit/apps/hadoop/etc/hadoop',
        'export SPARK_DIST_CLASSPATH': '$(hadoop classpath)'
    },
    'spark-defaults.conf': {
        # spark的资源管理器
        'spark.master': 'yarn',
        # eventlog可以记录spark应用程序的事件和元数据,使用eventlog可以回放事件数据,以此重新构建程序的执行过程
        'spark.eventLog.enabled': 'true',
        'spark.eventLog.dir': 'hdfs://node02:8020/spark-eventlogs',
        'spark.executor.memory': '4g',
        'spark.driver.memory': '4g',
        # 点击yarn上的spark任务的history按钮,进入spark的历史服务器
        'spark.yarn.historyServer.address': 'node02:18080',
        'spark.history.fs.logDirectory': 'hdfs://node02:8020/spark-history',
        'spark.history.retainedApplications': '30'
    },
    'yarn-site.xml': {
        # 是否启动一个线程检查每个任务正使用的物理内存量
        'yarn.nodemanager.pmem-check-enabled': 'false',
        # 是否启动一个线程检查每个任务正使用的虚拟内存量
        'yarn.nodemanager.vmem-check-enabled': 'false'
    }
}


def configure_spark(configurations):
    # 配置每个配置文件
    for config_file, config_props in configurations.items():
        if config_file == 'spark-env.sh':
            update_properties_file(spark_env_custom, config_props)
        elif config_file == 'spark-defaults.conf':
            update_properties_file(spark_default_conf_custom, config_props)
        else:
            hadoop_config_path = '{}/etc/hadoop/{}'.format(hadoop_home, config_file)
            update_config_file(hadoop_config_path, config_props)


configure_spark(configurations)

