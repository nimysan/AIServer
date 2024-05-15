from flask import Flask, jsonify, request

from endpoints.api import api_bp
from endpoints.statistics import bp as log_bp
from endpoints.bedrock import bp as bedrock_bp
from endpoints.config_item import bp as config_bp
from endpoints.user import bp as user_bp
from security import is_authenticated

print("hello --- api ---")


# 定义认证装饰器


def register_api_endpoints(app: Flask):
    api_bp.register_blueprint(log_bp)
    api_bp.register_blueprint(bedrock_bp)
    api_bp.register_blueprint(config_bp)

    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)


@api_bp.before_request
def require_auth():
    """
    在每个请求之前检查身份验证状态
    """
    # 从请求中获取身份验证凭据(例如 JWT 令牌或会话 ID)
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        # 如果没有提供身份验证凭据,返回 401 Unauthorized
        return jsonify({"error": "Missing authentication credentials"}), 401

    # 验证身份验证凭据
    is_auth, error_msg = is_authenticated(auth_header)

    if not is_auth:
        # 如果身份验证失败,返回 401 Unauthorized
        return jsonify({"error": error_msg}), 401
