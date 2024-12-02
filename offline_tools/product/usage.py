import pandas as pd
import json
# Read the Excel file into a DataFrame
df = pd.read_excel('主要な電気製品の起動電力一覧.xlsx')

# Convert each row to a dictionary (JSON object)
json_data = df.to_dict(orient='records')

# Print the JSON data
usage = []
for item in json_data:
    print(item)
    usage.append(item)

with open('usage.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(usage, indent=4, ensure_ascii=False))