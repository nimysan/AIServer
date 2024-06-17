import openpyxl
import xml.etree.ElementTree as ET


def row_to_line(row, index, name, root_element):
    cell = row[index]  # Category
    cell_element = ET.SubElement(root_element, name)
    value = str(cell)
    cell_element.text = value
    if name == 'Subcategory' and value == "None":
        cell_element.text = current_sub_catetory;
    if name == "Category" and value == "None":
        cell_element.text = current_category;
    return value


# Charger le fichier Excel
workbook = openpyxl.load_workbook('/Users/yexw/accounts/华宝/AI质检/Quality Inspection Standards.xlsx')
worksheet = workbook.active

# Créer l'élément racine
root = ET.Element('Quality_Inspection_Standards')

current_category = ""
current_sub_catetory = ""
# Parcourir les lignes et les colonnes du fichier Excel
for row in worksheet.iter_rows(min_row=3, values_only=True):

    row_element = ET.SubElement(root, 'Standard')

    catetory_value = row_to_line(row, 0, "Category", row_element)
    if catetory_value != 'None':
        current_category = catetory_value

    current_sub_catetory_value = row_to_line(row, 1, "Subcategory", row_element)
    if current_sub_catetory_value != 'None':
        current_sub_catetory = current_sub_catetory_value

    row_to_line(row, 2, "Details", row_element)
    row_to_line(row, 3, "Deduction_Score", row_element)
    row_to_line(row, 4, "Frequency", row_element)
    row_to_line(row, 5, "Deduction_Score_Cumulative", row_element)

# Créer un arbre XML
tree = ET.ElementTree(root)

# Écrire l'arbre XML dans un fichier
tree.write('output.xml', encoding='utf-8', xml_declaration=True, method='xml')
