import pandas as pd

# 读取Excel文件
df = pd.read_excel('各产品故障码对应方法.xlsx', header=None)

# 提取产品列表
products = df.iloc[0, 1:].tolist()

# 创建列表存储数据
data = []

# 遍历数据行
for i in range(1, df.shape[0]):
    error_code = df.iloc[i, 0]
    for j in range(1, df.shape[1]):
        product = products[j-1]
        handling_method = df.iloc[i, j]
        if pd.notnull(handling_method):
            item = {
                "error_code": error_code,
                "product": product,
                "handling_method": handling_method
            }
            data.append(item)

# 将数据转换为JSON格式
import json
json_data = json.dumps(data, indent=4, ensure_ascii=False)

# 打印JSON数据
print(json_data)

# Write the JSON data to a file
with open('error_code.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(data, indent=4, ensure_ascii=False))