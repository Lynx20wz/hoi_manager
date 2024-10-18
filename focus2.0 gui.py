import os
import re
import sys
from PIL import Image
from tkinter import filedialog
import json

import customtkinter
from MoreCustomTkinterWidgets import askfile

import find_part_focus_in_file

ico_uptade = customtkinter.CTkImage(
        light_image=Image.open('перезагрузка.png'),
        dark_image=Image.open('перезагрузка.png'), size=(30, 30)
)

focus_name_massiv = []
focus_dictionary = {}
ideologies_massiv = ['фашизм', 'комунизм', 'демокртия', 'нейтралитет']

# colors
C_DARK_BLUE = '#010046'

# font
F_UNI_HEAVY_CAPS = ('Uni Sans Heavy Caps', 22)


class country_class:
    def __init__(self, tag, name, ideologies, capital=None, leader=None, create_country=None):
        self.tag = tag
        self.name = name
        self.capital = capital
        self.ideologies = ideologies
        self.leader = leader

        if create_country == 1:
            create_country(tag, name, ideologies, capital, leader)

    def create_country(self, tag, name, ideologies, capital=None, leader=None):
        with open(f"{name}.txt"):
            pass


class focus_class:

    # инициализация

    def __init__(self, id, cost, prerequisite=None, mutually_exclusive=None, create_focus=None):
        self.id_focus = id
        self.cost = cost
        self.prerequisite = prerequisite
        self.mutually_exclusive = mutually_exclusive
        focus_name_massiv.append(self.id_focus)
        focus_dictionary[id] = {'self': self, 'id': self.id_focus, 'cost': self.cost, 'prerequisite': self.prerequisite,
                                'mutually_exclusive': self.mutually_exclusive}
        if create_focus == 1:
            self.focus_to_file(id, cost, prerequisite, mutually_exclusive)

    def __str__(self):
        output = f'\nФокус: "{self.id_focus}" | {self.cost}\n'
        if self.prerequisite:
            output += f'prerequisite: {self.prerequisite}\n'
        if self.mutually_exclusive:
            output += f'mutually_exclusive: {self.mutually_exclusive}\n'
        return output

    @classmethod
    @property
    def all_focus(cls) -> str:
        """
        :return: строку с названием всех фокусов через запятую
        :rtype: str
        """
        output = ', '.join(focus_name_massiv)
        return output

    @staticmethod
    def clear_focus_file():  # очистка всего файла
        with open("focus.txt", "w") as file:
            file.write('')
        focus_name_massiv.clear()
        focus_dictionary.clear()
        print("Содержимое файла focus.txt было полностью удалено.")

    def search_focus_in_dictionary(id):
        for search_focus in focus_dictionary:
            if search_focus == id:
                search_focus = focus_dictionary[search_focus]['self']
                return search_focus

    # блок изменений частей

    def set_id(self, id):
        self.id_focus = id

    def set_cost(self, cost):
        self.cost = cost

    def set_pre(self, prerequisite):
        self.prerequisite = prerequisite

    def set_muex(self, mutually_exclusive):
        self.mutually_exclusive = mutually_exclusive

    def editing_focus(self):
        pass

    def focus_to_file(self, id, cost, prerequisite=None, mutually_exclusive=None):
        with open("focus.txt", 'a') as focus_file:
            focus_entry = f"focus = {{\n    id = {self.id_focus}\n    cost = {self.cost}\n"
            focus_entry += f'}}\n\n'
            focus_file.write(focus_entry)


class App_class(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.resizable(False, False)
        self.bg_image = customtkinter.CTkImage(Image.open("bg.jpg"), size=(800, 600))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        # self.attributes('-topmost', True) #закрепить наверху
        self.title("Modding manager")

        tab = customtkinter.CTkTabview(self, width=800, height=570, corner_radius=15, anchor='nw')
        tab.grid(row=0, column=0)

        tab.add('focus')
        tab.set('focus')
        tab.add('spirits')

        # кнопки

        # кнопка открыть файл
        self.btnopenfocusfile = customtkinter.CTkButton(
                tab.tab('focus'), height=33, width=130, fg_color=C_DARK_BLUE,
                text='открыть', command=self.open_file, corner_radius=0, font=F_UNI_HEAVY_CAPS
        )
        self.btnopenfocusfile.grid(padx=5, pady=(15, 0))

        # кнопка сохранить
        self.btnsavefocusfile = customtkinter.CTkButton(
                tab.tab('focus'), height=33, width=130, fg_color=C_DARK_BLUE, text='сохранить', command=self.save_file,
                corner_radius=0, font=F_UNI_HEAVY_CAPS
        )
        self.btnsavefocusfile.grid(padx=5, pady=5)

        # кнопка обновления
        # self.updatebtn = customtkinter.CTkButton(master=tab.tab('focus'), command=lambda: app.update(), image=ico_uptade)
        # self.updatebtn.grid(padx=20, pady=30)

    def open_file(self):
        focus_file = filedialog.askopenfilename(title='Выберете фокус файл', filetypes=[('focus file', '*.txt')])
        result = find_part_focus_in_file.find_part_focus(focus_file)
        try:
            print(f"Всего было найдено фокусов {len(*result[1].values())}:")
        except TypeError:
            print("Фокусы в файле не найдены!")
            focus_tree_quest = input("Создать новую ветку фокусов?: ")
            if focus_tree_quest == 'yes' or focus_tree_quest == 'да':
                focus_tree_tag_quest = input("На какую страну делаем ветку фокусов?: ").lower()
                if focus_tree_tag_quest.upper() in tag_countries:
                    create_focus_tree(focus_tree_tag_quest)
                else:
                    create_focus_tree(get_key(focus_tree_tag_quest))
            else:
                pass

    def save_file(self):
        pass


def get_key(significance):
    for k, s in tag_countries.items():
        for s in s:
            if s == significance:
                return k
    else:
        unknown_tag_quest = input(
                'Такого названия не найдено! Хотите создать новую страну?: '
        )
        if unknown_tag_quest == 'yes' or unknown_tag_quest == 'да':
            tag = input('Введите трёх-символьный тэг страны (например: "GER"): ').upper()
            if len(tag) == 3 and re.match(r'^[A-Z]+$', tag):
                name = input("Введите название страны на вашем языке: ").lower()
                ideologies_quest = input(
                        "Введите идеологию страны (фашизм, коммунизм, нейтралитет, демократия, своя): "
                )
                if ideologies_quest in ideologies_massiv:
                    pass
        return 'MOD'


def create_focus_tree(id):
    id = id.upper()
    with open("focus.txt", 'w') as focus_file:
        focus_tree = f'''focus_tree = {{
    id = {id}_focus_tree
    country = {{
        factor = 0
        modifier = {{
            add = 15
            original_tag = {id}
        }} 
    }}'''
        focus_file.write(focus_tree)


if __name__ == '__main__':
    with open('tag_countries.json', 'r', encoding='utf-8') as file:
        tag_countries = json.loads(file.read())
    app = App_class()
    app.mainloop()
