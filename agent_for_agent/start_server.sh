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

# 定义 PID 文件路径
PID_FILE="gunicorn.pid"

# 停止已运行的进程
stop_server() {
    if [ -f "$PID_FILE" ]; then
        echo "Stopping existing Gunicorn process..."
        PID=$(cat "$PID_FILE")
        kill $PID
        rm "$PID_FILE"
        sleep 2
    fi
}

# 启动服务器
start_server() {
    echo "Starting Gunicorn server..."
    nohup $(which python) -m gunicorn --config gunicorn_config.py --log-file api_server.log --pid "$PID_FILE" wsgi:web &
    echo "Server started in background. PID: $!"
}

# 重启服务器
restart_server() {
    stop_server
    start_server
}

# 根据命令行参数执行相应的操作
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0