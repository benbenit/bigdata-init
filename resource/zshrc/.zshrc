alias virtualenv="~/.local/bin/virtualenv"

# 启用代理函数
setProxy() {
    export http_proxy="http://172.16.167.1:7890"
    export https_proxy="http://172.16.167.1:7890"
    echo "代理已启用"
}

# 禁用代理函数
unsetProxy() {
    unset http_proxy
    unset https_proxy
    echo "代理已禁用"
}

export JAVA_HOME=/usr/java/default
export PATH=$PATH:$JAVA_HOME/bin

export HADOOP_HOME=~/apps/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

export ZOOKEEPER_HOME=~/apps/zookeeper
export PATH=$PATH:$ZOOKEEPER_HOME/bin

export HIVE_HOME=~/apps/hive
export PATH=$PATH:$HIVE_HOME/bin

export FLUME_HOME=~/apps/flume
export PATH=$PATH:$FLUME_HOME/bin

export KAFKA_HOME=~/apps/kafka
export PATH=$PATH:$KAFKA_HOME/bin

export HBASE_HOME=~/apps/hbase
export PATH=$PATH:$HBASE_HOME/bin

export PHOENIX_HOME=~/apps/phoenix
export PATH=$PATH:$PHOENIX_HOME/bin

export SPARK_HOME=~/apps/spark
export PATH=$PATH:$SPARK_HOME/bin

export FLINK_HOME=~/apps/flink
export PATH=$PATH:$FLINK_HOME/bin
