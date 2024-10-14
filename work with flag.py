import os
import re
import time
from tkinter import filedialog
from typing import Optional

import customtkinter
from CTkMessagebox import *
from CTkToolTip import *
from PIL import Image

customtkinter.set_appearance_mode("System")

C_BLUE = '#26658d'
C_DBLUE = '#318405a'
C_DGREY = '#4d4d4d'
SIZES = [(82, 52), (41, 26), (10, 7)]
WEIGHT_APP = 800
HEIGHT_APP = 350
BASE_IDEOLOGY = ["fascism", "communism", "neutrality", "democratic"]


class App(customtkinter.CTk):
    def __init__(self):
        """
        Инициализация основного приложения. Устанавливает параметры окна, создает и конфигурирует элементы управления.
        :var self.correct_tag: Проверка на корректный тэг
        :var self.correct_ideologies: Проверка что все кастомные идеологии подходят под требования
        :var self.folder_path: Путь до папки с изначальными флагами
        :var self.flags_folder_path: Конечный путь до папки
        :var self.ideology: Идеологии которые участвуют в выборке в CTkOptionMenu
        :var self.selected: Словарь соответствия путь до флага, выбор идеологии
        :var self.open_panel_with_custom_ideologies: Открыто ли меню кастомных идеологий
        :var self.custom_ideologies_list: Список кастомных идеологий (сохраняется с перезаходом в меню)
        :var self.scrollable_frame: Меню кастомных идеологий
        :var self.frames_with_entry_custom_ideologies: Хранит все фрэймы в которых находятся поля для ввода кастомных идеологий, а также кнопка удаления поля
        :var self.ideologies_menus: Массив содержащий в себе объекты поля с кастомными идеологиями
        :var self.frames_with_flags: Содержит все фреймы с флагами и соответствующими CTkOptionMenu
        :var self.list_frames: Содержит список фреймов в которых будут флаги и т.д
        :var self.custom_ideologies_entry_values: Массив хранящий значение всех полей с кастомными идеологиями
        """
        super().__init__()
        self.geometry(f"{WEIGHT_APP}x{HEIGHT_APP}")
        self.resizable(False, False)
        self.title("Создатель флагов")
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Атрибуты
        self.correct_tag: bool = False
        self.correct_ideologies = True
        self.folder_path: Optional[str] = None
        self.flags_folder_path: Optional[str] = None
        self.ideology: dict = {0: "fascism", 1: "communism", 2: "neutrality", 3: "democratic"}
        self.selected: dict = {}
        self.open_panel_with_custom_ideologies: customtkinter.BooleanVar = customtkinter.BooleanVar(value=False)
        self.custom_ideologies_list: list[str] = []
        self.scrollable_frame: Optional[customtkinter.CTkFrame] = None
        self.frames_with_entry_custom_ideologies: list = []
        self.ideologies_menus: list = []
        self.frames_with_flags: list = []
        self.list_frames: list = []

        # Компоненты
        # Пустой фрэйм где будут флаги
        self.frame_ideology = customtkinter.CTkFrame(self)
        self.frame_ideology.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.frame_ideology.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame_ideology.rowconfigure((0, 1), weight=1)

        self.topbar = customtkinter.CTkFrame(self, fg_color='transparent')
        self.topbar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.topbar.columnconfigure((0, 1, 2), weight=1)
        self.topbar.rowconfigure(0, weight=1)

        self.button_open_folder = customtkinter.CTkButton(
                self.topbar,
                text='Открыть папку с флагами',
                command=self.open_folder,
                fg_color='grey',
                hover_color=C_DGREY
        )
        self.button_open_folder.grid(row=0, column=0, sticky="w")

        # ТЭГ страны
        self.choose_tag = customtkinter.CTkEntry(self.topbar, placeholder_text='тэг', width=50, border_color=C_DGREY)
        self.choose_tag.grid(row=0, column=1)
        self.choose_tag.bind("<KeyRelease>", self.validate_tag)

        self.choose_tag_tt = CTkToolTip(self.choose_tag, message='На англ.\nДлина = 3', bg_color=C_DGREY)

        self.button_open_flags_folder = customtkinter.CTkButton(
                self.topbar,
                text='Открыть папку flags',
                command=self.open_folder_flags,
                fg_color='grey',
                hover_color=C_DGREY
        )
        self.button_open_flags_folder.grid(row=0, column=2, sticky="e")

        self.check_custom_ideologies = customtkinter.CTkCheckBox(
                self,
                text='Кастомные идеологии?',
                command=self.open_panel_custom_ideologies,
                variable=self.open_panel_with_custom_ideologies,
                state='disabled'
        )
        self.check_custom_ideologies.grid(row=2, column=0, padx=10, pady=(0, 10))

        # Кнопка start
        self.start = customtkinter.CTkButton(
                self,
                text='Начать',
                state='disabled',
                fg_color='grey',
                command=self.start,
        )
        self.start.grid(row=4, column=0, padx=10, pady=(0, 10))

    @property
    def custom_ideologies_entry_values(self) -> list:
        output = [
            frame.children.get('!ctkentry').get()
            for frame in self.frames_with_entry_custom_ideologies
        ]

        filtered_output = [
            value for value in output
            if value and all(char.isascii() for char in value)
        ]

        if filtered_output:
            self.correct_ideologies = True
        else:
            self.correct_ideologies = False

        return filtered_output

    def validate_tag(self, event):
        """
        Проверяет корректность введенного тэга.
        """
        tag = self.choose_tag.get().upper()
        if len(tag) == 0:
            self.choose_tag.configure(border_color=C_DGREY)
            self.choose_tag_tt.configure(bg_color=C_DGREY, message='На англ.\nДлина = 3')
            self.correct_tag = False
        elif len(tag) != 3 or not re.match("^[A-Za-z]+$", tag):
            self.choose_tag.configure(border_color='red')
            self.choose_tag_tt.configure(bg_color='red', message='На англ.\nДлина = 3')
            self.correct_tag = False
        else:
            self.choose_tag.configure(border_color='green')
            self.choose_tag_tt.configure(bg_color='green', message='На англ.\nДлина = 3')
            self.correct_tag = True
        self.check_start_button_state()

    def open_folder(self):
        """
        Открывает диалог для выбора папки с флагами.
        Загружает изображения, если папка валидна.
        """
        self.folder_path: str = filedialog.askdirectory(title='Выберете папку с флагами')
        if self.folder_path:
            if any(frame.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tga')) for frame in os.listdir(self.folder_path)):
                load = self.load_flags(self.folder_path)
            if load:
                self.button_open_folder.configure(fg_color=C_BLUE)
                self.check_custom_ideologies.configure(state='normal')
                self.check_start_button_state()
            else:
                pass
        else:
            self.folder_path = ''
            self.button_open_folder.configure(fg_color='red', text='Папка не выбрана!')
            self.button_open_folder.update()
            time.sleep(1)
            self.check_custom_ideologies.configure(state='disabled')
            self.button_open_folder.configure(fg_color='grey', text='Открыть папку с флагами')

    def open_folder_flags(self):
        """
        Открывает диалог для выбора папки 'flags'.
        Проверяет, соответствует ли папка нужному названию.
        """
        path = filedialog.askdirectory(title='Выберете папку с флагами')
        if path:
            self.flags_folder_path = os.path.join(path, 'flags')
            self.button_open_flags_folder.configure(fg_color=C_BLUE)
            self.check_start_button_state()
        else:
            self.button_open_flags_folder.configure(fg_color='red', text='Папка не выбрана!')
            self.button_open_flags_folder.update()
            time.sleep(1)
            self.button_open_flags_folder.configure(fg_color='grey', text='Открыть папку flags')

    def load_flags(self, path) -> Optional[bool]:
        """
        Загружает изображения из выбранной папки и инициализирует элементы интерфейса для выбора идеологий.

        :param path: Путь к папке с изображениями флагов.
        """
        if self.list_frames:
            for frame in self.list_frames:
                frame.grid_forget()
            self.list_frames.clear()
            self.selected.clear()
            self.frames_with_flags.clear()
            self.ideologies_menus.clear()
            self.choose_tag.update()
            self.choose_tag.delete(0, len(self.choose_tag.get()))
            self.flags_folder_path = None
        images = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tga'))]
        num_flags = len(images)

        if num_flags >= 11:
            self.list_frames.clear()
            CTkMessagebox(title='Ошибка', message='На данный момент доступно не более 10 флагов за раз!')
            return None

        # Frame с идеологиями
        for v in range(num_flags + (5 // num_flags)):
            self.fi = customtkinter.CTkFrame(self.frame_ideology)
            self.fi.grid(row=v // 5, column=v % 5, padx=5, pady=(5, 5))
            self.fi.columnconfigure(0, weight=1)
            self.fi.rowconfigure(0, weight=1)
            self.fi.rowconfigure(1, weight=1)
            self.list_frames.append(self.fi)

        if len(self.list_frames) >= 6:
            self.geometry(f'{WEIGHT_APP}x{HEIGHT_APP + 50}')
        else:
            self.geometry(f'{WEIGHT_APP}x{HEIGHT_APP}')

        for i in range(len(self.list_frames)):
            image_index = i if num_flags > i else None

            flag_frame = customtkinter.CTkFrame(self.list_frames[i])
            flag_frame.grid(column=0, row=0)

            if image_index is not None:
                open_image = customtkinter.CTkImage(Image.open(os.path.join(path, images[image_index])), size=(110, 70))
                flag_label = customtkinter.CTkLabel(flag_frame, image=open_image, text='')
                flag_label.grid(column=0, row=0)

                delete_button = customtkinter.CTkButton(
                        flag_frame,
                        text='✖',
                        command=lambda frame=flag_frame, index=i: self.remove_flag(frame, index),
                        width=30,
                        height=30,
                        fg_color='red',
                        state='normal'
                )
                # События для кнопки (наведение и выход)
                flag_label.bind("<Enter>", lambda e, btn=delete_button: btn.grid(row=0, column=0))
                flag_label.bind("<Leave>", lambda e, btn=delete_button: btn.grid_remove())
                delete_button.bind("<Enter>", lambda e, btn=delete_button: btn.grid(row=0, column=0))
                ideology_menu = customtkinter.CTkOptionMenu(
                        flag_frame,
                        command=lambda value, index=i: self.on_ideology_select(index, value),
                        values=list(self.ideology.values())
                )
                ideology_menu.set(list(self.ideology.values())[0])
                self.selected[i] = []
                massiv = self.selected[i]
                massiv.append(os.path.join(path, images[image_index]))
                massiv.append(ideology_menu.get())
                ideology_menu.grid(row=1, column=0, padx=5, pady=(5, 5))
                self.ideologies_menus.append(ideology_menu)
                self.frames_with_flags.append(flag_frame)

            else:
                placeholder_label = customtkinter.CTkLabel(flag_frame, image=None, text='(флага нет)')
                placeholder_label.grid(column=0, row=0)
                ideology_menu = customtkinter.CTkOptionMenu(
                        flag_frame,
                        values=list(self.ideology.values()),
                        state='disabled'
                )
                ideology_menu.set('')
                ideology_menu.grid(row=1, column=0, padx=5, pady=(5, 5))
        return True

    def remove_flag(self, frame: customtkinter.CTkFrame, first_index: int):
        """
        Удаляет флаг из списка и очищает соответствующую ячейку интерфейса.
        """
        index = self.frames_with_flags.index(frame)

        current_frame: customtkinter.CTkFrame = self.frames_with_flags[index]
        current_frame_children: customtkinter.CTkFrame.children = current_frame.children

        flag: customtkinter.CTkLabel = current_frame_children.get('!ctklabel')
        flag.configure(image=None, text='(флага нет)')
        flag.unbind("<Enter>")
        flag.unbind("<Leave>")
        flag.grid(column=0, row=0)

        optionmenu: customtkinter.CTkOptionMenu = current_frame_children.get('!ctkoptionmenu')
        optionmenu.set('')
        optionmenu.configure(state='disabled')
        optionmenu.grid(row=1, column=0, padx=5, pady=(5, 5))

        button: customtkinter.CTkButton = current_frame_children.get('!ctkbutton')
        button.destroy()

        self.frames_with_flags.pop(index)
        self.ideologies_menus.pop(index)
        self.selected.pop(first_index)

        for frames in range(index, len(self.frames_with_flags)):
            try:
                next_frame = self.list_frames[frames + 1]
                next_frame_position = next_frame.grid_info().get('column')
                current_frame = self.list_frames[frames]
                current_frame_position = current_frame.grid_info().get('column')
                current_frame.grid(column=next_frame_position)
                next_frame.grid(column=current_frame_position)
            except IndexError:
                print('Пропущено!')
        self.list_frames.pop(index)

        self.check_start_button_state()

    def on_ideology_select(self, frame_index, selected_values):
        """
        Обрабатывает выбор идеологии для конкретного флага.

        :param frame_index: Индекс фрейма, соответствующий выбранному флагу.
        :param selected_values: Выбранная идеология.
        """
        massiv = self.selected[frame_index]
        massiv.pop(1)
        massiv.append(selected_values)
        self.check_start_button_state()

    def open_panel_custom_ideologies(self):
        """
        Открывает или закрывает панель кастомных идеологий в зависимости от состояния чекбокса.
        """
        if self.open_panel_with_custom_ideologies.get():
            if len(self.list_frames) >= 6:
                self.geometry(f'{WEIGHT_APP}x{HEIGHT_APP + 300}')
            else:
                self.geometry(f"{WEIGHT_APP}x{HEIGHT_APP + 200}")
            if not self.scrollable_frame:  # Создаем фрейм только один раз
                self.scrollable_frame = customtkinter.CTkFrame(self)
                self.scrollable_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
                self.scrollable_frame.columnconfigure(2, weight=1)
                self.scrollable_frame.columnconfigure(3, weight=1)
                self.scrollable_frame.rowconfigure(0, weight=1)
                self.scrollable_frame.rowconfigure(1, weight=1)
                for entry_frame in self.frames_with_entry_custom_ideologies:
                    entry_frame.grid_forget()
                self.frames_with_entry_custom_ideologies.clear()
                for ideology in BASE_IDEOLOGY:
                    self.create_ideology_entry(ideology)

        else:
            if len(self.list_frames) >= 6:
                self.geometry(f'{WEIGHT_APP}x{HEIGHT_APP + 50}')
            else:
                self.geometry(f"{WEIGHT_APP}x{HEIGHT_APP}")
            if self.scrollable_frame:
                self.scrollable_frame.grid_forget()
                self.scrollable_frame = None
                for entry_frame in self.frames_with_entry_custom_ideologies:
                    entry_frame.grid_forget()
                self.update_ideology_menus(base=True)

    def create_ideology_entry(self, initial_text: str) -> None:
        # Создаем новый фрейм для группы элементов
        frame = customtkinter.CTkFrame(self.scrollable_frame)
        frame.grid(row=len(self.frames_with_entry_custom_ideologies) % 5, column=len(self.frames_with_entry_custom_ideologies) // 5, padx=5, pady=5)

        entry = customtkinter.CTkEntry(frame, corner_radius=0)
        entry.configure()
        entry.insert(0, initial_text)
        entry.grid(row=0, column=0, padx=(0, 5))

        entry_tt = CTkToolTip(entry, message='На английском!\nНе < 1 символа', bg_color=C_DGREY)

        entry.bind("<KeyRelease>", command=lambda event: self.validate_ideology(entry=entry, tooltip=entry_tt))
        entry.bind("<KeyRelease>", command=self.update_ideology_menus)

        remove_button = customtkinter.CTkButton(
                frame,
                text='-',
                command=lambda: self.remove_entry(frame),
                width=30,
                fg_color='red',
                font=('CTkFont', 24),
                corner_radius=0
        )
        remove_button.grid(row=0, column=1)
        self.frames_with_entry_custom_ideologies.append(frame)
        self.update_add_button()

    def remove_entry(self, frame_to_remove):
        if frame_to_remove in self.frames_with_entry_custom_ideologies:
            frame_to_remove.grid_forget()
            ideology_remove = frame_to_remove.children.get('!ctkentry').get()
            for menu in self.ideologies_menus:
                if menu.get() == ideology_remove:
                    menu.set('')
            for select in self.selected.values():
                if select[1] == ideology_remove:
                    select[1] = ''
            self.frames_with_entry_custom_ideologies.remove(frame_to_remove)

            print(len(self.selected))
            for i in range(len(self.frames_with_entry_custom_ideologies)):
                row = i % 5
                column = i // 5
                self.frames_with_entry_custom_ideologies[i].grid(row=row, column=column, padx=5, pady=5)

            # Обновляем кнопку добавления
            self.update_add_button()
            self.update_ideology_menus()

    def update_add_button(self):
        # Удаляем существующую кнопку +
        for widget in self.scrollable_frame.grid_slaves():
            if isinstance(widget, customtkinter.CTkButton) and widget.cget("text") == '+':
                widget.grid_forget()
                break

        if len(self.frames_with_entry_custom_ideologies) < len(self.selected):
            add_button_row = len(self.frames_with_entry_custom_ideologies) % 5
            add_button_column = len(self.frames_with_entry_custom_ideologies) // 5
            add_button = customtkinter.CTkButton(
                    self.scrollable_frame,
                    text='+',
                    command=lambda: self.create_ideology_entry('')
            )
            add_button.grid(row=add_button_row, column=add_button_column, padx=5, pady=5)

    def validate_ideology(self, entry: customtkinter.CTkEntry, tooltip: CTkToolTip):
        if len(entry.get()) == 0:
            entry.configure(border_color=C_DGREY)
            tooltip.configure(bg_color=C_DGREY, message='На английском!\nНе < 1 символа')
            self.correct_ideologies = False
        elif not re.match("^[A-Za-z_]+$", entry.get()):
            entry.configure(border_color='red')
            tooltip.configure(bg_color='red', message='На английском!\nНе < 1 символа')
            self.correct_ideologies = False
        else:
            entry.configure(border_color='green')
            tooltip.configure(bg_color='green', message='На английском!\nНе < 1 символа')
            self.correct_ideologies = True

    def update_ideology_menus(self, event=None, base=False):
        """
        Обновляет меню выбора идеологий на основе введенных кастомных значений.
        """
        if base:
            new_values = BASE_IDEOLOGY.copy()
        else:
            new_values = self.custom_ideologies_entry_values
            self.custom_ideologies_list = new_values
        for menu in self.ideologies_menus:
            menu.configure(values=new_values)
            if base:
                menu.set(new_values[0])
        self.check_start_button_state()

    def check_start_button_state(self):
        """
        Проверяет состояние кнопки 'Начать' и активирует её, если все условия выполнены.
        """
        if self.folder_path and self.flags_folder_path and self.correct_tag and all(
                select[0] and select[1] for select in self.selected.values()
        ) and self.correct_ideologies:
            self.start.configure(state='normal', fg_color=C_BLUE)
        else:
            self.start.configure(state='disabled', fg_color='gray')
        print(
                f'folder_path: {bool(self.folder_path)}\nflags_folder_path: {bool(self.flags_folder_path)}\ncorrect_tag: {self.correct_tag}\ncorrect_ideologies: {self.correct_ideologies}\nall_selected: {all(self.selected.values())}\n{'-' * 10}\nSelected:\n{list(self.selected.values())}\n{'-' * 30}'
        )

    def start(self):
        """
        Запускает процесс создания флагов на основе выбранных изображений и идеологий.
        Сохраняет изображения в соответствующие директории.
        """
        if not os.path.basename(self.flags_folder_path) == 'flags':
            os.makedirs(self.flags_folder_path, exist_ok=True)
        for select in self.selected.values():
            image_path = select[0]
            select_ideology = select[1]
            tag = self.choose_tag.get().upper()
            base_name = f'{tag}_{select_ideology}'

            for i, size in enumerate(SIZES, start=1):
                with Image.open(image_path) as image:
                    if i == 1:
                        ready_image = os.path.join(self.flags_folder_path, f'{base_name}.tga')
                    elif i == 2:
                        ready_image = os.path.join(self.flags_folder_path, f'medium//{base_name}.tga')
                    elif i == 3:
                        ready_image = os.path.join(self.flags_folder_path, f'small//{base_name}.tga')

                    os.makedirs(os.path.dirname(ready_image), exist_ok=True)
                    _ = sum(1 for file in os.listdir(os.path.dirname(ready_image)) if file.startswith(base_name))
                    if _ != 0:
                        ready_image = f"{ready_image.rsplit('.', 1)[0]} ({_}).tga"
                    image.resize(size).save(ready_image)
        os.startfile(self.flags_folder_path)


if __name__ == '__main__':
    app = App()
    app.mainloop()
