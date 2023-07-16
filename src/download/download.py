# -*- coding: utf-8 -*-

import os
import subprocess
import urllib
import urllib2

# 定义要下载的框架及其版本
frameworks = {
    'scala': 'https://downloads.lightbend.com/scala/2.12.10/scala-2.12.10.tgz',
    'hadoop': 'https://archive.apache.org/dist/hadoop/common/hadoop-3.1.3/hadoop-3.1.3.tar.gz',
    # 官方hive
    # 'hive': 'https://archive.apache.org/dist/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz',
    # 重新编译的hive 3.1.2 版本, 适用 hadoop 3.1.3 spark 3.1.3
    'hive': 'https://github.com/benbenit/hive-on-spark/releases/download/rel%2Frelease-3.1.2/apache-hive-3.1.2-bin.tar.gz',
    'spark': 'https://archive.apache.org/dist/spark/spark-3.1.3/spark-3.1.3-bin-without-hadoop.tgz',
    # 'flume': 'https://archive.apache.org/dist/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz',
    # 'hbase': 'https://archive.apache.org/dist/hbase/2.4.11/hbase-2.4.11-bin.tar.gz',
    # 'kafka': 'https://archive.apache.org/dist/kafka/3.0.0/kafka_2.12-3.0.0.tgz',
    # 'maxwell': 'https://github.com/zendesk/maxwell/releases/download/v1.29.2/maxwell-1.29.2.tar.gz',
    # 'phoenix': 'https://archive.apache.org/dist/phoenix/phoenix-5.1.2/phoenix-hbase-2.4-5.1.2-bin.tar.gz',
    # 'zookeeper': 'https://archive.apache.org/dist/zookeeper/zookeeper-3.5.7/apache-zookeeper-3.5.7-bin.tar.gz',
    # 'flink': 'https://archive.apache.org/dist/flink/flink-1.13.6/flink-1.13.6-bin-scala_2.12.tgz',
}

# 获取系统代理配置
proxies = urllib.getproxies()

# 定义目标目录
target_dir = os.path.expanduser('/home/benbenit/apps')

# 定义压缩包路径列表
target_files = []

# 下载并解压框架
for framework, url in frameworks.items():
    if not os.path.exists(os.path.join(target_dir, ''.join(framework))):
        # 下载tar包名字: apache-flume-1.9.0-bin.tar.gz
        download_tar_name = ''.join(os.path.basename(url))
        # 下载tar包路径: /home/benbenit/apps/apache-flume-1.9.0-bin.tar.gz
        target_file = os.path.join(target_dir, download_tar_name)
        # 解压tar包之后名字: apache-flume-1.9.0-bin
        if framework == 'flink' or 'scala':
            extracted_dir_name = os.path.splitext(download_tar_name)[0]
        else:
            extracted_dir_name = os.path.splitext(os.path.splitext(download_tar_name)[0])[0]
        # 解压tar包之后路径: /home/benbenit/apps/apache-flume-1.9.0-bin
        extracted_dir = os.path.join(target_dir, extracted_dir_name)
        # 重命名目录: /home/benbenit/apps/flume
        renamed_dir = os.path.join(target_dir, framework)

        # 创建代理处理器
        proxy_handler = urllib2.ProxyHandler(proxies)

        # 创建 URL opener，并设置代理处理器
        opener = urllib2.build_opener(proxy_handler)

        # 下载框架
        if not os.path.exists(renamed_dir):
            if not os.path.exists(extracted_dir):
                if not os.path.exists(target_file):
                    print('正在下载 {}'.format(url))
                    urllib.urlretrieve(url, target_file)

        # 解压框架
        if not os.path.exists(renamed_dir):
            if not os.path.exists(extracted_dir):
                print('正在解压 {}'.format(download_tar_name))
                subprocess.check_call(['tar', 'xf', target_file, '-C', target_dir])

        # 重命名文件夹
        if not os.path.exists(renamed_dir):
            extracted_dir_list = os.listdir(target_dir)
            for extracted_name in extracted_dir_list:
                if os.path.isdir(os.path.join(target_dir, extracted_name)) and framework in extracted_name:
                    extracted_dir_new = os.path.join(target_dir, extracted_name)
                    print('重命名 {} 为 {}'.format(extracted_name, framework))
                    os.rename(extracted_dir_new, renamed_dir)
                    break

        # 将压缩包路径添加到列表中
        target_files.append(target_file)
    else:
        print(framework + ' 安装完成！')

    # 删除压缩包
    if target_files:
        for target_file in target_files:
            if os.path.exists(target_file):
                print('删除压缩包 {}'.format(os.path.basename(target_file)))
                os.remove(target_file)
            else:
                print('{}已删除,无需重复删除'.format(target_file))


