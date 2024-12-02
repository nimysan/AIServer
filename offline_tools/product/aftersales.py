import pandas as pd

# 读取Excel文件
excel_name = "储能、太阳能板规格表.xlsx"
df = pd.read_excel(excel_name, sheet_name='保証期間', header=0)


def b2022():
    global warranty_info, index, row, product_name, website_warranty, retailer_warranty
    # 提取保修政策信息
    warranty_info = []
    for index, row in df.iterrows():
        product_name = row[df.columns[0]]  # 第一列作为产品名称
        website_warranty = row[df.columns[1]]  # 第二列作为官网购买保修期限
        retailer_warranty = row[df.columns[2]]  # 第三列作为其他渠道购买保修期限

        # 过滤掉产品名称为空或保修期限为空的情况
        if pd.notnull(product_name) and pd.notnull(website_warranty) and pd.notnull(retailer_warranty):
            warranty_info.append({
                'product_list': product_name,
                '公式サイトでご購入': website_warranty,
                '楽天/ヤフー/アマゾン/実店舗でご購入': retailer_warranty,
                '满足条件': '注文日は2022年1月1日以降の製品'
            })

    return warranty_info;

def a2022():
    global warranty_info, index, row, product_name, website_warranty, retailer_warranty
    # 提取保修政策信息
    warranty_info = []
    for index, row in df.iterrows():

        product_name = row[df.columns[0]]  # 第一列作为产品名称
        a = row[df.columns[3]]  # 第二列作为官网购买保修期限
        b = row[df.columns[4]]  # 第三列作为其他渠道购买保修期限
        c = row[df.columns[5]]  # 第三列作为其他渠道购买保修期限

        # 如果第4列的值为"NA"或者是空值,则将其设置为字符串"N/A"

        if pd.isnull(a) or str(a) == "NA":
            a = "N/A"

        # 如果第5列的值为"NA"或者是空值,则将其设置为字符串"N/A"

        if pd.isnull(b) or str(b) == "NA":
            b = "N/A"

        # 如果第6列的值为"NA"或者是空值,则将其设置为字符串"N/A"

        if pd.isnull(c) or str(c) == "NA":
            c = "N/A"

        # 过滤掉产品名称为空或保修期限为空的情况
        if pd.notnull(product_name) and pd.notnull(website_warranty) and pd.notnull(retailer_warranty):
            warranty_info.append({
                'product_list': product_name,
                '公式サイトでご購入': a,
                '楽天/ヤフー/アマゾン/実店舗でご購入': b,
                '保証延長対応ですか？':c,
                '满足条件': '注文日は2021年12月31日までの製品'
            })
    return warranty_info;

a = b2022()
b = a2022()

object= {
    "注文日は2021年12月31日までの製品": b,
    "注文日は2022年1月1日以降の製品":a
}

import json

# Write the JSON data to a file
with open('warranty_info.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(object, indent=4, ensure_ascii=False))