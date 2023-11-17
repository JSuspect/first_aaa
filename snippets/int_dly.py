from pprint import pprint
import pathlib


def get_int_dly(config):
    with open(config, 'r') as file:
        int_show = file.read().split('\n')
    print('='*20, config.name, '='*20)
    for line in int_show:
        if 'gigabitethernet' in line:
            intf = line
        elif 'tunnel' in line:
            intf = line
        elif 'DLY' in line:
            dly = line.split(',')[-2]
            print(f'{intf}{dly}')



file_dir = pathlib.Path('/mnt/c/Users/SBakhvalov/Documents/_wsl_dir/cppk/show')

for file_path in file_dir.glob('*sh_int.txt'):
    print(file_path)
    get_int_dly(file_path)