import json
import os
import sys
import time
from pathlib import Path

from tkinter import filedialog
from loguru import logger
from prettytable import PrettyTable

from find_part_focus_in_file import find_part_focus, country
from get_name_with_help_id import get_name_with_help_id

logger.remove()
logger.add(
        sink='logs/read_focus.log',  # для консоли sys.stdout с библиотекой sys
        level='INFO',
        mode='w',
        format='{time:H:mm:ss} | <level>{level}</level> | {line}: {message}',
)
focus_files = []


def open_folder_with_focus() -> str:
    file_folder = ''
    while file_folder == '':
        print('Откройте папку с файлами фокусов:')
        # TODO исправить выбор папки
        file_folder = filedialog.askdirectory(
                title='Открыть папку с фокусами',
                initialdir='C:/Program Files (x86)/steam/steamapps/common/Hearts of Iron IV'
        )
        if file_folder == '':
            print(f"Папка не выбрана!")
            while True:
                q_exit = input('Попробовать ещё раз или выход?\n[в/п]: ')
                if q_exit == 'п':
                    break
                elif q_exit == 'в':
                    sys.exit()
                else:
                    print("Команда не найдена! Повторите попытку.")
        else:
            logger.info('Выбран путь: ' + file_folder)
            return file_folder


file_folder = open_folder_with_focus()
print("Выбранный путь к файлу: ", file_folder.replace(' ', '_'))

for files in os.listdir(file_folder):
    start_time = time.time()
    if Path(files).suffix == '.txt':
        logger.info(f'Файлы: {files}')
        focus_files.append(files)
    else:
        logger.warning(f'Посторонние файлы:{files}')
        print(f"В папке обнаружены посторонние файлы: [red]{files}[/red].\nПожалуйста выберете другую папку.")
        open_folder_with_focus()
else:
    focus_files = ', '.join(focus_files)
    print(f"Найдены следующие файлы фокусов:\n[dodger_blue2]{focus_files}[/dodger_blue2]")
    # question = input("Продолжить работу с ними?\n[да/нет]: ")
    question = 'да'  # TODO потом убрать
    print('')
    if question == 'да' or question == 'yes':
        for files in os.listdir(file_folder):
            find_part_focus(f'{file_folder}/{files}')  # вызов функции поиска фокусов
            logger.info(f'Вызвана функция find_part_focus {file_folder}/{files}.\n')
            country_table = PrettyTable(field_names=['Country', 'Number of focus'])
        for key_c, value_c in country.items():
            name_country = get_name_with_help_id(key_c)
            table = PrettyTable(field_names=['ID', 'cost', 'prerequisite'], title=f'focuses {name_country}')
            for key_f, value_f in value_c.items():
                table.add_row(
                        [value_f.get('id'), value_f.get('cost'), ', '.join(value_f.get('prerequisite'))
                        if isinstance(value_f.get('prerequisite'), list) else value_f.get('prerequisite')]
                )
            print(table)
            country_table.add_row([name_country.capitalize(), len(value_c)])
            print(country_table)

        with open('focus_json.json', 'w') as json_file:
            json_record = country
            logger.info(f'Запись в json {json_record}')
            json.dump(json_record, json_file, indent=4)
            end_time = time.time()
            logger.info(f'Время выполнения: {end_time - start_time}')
    else:
        open_folder_with_focus()
