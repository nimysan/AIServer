import time
from string import Template

import pandas as pd
import subprocess
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

template = Template("""
您是一个精确的订单识别系统。您的任务是从给定文本中识别并提取订单号。

分析<ticket_content>内容并严格按照以下规则提取提到的订单号信息：
<ticket_content>
$subject
$description
</ticket_content>


可能的订单号格式如下：
    Amazon: 由三组数字组成，每组之间用连字符分隔，格式为三组数字，如111-2222222-3333333
    Yahoo: 完整格式为"jackery-japan-"后跟数字
    Rakuten: 多组数字，以连字符分隔，通常包含日期信息
    Shopify-JP: 完整格式为"Jackery Japan-"后跟数字
    Others: 根据上下文明确提到的订单号，可能包含字母、数字、下划线和连字符的组合
严格遵循以下指示：

    1. 按照以上格式识别可能存在的订单号， 订单号的内容必须完全来自于<ticket_content>中
    2. 只输出JSON数组，格式为：
    [
    {
    "order_number": "实际找到的订单号",
    "channel": "对应的渠道名称"
    },
    ...
    ]
    3. 如果没有找到任何匹配的订单号，输出空数组 []。
    4. 不要输出任何解释、注释、占位符或额外文字。
    5. 绝对不要编造、推测订单号或使用示例数据，只返回文本中明确存在的订单号。
    6. 确保输出是有效的JSON格式。
    7. 在输出前，仔细检查每个识别到的订单号是否确实出现在原文中，并完全符合指定的格式。
    8. 不要将电话号码、日期或其他数字序列误认为订单号。
    9. 不要将邮件地址识别为订单号.
    10. 只有在文本明确提到订单号或订单编号时，才考虑将其识别为"Others"类型的订单号。
    11. 如果对某个可能的订单号有任何疑问，宁可不输出也不要输出不确定的信息。


```

""")

CHANNEL_MAP = {

    "Amazon": "Amazon",

    "Yahoo": "Yahoo",

    "Rakuten": "Rakuten",

    "Shopify-JP": "Shopify-JP"

}


def validate_channel(channel):
    if channel not in CHANNEL_MAP:
        raise ValueError(f"Invalid channel: {channel}. Must be one of {list(CHANNEL_MAP.keys())}")

    return CHANNEL_MAP[channel]


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


processed_count = 0


def process_row(index, row, pbar, max_retries=5, retry_delay=1):
    global processed_count
    ticket_subject = row['Ticket subject']
    ticket_content = row['Ticket - Description']

    # print(template % data)
    prompt = template.substitute(subject=ticket_subject, description=ticket_content)
    data = {
        "input": prompt
        # ,
        # "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0"
    }
    json_data = json.dumps(data)
    # print(json_data)
    curl_command = [
        'curl', '-X', 'POST',
        'http://localhost:5000/api/bedrock/chat',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Basic YWRtaW46KGBnSHBOfjI=',
        '-d', json_data,
        '--max-time', '10'  # 设置10秒超时
    ]

    for attempt in range(max_retries):
        try:
            result = subprocess.run(curl_command, capture_output=True, text=True, check=True)

            output = json.loads(result.stdout)
            json_output = output['result']['content'][0]['text']

            # print(json_output)
            response = json.loads(json_output)
            processed_count += 1
            pbar.update(1)
            pbar.set_description(f"Processed: {processed_count}")

            return index, ticket_subject, json.dumps(response)
        except Exception as e:
            print(e)
            print(f"Error occurred for ticket_subject {ticket_subject} (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                processed_count += 1
                pbar.update(1)
                pbar.set_description(f"Processed: {processed_count}")
                return index, ticket_subject, "无法解析返回" + str(e)

    # This line should never be reached, but just in case
    return index, ticket_subject, "无法解析返回" + "Maximum retries reached"


def main(excel_path, output_path, concurrency):
    df = pd.read_excel(excel_path)

    results = []

    with tqdm(total=len(df), desc="Processed: 0") as pbar:

        with ThreadPoolExecutor(max_workers=concurrency) as executor:

            future_to_index = {executor.submit(process_row, index, row, pbar): index

                               for index, row in df.iterrows()}

            for future in as_completed(future_to_index):

                try:

                    index, category, orders = future.result(timeout=60)  # 5分钟超时

                    results.append((index, category, orders))

                except TimeoutError:

                    print(f"Task for index {future_to_index[future]} timed out")

                except Exception as exc:

                    print(f"Task for index {future_to_index[future]} generated an exception: {exc}")

                finally:

                    pbar.update(1)

    # 将结果添加到DataFrame

    for index, category, orders in results:
        df.at[index, 'new_order_id_list'] = str(orders)

    # 保存更新后的DataFrame到新的Excel文件

    output_path = excel_path.rsplit('.', 1)[0] + '_' + output_path + '.xlsx'

    df.to_excel(output_path, index=False)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python script.py <excel_file_path> <output_path> <concurrency>")

        sys.exit(1)

    excel_file = sys.argv[1]

    output_path = sys.argv[2]

    concurrency = int(sys.argv[3])

    main(excel_file, output_path, concurrency)
