import time

import pandas as pd
import subprocess
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


processed_count = 0

import re
from bs4 import BeautifulSoup


def extract_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    sections = soup.find_all('div', class_='form-section')

    info = {}

    for section in sections:
        label = section.b.text.strip(':')
        content = section.pre.text.strip()
        info[label] = content

    return info


def process_row(index, row, intent_list, pbar, max_retries=5, retry_delay=3):
    global processed_count
    category = row['工单号']
    inquiry = extract_info(row['邮件正文'])

    data = {
        "intent_list": intent_list,
        "customer_inquiry": inquiry
    }

    json_data = json.dumps(data)
    curl_command = [
        'curl', '-X', 'POST',
        'http://localhost:5000/api/bestqi/intent',
        '-H', 'Content-Type: application/json',
        '-H', 'Authorization: Basic YWRtaW46KGBnSHBOfjI=',
        '-d', json_data
    ]

    for attempt in range(max_retries):
        try:
            result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
            response = json.loads(result.stdout)

            processed_count += 1
            pbar.update(1)
            pbar.set_description(f"Processed: {processed_count}")

            return index, category, response['intent'], response['reason']
        except Exception as e:
            print(f"Error occurred for category {category} (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                processed_count += 1
                pbar.update(1)
                pbar.set_description(f"Processed: {processed_count}")
                return index, category, "无法解析返回", str(e)

    # This line should never be reached, but just in case
    return index, category, "无法解析返回", "Maximum retries reached"


def main(excel_path, json_path, output_path, concurrency):
    # df = pd.read_excel(excel_path, nrows=10)
    df = pd.read_excel(excel_path)
    intent_list = load_json(json_path)

    results = []

    with tqdm(total=len(df), desc="Processed: 0") as pbar:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            future_to_index = {executor.submit(process_row, index, row, intent_list, pbar): index
                               for index, row in df.iterrows()}
            for future in as_completed(future_to_index):
                index, category, intent, reason = future.result()
                results.append((index, category, intent, reason))

    # 将结果添加到DataFrame
    for index, category, intent, reason in results:
        df.at[index, 'intent'] = intent
        df.at[index, 'reason'] = reason

    # 保存更新后的DataFrame到新的Excel文件
    output_path = excel_path.rsplit('.', 1)[0] + '_' + output_path + '.xlsx'
    df.to_excel(output_path, index=False)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <excel_file_path> <json_file_path> <output_path> <concurrency>")
        sys.exit(1)

    excel_file = sys.argv[1]
    json_file = sys.argv[2]
    output_path = sys.argv[3]
    concurrency = int(sys.argv[4])
    main(excel_file, json_file, output_path, concurrency)
