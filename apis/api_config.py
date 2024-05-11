import functools
import logging

from flask import current_app, app, jsonify, request

from brclient.config import ConfigItemRepository

from flask import (
    Blueprint
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

bp = Blueprint('config', __name__, url_prefix='/config')

config_repository = ConfigItemRepository("us-west-2")


@bp.route('/add', methods=["POST"])
def addItem():
    """
    test:

    curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:5000/user/register
    :return:
    """
    logger.info(f"request is {request}")
    # 获取POST请求中的JSON数据
    data = request.get_json()
    logger.info(data)
    # 检查JSON数据是否存在
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    # 获取username和password参数
    item_key = data.get('key')
    item_value = data.get('value')
    item_name = data.get('name')

    config_repository.create_item(item_key, item_name, item_value)
    # 在这里调用user_repository.create_user()方法创建用户
    # ...

    return jsonify({'message': 'Config created successfully'}), 200


@bp.route('/list', methods=["GET"])
def list():
    """
    test:

    curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:5000/user/register
    :return:
    """
    data = config_repository.list_all()
    return data, 200