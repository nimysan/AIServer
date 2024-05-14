#!/bin/bash

# 检查 Python 版本
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is required to run this script."
    exit 1
fi

# 创建虚拟环境
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 安装 requirements.txt 中的依赖项
pip install -r requirements.txt
gunicorn --config gunicorn_config.py wsgi:web