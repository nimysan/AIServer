import functools
import logging

from flask import jsonify, current_app
from flask_cors import cross_origin

from flask import (
    Blueprint, g, redirect, request, url_for
)

from model.user import print_base64_credentials

logger = logging.getLogger(__name__)

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=["POST"])
def register():
    """
    test:

    curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:5000/user/register
    :return:
    """
    logger.info(f"request is {request}")
    # 获取POST请求中的JSON数据
    data = request.get_json()

    # 检查JSON数据是否存在
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    # 获取username和password参数
    username = data.get('username')
    password = data.get('password')

    # 检查是否缺少必需的参数
    if not username or not password:
        return jsonify({'error': 'Missing required parameters'}), 400

    user_repository = current_app.user_repository;
    logger.info(f"Received username: {username}, password: {password}")
    user_repository.create_user(None, username, password, "")
    # 在这里调用user_repository.create_user()方法创建用户
    # ...

    return jsonify({'message': 'User created successfully'}), 201
    return "", 200


@bp.route('/login', methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    """
    test:

     curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:5000/user/login

    :return:
    """
    logger.info(f"request is {request}")
    # 获取POST请求中的JSON数据
    data = request.get_json()

    # 检查JSON数据是否存在
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    # 获取username和password参数
    username = data.get('username')
    password = data.get('password')

    # 检查是否缺少必需的参数
    if not username or not password:
        return jsonify({'error': 'Missing required parameters'}), 400

    logger.info(f"Received username: {username}, password: {password}")
    user_repository = current_app.user_repository
    user = user_repository.load_user_by_username(username)

    logger.info(f"Received username: {user}")
    base64_token = print_base64_credentials(user["userName"],user["password"])
    if user and user['password'] == password:
        return jsonify({'message': 'User login successfully', 'user': {
            "user_id": user["userId"],
            "user_name": user["userName"],
            "user_token": base64_token
        }}), 200

    return "login fail", 401
    # return "", 200


def login_required(view):
    """
    Require Authentication in Other Views
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/logout', methods=["POST"])
@cross_origin(supports_credentials=True)
def logout():
    logger.debug("logout")
    return "", 200
