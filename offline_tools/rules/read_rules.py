import json

import pandas as pd

# 读取Excel表格数据
df = pd.read_excel('rules.xlsx', sheet_name='整理后的订单处理规则', header=0)

# 将预售订单标记为1,非预售订单标记为0
# df['is_pre_sales_order'] = df['is_pre_sales_order'].map({'yes': 1, 'no': 0})

# 将NaN替换为空字符串
df = df.fillna('')

# 生成规则对象
rules = {}
for _, row in df.iterrows():
    intent = row['intent']
    order_status = row['order_status']
    is_pre_sales_order = row['is_pre_sales_order']
    order_channel = row['order_channel']
    rule_for_handle = row['rule_for_handle']
    customer_reply_rule = row['customer_reply_rule']
    agent_action = row['agent_action']
    target_ticket_status = row['target_ticket_status']

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


def get_rule(intent, order_status, order_channel, is_pre_sales_order):
    try:
        return rules[intent][order_status][is_pre_sales_order][order_channel]
    except KeyError:
        return {'rule_for_handle': 'No matching rule found', 'customer_reply_rule': None, 'agent_action': None,
                'target_ticket_status': None}
