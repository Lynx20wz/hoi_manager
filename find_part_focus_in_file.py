import sys
from tkinter import filedialog

from loguru import logger
from get_name_with_help_id import get_name_with_help_id

logger.remove()
logger.add(
        sink='logs/find_part.log',
        level='INFO',
        mode='w',
        format='{time:H:mm:ss} | <level>{level}</level> | {line}: {message}',
)

country = {}


def same_id(tag, dict: dict, name):
    value_dict = country[tag]
    name_2 = get_name_with_help_id(tag)
    country[tag] = {
        name: dict,
        name_2: value_dict
    }


def sort_focus_dict(f_dict):
    id = f_dict.get('id')
    cost = f_dict.get('cost')
    prerequisite = f_dict.get('prerequisite', 'None')
    mutually_exclusive = f_dict.get('mutually_exclusive', 'None')
    focus_dict_sort = {'id': id, 'cost': cost, 'prerequisite': prerequisite, 'mutually_exclusive': mutually_exclusive}
    return focus_dict_sort


def block_code(name_part: str, file, focus_dict: dict):
    for line in file.readlines():
        if line.startswith('}'):
            break
        else:
            part = line[len(f'{name_part} = '):]
            if focus_dict.get(name_part) != None:
                if isinstance(focus_dict.get(name_part), list):
                    part1 = focus_dict.get(name_part)
                    all_part = part1.append(part)
                else:
                    part1 = focus_dict.get(name_part)
                    all_part = [name_part, part1]
                    focus_dict[name_part] = all_part
                logger.info(f'{all_part}')
            else:
                focus_dict[name_part] = part
                logger.info(part)


def find_part_focus(file: str) -> dict:
    repetitive_tag = False
    name_country = file[file.rfind('/') + 1:file.find('.')]
    tag = get_name_with_help_id(name_country)
    number_of_spaces_focus = None
    print(f'{name_country.capitalize()}: {tag}')
    with open(file, 'r', encoding='UTF-8') as focus_file:
        focus_block = False
        prerequisite = None
        focus_dict = {}
        for line in focus_file:
            number_of_spaces = line.count('\t')
            line = line.strip()
            if line.startswith('focus = {') or focus_block is True:
                if number_of_spaces_focus is None:
                    number_of_spaces_focus = number_of_spaces
                line = line.replace('#', '')
                focus_block = True
                if focus_block:
                    if line.startswith('tag =') and tag is None:
                        tag = line[len('tag = '):]
                        name_country = get_name_with_help_id(tag)
                        if tag in country and name_country not in country[tag]:
                            repetitive_tag = True
                    if line.startswith('id ='):
                        if focus_dict.get('id') is None:
                            id_focus = line[len('id = '):]
                            logger.info(f'ID фокуса: {id_focus}')
                            focus_dict['id'] = id_focus
                    if line.startswith('prerequisite ='):
                        focus_count = line.count('focus =')
                        if focus_count == 1:
                            prerequisite = line[len('prerequisite = { focus = '):line.rfind('}') - 1]
                            focus_dict['prerequisite'] = prerequisite
                        elif focus_count == 0 and '}' not in line:
                            block_code('prerequisite', focus_file, focus_dict)
                        else:
                            prerequisite = line[len('prerequisite = { focus = '):line.rfind('}') - 1].split(
                                    ' focus = '
                            )
                            focus_dict['prerequisite'] = prerequisite
                            prerequisite = ', '.join(i.strip() for i in prerequisite)

                    if line.startswith('mutually_exclusive ='):
                        focus_count = line.count('focus =')
                        if focus_count == 1:
                            mutually_exclusive = line[len('mutually_exclusive = { focus = '):line.rfind('}') - 1]
                            focus_dict['mutually_exclusive'] = mutually_exclusive
                        elif focus_count == 0 and '}' not in line:
                            block_code('mutually_exclusive', focus_file, focus_dict)
                        elif focus_count == 0:
                            pass
                        else:
                            mutually_exclusive = line[
                                                 len('mutually_exclusive = { focus = '):line.rfind('}') - 1].split(
                                    ' focus = '
                            )
                            focus_dict['mutually_exclusive'] = mutually_exclusive
                            # logger.info(f'Простой случай: {mutually_exclusive}')
                            mutually_exclusive = ', '.join(i.strip() for i in mutually_exclusive)

                    if line.startswith('cost ='):
                        if focus_dict.get('cost') is None:
                            cost = line[len('cost = '):]
                            focus_dict['cost'] = cost

                    if line.startswith('}') and number_of_spaces == number_of_spaces_focus:
                        logger.info(f'ID: {id_focus}, cost: {cost}, prerequisite: {prerequisite}')
                        focus_block = False
                        if focus_dict.get('prerequisite') is None:
                            focus_dict['prerequisite'] = 'None'
                        if focus_dict.get('mutually_exclusive') is None:
                            focus_dict['mutually_exclusive'] = 'None'
                        # logger.info(id_focus)
                        focus_dict = sort_focus_dict(focus_dict)
                        # logger.info(f'{id_focus}\n')
                        if tag not in country:
                            country[tag] = {}
                        if repetitive_tag is True:
                            same_id(tag, focus_dict, name_country)
                            country[tag][name_country][focus_dict.get('id')] = focus_dict.copy()
                        else:
                            country[tag][focus_dict.get('id')] = focus_dict.copy()
                        focus_dict.clear()
                        number_of_spaces_focus = None
    return tag


if __name__ == '__main__':
    file = ''
    while file == '':
        print('Откройте папку с файлами фокусов:')
        # TODO исправить выбор папки
        file = filedialog.askopenfilename(title='Выберете файл фокуса', filetypes=[('Фокус файл', '*.txt')])
        if file == '':
            print(f"Файл не выбран!")
            while True:
                q_exit = input('Попробовать ещё раз или выход?\n[в/п]: ')
                if q_exit == 'п':
                    break
                elif q_exit == 'в':
                    sys.exit()
                else:
                    print("Команда не найдена! Повторите попытку.")
        else:
            logger.info('Выбран путь: ' + file)
            find_part_focus(file)
