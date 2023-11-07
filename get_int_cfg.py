import os
import re
from openpyxl import load_workbook

# Путь к файлам конфигурации
config_path = '/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/rusatom/config'
# Путь к Excel файлу
excel_path = '/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/rusatom/table.xlsx'

regex = re.compile(
    r'interface (FastEthernet|GigabitEthernet)\S+.*?'  # Начало блока интерфейса
    r'(?:switchport mode (access|trunk).*?)?'  # Необязательная строка switchport mode
    r'(?:switchport access vlan (\d+)|switchport trunk allowed vlan (\d+)).*?'  # VLAN настройки
    r'!',  # Конец блока интерфейса
    re.DOTALL | re.IGNORECASE
)





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
    
    matches = regex.finditer(config)

    for match in matches:
        interface = match.group(1) + str(match.group(2))  # Concatenate interface type with port number
        mode = match.group(4)
        vlan = 'unknown'  # Default value if VLAN is not found

        # Access VLAN
        if mode == 'access' and match.group(5):
            vlan = match.group(5)
        # Trunk VLAN
        elif mode == 'trunk' and match.group(6):
            vlan = match.group(6)
        ports_data.append((hostname, management_ip, interface, mode, vlan))

    # Извлекаем информацию о портах
#    ports_data = []
#    for port_match in re.finditer(r'interface (\S+)\s+(?:.*\n)+?switchport (?:mode (\S+)).+?vlan (\d+)', config):
#        port, mode, vlan = port_match.groups()
#        ports_data.append((hostname, management_ip, interface, mode, vlan))

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
