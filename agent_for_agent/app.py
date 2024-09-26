from flask import Flask, Blueprint, request, jsonify
import requests
import json

from api.order import order_endpoint
import logging

app = Flask(__name__)

# 创建一个Blueprint
api = Blueprint('api', __name__, url_prefix="/api")

# 注册order_cancel Blueprint
app.register_blueprint(order_endpoint, url_prefix='/api/order')


# 健康检查接口

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Service is up and running"
    }), 200


@api.route('/execute', methods=['POST'])
def execute_api_call():
    # 获取请求体JSON数据
    input_data = request.json

    # 从JSON数据中获取必要的信息
    api_endpoint = input_data.get('api_endpoint')
    # 检查并修改 api_endpoint
    if not api_endpoint.startswith(('http://', 'https://')):
        api_endpoint = f'https://cx-api.plaza.red{api_endpoint}'
    logging.info(f"API Endpoint: {api_endpoint}")

    http_method = input_data.get('http_method')
    request_payload = input_data.get('request_payload', {})
    logging.info(f"{request_payload}")

    # 验证必需的参数
    if not api_endpoint or not http_method:
        return jsonify({
            "code": 400,
            "message": {"error": "Missing required parameters"}
        }), 400

    # 验证HTTP方法
    if http_method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
        return jsonify({
            "code": 400,
            "message": {"error": "Invalid HTTP method"}
        }), 400

    try:
        # 执行API调用
        response = requests.request(
            method=http_method,
            url=api_endpoint,
            json=request_payload,
            headers={
                'Content-Type': 'application/json'
            }
        )
        logging.info("----###----")
        logging.info(response)
        # 打印完整的响应内容

        logging.info(f"Response: response")
        logging.info("----###----")
        # 返回结果
        return jsonify({
            "code": response.status_code,
            "message": response.json()
        }), 200

    except requests.RequestException as e:
        logging.info("----##requests.RequestException#----")
        return jsonify({
            "code": 500,
            "message": {"error": str(e)}
        }), 500


# 注册Blueprint
app.register_blueprint(api, url_prefix='/api')


def list_routes():
    """列出所有已注册的路由"""
    logging.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        logging.info(f"{rule.endpoint:50s} {rule.methods} {rule.rule}")


if __name__ == '__main__':
    list_routes()
    app.run(debug=True)
