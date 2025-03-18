from customtkinter import *

from main_menu2 import MainMenu



root = CTk()
root.title("Laboratory Inventory")
root.geometry("800x600")


set_appearance_mode("light")

main_menu = MainMenu(root)


root.mainloop()