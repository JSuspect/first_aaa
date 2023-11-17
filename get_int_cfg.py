import os
import re
from openpyxl import load_workbook


# Путь к файлам конфигурации
config_path = '/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/rusatom/config/source_cfg'
# Путь к Excel файлу
excel_path = '/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/rusatom/table.xlsx'

regex_interfsces_cfg = re.compile(r'interface\sFastEthernet[^!]*?!|interface\sGigabitEthernet[^!]*?!')

# Функция для извлечения данных из конфигурационного файла
def parse_config(config_file):
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'Windows-1252']
    config = None

        # Попробуйте открыть файл с каждой кодировкой из спискаd
    for encoding in encodings:
        try:
            with open(config_file, 'r', encoding=encoding) as file:
                config = file.read()
            break  # Прерываем цикл, если чтение прошло успешно
        except UnicodeDecodeError:
            pass  # Пропустить и попробовать следующую кодировку, если возникает ошибка
        
    # Если после всех попыток config все еще None, бросить исключение
    if config is None:
        raise ValueError(f"Не удалось открыть файл {config_file} с любой из проверенных кодировок.")

    # Извлекаем имя хоста
    hostname_match = re.search(r'hostname (\S+)', config)
    hostname = hostname_match.group(1) if hostname_match else None

    # Извлекаем IP-адрес управления
    management_ip_match = re.search(r'interface Vlan10\s+ip address (\S+)', config)
    management_ip = management_ip_match.group(1) if management_ip_match else None
    
    ports_data = []
    matches = regex_interfsces_cfg.finditer(config)

    for match in matches:
        vlan = None
        interface = None
        interface_type = None
        shutdown = None
        description = None

        int_config = match.group()

        interface_match = re.search(r'interface\s(FastEthernet\S+|GigabitEthernet\S+)', int_config)
        interface = interface_match.group(1)

        description_match = re.search(r'description (.*)', int_config)
        description = description_match.group(1) if description_match else None

        type_match = re.search(r'(?:switchport mode (access|trunk))', int_config)
        interface_type = type_match.group(1) if type_match else None

        shutdown_match = re.search(r'shutdown', int_config)
        shutdown = shutdown_match.group() if shutdown_match else None
        
        vlan_access_match = re.search(r'(?:switchport (access vlan) (\d+))', int_config)
        vlan_trunk_match = re.search(r'(?:switchport (trunk allowed vlan) (\S+))', int_config)
        
        if ((interface_type == 'access') or interface_type == None) and (vlan_access_match is not None):
            vlan = vlan_access_match.group(2)
            interface_type = 'access'
        elif (interface_type == 'access') and (vlan_access_match is None):
            vlan = '1'
        elif (interface_type == 'trunk') and (vlan_trunk_match is not None):
            vlan =  vlan_trunk_match.group(2)
        elif (interface_type == 'trunk') and (vlan_trunk_match is None):
            vlan = 'ALL'
        elif (interface_type is None) and (vlan_access_match is None) and (vlan_trunk_match is None) and (description is None):
            interface_type = 'NOTCONFIG'

        ports_data.append((hostname, description, management_ip, interface, interface_type, vlan, shutdown))

    return ports_data

# Загружаем рабочую книгу и выбираем активный лист
wb = load_workbook(excel_path)
ws = wb['py_proc']

# Извлекаем и добавляем информацию по портам в Excel
for config_filename in os.listdir(config_path):
    full_path = os.path.join(config_path, config_filename)
    if os.path.isfile(full_path):
        ports_data = parse_config(full_path)
        for data in ports_data:
            print(data)
            ws.append(data)

# Сохраняем изменения в Excel файле
wb.save(excel_path)
print("Excel файл успешно обновлен.")
