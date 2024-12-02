import pandas as pd
import json

excel_name = "储能、太阳能板规格表.xlsx"
df = pd.read_excel(excel_name, sheet_name='アクセサリー', header=0)

# 将DataFrame转换为字典列表
data = df.to_dict(orient='records')

# 提取每一行数据为JSON,并放入数组
result = []
for row in data:
    product_name = row.pop(df.columns[0])  # 将第一列作为产品名称
    specs = {}
    for key, value in row.items():
        if pd.notnull(value):
            specs[key] = value
    product_info = {
        'product_name': product_name,
        'specs': specs
    }

    if pd.notnull(product_name) and specs:  # 过滤掉product_name为空或specs为空的情况
        result.append(product_info)

# Write the JSON data to a file
with open('acc.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(result, indent=4, ensure_ascii=False))