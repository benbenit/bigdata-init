# -*- coding: utf-8 -*-
import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../util")
from xml_conf import update_config_file
from properties_conf import update_properties_file

hadoop_home = '/home/benbenit/apps/hadoop'
hadoop_conf_dir = '{}/etc/hadoop'.format(hadoop_home)
hadoop_guava_jar_path = '{}/share/hadoop/common/lib/guava-27.0-jre.jar'.format(hadoop_home)

hive_home = '/home/benbenit/apps/hive'
hive_conf_dir = "{}/conf".format(hive_home)
hive_lib_dir = '{}/lib'.format(hive_home)

hive_site = "{}/hive-site.xml".format(hive_conf_dir)
hive_log4j_temp = "{}/hive-log4j2.properties.template".format(hive_conf_dir)
hive_log4j_custom = '{}/hive-log4j2.properties'.format(hive_conf_dir)
hive_env_temp = "{}/hive-env.sh.template".format(hive_conf_dir)
hive_env_custom = "{}/hive-env.sh".format(hive_conf_dir)
hive_guava_jar_path = '{}/guava-19.0.jar'.format(hive_lib_dir)
mysql_driver_url = "https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.49/mysql-connector-java-5.1.49.jar"

if not os.path.exists(hive_site):
    with open(hive_site, "w") as f:
        f.write("<?xml version='1.0'?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n<configuration>\n</configuration>")

# hive的log日志路径
if not os.path.exists(hive_log4j_custom):
    cp_log4j_cmd = ["cp", hive_log4j_temp, hive_log4j_custom]
    subprocess.call(cp_log4j_cmd)

# 新版hive默认申请JVM堆内存为256M,申请的太小,可能会OOM
if not os.path.exists(hive_env_custom):
    cp_hive_env_cmd = ["cp", hive_env_temp, hive_env_custom]
    subprocess.call(cp_hive_env_cmd)

configurations = {
    'hive-env.sh': {
        'HADOOP_HEAPSIZE': '2048'
    },
    'hive-log4j2.properties': {
        'property.hive.log.dir': '/home/benbenit/apps/hive/logs'
    },
    'core-site.xml': {
        # 将hiveserver2的启动用户设置为hadoop的代理用户
        'hadoop.proxyuser.benbenit.hosts': '*',
        'hadoop.proxyuser.benbenit.groups': '*',
        'hadoop.proxyuser.benbenit.users': '*'
    },
    'hive-site.xml': {
        # mysql 连接配置 url, driver, name, password
        'javax.jdo.option.ConnectionURL': 'jdbc:mysql://node02:3306/hive_metastore?createDatabaseIfNotExist=true&amp;useSSL=false',
        'javax.jdo.option.ConnectionDriverName': 'com.mysql.jdbc.Driver',
        'javax.jdo.option.ConnectionUserName': 'root',
        'javax.jdo.option.ConnectionPassword': 'hadoop',
        # hive在hdfs默认的工作路径
        'hive.metastore.warehouse.dir': '/user/hive/warehouse',
        # metastore服务的地址
        'hive.metastore.uris': 'thrift://node02:9083',
        'hive.metastore.schema.verification': 'false',
        'hive.metastore.event.db.notification.api.auth': 'false',
        # 指定hiveserver2连接的host和端口号
        'hive.server2.thrift.bind.host': 'node02',
        'hive.server2.thrift.port': '10000',
        # hive客户端显示当前表头
        'hive.cli.print.header': 'true'
        # hive客户端显示当前库
        # 'hive.cli.print.current.db': 'true'
    },
    'yarn-site.xml': {
        # 是否启动一个线程检查每个任务正使用的物理内存量
        'yarn.nodemanager.pmem-check-enabled': 'false',
        # 是否启动一个线程检查每个任务正使用的虚拟内存量
        'yarn.nodemanager.vmem-check-enabled': 'false'
        # 一个NodeManager节点分配给Container使用的内存:64G
        # 'yarn.nodemanager.resource.memory-mb': ''.join('65536'),
        # 一个NodeManager节点分配给Container使用的虚拟CPU核数
        # 'yarn.nodemanager.resource.cpu-vcores': ''.join('16'),
        # 单个Container能够使用的最大内存:16G
        # 'yarn.scheduler.maximum-allocation-mb': ''.join('16384'),
        # 单个Container能够使用的最小内存:512M
        # 'yarn.scheduler.minimum-allocation-mb': ''.join('512')
    }
}


def configure_hive(configurations):
    for config_file, config_props in configurations.items():
        if config_file == "hive-site.xml":
            update_config_file(hive_site, config_props)
        elif config_file == "hive-log4j2.properties":
            update_properties_file(hive_log4j_custom, config_props)
        elif config_file == "hive-env.sh":
            update_properties_file(hive_env_custom, config_props)
        else:
            hadoop_conf_file = '{}/{}'.format(hadoop_conf_dir, config_file)
            update_config_file(hadoop_conf_file, config_props)


configure_hive(configurations)

# 使用wget命令下载MySQL驱动到Hive的lib目录
if not os.path.exists('{}/mysql-connector-java-5.1.49.jar'.format(hive_lib_dir)):
    download_mysql_driver_cmd = ["wget", mysql_driver_url, "-P", hive_lib_dir]
    subprocess.call(download_mysql_driver_cmd)

# 使用高版本的 guava 替换 lib下的jar包,若自己编译的则不用修改
if os.path.exists(hive_guava_jar_path):
    rm_guava_cmd = ["rm", hive_guava_jar_path]
    subprocess.call(rm_guava_cmd)

if not os.path.exists('{}/guava-27.0-jre.jar'.format(hive_lib_dir)):
    cp_guava_cmd = ["cp", hadoop_guava_jar_path, hive_lib_dir]
    subprocess.call(cp_guava_cmd)

# 解决log4j版本冲突
if os.path.exists('{}/log4j-slf4j-impl-2.10.0.jar'.format(hive_lib_dir)):
    rename_cmd = ['mv', '{}/log4j-slf4j-impl-2.10.0.jar'.format(hive_lib_dir), '{}/log4j-slf4j-impl-2.10.0.jar.bak'.format(hive_lib_dir)]
    subprocess.call(rename_cmd)


print("""
修改 Hive 配置完成
请运行 schematool -initSchema -dbType mysql -verbose 初始化元数据库
若使用 spark 引擎,请先安装配置spark,并启动hadoop集群,
运行 hive_on_spark.py 脚本
""")

