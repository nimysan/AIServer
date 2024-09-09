import time
from string import Template

import pandas as pd
import subprocess
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# data = {"subject": "Eve", "description": 45}
template = Template("""您是一个精确的订单识别系统。您的任务是从给定文本中识别并提取订单号。可能的订单号格式如下：
<samples>
Amazon	250-2127273-8839034	249-1381907-2244648
Yaho	jackery-japan-10063258	jackery-japan-10003657
Rakuten	374756-20240909-0632640638	374756-20191008-00004735
Shopify-JP	Jackery Japan-202412404410	Jackery Japan-202363447
Others: 从上下文是否有提到订单号来判断, 包含一些字母数字下划线_-等字符的组合
<samples>
严格遵循以下指示：

1. 仅识别完全匹配上述格式的订单号。
2. 只输出JSON数组，格式为：
   [
     {
       "order_number": "实际找到的订单号",
       "channel": "对应的渠道名称"
     },
     ...
   ]
3. 如果没有找到任何匹配的订单号，输出空数组 []。
4. 不要输出任何解释、注释或额外文字。
5. 不要使用<samples>中的例子数据，只输出在给定文本中实际找到的订单号， 不要编造订单号。
6. 确保输出是有效的JSON格式。

分析以下文本并严格按照上述规则提取订单信息：
<文本开始>
$subject
$description
<文本结束>
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


def process_row(index, row, pbar, max_retries=2, retry_delay=1):
    global processed_count
    ticket_subject = row['Ticket subject']
    ticket_content = row['Ticket - Description']

    # print(template % data)
    prompt = template.substitute(subject=ticket_subject, description=ticket_content)
    data = {
        "input": prompt
        # "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0"
    }
    json_data = json.dumps(data)
    # print(json_data)
    curl_command = [
        'curl', '-X', 'POST',
        'http://localhost:5000/api/bedrock/chat',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Basic YWRtaW46KGBnSHBOfjI=',
        '-d', json_data
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
    df = pd.read_excel(excel_path, nrows=10)
    # df = pd.read_excel(excel_path)
    results = []

    with tqdm(total=len(df), desc="Processed: 0") as pbar:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            future_to_index = {executor.submit(process_row, index, row, pbar): index
                               for index, row in df.iterrows()}
            for future in as_completed(future_to_index):
                index, category, orders = future.result()
                results.append((index, category, orders))

    # 将结果添加到DataFrame
    for index, category, orders in results:
        # 将orders转换为字符串
        df.at[index, 'new_order_id_list'] = str(orders)

    # 保存更新后的DataFrame到新的Excel文件
    output_path = excel_path.rsplit('.', 1)[0] + '_' + output_path + '.xlsx'
    df.to_excel(output_path, index=False)
    print(f"\nResults saved to {output_path}")


# 在主程序部分，修正output_path的赋值
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <excel_file_path> <output_path> <concurrency>")
        sys.exit(1)

    excel_file = sys.argv[1]
    output_path = sys.argv[2]  # 修正这里，使用sys.argv[2]而不是sys.argv[1]
    concurrency = int(sys.argv[3])
    main(excel_file, output_path, concurrency)
