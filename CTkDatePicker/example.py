from customtkinter import *
from CTkDatePicker import CTkDatePicker


class DatePickerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("450x200")
        self.root.title("CTkDatePicker Example")

        self.date_picker = CTkDatePicker(self.root,fg_color="blue", bg_color="black")
        self.date_picker.pack(padx=20, pady=20)
        self.date_picker.set_allow_manual_input(False)


    def run(self):
        self.root.mainloop()



root = CTk()
set_appearance_mode("dark")
app = DatePickerApp(root)
app.run()