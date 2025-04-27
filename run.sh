#!/bin/bash

# 源码部署启动实例 sh 代码

# 使用虚拟环境的 python
source .venv/bin/activate

echo "使用的 python：$(which python)"

LOG_PATH=log.log

nohup python main.py > $LOG_PATH 2>&1 &

echo "服务已启动，日志文件位置：$LOG_PATH"
echo "查看日志：tail -f $LOG_PATH"
echo "查看服务进程：ps aux | grep main.py"
echo "停止进程：kill -9 <服务PID>"