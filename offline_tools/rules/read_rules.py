import json
import pandas as pd

# 读取Excel表格数据
df = pd.read_excel('修改订单处理规则1126.xlsx', sheet_name='意图规则', header=0)

# 将NaN替换为空字符串
df = df.fillna('')

# 拆分order_status为多个值
df = df.assign(order_status=df['order_status'].str.split(',')).explode('order_status')

# 生成规则对象
rules = {}
for _, row in df.iterrows():
    intent = row['intent']
    order_status = row['order_status'].strip()  # 去除空格
    is_pre_sales_order = row['is_pre_sales_order']
    order_channel = row['order_channel']
    rule_for_handle = row['rule_for_handle']
    customer_reply_rule = row['customer_reply_rule']
    agent_action = row['agent_action']
    target_ticket_status = row['target_ticket_status']
    target_ticket_label = row['ticket_label']

    if intent not in rules:
        rules[intent] = {}
    if order_status not in rules[intent]:
        rules[intent][order_status] = {}
    if is_pre_sales_order not in rules[intent][order_status]:
        rules[intent][order_status][is_pre_sales_order] = {}
    if order_channel not in rules[intent][order_status][is_pre_sales_order]:
        rules[intent][order_status][is_pre_sales_order][order_channel] = {}

    rules[intent][order_status][is_pre_sales_order][order_channel] = {
        'rule_for_handle': rule_for_handle,
        'customer_reply_rule': customer_reply_rule,
        'agent_action': agent_action,
        'target_ticket_status': target_ticket_status
    }

# Write the JSON data to a file
with open('rules.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(rules, indent=4, ensure_ascii=False))