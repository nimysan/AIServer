"""
CRUD一些动态配置， 这些配置会保存在数据库里面
"""
import logging

from flask import Blueprint, request, current_app, jsonify
from model.config import ConfigItemRepository

bp = Blueprint("ai_config", __name__, url_prefix='/config')

logger = logging.getLogger(__name__)
@bp.route("", methods=["POST"])
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
      
    item_name = data.get('name')
    item_key = data.get('key')
    item_value = data.get('value')

    current_app.config_repository.create_item(item_key, item_name, item_value)
    # 在这里调用user_repository.create_user()方法创建用户
    # ...

    return jsonify({'message': 'Config created successfully'}), 200


@bp.route("<item_key>", methods=["DELETE"])
def delete(item_key):
    """
    test:

    curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:5000/user/register
    :return:
    """
    current_app.config_repository.deleteByKey(item_key)
    return "", 200


@bp.route("", methods=["GET"])
def list_config():
    """
    test:

    curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://localhost:5000/user/register
    :return:
    """
    data = current_app.config_repository.list_all()
    return data, 200
