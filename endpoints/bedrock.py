import logging

from flask import Blueprint, request, current_app, jsonify

from brclient.bedrock_client import BedrockClient

bp = Blueprint("bedrock", __name__, url_prefix='/bedrock')

logger = logging.getLogger(__name__)


def load_bedrock_client(region):
    bedrock_client = BedrockClient(region)
    return bedrock_client


@bp.route('/rag', methods=['POST', 'GET'])
# @require_auth
def retrieve_and_generate():
    logger.debug(request.get_data())
    data = request.get_json()
    question = data['input']

    knowledge_base_id = current_app.config["KNOWLEDGE_BASE"]
    work_region = current_app.config["REGION"]
    bedrock_client = load_bedrock_client(region=work_region)

    logger.debug("The knowledge base is " + knowledge_base_id)

    search_filter = {}
    if "filter" in data:
        search_filter = data["filter"]
        logger.debug(f"filter is {search_filter}")

    if "prompt" in data:
        return jsonify(
            {'result': bedrock_client.ask_knowledge_base(question, knowledge_base_id, search_filter,
                                                         prompt_template=data['prompt'])})
    else:
        return jsonify(
            {'result': bedrock_client.ask_knowledge_base(question, knowledge_base_id, search_filter)})


@bp.route('/chat', methods=['POST'])
# @require_auth
def chat_with_model():
    logger.debug(request.get_data())
    data = request.get_json()
    prompt = data['input']
    image_key = "images"

    work_region = current_app.config["REGION"]
    bedrock_client = load_bedrock_client(region=work_region)
    if image_key not in data:
        return jsonify({'result': bedrock_client.invoke_claude_3_with_text(prompt)})
    else:
        return jsonify({'result': bedrock_client.invoke_claude_3_with_image_and_text(prompt, data[image_key])})
