config_lines = [
    # ... Ваш список строк ...
]

# Список для хранения информации об интерфейсах
interfaces = []

# Временная переменная для хранения данных текущего интерфейса
current_interface = {}

for line in config_lines:
    if line.startswith('interface '):
        # Если начинается новый интерфейс, сохраняем предыдущий и начинаем новый
        if current_interface:
            interfaces.append([
                current_interface.get('name', ''),
                current_interface.get('description', ''),
                current_interface.get('mode', ''),
                current_interface.get('vlan', '')
            ])
        current_interface = {'name': line.split()[1]}
    elif 'description' in line:
        # Извлекаем описание интерфейса
        current_interface['description'] = ' '.join(line.split()[1:])
    elif 'switchport mode' in line:
        # Извлекаем режим интерфейса
        current_interface['mode'] = line.split()[-1]
    elif 'switchport access vlan' in line:
        # Извлекаем VLAN для режима доступа
        current_interface['vlan'] = line.split()[-1]

# Не забываем добавить последний интерфейс
if current_interface:
    interfaces.append([
        current_interface.get('name', ''),
        current_interface.get('description', ''),
        current_interface.get('mode', ''),
        current_interface.get('vlan', '')
    ])

# Выводим результат
for interface in interfaces:
    print(interface)
