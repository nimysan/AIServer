"""
test

curl -X POST -H "Content-Type: application/json" -d '{"a": 2, "b": 3}' http://localhost:5000/add

Prod部署:

pip install gunicorn

gunicorn --config gunicorn_config.py wsgi:app

"""
import base64
import json
import logging
import os
from functools import wraps

from flask import Flask, request, jsonify, Config
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from opentracing import tags

from brclient.bedrock_client import BedrockClient

logger = logging.getLogger("flask.app")
logging.basicConfig(level=logging.INFO)
# print(logger)
logger.info('Started')
# 读取 JSON 配置文件
config_file = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_file, "r") as f:
    config = json.load(f)

    # 创建国家-ID 字典
    knowledge_base_dict = {market["name"]: market["id"] for market in config.get("knowledge_base_dict", [])}
    logger.debug(f"--->The knowledge base config is {knowledge_base_dict}")
    auth_username = config.get("username")
    auth_password = config.get("password")


def require_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        logger.debug(f"auth_header {auth_header}")
        if not auth_header:
            return {'message': 'Authentication required'}, 401

        auth_token = auth_header.split(' ')[1]
        logger.debug(f"auth_token {auth_token}")
        decoded_token = base64.b64decode(auth_token).decode('utf-8')
        username, password = decoded_token.split(':')
        logger.debug(f"Username {username} and password {password}")
        # Replace this with your own authentication logic
        if username != auth_username or password != auth_password:
            return {'message': 'Invalid credentials'}, 401

        return func(*args, **kwargs)

    return decorated


def init_tracer():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': 'localhost',
                'reporting_port': '6831',
            },
            'logging': True,
        },
        service_name='your-flask-app'
    )
    return config.initialize_tracer()


bedrock_client = BedrockClient()
tracer = init_tracer()

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
app.json.ensure_ascii = False  # 解决中文乱码问题
tracing = FlaskTracing(tracer, True, app)


@app.before_request
def start_trace():
    with tracer.start_span('request') as span:
        span.set_tag(tags.HTTP_METHOD, request.method)
        span.set_tag(tags.HTTP_URL, request.path)


@app.after_request
def finish_trace(response):
    tracer.active_span.finish()
    return response


@app.route('/suggest', methods=['POST'])
@require_auth
def ask_knowledge_base():
    print(request.get_data())
    data = request.get_json()
    input = data['input']
    knowledge_base_id = knowledge_base_dict.get(data['market'])
    # prompt_template = data['prompt']
    if "prompt" in data:
        return jsonify(
            {'result': bedrock_client.ask_knowledge_base(input, knowledge_base_id, prompt_template=data['prompt'])})
    else:
        return jsonify(
            {'result': bedrock_client.ask_knowledge_base(input, knowledge_base_id)})


@app.route('/chat', methods=['POST'])
@require_auth
def suggest():
    print(request.get_data())
    data = request.get_json()
    input = data['input']

    return jsonify({'result': bedrock_client.invoke_claude_3_with_text(input)})


if __name__ == '__main__':
    app.run(debug=True)
