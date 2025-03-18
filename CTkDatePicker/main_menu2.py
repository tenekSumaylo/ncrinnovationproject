from customtkinter import *
from CTkDatePicker import CTkDatePicker

#from PIL import Image

class MainMenu:
    def __init__(self, root):
        self.root = root

        #main buttons
        self.lab_inventory = CTkLabel(self.root, text='NCR Laboratory Inventory System',font=("Sora", 30))
        self.borrow_button = CTkButton(self.root, text='Borrow', font=("Sora", 15, "bold"),height=100,width=190, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.borrow_pressed)
        self.return_button = CTkButton(self.root, text='Return', font=("Sora", 15, "bold"),height=100,width=190, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.return_pressed)
        self.user_info_button = CTkButton(self.root, text='User Information', font=("Sora", 15, "bold"),height=100,width=190, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.user_info_pressed)
        self.admin_button = CTkButton(self.root, text='Admin', font=("Sora", 15, "bold"),height=100,width=190, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.admin_pressed)


        #back buttons
        self.main_back = CTkButton(self.root, text='Back to Menu', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", border_width=2,width=50,height=40,command=self.go_to_main)
        self.borrow_back = CTkButton(self.root, text='Back',font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", border_width=2,width=50,height=40,command=self.show_borrow_selection_menu)
        self.return_back = CTkButton(self.root, text='Back', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", border_width=2,width=50,command=self.remove_back_buttons)
        self.user_info_back = CTkButton(self.root, text='Back', font=("Sora", 15, "bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", border_width=2,width=50,command=self.remove_back_buttons)
        self.admin_back = CTkButton(self.root, text='Back', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=32, border_color="#4CAF50", border_width=2,width=50,height=40, command=self.show_admin_selection_menu)
        self.admin_main_back = CTkButton(self.root, text='Back', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=32, border_color="#4CAF50", border_width=2,width=50, height=40, command=self.show_admin_menu)

        #borrow_buttons
        # first part buttons and labels
        self.borrow_scan_id = CTkLabel(self.root, text='Scan your ID', font=("Sora", 30))
        self.borrow_scan_entry = CTkEntry(self.root, width=300)
        self.borrow_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50",command=self.show_borrow_selection_menu)

        self.borrow_keys = CTkButton(self.root, text='Keys', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50",command=self.show_borrow_menu)
        self.borrow_tools = CTkButton(self.root, text='Tools', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=32, border_color="#4CAF50",command=self.show_borrow_menu)

        # second part main function
        self.borrow_items = CTkLabel(self.root, text='Scan the items you want to borrow')
        self.borrow_entry = CTkEntry(self.root, width=150)
        self.borrow_submit = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50",command=self.borrow_add_entry)
        self.borrow_continue = CTkButton(self.root, text='Continue', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50",command=self.borrow_end)
        self.borrow_text = CTkTextbox(self.root, width=250, height=180)

        # End part
        self.borrow_end_text = CTkLabel(self.root, text='Thank you!, Please return the items soon', font=("Sora", 20))

        self.borrow_entry.bind('<Return>', self.borrow_add_entry)



        #return_buttons
        #first part
        self.return_scan_id = CTkLabel(self.root, text='Scan your ID', font=("Sora", 30))
        self.return_scan_entry = CTkEntry(self.root, width=300)
        self.return_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50",command=self.show_return_menu)

        # second part main function
        self.return_items = CTkLabel(self.root, text='What would you like to return?', font=("Sora", 30))
        self.return_items_entry = CTkEntry(self.root, width=150, placeholder_text='Enter Borrowed items')
        self.return_drop_box = CTkComboBox(self.root, values=["Select an Option","Borrow Log 1","Borrow Log 2","Borrow Log 3", "Borrow Log 4", "Borrow Log 5"], width=300, height=30,command=self.show_return_borrow_logs)
        self.return_borrow_list = CTkTextbox(self.root, width=300, height=180)
        self.return_to_return_list = CTkTextbox(self.root, width=300, height=180)
        self.return_continue = CTkButton(self.root, text='Continue',font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50",command=self.return_end)

        # End part
        self.return_end_text = CTkLabel(self.root, text='Thank you for returning the items!', font=("Sora", 30))



        #User Info Buttons
        #first part
        self.user_info_main = CTkLabel(self.root, text = 'NCR Key-Tool Logging User Information', font=("Sora", 30))
        self.user_info_search = CTkButton(self.root, text='Search',font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", command=self.show_user_info_search_menu)
        self.user_info_register = CTkButton(self.root, text='Register', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50",command=self.show_user_info_register_menu)

        #search part
        self.user_info_search_label = CTkLabel(self.root, text='Enter your QLID or RFID', font=("Sora", 30))
        self.user_info_search_entry = CTkEntry(self.root, width=150)
        self.user_info_search_submit = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", command=self.show_user_info_credentials)

        self.user_info_search_query = CTkLabel(self.root, text=f'Name: {"Name"}\n QLID: {"QLID"}\n RFID: {"RFID"}\n Status: {"Status"}')
        self.user_info_toggle_status = CTkButton(self.root, text='Toggle Status', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50")#command=add command here

        #register part
        self.user_info_register_label =CTkLabel(self.root, text='Register your details below')

        self.user_info_register_first_name_label= CTkLabel(self.root,text='First Name:')
        self.user_info_register_first_name_entry = CTkEntry(self.root, width=150)

        self.user_info_register_last_name_label= CTkLabel(self.root, text='Last Name: ')
        self.user_info_register_last_name_entry = CTkEntry(self.root, width=150)

        self.user_info_register_qlid_label = CTkLabel(self.root, text='Enter your QLID')
        self.user_info_register_qlid_entry = CTkEntry(self.root, width=150)

        self.user_info_register_rfid_label = CTkLabel(self.root, text='Enter your RFID')
        self.user_info_register_rfid_entry = CTkEntry(self.root, width=150)

        self.user_info_register_submit_label = CTkLabel(self.root, text='User registered!', font=("Sora", 30))
        self.user_info_register_submit = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", command= self.user_registered_end)



        #Admin part
        #first part
        self.admin_scan_id = CTkLabel(self.root, text='Admin Password', font=("Sora", 30))
        self.admin_scan_entry = CTkEntry(self.root, width=300)
        self.admin_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32, border_color="#4CAF50",command=self.show_admin_menu)


        self.admin_label = CTkLabel(self.root, text='Admin configurations', font=('Sora', 30))
        self.admin_register_item_button = CTkButton(self.root, text='Register New Item', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", command=self.show_admin_selection_menu)
        self.admin_log_reports_button = CTkButton(self.root, text="Logs and Reports", font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50") #command


        #Register Item part
        self.admin_item_label = CTkLabel(self.root, text='What would you like to register?', font=('Sora', 30))
        self.admin_keys = CTkButton(self.root, text='Keys', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=32,border_color="#4CAF50", command=self.admin_register_key_menu)
        self.admin_tools = CTkButton(self.root, text='Equipment', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=32, border_color="#4CAF50", command=self.admin_register_tool_menu)

        self.admin_item_frame = CTkFrame(master=root, border_color="#004E42", border_width=2, width=250, height=400)
        self.admin_item_tool_frame = CTkFrame(master=root, border_color="#004E42", border_width=2, width=550, height=400)


        #Key part
        self.admin_item_key_ID_label = CTkLabel(master=self.admin_item_frame, text='Key ID:', font=('Sora', 15))
        self.admin_item_key_ID_entry = CTkEntry(master=self.admin_item_frame, width=200)
        self.admin_item_key_ID_barcode = CTkLabel(master=self.admin_item_frame, text='Barcode:', font=('Sora', 15))
        self.admin_item_key_ID_barcode_entry = CTkEntry(master=self.admin_item_frame, width=200)
        self.admin_item_key_ID_description = CTkLabel(master=self.admin_item_frame, text='Description', font=('Sora', 15))
        self.admin_item_key_ID_description_box = CTkTextbox(master=self.admin_item_frame, width=200, height=180)

        self.admin_item_key_ID_submit = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=32, border_color="#4CAF50",command=self.show_key_register_end)
        self.admin_item_key_end = CTkLabel(self.root, text='Key registered!', font=("Sora", 30))

        #Tool part
        self.admin_item_tool_ID_name = CTkLabel(master=self.admin_item_tool_frame, text='Equipment Name:', font=('Sora', 15))
        self.admin_item_tool_ID_name_entry = CTkEntry(master=self.admin_item_tool_frame, width=200)
        self.admin_item_tool_ID_label = CTkLabel(master=self.admin_item_tool_frame, text='Unit ID:', font=('Sora', 15))
        self.admin_item_tool_ID_entry = CTkEntry(master=self.admin_item_tool_frame, width=200)
        self.admin_item_tool_ID_barcode = CTkLabel(master=self.admin_item_tool_frame, text='Barcode:', font=('Sora', 15))
        self.admin_item_tool_ID_barcode_entry = CTkEntry(master=self.admin_item_tool_frame, width=200)
        self.admin_item_tool_ID_description = CTkLabel(master=self.admin_item_tool_frame, text='Description',font=('Sora', 15))
        self.admin_item_tool_ID_description_box = CTkTextbox(master=self.admin_item_tool_frame, width=500, height=80)

        self.admin_item_tool_ID_date_acquired = CTkLabel(master=self.admin_item_tool_frame, text='Unit ID:', font=('Sora', 15))
        self.admin_item_tool_ID_date_acquired_calendar = CTkDatePicker(self.root)
        self.admin_item_tool_ID_date_calibrated = CTkLabel(master=self.admin_item_tool_frame, text='Barcode:',font=('Sora', 15))
        self.admin_item_tool_ID_date_calibrated_calendar = CTkDatePicker(self.root)


        self.admin_item_tool_ID_submit = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"),hover_color="#4CAF50", fg_color="#004E42", corner_radius=32,border_color="#4CAF50", command=self.show_tool_register_end)
        self.admin_item_tool_end = CTkLabel(self.root, text='Equipment registered!', font=("Sora", 30))

        #################################################################################################################################################################################################

        #UI Start program
        self.show_main_buttons()


    #Clear screen and entries
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.place_forget()

        self.admin_item_frame.grid_forget()

    def clear_all_entry(self):
        self.borrow_text.delete("1.0", END)
        self.borrow_scan_entry.delete(0, 'end')
        self.borrow_entry.delete(0, 'end')

        self.return_scan_entry.delete(0, 'end')
        self.return_items_entry.delete(0,'end')
        self.return_borrow_list.delete("1.0", END)
        self.return_to_return_list.delete("1.0", END)

        self.user_info_search_entry.delete(0, 'end')
        self.user_info_register_first_name_entry.delete(0, 'end')
        self.user_info_register_last_name_entry.delete(0, 'end')
        self.user_info_register_qlid_entry.delete(0, 'end')
        self.user_info_register_rfid_entry.delete(0, 'end')

        self.admin_item_key_ID_entry.delete(0, 'end')
        self.admin_item_key_ID_barcode_entry.delete(0, 'end')
        self.admin_item_key_ID_description_box.delete("1.0", END)

#################################################################################################################################################################################################

    #Main menu functions
    def show_main_buttons(self):
        self.lab_inventory.place(relx=0.5, rely=0.2, anchor='center')
        self.show_borrow_button()
        self.show_return_button()
        self.show_user_info_button()
        self.show_admin_button()

    ##still needs edit
    def borrow_pressed(self):
        self.clear_window()

        self.show_main_back()
        self.show_borrow_id_menu()

    def return_pressed(self):
        self.clear_window()

        self.show_main_back()
        self.show_return_id_menu()

    def user_info_pressed(self):
        self.clear_window()

        self.show_main_back()
        self.show_user_info_menu()

    def admin_pressed(self):
        self.clear_window()

        self.show_main_back()
        self.show_admin_login()

    def show_borrow_button(self):
        self.borrow_button.place(relx=0.35, rely=0.4, anchor="center")  # use this line to change position of button

    def show_return_button(self):
        self.return_button.place(relx=0.65, rely=0.4, anchor="center")  # use this line to change position of button

    def show_user_info_button(self):
        self.user_info_button.place(relx=0.35, rely=0.6, anchor="center")  # use this line to change position of button

    def show_admin_button(self):
        self.admin_button.place(relx=0.65, rely=0.6, anchor="center")  # use this line to change position of button

    #End of Main menu Functions

#################################################################################################################################################################################################

    #Back Button functions
    def show_main_back (self):
        self.main_back.place(relx=0.15, rely=0.9, anchor="center") #use this line to change position of button

    def go_to_main(self):
        self.clear_window()
        self.clear_all_entry()
        self.show_main_buttons()

    ###

    def remove_back_buttons(self):
        self.main_back.place_forget()
        self.borrow_back.place_forget()
        self.return_back.place_forget()
        self.user_info_back.place_forget()
    #End of Back Button Functions

#################################################################################################################################################################################################

    #Borrow Section
    def show_borrow_id_menu(self):
        self.borrow_scan_id.place(relx=0.5, rely=0.2, anchor= 'center')
        self.borrow_scan_entry.place (relx=0.5, rely=0.4, anchor= 'center')
        self.borrow_scan_next.place(relx=0.5, rely=0.6, anchor= 'center')

    def show_borrow_selection_menu(self):
        self.clear_window()
        self.show_main_back()

        self.borrow_keys.place(relx=0.4, rely=0.4, anchor= 'center')
        self.borrow_tools.place(relx=0.6, rely=0.4, anchor= 'center')

    def show_borrow_menu(self): # use this command to change position of buttons
        self.clear_window()
        self.clear_all_entry()
        self.remove_back_buttons()
        self.borrow_back.place(relx=0.5, rely=0.8, anchor="center")

        self.borrow_items.place(relx=0.2, rely=0.2, anchor="center")
        self.borrow_entry.place(relx=0.2, rely=0.4, anchor="center")
        self.borrow_submit.place(relx=0.2, rely=0.6, anchor="center")
        self.borrow_text.place(relx=0.75, rely=0.4, anchor="center")
        self.borrow_continue.place(relx=0.65, rely=0.6, anchor='w')

    def borrow_add_entry(self, event=None):
        entry_text = self.borrow_entry.get()
        self.borrow_text.insert('end', entry_text + '\n')
        self.borrow_entry.delete(0,'end')


    def borrow_end(self):
        self.clear_window()
        self.show_main_back()
        self.borrow_end_text.place(relx=0.5, rely=0.4, anchor='center')
    #End of Borrow Section

#################################################################################################################################################################################################

    #Retun Section
    def show_return_id_menu(self):
        self.return_scan_id.place(relx=0.5, rely=0.2, anchor='center')
        self.return_scan_entry.place(relx=0.5, rely=0.4, anchor='center')
        self.return_scan_next.place(relx=0.5, rely=0.6, anchor='center')

    def show_return_menu(self):
        self.clear_window()
        self.show_main_back()

        self.return_items.place(relx=0.5, rely=0.15, anchor='center')
        self.return_items_entry.place(relx=0.16, rely=0.25, anchor='center')
        self.return_drop_box.place(relx=0.5, rely=0.25, anchor='center')
        self.return_borrow_list.place(relx=0.25, rely=0.45, anchor='center')
        self.return_to_return_list.place(relx=0.75, rely=0.45, anchor='center')
        self.return_continue.place(relx=0.5, rely=0.65, anchor='center')

    def show_return_borrow_logs(self, value):
        index = self.return_drop_box._values.index(value)

        if index == 0:
            self.return_borrow_list.delete("1.0",END)
        elif index == 1:
            self.return_borrow_list.delete("1.0",END)
            self.return_borrow_list.insert(END, "1.) Put the Data base stuff here (1)")
        elif index == 2:
            self.return_borrow_list.delete("1.0", END)
            self.return_borrow_list.insert(END, "1.) Put the Data base stuff here (2)")
        elif index == 3:
            self.return_borrow_list.delete("1.0", END)
            self.return_borrow_list.insert(END, "1.) Put the Data base stuff here (3)")
        elif index == 4:
            self.return_borrow_list.delete("1.0", END)
            self.return_borrow_list.insert(END, "1.) Put the Data base stuff here (4)")
        elif index == 5:
            self.return_borrow_list.delete("1.0", END)
            self.return_borrow_list.insert(END, "1.) Put the Data base stuff here (5)")



    def return_end(self):
        self.clear_window()
        self.show_main_back()

        self.return_end_text.place(relx=0.5, rely=0.4, anchor='center')
    #End of Return Section

#################################################################################################################################################################################################

    #User Information Section

    def show_user_info_menu(self):
        self.user_info_main.place(relx=0.5, rely=0.2, anchor='center')
        self.user_info_search.place(relx=0.5, rely=0.4, anchor='center')
        self.user_info_register.place(relx=0.5, rely=0.6, anchor='center')

    def show_user_info_search_menu(self):
        self.clear_window()
        self.show_main_back()

        self.user_info_search_label.place(relx=0.5, rely=0.2, anchor='center')
        self.user_info_search_entry.place(relx=0.5, rely=0.4, anchor='center')
        self.user_info_search_submit.place(relx=0.5, rely=0.6, anchor='center')



    def show_user_info_credentials(self):
        self.clear_window()
        self.show_main_back()

        self.user_info_search_query.place(relx=0.5, rely=0.2, anchor='center')
        self.user_info_toggle_status.place(relx=0.5, rely=0.4, anchor='center')
    def show_user_info_register_menu(self):
        self.clear_window()
        self.show_main_back()

        self.user_info_register_label.place(relx=0.5, rely=0.2, anchor='center')
        self.user_info_register_first_name_label.place(relx=0.5, rely=0.3, anchor='center')
        self.user_info_register_first_name_entry.place(relx=0.5, rely=0.34, anchor='center')

        self.user_info_register_label.place(relx=0.5, rely=0.2, anchor='center')
        self.user_info_register_last_name_label.place(relx=0.5, rely=0.4, anchor='center')
        self.user_info_register_last_name_entry.place(relx=0.5, rely=0.44, anchor='center')

        self.user_info_register_qlid_label.place(relx=0.5, rely=0.5, anchor='center')
        self.user_info_register_qlid_entry.place(relx=0.5, rely=0.54, anchor='center')

        self.user_info_register_rfid_label.place(relx=0.5, rely=0.6, anchor='center')
        self.user_info_register_rfid_entry.place(relx=0.5, rely=0.64, anchor='center')

        self.user_info_register_submit.place(relx=0.5, rely=0.7, anchor= 'center')

    def user_registered_end(self):
        self.clear_window()
        self.show_main_back()

        self.user_info_register_submit_label.place(relx=0.5, rely=0.3, anchor='center')


###############################################################################################################################################################################################################

    def show_admin_login(self):
        self.clear_window()
        self.show_main_back()

        self.admin_scan_id.place(relx=0.5, rely=0.2, anchor='center')
        self.admin_scan_entry.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_scan_next.place(relx=0.5, rely=0.6, anchor='center')

    def show_admin_menu(self):
        self.clear_window()
        self.show_main_back()

        self.admin_label.place(relx=0.5, rely=0.2, anchor='center')
        self.admin_register_item_button.place(relx=0.5,rely=0.4, anchor='center')
        self.admin_log_reports_button.place(relx=0.5, rely=0.6, anchor='center')

    def show_admin_selection_menu(self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')

        self.admin_item_label.place(relx=0.5, rely=0.2, anchor='center')
        self.admin_keys.place(relx=0.4, rely=0.4, anchor='center')
        self.admin_tools.place(relx=0.6, rely=0.4, anchor='center')

    def admin_register_key_menu(self):
        self.clear_window()
        self.clear_all_entry()
        self.remove_back_buttons()
        self.admin_back.place(relx=0.5, rely=0.9, anchor="center")

        self.admin_item_frame.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_item_key_ID_label.place(relx=0.5, rely=0.1, anchor='center')
        self.admin_item_key_ID_entry.place(relx=0.5, rely=0.17, anchor='center')
        self.admin_item_key_ID_barcode.place(relx=0.5, rely=0.25, anchor='center')
        self.admin_item_key_ID_barcode_entry.place(relx=0.5, rely=0.32, anchor='center')
        self.admin_item_key_ID_description.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_item_key_ID_description_box.place(relx=0.5, rely=0.7, anchor='center')
        self.admin_item_key_ID_submit.place(relx=0.5, rely=0.8, anchor='center')

    def show_key_register_end(self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')

        self.admin_item_key_end.place(relx=0.5, rely=0.3, anchor='center')

    def admin_register_tool_menu(self):
        self.clear_window()
        self.clear_all_entry()
        self.remove_back_buttons()
        self.admin_back.place(relx=0.5, rely=0.9, anchor="center")

        self.admin_item_tool_frame.place(relx=0.5, rely=0.4, anchor='center')

        self.admin_item_tool_ID_name.place(relx=0.5, rely=0.1, anchor='center')
        self.admin_item_tool_ID_name_entry.place(relx=0.5, rely=0.17, anchor='center')

        self.admin_item_tool_ID_label.place(relx=0.2, rely=0.25, anchor='center')
        self.admin_item_tool_ID_entry.place(relx=0.2, rely=0.32, anchor='center')

        self.admin_item_tool_ID_barcode.place(relx=0.8, rely=0.25, anchor='center')
        self.admin_item_tool_ID_barcode_entry.place(relx=0.8, rely=0.32, anchor='center')

        self.admin_item_tool_ID_description.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_item_tool_ID_description_box.place(relx=0.5, rely=0.57, anchor='center')
        self.admin_item_tool_ID_submit.place(relx=0.5, rely=0.8, anchor='center')



    def show_tool_register_end(self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')

        self.admin_item_tool_end.place(relx=0.5, rely=0.3, anchor='center')


