import os
from time import sleep
from tkinter import filedialog

import customtkinter
import loc

customtkinter.set_appearance_mode("System")


class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x175")
        self.resizable(False, False)
        self.title("Помощник локализации")
        self.attributes('-topmost', True)  # закрепить наверху
        self.mode = customtkinter.IntVar(value=1)

        self.chance_file = customtkinter.CTkFrame(self, fg_color='transparent')
        self.chance_file.grid(column=0, row=0, padx=20, pady=10, sticky='ew')
        self.chance_file.grid_columnconfigure((0, 1), weight=1)

        self.setting_frame = customtkinter.CTkFrame(self)
        self.setting_frame.grid(row=1, column=0)

        self.window_with_file = customtkinter.CTkEntry(master=self.chance_file, width=400, placeholder_text='Введите путь к файлу', corner_radius=0)
        self.window_with_file.grid(row=0, column=0, sticky='e')

        self.clipboard = customtkinter.CTkButton(master=self.chance_file, text='Вставить', command=self.btn_clip, width=60, corner_radius=0)
        self.clipboard.grid(row=0, column=0, sticky='e')

        self.btn_open = customtkinter.CTkButton(master=self.chance_file, text='Найти файл', command=self.open_file, corner_radius=0)
        self.btn_open.grid(row=0, column=1, padx=(15, 0))

        # настройки
        self.chance_mode1 = customtkinter.CTkRadioButton(self.setting_frame, variable=self.mode, value=1, text='Авто-локализация', state='disabled')
        self.chance_mode1.grid(row=1, column=0, padx=10, pady=(10, 5), sticky='w')
        self.chance_mode2 = customtkinter.CTkRadioButton(self.setting_frame, variable=self.mode, value=2, text='Сделать заготовку', state='disabled')
        self.chance_mode2.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='w')

        self.need_zero = customtkinter.BooleanVar(value=False)
        self.check_zero = customtkinter.CTkCheckBox(
                self.setting_frame, text='Вставлять ли "0"?', variable=self.need_zero, onvalue=True, offvalue=False,
                state='disabled'
        )
        self.check_zero.grid(row=1, column=1, pady=(10, 5), padx=10, sticky='w')

        self.need_space = customtkinter.BooleanVar(value=False)
        self.check_space = customtkinter.CTkCheckBox(
                self.setting_frame, text='Вставлять ли пробелы?', variable=self.need_space, onvalue=True,
                offvalue=False, state='disabled'
        )
        self.check_space.grid(row=2, column=1, pady=(5, 10), padx=10, sticky='w')

        self.btn_start = customtkinter.CTkButton(self, text='Начать', command=self.start, state='disabled', width=354)
        self.btn_start.grid(row=2, column=0, pady=10)

    def open_file(self):
        global input_file
        possible_file = self.window_with_file.get().replace('"', '').strip()
        if possible_file == '':
            input_file = filedialog.askopenfilename(title='Выберете файл для локализации', filetypes=[('Файл hoi4', '*.txt')])
            if input_file == '':
                self.window_with_file.configure(placeholder_text='Файл не выбран!', placeholder_text_color='red3')
                self.update()
                sleep(2)
                self.window_with_file.configure(placeholder_text='Введите путь к файлу', placeholder_text_color=('gray52', 'gray62'))
            elif os.path.isfile(input_file):
                self.window_with_file.insert(0, input_file)
                self.chance_mode1.configure(state='normal')
                self.chance_mode2.configure(state='normal')
                self.check_zero.configure(state='normal')
                self.check_space.configure(state='normal')
                self.btn_start.configure(state='normal')
            else:
                self.chance_mode1.configure(state='disabled')
                self.chance_mode2.configure(state='disabled')
                self.check_zero.configure(state='disabled')
                self.check_space.configure(state='disabled')
                self.btn_start.configure(state='disabled')
                self.window_with_file.delete(0, 1000)
                self.window_with_file.configure(placeholder_text='Файл не существует!', placeholder_text_color='red3')
                self.update()
                sleep(2)
                self.window_with_file.configure(placeholder_text='Введите путь к файлу', placeholder_text_color=('gray52', 'gray62'))
        elif os.path.isfile(possible_file):
            input_file = possible_file
            self.window_with_file.insert(0, input_file)
            self.chance_mode1.configure(state='normal')
            self.chance_mode2.configure(state='normal')
            self.check_zero.configure(state='normal')
            self.check_space.configure(state='normal')
            self.btn_start.configure(state='normal')
        else:
            self.chance_mode1.configure(state='disabled')
            self.chance_mode2.configure(state='disabled')
            self.check_zero.configure(state='disabled')
            self.check_space.configure(state='disabled')
            self.btn_start.configure(state='disabled')
            self.window_with_file.delete(0, 1000)
            self.window_with_file.configure(placeholder_text='Файл не существует!', placeholder_text_color='red3')
            self.update()
            sleep(2)
            self.window_with_file.configure(placeholder_text='Введите путь к файлу', placeholder_text_color=('gray52', 'gray62'))
            self.focus()

    def btn_clip(self):
        clip_text = self.clipboard_get()
        self.window_with_file.insert(0, clip_text)

    def start(self):
        loc.work(self.mode.get(), self.need_zero.get(), self.need_space.get(), input_file)


if __name__ == '__main__':
    app = Gui()
    app.mainloop()
