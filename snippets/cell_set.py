import openpyxl
from pathlib import Path

path_book = Path('/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/rusatom/table.xlsx')
target_book = openpyxl.load_workbook(path_book, data_only=True)

target_sheet = target_book['py_proc']

vlan_set = set()

for row in target_sheet.iter_rows():
    cell_value = row[5].value

    # Check if the cell value is not None
    if cell_value is not None:
        print(row[5])
        print(row[5].coordinate)
        print(cell_value)

        # Check if the cell value contains a comma and split if it does
        if ',' in cell_value:
            row_split = cell_value.split(',')
            for i in row_split:
                vlan_set.add(i.strip())  # strip() removes any leading/trailing whitespace
        else:
            vlan_set.add(cell_value.strip())  # also stripping here for consistency
    else:
        # Optional: Print something if the cell is empty
        print(f"Empty cell at {row[5].coordinate}")


list_vlan_set = []


for vlan in vlan_set:
    if vlan.isdigit():
        vlan = int(vlan)
        list_vlan_set.append(vlan)


list_vlan_set.sort()

print(
    f'Таблица: {path_book.name}\n'
    f'Полный путь: {path_book}\n'
    f'Содержит следующие наборы VLAN: {vlan_set}\n'
    )

print('Упорядоченный набор VLAN:')
for vlan in list_vlan_set:
        print(f'VLAN {vlan}')