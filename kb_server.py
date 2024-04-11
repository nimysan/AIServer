"""
test

curl -X POST -H "Content-Type: application/json" -d '{"a": 2, "b": 3}' http://localhost:5000/add

Prod部署:

pip install gunicorn

gunicorn --config gunicorn_config.py wsgi:app

"""
import json
import logging
import os

from flask import Flask, request, jsonify, Config
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from opentracing import tags

from brclient.bedrock_client import BedrockClient

# 读取 JSON 配置文件
config_file = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_file, "r") as f:
    config = json.load(f)

    # 创建国家-ID 字典
    knowledge_base_dict = {market["name"]: market["id"] for market in config.get("knowledge_base_dict", [])}
    print(f"--->The knowledge base config is {knowledge_base_dict}")


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
def ask_knowledge_base():
    print(request.get_data())
    data = request.get_json()
    input = data['input']
    knowledge_base_id = knowledge_base_dict.get(data['market'])
    return jsonify({'result': bedrock_client.ask_knowledge_base(input, knowledge_base_id)})


@app.route('/chat', methods=['POST'])
def suggest():
    print(request.get_data())
    data = request.get_json()
    input = data['input']

    return jsonify({'result': bedrock_client.invoke_claude_3_with_text(input)})


if __name__ == '__main__':
    app.run(debug=True)
