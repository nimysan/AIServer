# Gunicorn configuration file
import multiprocessing

# 监听的IP地址和端口
bind = "0.0.0.0:8000"

# 工作进程数
# workers = multiprocessing.cpu_count() * 2 + 1

workers = 1

# 工作模式
worker_class = 'sync'

# 最大并发请求数
worker_connections = 1000

# 进程名称
proc_name = 'AIServer'

# 超时时间
timeout = 30

# 访问日志格式
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 错误日志
errorlog = '-'

# 日志级别
loglevel = 'info'