import logging
import re
from string import Template

from flask import Blueprint, request, current_app, jsonify

from brclient.bedrock_client import bedrock_sonnet_3_5_model_id, bedrock_sonnet_model_id, bedrock_opus_model_id

bp = Blueprint("bestqi", __name__, url_prefix='/bestqi')

logger = logging.getLogger(__name__)

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

Please read <customer_inquiry> and output intent and reason accounting to above <intent_list>
please output 2 files, intent and reason.
1. "intent" find the intent. the intent value must be one of intent from giving <intent_list>。 If a category contains sub-categories, it must match to the final sub-category. The output content should be formatted as category - sub_category - sub_category。
2. "reason" field. Why the customer_inquiry map the intent

the generated output format must be below (不要任何导言，直接输出需要的内容）:  
intent content with reason by 5 # as the separator; The format as below:
direct intent string without intent as prefix ##### direct reason string.

sample output:

intent: intent_name ##### reason: string reason

''')
import json


def process_content(content):
    try:
        # 尝试按 ##### 分割内容
        parts = content.split('#####')

        if len(parts) != 2:
            raise ValueError("Content does not contain exactly one '#####' separator")

        intent = parts[0].strip()
        intent = re.sub(r'^intent:\s*', '', intent)
        reason = parts[1].strip()
        reason = re.sub(r'^reason:\s*', '', reason)

        # 创建 JSON 对象
        result = {
            "intent": intent,
            "reason": reason
        }

        # 验证 JSON 是否可以被正确序列化和反序列化
        json_string = json.dumps(result, ensure_ascii=False)
        json.loads(json_string)

        return json_string

    except json.JSONDecodeError as e:
        return json.dumps({
            "error": "JSON encoding/decoding error",
            "details": str(e)
        }, ensure_ascii=False)
    except ValueError as e:
        print("##################")
        print(content)
        print("@@@@@@@@@@@@@@@@@@")
        return json.dumps({
            "error": "Invalid content format",
            "details": str(e)
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "error": "Unexpected error",
            "details": str(e)
        }, ensure_ascii=False)

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
    # print("------ " + bedrock_opus_model_id)
    return process_content(bedrock_client.invoke_claude_3_with_text(prompt, model_id=bedrock_sonnet_3_5_model_id)["content"][0]["text"])


