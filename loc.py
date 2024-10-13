import os
import sys
import re
from tkinter import filedialog

from loguru import logger

print(
        "Здравствуйте, это программа предназначена для помощи в локализации при моддинге в Hearts of Iron IV. Эта программа может работать в нескольких режимах:\n1) Выбрать файл который будет локализован\n2) Выбрать файл и сделать из него заготовку под локализацию"
)
logger.remove()


def work(mode: int, zero: bool, space: bool, file: str = ''):
    global file_output
    file_output = os.path.dirname(file) + '/ready localisation/loc.yml'
    if not os.path.exists(file_output):
        os.makedirs(file_output)
    if file == '':
        print('Откройте файл для локализации')
        file = filedialog.askopenfilename(title='Выберете файл для локализации', filetypes=[('Файл hoi4', '*.txt')])
    if file == '':
        print(f"Файл не выбран!")
        while True:
            q_exit = input('Попробовать ещё раз или выход?\n[в/п]: ')
            if q_exit == 'п':
                break
            elif q_exit == 'в':
                sys.exit()
            else:
                print("[red]Некорректный ввод![/red] Повторите попытку.\n")
    else:
        logger.info('Выбран путь: ' + file)
        with open(file, 'r', encoding='UTF-8') as file_input:
            full_loc = {}
            for line in file_input:
                if line.strip().startswith('id = '):
                    id_foc = line[len('id =  '):].strip()
                    loc_id = re.sub(r'^[A-Z]{3}_', '', id_foc).capitalize().replace('_', ' ')
                    full_loc[id_foc] = loc_id
        with open(file_output, 'w+', encoding='UTF-8') as FO:
            lines = FO.readlines()
            if not any(line.strip() == 'l_:' for line in lines):
                FO.write('l_english:\n')
            for key, value in full_loc.items():
                if mode == 1:
                    text_output = f'{key}: "{value}"\n'
                    if zero in ['д', True]:
                        text_output = f'{key}:0 "{value}"\n'
                    if space in ['д', True]:
                        text_output = ' ' + text_output
                elif mode == 2:
                    text_output = f'{key}: ""\n'
                    if zero in ['д', True]:
                        text_output = f'{key}:0 ""\n'
                    if space in ['д', True]:
                        text_output = ' ' + text_output
                FO.write(text_output)


if __name__ == '__main__':
    while True:
        while True:
            working_mode = int(input("Выберите пожалуйста вариант работы [1/2]: "))
            if working_mode in (1, 2):
                break
            else:
                print("[red]Некорректный ввод![/red] Повторите попытку.\n")
        while True:
            print()
            need_zero = input(
                    "Нужно ли вставлять '0' в локализацию? Примеры: \n"
                    "Focus_example:0 \"Focus example\" \nИЛИ \nFocus_example: \"Focus example\" \n[д/н]: "
            )
            if need_zero in ('д', 'н'):
                break
            else:
                print("[red]Некорректный ввод![/red] Повторите попытку.\n")
        while True:
            print()
            need_space = input(
                    "Нужны ли пробелы в локализации? Примеры:\nl_english:\nUsa_focus: \"Usa focus\" \nИЛИ \nl_english:\n Usa_focus: \"Usa focus\" \n[д/н]: "
            )
            if need_space in ('д', 'н'):
                break
            else:
                print("[red]Некорректный ввод![/red] Повторите попытку.\n")
        work(working_mode, need_zero, need_space)
        print()
        print(
                "[green]Локализация успешно создана![/green]\nДля перехода в файл напишите напишите 'о', для повтора скрипта 'п', для выхода любое другое."
        )
        exit_ask = input('[о, п, (другое)]: ')
        if exit_ask == 'о':
            os.startfile(file_output)
        elif exit_ask == 'п':
            pass
        else:
            sys.exit()
