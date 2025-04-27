#!/bin/bash

PYTHON_INTERPRETER=/root/miniconda3/envs/python310/bin/python


# 获取脚本所在的绝对路径，保证在任何目录下都能找到项目的 main.py 文件
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# 获取脚本的父目录，找到绝对路径的 main.py
PY_MAIN_FILE=$(dirname "$SCRIPT_DIR")/main.py

# 执行项目的 main.py
$PYTHON_INTERPRETER $PY_MAIN_FILE