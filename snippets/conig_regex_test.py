import os
import re

file_path = '/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/rusatom/config/source_cfg/conf_int.txt'
file_path2 = '/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/rusatom/config/source_cfg/conf_full.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    config_int = file.read()
with open(file_path2, 'r', encoding='utf-8') as file:
    config_full = file.read()

int_cfg = re.findall(r'interface\sFastEthernet[^!]*?!|interface\sGigabitEthernet[^!]*?!', config_full)

shutdown = None

for i in int_cfg:
    list_int = i.split('\n')
    if ' shutdown' in list_int:
        shutdown = 'yes'
    else
    for n in list_int:
    
# Проверка регулярки
re.findall(r'^interface\s*(?P<text>[^!]+)(?:!)?')

regex = re.compile(
    r'interface\s(FastEthernet\S+|GigabitEthernet\S+)'  # Начало блока интерфейса
    r'(?:switchport mode (access|trunk).*?)?'  # Необязательная строка switchport mode
    r'(?:switchport access vlan (\d+)|switchport trunk allowed vlan (\S+)).*?'  # VLAN настройки
    r'!',  # Конец блока интерфейса
    re.DOTALL | re.IGNORECASE
)


match1 = re.finditer(r'(interface\s*[^!]+!?)', config)
# От Рината
regex = re.compile(r'^interface\s*(?<text>[^!])+(?:!)?')
# От Рината исправленное
regex = re.compile(r'^interface\s*(?P<text>[^!]+)(?:!)?')

matches = regex.finditer(config)

for match in matches:
    interface = match.group(1) + str(match.group(2))  # Concatenate interface type with port number
    mode = match.group(4)
    vlan = 'unknown'  # Default value if VLAN is not found


    interface = match.group(1) + str(match.group(2))  # Concatenate interface type with port number
    mode = match.group(4)
    vlan = 'unknown'  # Default value if VLAN is not found
    # Access VLAN
    if mode == 'access' and match.group(5):
        vlan = match.group(5)
    # Trunk VLAN
    elif mode == 'trunk' and match.group(6):
        vlan = match.group(6)
