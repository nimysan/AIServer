import requests
import json
import logging


def find_event_before_last_message_end(data_list):
    message_end_index = None
    for i in range(len(data_list) - 1, -1, -1):
        if data_list[i].get('event') == 'message_end':
            message_end_index = i
            break

    if message_end_index is not None and message_end_index > 0:
        return data_list[message_end_index - 1]
    return None  # 如果没有找到匹配的项或 message_end 是第一项

def bytes_to_json(byte_data):
    # 将 bytes 解码为字符串

    string_data = byte_data.decode('utf-8')

    # 分割字符串为单独的 JSON 对象

    json_strings = string_data.split('\n\n')

    # 解析每个 JSON 对象

    json_objects = []

    for json_str in json_strings:

        if json_str.startswith('data: '):
            json_str = json_str[6:]  # 移除 'data: ' 前缀

        try:

            json_obj = json.loads(json_str)

            json_objects.append(json_obj)

        except json.JSONDecodeError:

            pass  # 忽略无法解析的行

    return json_objects


def call_dify_agent(message, conversation_id=None):
    url = "https://dify.plaza.red/v1/chat-messages"

    headers = {
        "Authorization": "Bearer app-22rGlxQJopqiOpZPfhKnMqfm",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {},
        "query": message,
        "user": "abc-123",
        "response_mode": "streaming",
        "conversation_id": conversation_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    logging.info(response.content)

    if response.status_code == 200:
        event_data = bytes_to_json(response.content)
        return find_event_before_last_message_end(event_data)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


# 使用示例
result = call_dify_agent("こんにちは。注文した商品の到着予定を教えていただけますでしょうか？注文番号は JP-123-123-123 です。")
if result:
    # print(result)
    # return response.json()
    # print(json.dumps(result, indent=2))
    print(result['thought'])
