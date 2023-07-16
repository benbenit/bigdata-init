#!/bin/bash

if [ $# -lt 1 ]
then
    echo "No Args Input..."
    exit ;
fi

case $1 in
"start")
        echo " ======启动 hadoop集群 ======="
        echo " --------------- 启动 hdfs ---------------"
        ssh node02 "/home/benbenit/apps/hadoop/sbin/start-dfs.sh"
        echo " --------------- 启动 yarn ---------------"
        ssh node03 "/home/benbenit/apps/hadoop/sbin/start-yarn.sh"
;;
"stop")
        echo " ==========关闭 hadoop集群 ========="
        echo " --------------- 关闭 yarn ---------------"
        ssh node03 "/home/benbenit/apps/hadoop/sbin/stop-yarn.sh"
        echo " --------------- 关闭 hdfs ---------------"
        ssh node02 "/home/benbenit/apps/hadoop/sbin/stop-dfs.sh"
;;
*)
    echo "Input Args Error..."
;;
esac