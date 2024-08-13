import logging
from string import Template

from flask import Blueprint, request, current_app, jsonify

bp = Blueprint("bestqi", __name__, url_prefix='/bestqi')

logger = logging.getLogger(__name__)

from string import Template
name = "Alice"
age = 25
intent_prompt = Template('''
You are a customer service representative. 
Please perform intent recognition based on the user's submitted content, which includes a subject and content. 
Rely primarily on the content to determine the intent. Always output only the single most relevant intent. 
Select the matching intent from the following intent_list in JSON format
<intent_list>
$intent_list
</intent_list>

The content of the customer's inquiry is
<customer_inquiry>
$customer_inquiry
</customer_inquiry>

Please output the intent according to the provided list of intents according the category and category description. your output should provide a complete JSON object. 
The output format should be JSON, and please ensure that the outputted JSON is correctly formatted, including any necessary JSON escape settings, 
to ensure that the outputted JSON can be parsed correctly.Avoid quotation mark within a quotation mark, 
if encountering a quotation mark within a quotation mark, it needs to be single quotation mark instead. reason field please use chinese
The format is as follows:
        {
            "reason": "xxx",
            "intent": intent object
        }
''')

def remove_rewrite_prompt(string):
    if "_rewrite_prompt" in string:
        return string.replace("_rewrite_prompt", "")
    else:
        return string


def load_bedrock_client(region):
    bedrock_client = current_app.aws_bedrock_client
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


def reload_config():
    global config_data
    config_data = current_app.config_repository.list_all()
    # print(config_data)

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
    # refresh config data
    reload_config()

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


@bp.route('/intent', methods=['POST', 'GET'])
# @require_auth
def bestqi_intent():
    """
    意图识别
    :return:
    """
    logger.debug(request.get_data())
    data = request.get_json()
    intent_list = data['intent_list']
    # intent_description = data['intent_description']
    customer_inquiry = data['customer_inquiry']
    prompt = intent_prompt.substitute(intent_list=intent_list, customer_inquiry=customer_inquiry)

    work_region = current_app.config["REGION"]
    bedrock_client = load_bedrock_client(region=work_region)
    return bedrock_client.invoke_claude_3_with_text(prompt)["content"][0]["text"]


