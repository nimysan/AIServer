import base64
import logging
import os
from functools import wraps

from flask import Flask, request, send_from_directory
from flask_cors import CORS

# self code
import config
from endpoints import register_api_endpoints
from model import init_model_access
from apis import api_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def init_app(app):
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
    app = Flask(__name__, static_folder='../flowbite-react-admin-dashboard/dist')
    # some setup
    init_app(app)

    # configuration
    app.config.from_object(config.DevelopmentConfig)

    with app.app_context():
        init_model_access()
        # register api endpoints
        register_api_endpoints(app)  # 参考 https://blog.csdn.net/qq_30117567/article/details/122645987

    server_react_as_webui(app)

    return app


# def require_auth(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         logger.debug(f"auth_header {auth_header}")
#         if not auth_header:
#             return {'message': 'Authentication required'}, 401
#
#         auth_token = auth_header.split(' ')[1]
#         logger.debug(f"auth_token {auth_token}")
#         decoded_token = base64.b64decode(auth_token).decode('utf-8')
#         username, password = decoded_token.split(':')
#         logger.debug(f"Username {username} and password {password}")
#         # Replace this with your own authentication logic
#         if username != auth_username or password != auth_password:
#             return {'message': 'Invalid credentials'}, 401
#
#         return func(*args, **kwargs)
#
#     return decorated


if __name__ == '__main__':
    app = create_app();
    app.run(debug=True)
