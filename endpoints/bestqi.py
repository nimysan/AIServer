import logging
from string import Template

from flask import Blueprint, request, current_app, jsonify

from brclient.bedrock_client import bedrock_sonnet_3_5_model_id

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

Please output the intent according to the provided list of intents according the category and category description. your output should provide a complete JSON object. 
The output format should be JSON, and please ensure that the outputted JSON is correctly formatted, including any necessary JSON escape settings, 
to ensure that the outputted JSON can be parsed correctly.Avoid quotation mark within a quotation mark, 
if encountering a quotation mark within a quotation mark, it needs to be single quotation mark instead. reason field please use chinese
find the intent and output as category -  category-sub category-sub category. Only give the best match intent chain and also give the reason.

下面是一个输出的例子:
<sample-intent-list>
[
  {
    "category": "售前咨询",
    "description": "顾客还没有成功支付订单，还没有购买商品，咨询产品规格参数、产品功能咨询、寻求折扣、售后政策、产品适配问题、功能是否满足客户需求等问题"
  },
  {
    "category": "产品体验问题",
    "description": "客户已经购买了商品,对于商品的兼容问题、不符合顾客期望等使用产品的体验反馈。"
  },
  {
    "category": "质量问题,功能问题",
    "description": "客户对于购买的商品或服务存在不满意的地方,表达了负面情绪。",
    "sub_categories": [
      {
        "category": "不制冰",
        "description": "无法制冰，加水亮缺水灯等等"
      },
      {
        "category": "不工作",
        "description": "设备不亮，没有反应"
      },
      {
        "category": "异响",
        "description": "设备发出很大的声音"
      },
      {
        "category": "其他功能问题",
        "description": "不属于不制冰、不工作、异响的其他产品功能问题"
      }
    ]
  },
  {
    "category": "广告/无意义",
    "description": "寻求广告、营销、合作的邮件或者回复hello，你好没有意义的句子。"
  },
  {
    "category": "其他问题",
    "description": "顾客还没有成功支付订单，还没有购买商品，咨询产品规格参数、产品功能咨询、寻求折扣、售后政策、产品适配问题、功能是否满足客户需求等问题。"
  }
]
</sample-intent-list>

Output example:
        {
            "intent": "质量问题,功能问题 - 异响"
            "reason": "xxx", //reason for why match this category
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
    return bedrock_client.invoke_claude_3_with_text(prompt, model_id=bedrock_sonnet_3_5_model_id)["content"][0]["text"]


