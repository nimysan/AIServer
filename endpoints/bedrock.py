import logging
from string import Template

from flask import Blueprint, request, current_app, jsonify

from brclient.bedrock_client import BedrockClient

bp = Blueprint("bedrock", __name__, url_prefix='/bedrock')

logger = logging.getLogger(__name__)

from model.config import ConfigItemRepository

config_repository = ConfigItemRepository("us-west-2")
config_data = config_repository.list_all()


def remove_rewrite_prompt(string):
    if "_rewrite_prompt" in string:
        return string.replace("_rewrite_prompt", "")
    else:
        return string


def load_bedrock_client(region):
    bedrock_client = BedrockClient(region)
    return bedrock_client


def get_config(prompt_key):
    for data in config_data:
        if data.get('item_key') == prompt_key:
            return data.get('item_value')
    return None


def find_rewrite_prompt(brand, intent):
    """
    根据品牌和意图构建重写提示
    :param brand: 品牌名称
    :param intent: 意图名称
    :param content: 原始内容
    :return: 重写后的提示
    """
    # 首先根据品牌过滤config_data
    brand_data = [data for data in config_data if data.get('item_key').startswith(brand)]
    print(brand_data)
    # 然后在品牌数据中寻找精确匹配的brand_intent
    if intent:
        brand_intent_key = f"{brand}_{intent}_rewrite_prompt"
    else:
        brand_intent_key = f"{brand}_rewrite_prompt"
    print(brand_intent_key)
    for data in brand_data:
        if data.get('item_key') == brand_intent_key:
            print("level 2 match")
            prompt = data.get('item_value')
            break
    else:
        # 如果没有精确匹配,则寻找包含intent的
        for data in brand_data:
            key_head = remove_rewrite_prompt(data.get('item_key'))
            print(f" ------>>>>>> {brand}_{intent} ----- {data.get('item_key')} ---- {key_head}")

            if (brand + "_" + intent).startswith(key_head):
                print("level 1 match")
                prompt = data.get("item_value")
                break
        else:
            # 如果仍然没有找到,则使用默认提示
            prompt = get_config("rewrite_prompt")
    print("f write protmp ----< {prompt}")
    return prompt


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


@bp.route('/rag_with_rewrite', methods=['POST', 'GET'])
# @require_auth
def retrieve_and_generate_and_rewrite():
    logger.debug(request.get_data())
    data = request.get_json()
    question = data['input']

    intent = data['ticketIntent']

    brand = data['ticketBrand']

    knowledge_base_id = current_app.config["KNOWLEDGE_BASE"]
    work_region = current_app.config["REGION"]
    bedrock_client = load_bedrock_client(region=work_region)

    logger.debug("The knowledge base is " + knowledge_base_id)

    search_filter = {}
    if "filter" in data:
        search_filter = data["filter"]
        logger.debug(f"filter is {search_filter}")

    if "prompt" in data:
        suggest = bedrock_client.ask_knowledge_base(question, knowledge_base_id, search_filter,
                                                    prompt_template=data['prompt'])
    else:
        suggest = bedrock_client.ask_knowledge_base(question, knowledge_base_id, search_filter)

    #是否做改写
    rewrite_prompt = find_rewrite_prompt(brand, intent);
    content = suggest['response']['output']['text'];
    if rewrite_prompt:
        template = Template(rewrite_prompt)
        substituted_string = template.substitute(content=content, question=question)
        print(f"Final ---- {substituted_string}")
        rewrite_response = bedrock_client.invoke_claude_3_with_text(substituted_string)
        rewrite_value = rewrite_response['content'][0]['text']
        suggest['rewrite_value'] = rewrite_value
    else:
        suggest['rewrite_value'] = content

    return jsonify({'result': suggest})


@bp.route('/chat', methods=['POST', 'GET'])
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


if __name__ == '__main__':
    config_data = config_repository.list_all()
    print(config_data)
    config_data = [
        {'item_key': 'brand1_product_info_rewrite_prompt', 'item_value': 'product_info'},
        {'item_key': 'brand1_product_info_product_recommendation_rewrite_prompt',
         'item_value': 'for product_info_product_recommendation'},
        {'item_key': 'intent3__rewrite_prompt', 'item_value': 'This is a generic rewrite prompt for intent3.'},
        {'item_key': 'rewrite_prompt', 'item_value': 'This is the default rewrite prompt.'}
    ]

    brand = 'brand1'
    content = '>>>>>This is some original content.'

    # prompt = build_rewrite_prompt(brand, "product_info", content)
    # print(prompt)

    prompt = find_rewrite_prompt(brand, "product_info_product_compatibility", content)
    print(prompt)

    # prompt = build_rewrite_prompt(brand, "product_info_product_recommendation", content)
    # print(prompt)
