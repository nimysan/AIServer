import logging
import os

from flask import Flask, send_from_directory
from flask_cors import CORS

# self code
import config
from endpoints import register_api_endpoints
from model import init_model_repositories, get_user_repository

from logging.handlers import RotatingFileHandler

# 创建一个日志文件处理程序
file_handler = RotatingFileHandler('flask_app.log', maxBytes=10000, backupCount=5)
file_handler.setLevel(logging.INFO)

# 创建一个控制台日志处理程序
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def init_app(app):
    """
    Some normal app settings
    :param app:
    :return:
    """
    CORS(app)
    app.json.ensure_ascii = False  # 解决中文乱码问题


def server_react_as_webui(app):
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if os.path.isfile(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')


def create_app():
    # 同时部署/api和ui dashboard
    app = Flask(__name__, static_folder='../ai-frontend/dist')
    # some setup
    init_app(app)

    # configuration
    app.config.from_object(config.DevelopmentConfig)

    with app.app_context():
        # init model and database layer
        init_model_repositories(app)
        # register api endpoints
        register_api_endpoints(app)  # 参考 https://blog.csdn.net/qq_30117567/article/details/122645987

    server_react_as_webui(app)

    return app


if __name__ == '__main__':
    app = create_app();
    app.run(debug=True)
