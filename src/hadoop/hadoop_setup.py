# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../util")
from xml_conf import update_config_file

# 定义配置信息
hadoop_home = '/home/benbenit/apps/hadoop'
configurations = {
    'hadoop-env.sh': {
        'JAVA_HOME': '/usr/java/latest'
    },
    'core-site.xml': {
        'fs.defaultFS': 'hdfs://node02:8020',
        'hadoop.http.staticuser.user': 'benbenit',
        'hadoop.tmp.dir': '{}/data'.format(hadoop_home)
    },
    'hdfs-site.xml': {
        'dfs.replication': '3',
        'dfs.namenode.http-address': 'node02:9870',
        'dfs.namenode.https-address': 'node02:9871',
        'dfs.namenode.secondary.http-address': 'node04:9868',
        'dfs.namenode.secondary.https-address': 'node04:9869'
    },
    'mapred-site.xml': {
        'mapreduce.framework.name': 'yarn',
        # 历史服务器设置
        'mapreduce.jobhistory.address': 'node02:10020',
        'mapreduce.jobhistory.webapp.address': 'node02:19888',
        'mapreduce.jobhistory.webapp.https.address': 'node02:19890'
    },
    'yarn-site.xml': {
        'yarn.nodemanager.aux-services': 'mapreduce_shuffle',
        'yarn.resourcemanager.hostname': 'node03',
        'yarn.nodemanager.env-whitelist': 'JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME',
        # 开启日志聚集功能,保留3天
        'yarn.log-aggregation-enable': 'true',
        'yarn.log.server.url': 'https://node02:19890/jobhistory/logs',
        'yarn.log-aggregation.retain-seconds': '259200',
        'yarn.nodemanager.pmem-check-enabled': 'false',
        'yarn.nodemanager.vmem-check-enabled': 'false'
    },
    'workers': {
        'node02', 'node03', 'node04'
    }
}


# 配置Hadoop
def configure_hadoop(hadoop_home, configurations):
    # 配置每个配置文件
    for config_file, config_props in configurations.items():
        config_path = '{}/etc/hadoop/{}'.format(hadoop_home, config_file)
        if config_file == 'hadoop-env.sh':
            config_data = config_props.get('JAVA_HOME')
            sed_command = "sed -E -i 's|^[[:space:]]*#*[[:space:]]*(export[[:space:]]+JAVA_HOME)=.*$|\\1={}|' {}".format(config_data, config_path)
            os.system(sed_command)
            print("更新{}: JAVA_HOME".format(config_file))
        elif config_file == 'workers':
            config_data = "\n".join(config_props)
            with open(config_path, "w") as f:
                f.write(config_data)
            print("更新workers...")
        else:
            update_config_file(config_path, config_props)


configure_hadoop(hadoop_home, configurations)

print('本脚本仅用于修改hadoop配置文件,若第一次运行仍需同步集群,并运行"hdfs namenode -format"初始化集群')

