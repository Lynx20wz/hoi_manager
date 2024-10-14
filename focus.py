import re
part_focus_m = ['id', 'cost', 'prerequisite', 'mutually_exclusive']
focus_m = []
focus_fc_m = []
first_f = True


class fc:
    def __init__(self, id, cost=None, prerequisite=None, mutually_exclusive=None):
        self.id = id
        self.cost = cost
        self.pre = prerequisite
        self.muex = mutually_exclusive

    def set_id(self, id):
        self.id = id

    def set_cost(self, cost):
        self.cost = cost

    def set_pre(self, prerequisite):
        self.pre = prerequisite

    def set_muex(self, mutually_exclusive):
        self.muex = mutually_exclusive

    def part(self):
        output = f'\nФокус: "{self.id}" | {self.cost}\n'
        if self.pre:
            output += f'prerequisite: {self.pre}\n'
        if self.muex:
            output += f'mutually_exclusive: {self.muex}\n'

        return output

def created_focuses(id, cost, za_pre, id_pre, za_muex, id_muex):  #создание фокуса
    with open("focus.txt", "a") as file:
        focus = fc(id, cost, id_pre, id_muex)

        Focus = f"focus = {{\n    id = {focus.id}\n    cost = {focus.cost}\n"
        if za_pre == 'да' or za_pre == 'yes':
            Focus += f"    prerequisite = {{focus = {id_pre}}}\n"
        if za_muex == 'да' or za_muex == 'yes':
            Focus += f"    mutually_exclusive = {{focus = {id_muex}}}\n"
        Focus += "}\n\n"
        file.write(Focus)

    focus_m.append(id)
    focus_fc_m.append(focus)
    print(focus.part())


def edit_focus(id):  #редактирование фокусов
    id_fc = found_in_mas(id)
    while True:
        what_modify = input(f'Что изменить? {part_focus_m}:\n')
        if what_modify in part_focus_m:
            if what_modify  == 'id':
                new_id = input("Введите новое id для фокуса: ")
                id_fc.set_id = new_id
                focus_fc_m.append(id_fc)
                print(f"{id} был изменён на {new_id}")
                break
        else:
            print("Неверная часть фокуса!")


def found_in_mas(id):  #поиск в массиве по id
    for id_fc in focus_fc_m:
        if id_fc.id == id:
            return id_fc

def all_vosm_focus(id_pre):  # просчёт всех возможных фокусов
    global filtered_massiv
    filtered_massiv = [focus for focus in focus_m if focus != id_pre]
def all_focus():  #вывод всех фокусов
    if len(focus_m) < 1:
        print("Фокусов не было найдено")

    else:
        print(f"Всего фокусов {len(focus_m)}:")
        focus_str = ', '.join(''.join(focus) for focus in focus_m)
        print(focus_str)

def clear_focus_file():  #очитска всего файла
    focus_m.clear()
    with open("focus.txt", "w") as file:
        file.write("")
    print("Содержимое файла focus.txt было полностью удалено.")

def clear_focus(id):
    id_found = id[6:]
    with open("focus.txt", "r") as file:
        lines = file.readlines()

    new_lines = []
    focus_block = []
    in_focus_block = False
    for line in lines:
        if line.startswith('focus = {'):
            in_focus_block = True
            focus_block = [line]
        elif in_focus_block:
            focus_block.append(line)
            if line.strip() == '}':
                in_focus_block = False
                focus_id_line = [l for l in focus_block if f'id = {id_found}' in l]
                if not focus_id_line:
                    new_lines.extend(focus_block)
        else:
            new_lines.append(line)

    with open('focus.txt', 'w') as file:
        file.writelines(new_lines)


def add_muex(id, id_muex):  #добавление mutually_exclusive
    id_muex_fc = found_in_mas(id_muex)
    id_muex_fc.set_muex(id)
    with open ('focus.txt') as file:
        file.write(f"mutually_exclusive = {{focus = {id_muex}}}\n")


print("""Задрвствуйте, это программа создана для моддинга в Heart of Iron4. В данный момент вам доступны следующие комнады:
Настройки, фокусы, выход""")

try:
    with open("focus.txt", "r") as file:
        not_file = False
        for line in file:
            if "id =" in line:
                start_idx = line.find("id = ") + len("id = ")
                id_name = line[start_idx:].strip()
                focus_m.append(id_name)
                id_name_fc = fc(id_name)
                focus_fc_m.append(id_name_fc)
            if "cost = " in line:
                start_idx = line.find("cost = ") + len("cost = ")
                cost_read = line[start_idx:].strip()
                id_name_fc.set_cost(cost_read)
            if "prerequisite =" in line:
                start_idx = line.find("prerequisite = {focus =") + len("prerequisite = {focus =")
                pre_read = line[start_idx:].strip()
                pre_read = pre_read[:-1]
                id_name_fc.set_pre(pre_read)
            if "mutually_exclusive =" in line:
                start_idx = line.find("mutually_exclusive = ") + len("mutually_exclusive = ")
                muex_read = line[start_idx:].strip()
                muex_read = muex_read[:-1]
                id_name_fc.set_muex(muex_read)


except FileNotFoundError:
    print("Файл с фокусами не был найден!")
    not_file = True

if len(focus_m) > 0:
    print(f"Всего было найдено фокусов {len(focus_m)}:")
    focus_str = ', '.join(''.join(focus) for focus in focus_m)
    print(focus_str)
    first_f = False
else:
    if not not_file:
        print("В файле не были найдены фокусы")




while True:
    com = input("Напишите название команды: " ).lower()
    if com == 'настройки' or com == 'settings':
        ...
    elif com == 'clear':
        clear_focus_file()
    elif com == 'выход' or com == 'exit':
        break
    elif com == 'фокусы' or com == 'focus':
        while True:
            if len(focus_m) == 0:
                first_f = True
            filtered_massiv = []
            id_pre = ''
            za_pre = ''
            za_muex = ''
            id_muex = ''
            id = input('Введите название фокуса (на английском): ')
            if re.match(r'^[a-zA-Z0-9_ ]+$', id):
                if id == 'exit':
                    break
                elif id == 'clear':
                    clear_focus_file()
                elif id.startswith('clear '):
                    clear_focus(id)
                elif id == 'focuses':
                    all_focus()
                elif id in focus_m:
                    ed_f = input("Вы хотите изменить фокус или посмотреть его параметры?\n")
                    if ed_f == 'изменить':
                        edit_focus(id)
                    if ed_f == 'параметры':
                        id_fc = found_in_mas(id)
                        if id_fc is not None:
                            print(id_fc.part())
                        else:
                            print(f'Фокус с ID "{id}" не найден')
                else:
                    while True:
                        try:
                            cost = int(input('Сколько недель будет проходиться фокус: '))
                            break
                        except ValueError:
                            print("Некорректный ввод. Пожалуйста, введите целое число для количества недель.")
                    if not first_f:
                        za_pre = input("Сделать ли требование к предыдущему фокусу?\n")
                        if za_pre == 'да' or za_pre == 'yes':
                            if len(focus_m) > 1:
                                all_focus()
                                while True:
                                    id_pre = input("От какого фокуса вы хотите сделать требование?: ")
                                    if id_pre in focus_m:
                                        break
                                    elif id_pre == 'exit':
                                        break
                                    else:
                                        print("Введено некоректное имя фокуса!")
                            else:
                                id_pre = focus_m[0]
                        elif za_pre in focus_m:
                            id_pre = za_pre

                        if za_pre == 'да' or za_pre == 'yes' and len(focus_m) <= 1:
                            id_muex = None
                        else:
                            za_muex = input("Сделать ли этот фокус взаимоисключающимся?\n")
                            all_vosm_focus(id_pre)
                            if za_muex == 'да' or za_muex == 'yes' and len(filtered_massiv) <= 1:
                                id_muex = filtered_massiv[0]
                            elif za_muex == 'да' or za_muex == 'yes':
                                all_focus()
                                while True:
                                    id_muex = input("С каким фокусом его взаимоисключять?: ")
                                    if id_muex in focus_m and id_muex != id_pre:
                                        add_muex(id, id_muex)
                                        break
                                    elif id_pre == 'exit':
                                        break
                                    elif id_muex == id_pre:
                                        print("Нельзя делать взаимоисключение с фокусом от которого требование!")
                                    else:
                                        print("Введено некоректное имя фокуса!")
                        created_focuses(id, cost, za_pre, id_pre, za_muex, id_muex)
                    else:
                        first_f = False
                        created_focuses(id, cost, za_pre, id_pre, za_muex, id_muex)
                        all_focus()
            else:
                print('Название фокуса должно быть на английском!')
    else:
        print("Команда не найдена, повторите попытку")

print('Спасибо за использование программы!')
input("Нажмите enter для выхода")

