import os
import re
import customtkinter
import sys
from PIL import Image
from tkinter import filedialog

ico_uptade = customtkinter.CTkImage(
        light_image=Image.open('перезагрузка.png'),
        dark_image=Image.open('перезагрузка.png'), size=(30, 30)
)

focus_name_massiv = []
focus_dictionary = {}
ideologies_massiv = ['фашизм', 'комунизм', 'демокртия', 'нейтралитет']


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
        self.id = id
        self.cost = cost
        self.prerequisite = prerequisite
        self.mutually_exclusive = mutually_exclusive
        focus_name_massiv.append(self.id)
        focus_dictionary[id] = {'self': self, 'id': self.id, 'cost': self.cost, 'prerequisite': self.prerequisite,
                                'mutually_exclusive': self.mutually_exclusive}
        if create_focus == 1:
            self.focus_to_file(id, cost, prerequisite, mutually_exclusive)
        else:
            ...  # ничего не происходит

    def info(self):
        output = f'\nФокус: "{self.id}" | {self.cost}\n'
        if self.prerequisite:
            output += f'prerequisite: {self.pre}\n'
        if self.mutually_exclusive:
            output += f'mutually_exclusive: {self.muex}\n'
        return output

    @staticmethod
    def all_focus():
        output = ', '.join(focus_name_massiv)
        return output

    @staticmethod
    def clear_focus_file():  # очитска всего файла
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
        self.id = id

    def set_cost(self, cost):
        self.cost = cost

    def set_pre(self, prerequisite):
        self.pre = prerequisite

    def set_muex(self, mutually_exclusive):
        self.muex = mutually_exclusive

    def editing_focus(self):
        pass

    def focus_to_file(self, id, cost, prerequisite=None, mutually_exclusive=None):
        with open("focus.txt", 'a') as focus_file:
            focus_entry = f"focus = {{\n    id = {self.id}\n    cost = {self.cost}\n"
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
        self.iconbitmap('Hoi4 logo.ico')
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
                tab.tab('focus'), height=33, width=120, fg_color='#010046',
                text='открыть', command=self.open_file, corner_radius=10
        )
        self.btnopenfocusfile.grid(padx=5, pady=(15, 0))

        # кнопка сохранить
        self.btnsavefocusfile = customtkinter.CTkButton(
                tab.tab('focus'), height=33, width=120, fg_color='#010046', text='сохранить', command=self.save_file,
                corner_radius=10
        )
        self.btnsavefocusfile.grid(padx=5, pady=5)

        # кнопка обнвления
        self.updatebtn = customtkinter.CTkButton(master=tab.tab('focus'), command=self.uptadewidget, image=ico_uptade)
        self.updatebtn.grid(padx=20, pady=30)

    def uptadewidget(self):
        app.update()

    def open_file(self):
        if len(focus_name_massiv) > 0:
            print(f"Всего было найдено фокусов {len(focus_name_massiv)}:")
            # print(', '.join(focus_name_massiv))
            print(focus_class.all_focus())

        else:
            print("Фокусы в файле не найдены!")
            focus_tree_quest = input("Создать новую ветку фокусов?: ")
            if focus_tree_quest == 'yes' or focus_tree_quest == 'да':
                focus_tree_tag_quest = input("На какую страну делаем ветку фокусов?: ").lower()
                if focus_tree_tag_quest.upper() in tag_coutries:
                    create_focus_tree(focus_tree_tag_quest)
                else:
                    create_focus_tree(get_key(focus_tree_tag_quest))
            else:
                pass

    def save_file(self):
        pass


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


app = App_class()
app.mainloop()
