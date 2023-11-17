# Здесь представлен полный скрипт с учетом изменений и исправлением для KeyError

# Исходные строки конфигурации коммутатора Cisco
config_lines = [
    # ... здесь должен быть ваш список строк ...
]

# Словарь для хранения информации об интерфейсах
interfaces = {}

# Временная переменная для хранения данных текущего интерфейса
current_interface = {}

for line in config_lines:
    if line.startswith('interface '):
        # Если начинается новый интерфейс, сохраняем предыдущий и начинаем новый
        if 'name' in current_interface:
            # Сохраняем информацию о предыдущем интерфейсе
            interfaces[current_interface['name']] = {
                'description': current_interface.get('description', ''),
                'type': current_interface.get('type', 'access'), # По умолчанию тип 'access'
                'vlan': current_interface.get('vlan', ''),
                'shutdown': current_interface.get('shutdown', 'no')
            }
        # Сбрасываем или инициализируем current_interface для нового интерфейса
        current_interface = {'name': line.split()[1], 'shutdown': 'no'}
    elif 'description' in line:
        # Извлекаем описание интерфейса
        current_interface['description'] = ' '.join(line.split()[1:])
    elif 'switchport mode' in line:
        # Извлекаем режим интерфейса
        current_interface['type'] = line.split()[-1]
    elif 'switchport access vlan' in line:
        # Извлекаем VLAN для режима доступа
        current_interface['vlan'] = line.split()[-1]
    elif 'shutdown' in line:
        # Устанавливаем статус shutdown
        current_interface['shutdown'] = 'yes'

# Не забываем добавить последний интерфейс
if 'name' in current_interface:
    interfaces[current_interface['name']] = {
        'description': current_interface.get('description', ''),
        'type': current_interface.get('type', 'access'), # По умолчанию тип 'access'
        'vlan': current_interface.get('vlan', ''),
        'shutdown': current_interface.get('shutdown', 'no')
    }

# Выводим результат
print(interfaces)
