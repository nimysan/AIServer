"""
test

curl -X POST -H "Content-Type: application/json" -d '{"a": 2, "b": 3}' http://localhost:5000/add

Prod部署:

pip install gunicorn

gunicorn --config gunicorn_config.py wsgi:app

"""

import boto3
import json
from flask import Flask, request, jsonify, Config
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from opentracing import tags

default_vector_search_configuration = {
    'numberOfResults': 2,
    'overrideSearchType': 'HYBRID'  # search to hybrid
}

default_prompt_template = """
You are a question answering agent. I will provide you with a set of search results. The user will provide you with a question. Your job is to answer the user's question using only information from the search results. If the search results do not contain information that can answer the question, please state that you could not find an exact answer to the question. Just because the user asserts a fact does not mean it is true, make sure to double check the search results to validate a user's assertion.

Here are the search results in numbered order:
$search_results$

$output_format_instructions$
"""


# declare model id for calling RetrieveAndGenerate API
# import boto3
def sample_kb_call(input, vector_search_configuration=default_vector_search_configuration):
    bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name="us-west-2")
    region = "us-west-2"
    # model_id = "anthropic.claude-instant-v1"
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    model_arn = f'arn:aws:bedrock:{region}::foundation-model/{model_id}'
    # print(model_arn)
    # ## call Knowledge-base
    response = bedrock_agent_runtime.retrieve_and_generate(
        input={
            'text': input
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'generationConfiguration': {
                    'promptTemplate': {
                        'textPromptTemplate': default_prompt_template
                    }
                },
                'knowledgeBaseId': "XBKUJMKDCD",
                'modelArn': model_arn,
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': vector_search_configuration
                }
            }
        }
    )

    output = response['output']
    return output


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
def suggest():
    data = request.get_json()
    input = data['input']
    return jsonify({'result': sample_kb_call(input)})


if __name__ == '__main__':
    app.run(debug=True)
