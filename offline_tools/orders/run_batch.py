import time
from string import Template

import pandas as pd
import subprocess
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# data = {"subject": "Eve", "description": 45}
template = Template("""你是一个客服服务专员, 正在阅读客户提交的ticket, 你需要从subject和content中提取出来客户反馈内容中的订单信息 
<ticket_subject>
$subject
</ticket_subject>

<ticket_description>
$description
</<ticket_description>

规则：
1. 从subject和description中提取
2. 以下是可能出现订单渠道和订单数据格式
来自于：Amazon	
250-2127273-8839034	| 249-1381907-2244648
来自于：Yaho	
jackery-japan-10063258	| jackery-japan-10003657
来自于：Rakuten
374756-20240909-0632640638 |	374756-20191008-00004735
来自于：Shopify-JP	
Jackery Japan-202412404410 ｜Jackery Japan-202363447
3. 输出为json数组的格式例子
{
    "channel": Amazon | Yaho | Rakuten | Shopify-JP,
    "order_number: "Jackery Japan-202412404410"
}
4. 如果没有识别出订单， 请输出json空数组 []
5. 不要任何导言， 直接输出json
""")


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
            # print(f"ffff ---- {output}")
            json_output = output['result']['content'][0]['text']

            # print(json_output)
            response = json.loads(json_output)
            # print("------")
            processed_count += 1
            pbar.update(1)
            pbar.set_description(f"Processed: {processed_count}")

            return index, ticket_subject, response
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
    # intent_list = load_json(json_path)

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
        df.at[index, 'orders'] = orders
        # df.at[index, 'reason'] = reason

    # 保存更新后的DataFrame到新的Excel文件
    output_path = excel_path.rsplit('.', 1)[0] + '_' + output_path + '.xlsx'
    df.to_excel(output_path, index=False)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <excel_file_path> <output_path> <concurrency>")
        sys.exit(1)

    excel_file = sys.argv[1]
    output_path = sys.argv[1]
    concurrency = int(sys.argv[3])
    main(excel_file, output_path, concurrency)
