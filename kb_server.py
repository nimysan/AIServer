"""
test

curl -X POST -H "Content-Type: application/json" -d '{"a": 2, "b": 3}' http://localhost:5000/add

Prod部署:

pip install gunicorn

gunicorn --config gunicorn_config.py wsgi:app

"""

import boto3
import json
from flask import Flask, request, jsonify


def sample_invoke_model():
    bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-west-2")
    print(bedrock)
    body = json.dumps({
        "prompt": "\n\nHuman:explain black holes to 8th graders\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    # text
    print(response_body.get('completion'))


default_vector_search_configuration = {
    # 'filter': {
    #     # 'andAll': [
    #     #     {'... recursive ...'},
    #     # ],
    #     # 'equals': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'greaterThan': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'greaterThanOrEquals': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'in': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'lessThan': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'lessThanOrEquals': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'notEquals': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'notIn': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # },
    #     # 'orAll': [
    #     #     {'... recursive ...'},
    #     # ],
    #     # 'startsWith': {
    #     #     'key': 'string',
    #     #     'value': {...} | [...] | 123 | 123.4 | 'string' | True | None
    #     # }
    # },
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
    print(model_arn)
    ## call Knowledge-base
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
    print(output)
    print(json.dumps(response, indent=2))


app = Flask(__name__)


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    a = data['a']
    b = data['b']
    result = a + b
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
