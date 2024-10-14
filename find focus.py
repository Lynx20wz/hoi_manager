import sys
import customtkinter
import keyboard
import subprocess

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.attributes('-disabled')
        self.geometry("600x50")
        self.title("Найти фокус")
        # self.withdraw()
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=0)

        self.entry_field = customtkinter.CTkEntry(self, 500, 30, 10, placeholder_text="Введите название фокуса", )
        self.entry_field.grid(row=2, column=0   , padx=(25,10), pady=10,)

        self.btn = customtkinter.CTkButton(self, 25, 30, 10, text='Найти')
        self.btn.grid(row=2, column=1, padx = 5)

    def hk(self):
        self.deiconify()
        self.focus()


app = App()
keyboard.add_hotkey("alt+d", lambda: app.hk())
app.mainloop()