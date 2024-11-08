import pandas as pd
import json


# Read the Excel data into a pandas DataFrame
excel_name = "储能、太阳能板规格表.xlsx"
df = pd.read_excel(excel_name, sheet_name='ソラパ一覧',header=0)
# Convert the DataFrame to a dictionary
# print(df)
data = df.to_dict(orient='records')

#
def retrieve_solar(data):
    # Create a dictionary to store the combined data
    combined_data = {}
    # Iterate over each column in the data
    for col in df.columns[1:]:
        # Initialize a dictionary for the current column
        combined_data[col] = {}
        # Iterate over each row in the data
        for row in data:
            # Get the values from the first and current columns
            col1_value = row[df.columns[0]]
            col_value = row[col]
            # Skip rows with NaN values in the first column or the current column
            if pd.isna(col1_value) or pd.isna(col_value):
                continue

            # Combine the first and current columns
            key = str(col1_value)
            combined_data[col][key] = str(row[col])

    # Convert the combined data to JSON
    products = []
    for col, data_dict in combined_data.items():
        products.append(data_dict)
    return products;



products = retrieve_solar(data)
print(products)
# Write the JSON data to a file
with open('solar.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(products, indent=4, ensure_ascii=False))