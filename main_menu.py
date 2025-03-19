from customtkinter import *
from CTkDatePicker import CTkDatePicker
from CTkMessagebox import CTkMessagebox

import sys
sys.path.append('/home/keyloggerpi/ncr_innovation_project/PythonProject/Hardware_Services')
sys.path.append('/home/keyloggerpi/ncr_innovation_project/PythonProject/Database_Services')
sys.path.append('/home/keyloggerpi/ncr_innovation_project/PythonProject/Models')
import NcrEquipments as ncr_equipments
import NcrKeys as ncr_keys
import NcrEmployees as ncr_employees
import ReturnLogs as ncr_return_logs
import BorrowLogs as ncr_borrow_logs
import HardwareOperations as hardware_operations
import DatabaseOperations as database_operations
from dateutil import parser
from datetime import datetime
from dateutil.parser import ParserError

#from PIL import Image

class MainMenu:
    def __init__(self, root, db_actions, hardware_actions):
        #initialize the root for showing in CTK
        self.root = root
        
        #initialize instance members, ready for dependency injection however this does not support dependency injection
        self.db_actions = db_actions
        self.hardware_actions = hardware_actions
        
        # initialize instance list
        self.to_borrow_dict = {}
        self.return_logs_dict = {}
        self.item_logs_dict = {}
        
        
        # line after this is the initialization of buttons and widgets

        #main buttons
        self.lab_inventory = CTkLabel(self.root, text='NCR Laboratory Inventory System',font=("Sora", 20))
        self.borrow_button = CTkButton(self.root, text='Borrow', font=("Sora", 15, "bold"),height=80,width=170, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.borrow_pressed)
        self.return_button = CTkButton(self.root, text='Return', font=("Sora", 15, "bold"),height=80,width=170, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.return_pressed)
        self.user_info_button = CTkButton(self.root, text='User Information', font=("Sora", 15, "bold"),height=80,width=170, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.user_info_pressed)
        self.admin_button = CTkButton(self.root, text='Admin', font=("Sora", 15, "bold"),height=80,width=170, hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2 ,command=self.admin_pressed)


        #back buttons
        self.main_back = CTkButton(self.root, text='Back to Menu', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=80,height=50,command=self.go_to_main)
        self.borrow_back = CTkButton(self.root, text='Back',font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=80,height=50,command=self.show_borrow_selection_menu)
        self.admin_back = CTkButton(self.root, text='Back', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12, border_color="#4CAF50", border_width=2,width=80,height=50, command=self.show_admin_selection_menu)
        self.admin_main_back = CTkButton(self.root, text='Back', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12, border_color="#4CAF50", border_width=2,width=80, height=50, command=self.show_admin_menu)

        #borrow_buttons
        # first part buttons and labels
        self.borrow_scan_id = CTkLabel(self.root, text='Scan your ID', font=("Sora", 20))
        self.borrow_scan_entry = CTkEntry(self.root, width=280)
        self.borrow_scan_entry.bind('<Return>', lambda event: self.login_authentication(1, event))
        
        self.borrow_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=lambda: self.login_authentication(1))

        self.borrow_keys = CTkButton(self.root, text='Keys', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=lambda: self.show_borrow_menu('keys'))
        self.borrow_tools = CTkButton(self.root, text='Tools', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=lambda: self.show_borrow_menu('equipments'))

        # second part main function
        self.borrow_items = CTkLabel(self.root, text='Scan the items you want to borrow')
        self.borrow_entry = CTkEntry(self.root, width=180)
        self.borrow_submit = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42",  corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=self.borrow_add_entry)
        self.borrow_continue = CTkButton(self.root, text='Continue', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42",  corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=self.borrow_end)
        self.borrow_text = CTkTextbox(self.root, width=250, height=200)

        # End part
        self.borrow_end_text = CTkLabel(self.root, text='Thank you!, Please return the items soon', font=("Sora", 20))

        self.borrow_entry.bind('<Return>', self.borrow_add_entry)


        #return_buttons
        #first part
        self.return_scan_id = CTkLabel(self.root, text='Scan your ID', font=("Sora", 20))
        self.return_scan_entry = CTkEntry(self.root, width=300)
        self.return_scan_entry.bind('<Return>', lambda event: self.login_authentication(2, event))
        
        self.return_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=lambda: self.login_authentication(2))

        # second part main function
        self.return_items = CTkLabel(self.root, text='What would you like to return?', font=("Sora", 20))
        self.return_items_entry = CTkEntry(self.root, width=130, placeholder_text='Enter Borrowed items')
        self.return_drop_box = CTkComboBox(self.root, values=["Select an Option","Borrow Log 1","Borrow Log 2","Borrow Log 3", "Borrow Log 4", "Borrow Log 5"], width=280, height=30,command=self.show_return_borrow_logs)
        self.return_borrow_list = CTkTextbox(self.root, width=300, height=150)
        self.return_to_return_list = CTkTextbox(self.root, width=300, height=150)
        self.return_continue = CTkButton(self.root, text='Continue',font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=self.return_end)
        
        self.return_drop_box.bind( "<<ComboboxSelected>>", self.selected_return_log) # Combobox event for that 
        # End part
        self.return_end_text = CTkLabel(self.root, text='Thank you for returning the items!', font=("Sora", 20))

        #User Info Buttons
        #first part
        self.user_info_main = CTkLabel(self.root, text = 'NCR Key-Tool Logging User Information', font=("Sora", 20))
        self.user_info_search = CTkButton(self.root, text='Search',font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42",corner_radius=12,border_color="#4CAF50", border_width=2,width=120,height=50, command=self.show_user_info_search_menu)
        self.user_info_register = CTkButton(self.root, text='Register', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=120,height=50,command=self.show_user_info_register_menu)

        #search part
        self.user_info_search_label = CTkLabel(self.root, text='Enter your QLID or RFID', font=("Sora", 20))
        self.user_info_search_entry = CTkEntry(self.root, width=200)
        self.user_info_search_submit = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command=self.show_user_info_credentials)

        self.user_info_search_name = CTkLabel(self.root, text='Name:')
        self.user_info_search_name_box = CTkTextbox(self.root, width=300, height=10)
        self.user_info_search_qlid = CTkLabel(self.root, text='QLID:', height=10)
        self.user_info_search_qlid_box = CTkTextbox(self.root, width=300, height=10)
        self.user_info_search_rfid = CTkLabel(self.root, text='RFID:', height=10)
        self.user_info_search_rfid_box = CTkTextbox(self.root, width=300, height=10)
        self.user_info_search_status = CTkLabel(self.root, text='Status:', height=10)
        self.user_info_search_status_box = CTkTextbox(self.root, width=300, height=10)


        #register part
        self.user_info_register_label =CTkLabel(self.root, text='Register your details below', font=("Sora",20))

        self.user_info_register_first_name_label= CTkLabel(self.root,text='First Name:')
        self.user_info_register_first_name_entry = CTkEntry(self.root, width=180)

        self.user_info_register_last_name_label= CTkLabel(self.root, text='Last Name:')
        self.user_info_register_last_name_entry = CTkEntry(self.root, width=180)

        self.user_info_register_qlid_label = CTkLabel(self.root, text='Enter your QLID:')
        self.user_info_register_qlid_entry = CTkEntry(self.root, width=180)

        self.user_info_register_rfid_label = CTkLabel(self.root, text='Enter your RFID:')
        self.user_info_register_rfid_entry = CTkEntry(self.root, width=180)

        self.user_info_register_submit_label = CTkLabel(self.root, text='User registered!', font=("Sora", 30))
        self.user_info_register_submit = CTkButton(self.root, text='Submit', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42",corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command= self.user_registered_end)


        #Admin part
        #first part
        self.admin_scan_id = CTkLabel(self.root, text='Admin Password', font=("Sora", 20))
        self.admin_scan_entry = CTkEntry(self.root, width=300)
        self.admin_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"), hover_color="#4CAF50", fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command=self.show_admin_menu)


        self.admin_label = CTkLabel(self.root, text='Admin configurations', font=('Sora', 30))
        self.admin_register_item_button = CTkButton(self.root, text='Register New Item', font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42",corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command=self.show_admin_selection_menu)
        self.admin_log_reports_button = CTkButton(self.root, text="Logs and Reports", font=("Sora", 15,"bold"), hover_color="#4CAF50", fg_color="#004E42",corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50) #command for batch


        #Register Item part
        self.admin_item_label = CTkLabel(self.root, text='What would you like to register?', font=('Sora', 20))
        
        #batch logic
        self.admin_keys = CTkButton(self.root, text='Keys', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command=self.show_admin_key_decision_menu)
        self.admin_key_individual_add = CTkButton(self.root, text='Single Add', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command=self.admin_register_key_menu)
        self.admin_key_batch_add = CTkButton(self.root, text='Batch Add', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50,command= self.admin_register_key_batch)

        
        self.admin_tools = CTkButton(self.root, text='Tools', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command=self.show_admin_tool_decision_menu)
        self.admin_tool_individual_add = CTkButton(self.root, text='Single Add', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command=self.admin_register_tool_menu)
        self.admin_tool_batch_add = CTkButton(self.root, text='Batch Add', font=("Sora", 15, "bold"), hover_color="#4CAF50",fg_color="#004E42", corner_radius=12,border_color="#4CAF50", border_width=2,width=100,height=50, command=self.admin_register_tool_batch)
 
        
        self.admin_item_frame = CTkFrame(master=root, border_color="#004E42", border_width=2, width=250, height=370)
        self.admin_item_tool_frame = CTkFrame(master=root, border_color="#004E42", border_width=2, width=550, height=400)

        #batch add key frames
        self.admin_key_frame_ulabel = CTkLabel(self.root, text='Unit', font=('Sora', 15))
        self.admin_key_frame_unit = CTkFrame(master=root, border_color="#004E42", border_width=2, width=170, height=300)
        self.admin_key_frame_ubox = CTkTextbox(master=self.admin_key_frame_unit, width =150, height = 280)
        
        
        self.admin_key_frame_blabel = CTkLabel(self.root, text='Barcode', font=('Sora', 15))
        self.admin_key_frame_barcode = CTkFrame(master=root, border_color="#004E42", border_width=2, width=170, height=300)
        self.admin_key_frame_bbox = CTkTextbox(master=self.admin_key_frame_barcode, width =150, height = 280)
        
        self.admin_key_frame_dlabel = CTkLabel(self.root, text='Description', font=('Sora', 15))
        self.admin_key_frame_desc = CTkFrame(master=root, border_color="#004E42", border_width=2, width=170, height=300)
        self.admin_key_frame_dbox = CTkTextbox(master=self.admin_key_frame_desc, width =150, height = 280)
        
        #batch add tool frames
        self.admin_equipment_frame_nlabel = CTkLabel(self.root, text='Tool Name', font=('Sora', 15))
        self.admin_equipment_frame_name = CTkFrame(master=root, border_color="#004E42", border_width=2, width=110, height=300)
        self.admin_equipment_frame_nbox = CTkTextbox(master=self.admin_equipment_frame_name, width =90, height = 280)
        
        self.admin_equipment_frame_blabel = CTkLabel(self.root, text='Barcode', font=('Sora', 15))
        self.admin_equipment_frame_barcode = CTkFrame(master=root, border_color="#004E42", border_width=2, width=110, height=300)
        self.admin_equipment_frame_bbox = CTkTextbox(master=self.admin_equipment_frame_barcode, width =90, height = 280)
        
        self.admin_equipment_frame_dalabel = CTkLabel(self.root, text='Date Acquired', font=('Sora', 15))
        self.admin_equipment_frame_dateacq = CTkFrame(master=root, border_color="#004E42", border_width=2, width=110, height=300)
        self.admin_equipment_frame_dabox = CTkTextbox(master=self.admin_equipment_frame_dateacq, width =90, height = 280)
        
        self.admin_equipment_frame_dclabel = CTkLabel(self.root, text='Date Calibrated', font=('Sora', 15))
        self.admin_equipment_frame_datecal = CTkFrame(master=root, border_color="#004E42", border_width=2, width=110, height=300)
        self.admin_equipment_frame_dcbox = CTkTextbox(master=self.admin_equipment_frame_datecal, width =90, height = 280)
        
        #Key part
        self.admin_item_key_ID_label = CTkLabel(master=self.admin_item_frame, text='Unit', font=('Sora', 15))
        self.admin_item_key_ID_entry = CTkEntry(master=self.admin_item_frame, width=200)
        self.admin_item_key_ID_barcode = CTkLabel(master=self.admin_item_frame, text='Barcode:', font=('Sora', 15))
        self.admin_item_key_ID_barcode_entry = CTkEntry(master=self.admin_item_frame, width=200)
        self.admin_item_key_ID_description = CTkLabel(master=self.admin_item_frame, text='Description', font=('Sora', 15))
        self.admin_item_key_ID_description_box = CTkTextbox(master=self.admin_item_frame, width=200, height=180)

        self.admin_item_key_ID_submit = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"), hover_color="#4CAF50", fg_color="#004E42",bg_color="transparent", corner_radius=12,border_color="#4CAF50", border_width=2,height=50,command=self.show_key_register_end)
        self.admin_item_key_end = CTkLabel(self.root, text='Key registered!', font=("Sora", 30))
        
        self.admin_item_key_batch_submit = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"), hover_color="#4CAF50", fg_color="#004E42",bg_color="transparent", corner_radius=12,border_color="#4CAF50", border_width=2,height=50,command=self.show_key_register_batch_end)
        self.admin_item_tool_batch_submit = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"), hover_color="#4CAF50", fg_color="#004E42",bg_color="transparent", corner_radius=12,border_color="#4CAF50", border_width=2,height=50,command=self.show_tool_register_batch_end)

        #Tool part
        self.admin_item_tool_ID_name = CTkLabel(master=self.admin_item_tool_frame, text='Tool Name:', font=('Sora', 15))
        self.admin_item_tool_ID_name_entry = CTkEntry(master=self.admin_item_tool_frame, width=200)
        self.admin_item_tool_ID_barcode = CTkLabel(master=self.admin_item_tool_frame, text='Barcode:', font=('Sora', 15))
        self.admin_item_tool_ID_barcode_entry = CTkEntry(master=self.admin_item_tool_frame, width=200)
        self.admin_item_tool_ID_description = CTkLabel(master=self.admin_item_tool_frame, text='Tool Description',font=('Sora', 15))
        self.admin_item_tool_ID_description_box = CTkTextbox(master=self.admin_item_tool_frame, width=500, height=120)

        self.admin_item_tool_ID_date_acquired = CTkLabel(master=self.admin_item_tool_frame, text='Date Acquired:', font=('Sora', 15))
        self.admin_item_tool_ID_date_acquired_calendar = CTkDatePicker(self.admin_item_tool_frame)
        self.admin_item_tool_ID_date_calibrated = CTkLabel(master=self.admin_item_tool_frame, text='Date Calibrated:',font=('Sora', 15))
        self.admin_item_tool_ID_date_calibrated_calendar = CTkDatePicker(self.admin_item_tool_frame)

        self.admin_item_tool_ID_submit = CTkButton(self.root, text='Submit', font=("Sora", 15, "bold"),hover_color="#4CAF50", fg_color="#004E42",corner_radius=12,border_color="#4CAF50", border_width=2,height=50, command=self.show_tool_register_end)
        self.admin_item_tool_end = CTkLabel(self.root, text='Equipment/s registered!', font=("Sora", 20))

        self.admin_item_tool_ID_barcode_entry.bind('<Return>', self.admin_item_tool_batch_add_entry)
        
        
        
        
       
        
        
        
#########################################################################################################################################################################################################


        #UI Start program
        self.show_main_buttons()
        
        #instance members as holders for singleton data
        self.indicator = 0
        self.current_qlid = ''
        
    #Clear screen and entries
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.place_forget()

        self.admin_item_frame.grid_forget()

    def clear_all_entry(self):
        # borrow entries clear 
        # note: values in deleteion vary, if entry value starts at 0 else text box value starts at 1 
        self.borrow_text.delete("0.0", "end")
        self.borrow_scan_entry.delete(0, 'end')
        self.borrow_entry.delete(0, 'end')
        
        #return entries clear
        self.return_scan_entry.delete(0, 'end')
        self.return_items_entry.delete(0,'end')
        self.return_borrow_list.delete("0.0", "end")
        self.return_to_return_list.delete("0.0", "end")

        # search entries clear
        self.user_info_search_entry.delete(0, 'end')
        self.user_info_search_name_box.delete("0.0", "end")
        self.user_info_search_qlid_box.delete("0.0", "end")
        self.user_info_search_rfid_box.delete("0.0", "end")
        self.user_info_search_status_box.delete("0.0", "end")
        
        # register entries clear
        self.user_info_register_first_name_entry.delete(0, 'end')
        self.user_info_register_last_name_entry.delete(0, 'end')
        self.user_info_register_qlid_entry.delete(0, 'end')
        self.user_info_register_rfid_entry.delete(0, 'end')

        # admin entries clear
        self.admin_item_key_ID_entry.delete(0, 'end')
        self.admin_item_key_ID_barcode_entry.delete(0, 'end')
        self.admin_item_key_ID_description_box.delete("0.0", "end")
        
        # admin item entries clear

        self.admin_item_tool_ID_date_calibrated_calendar.date_entry.delete(0, 'end')
        self.admin_item_tool_ID_date_acquired_calendar.date_entry.delete(0,'end')
        

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
    #End of Back Button Functions

#################################################################################################################################################################################################

    #Borrow Section
    def show_borrow_id_menu(self):
        self.borrow_scan_id.place(relx=0.5, rely=0.2, anchor= 'center')
        self.borrow_scan_entry.place (relx=0.5, rely=0.4, anchor= 'center')
        self.borrow_scan_next.place(relx=0.5, rely=0.6, anchor= 'center')
        
    def login_authentication(self, valueType = 0, event = None):
        if valueType == 1:
                res = self.db_actions.search_employee( self.borrow_scan_entry.get(), self.borrow_scan_entry.get())
        else:
                res = self.db_actions.search_employee( self.return_scan_entry.get(), self.return_scan_entry.get())                

        if not res is None:
                self.to_borrow_dict.clear()
                self.current_qlid = res[ 0 ]
                if valueType == 1:
                        self.show_borrow_selection_menu()
                elif valueType == 2:
                        self.show_return_menu()
        else:
                self.message_box_test = CTkMessagebox(title="ERROR", message="Unsuccessful Login", button_color ="#004E42", border_width = 2, button_hover_color="#4CAF50")

    def show_borrow_selection_menu(self):
        self.clear_window()
        self.show_main_back()
        self.borrow_keys.place(relx=0.4, rely=0.4, anchor= 'center')
        self.borrow_tools.place(relx=0.6, rely=0.4, anchor= 'center')

    def show_borrow_menu(self, valueType): # use this command to change position of buttons
        if valueType == 'equipments':
                self.indicator = 1
        elif valueType == 'keys':
                self.indicator = 2
        
        self.clear_window()
        self.clear_all_entry()
        self.remove_back_buttons()
        self.borrow_back.place(relx=0.5, rely=0.8, anchor="center")
        self.borrow_items.place(relx=0.2, rely=0.2, anchor="center")
        self.borrow_entry.place(relx=0.2, rely=0.4, anchor="center")
        self.borrow_submit.place(relx=0.2, rely=0.72, anchor="center")
        self.borrow_text.place(relx=0.79, rely=0.4, anchor="center")
        self.borrow_continue.place(relx=0.8, rely=0.72, anchor='center')

    def borrow_add_entry(self, event=None):
        try:
                temp = {}
                temp_list = []
                
                if self.indicator == 1:
                        temp = self.db_actions.get_equipment_details( self.borrow_entry.get())
                        if not temp is None:
                                temp_list = [ temp[ 2 ], temp[ 0 ] ]
                        print( 'this is equipment' )
                elif self.indicator == 2:
                        temp = self.db_actions.get_key_details( self.borrow_entry.get() )
                        if not temp is None:
                                temp_list = [ temp[ 1 ], temp[ 0 ] ]
                        print( 'this is key' )
                        
                if not temp is None and self.to_borrow_dict.get( self.borrow_entry.get(), 'False') == 'False':
                        entry_text = temp_list[ 0 ]
                        self.borrow_text.insert('end', entry_text + '\n')
                        self.to_borrow_dict[ self.borrow_entry.get() ] = temp_list # put inside dictionary
                else:
                        print( 'BORROW ITEM ONLY ONCE' ) 
                        
                self.borrow_entry.delete(0,'end')                     
        except KeyError:
                print( temp ) 
        except TypeError:
                print( 'This is a type error' )
                
    
    
    def borrow_end(self):
        if not len(self.to_borrow_dict) == 0:
                borrow_list = []
                the_borrow_log = ncr_borrow_logs.BorrowLogs()
                for key, value in self.to_borrow_dict.items():  # extract the list from dictionary
                        print( f" {key} --  {value}")
                        borrow_list.append( value )
                the_borrow_log.set_borrow_logs( self.current_qlid, borrow_list )
                if self.db_actions.borrow_log_db(the_borrow_log, 1 if self.indicator == 1 else 2 ) == True:
                        print( 'SUCCESSFUL LOG' ) 
                
                self.clear_window()
                self.show_main_back()
                self.borrow_end_text.place(relx=0.5, rely=0.4, anchor='center')
                
                # clear all values needed
                self.current_qlid = ''
                self.to_borrow_dict.clear()
        else:
                print( 'BORROW SOMETHING TO PROCEED' )
 
        
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
        self.return_borrow_list.place(relx=0.25, rely=0.5, anchor='center')
        self.return_to_return_list.place(relx=0.75, rely=0.5, anchor='center')
        self.return_continue.place(relx=0.5, rely=0.8, anchor='center')
        
    def selected_return_log(self):
        print('tests')

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
        result = self.db_actions.search_employee( self.user_info_search_entry.get(), self.user_info_search_entry.get())
        if  result != None:
                self.clear_window()
                self.show_main_back()

                self.user_info_search_name.place(relx=0.3, rely=0.2, anchor='center')
                
                self.user_info_search_name_box.place(relx=0.65, rely=0.2, anchor='center')
                full_name = result[1] + " " + result[2]
                self.user_info_search_name_box.insert( "0.0", full_name)
                
                self.user_info_search_qlid.place(relx=0.3, rely=0.3, anchor='center')
                self.user_info_search_qlid_box.place(relx=0.65, rely=0.3, anchor='center')
                self.user_info_search_qlid_box.insert("0.0", result[0])
                
                self.user_info_search_rfid.place(relx=0.3, rely=0.4, anchor='center')
                self.user_info_search_rfid_box.place(relx=0.65, rely=0.4, anchor='center')
                self.user_info_search_rfid_box.insert("0.0", result[4])
        
                self.user_info_search_status.place(relx=0.3, rely=0.5, anchor='center')
                self.user_info_search_status_box.place(relx=0.65, rely=0.5, anchor='center')
                status = "Active" if result[3] == 1 else "Inactive"
                self.user_info_search_status_box.insert("0.0", status)


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

        self.user_info_register_submit.place(relx=0.5, rely=0.8, anchor= 'center')

    def user_registered_end(self):
        
        if self.db_actions.search_employee(self.user_info_register_qlid_entry.get(), self.user_info_register_rfid_entry.get()) == None:
                employee = ncr_employees.NcrEmployees()
                employee.first_name = self.user_info_register_first_name_entry.get().upper()
                employee.last_name = self.user_info_register_last_name_entry.get().upper()
                employee.q_lid = self.user_info_register_qlid_entry.get()
                employee.rfid = self.user_info_register_rfid_entry.get()
                if employee.employee_is_acceptable():
                        self.clear_window()
                        self.show_main_back()
                        if self.db_actions.register_employee( employee ):
                                self.user_info_register_submit_label.place(relx=0.5, rely=0.3, anchor='center')
                else:
                        self.message_box_test = CTkMessagebox(title="ERROR", message="Please fill up all boxes")
        
        else: # create an error message for existing
                     self.message_box_test = CTkMessagebox(title="ERROR", message="User already Exists")
        
        #End of User Information Section

###############################################################################################################################################################################################################

    #Start of Admin Section
    
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
        self.admin_main_back.place(relx=0.5, rely=0.9, anchor='center')

        self.admin_item_label.place(relx=0.5, rely=0.2, anchor='center')
        self.admin_keys.place(relx=0.4, rely=0.4, anchor='center')
        self.admin_tools.place(relx=0.6, rely=0.4, anchor='center')

    def show_admin_key_decision_menu(self):
        self.clear_window()
        self.admin_back.place(relx=0.5, rely=0.9, anchor='center')

        self.admin_key_individual_add.place(relx=0.6, rely=0.4, anchor='center')
        self.admin_key_batch_add.place(relx=0.4, rely=0.4, anchor='center')
        
    def show_admin_tool_decision_menu(self):
        self.clear_window()
        self.admin_back.place(relx=0.5, rely=0.9, anchor='center')

        self.admin_tool_individual_add.place(relx=0.6, rely=0.4, anchor='center')
        self.admin_tool_batch_add.place(relx=0.4, rely=0.4, anchor='center')
        
    def admin_register_key_batch(self):
        self.clear_window()
        self.admin_back.place(relx=0.4, rely=0.93, anchor='center')
        
        self.admin_key_frame_ulabel.place(relx=0.2, rely=0.1, anchor='center')
        self.admin_key_frame_unit.place(relx=0.2, rely=0.45, anchor='center')
        self.admin_key_frame_ubox.place(relx=0.5, rely=0.5, anchor='center')
        
        self.admin_key_frame_blabel.place(relx=0.5, rely=0.1, anchor='center')
        self.admin_key_frame_barcode.place(relx=0.5, rely=0.45, anchor='center')
        self.admin_key_frame_bbox.place(relx=0.5, rely=0.5, anchor='center') 
        
        self.admin_key_frame_dlabel.place(relx=0.8, rely=0.1, anchor='center')
        self.admin_key_frame_desc.place(relx=0.8, rely=0.45, anchor='center')
        self.admin_key_frame_dbox.place(relx=0.5, rely=0.5, anchor='center')
        
        self.admin_item_key_batch_submit.place(relx=0.6, rely=0.93, anchor='center')
    def admin_register_key_menu(self):
        self.clear_window()
        self.clear_all_entry()
        self.remove_back_buttons()
        self.admin_back.place(relx=0.4, rely=0.93, anchor="center")

        self.admin_item_frame.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_item_key_ID_label.place(relx=0.5, rely=0.1, anchor='center')
        self.admin_item_key_ID_entry.place(relx=0.5, rely=0.17, anchor='center')
        self.admin_item_key_ID_barcode.place(relx=0.5, rely=0.25, anchor='center')
        self.admin_item_key_ID_barcode_entry.place(relx=0.5, rely=0.32, anchor='center')
        self.admin_item_key_ID_description.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_item_key_ID_description_box.place(relx=0.5, rely=0.7, anchor='center')
        
        self.admin_item_key_ID_submit.place(relx=0.6, rely=0.93, anchor='center')

    def show_key_register_end(self):
        the_key = ncr_keys.NcrKeys()
        the_key.unit = self.admin_item_key_ID_entry.get()
        the_key.barcode = self.admin_item_key_ID_barcode_entry.get()
        the_key.description = self.admin_item_key_ID_description_box.get("0.0", "end")
        the_key.description = the_key.description + '.'
        index = the_key.description.rfind( '.' )
        the_key.description = the_key.description.replace('\n', ' ' )
        print( the_key.description )
        #print( index )
        the_key.description = the_key.description[:index-1]
        print( the_key.description ) 
        if self.db_actions.search_key( self.admin_item_key_ID_barcode_entry.get() ) == False and self.db_actions.search_equipment( self.admin_item_key_ID_barcode_entry.get()) == False :
                if the_key.ncr_key_accepted():
                        self.clear_window()
                        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
                        self.admin_item_key_end.place(relx=0.5, rely=0.3, anchor='center')
                        if self.db_actions.add_item_key( the_key ):
                                print( "Successful")
                else:
                        self.message_box_test = CTkMessagebox(title="ERROR", message="KEY was not Accepted")
        else:
                self.message_box_test = CTkMessagebox(title="ERROR", message="Barcode already exists for this unit")

    def show_key_register_batch_end(self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
        
        self.admin_item_key_end.place(relx=0.5, rely=0.3, anchor='center')
                
    def remove_new_lines(self, description):
        newstr = ''
        for i in description:
                if i == '\n':
                        newstr = newstr + ' '
                else:
                        newstr = newstr + i
        return newstr
                
     # error here 
    def admin_item_tool_batch_add_entry(self, event=None):
        print( 'UNDER INVESTIGATION' )
        #batch_text = self.admin_item_tool_ID_barcode_entry.get()
        #self.admin_item_tool_ID_batch_box.insert('end', batch_text + '\n')
        #self.admin_item_tool_ID_barcode_entry.delete(0, 'end')
    
    def admin_register_tool_batch(self):
        self.clear_window()
        self.admin_back.place(relx=0.4, rely=0.93, anchor='center')
        
        self.admin_equipment_frame_nlabel.place(relx=0.2, rely=0.1, anchor='center')
        self.admin_equipment_frame_name.place(relx=0.2, rely=0.45, anchor='center')
        self.admin_equipment_frame_nbox.place(relx=0.5, rely=0.5, anchor='center')
        
        self.admin_equipment_frame_blabel.place(relx=0.4, rely=0.1, anchor='center')
        self.admin_equipment_frame_barcode.place(relx=0.4, rely=0.45, anchor='center')
        self.admin_equipment_frame_bbox.place(relx=0.5, rely=0.5, anchor='center')
        
        self.admin_equipment_frame_dalabel.place(relx=0.6, rely=0.1, anchor='center')
        self.admin_equipment_frame_dateacq.place(relx=0.6, rely=0.45, anchor='center')
        self.admin_equipment_frame_dabox.place(relx=0.5, rely=0.5, anchor='center')
        
        self.admin_equipment_frame_dclabel.place(relx=0.8, rely=0.1, anchor='center')
        self.admin_equipment_frame_datecal.place(relx=0.8, rely=0.45, anchor='center')
        self.admin_equipment_frame_dcbox.place(relx=0.5, rely=0.5, anchor='center')
        
        
        self.admin_item_tool_batch_submit.place(relx=0.6, rely=0.93, anchor='center')
        
    def admin_register_tool_menu(self):
        self.clear_window()
        self.clear_all_entry()
        self.remove_back_buttons()
        self.admin_back.place(relx=0.4, rely=0.93, anchor="center")

        self.admin_item_tool_frame.place(relx=0.5, rely=0.43, anchor='center')

        self.admin_item_tool_ID_name.place(relx=0.5, rely=0.1, anchor='center')
        self.admin_item_tool_ID_name_entry.place(relx=0.5, rely=0.17, anchor='center')

        self.admin_item_tool_ID_barcode.place(relx=0.5, rely=0.25, anchor='center')
        self.admin_item_tool_ID_barcode_entry.place(relx=0.5, rely=0.32, anchor='center')

        self.admin_item_tool_ID_description.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_item_tool_ID_description_box.place(relx=0.5, rely=0.6, anchor='center')

        self.admin_item_tool_ID_date_acquired.place(relx=0.3, rely=0.8, anchor='center')
        self.admin_item_tool_ID_date_acquired_calendar.place(relx=0.3, rely=0.87, anchor='center')
        self.admin_item_tool_ID_date_calibrated.place(relx=0.7, rely=0.8, anchor='center')
        self.admin_item_tool_ID_date_calibrated_calendar.place(relx=0.7, rely=0.87, anchor='center')

        self.admin_item_tool_ID_submit.place(relx=0.6, rely=0.93, anchor='center')


    def show_tool_register_end(self):
        the_equipment = ncr_equipments.NcrEquipments()
        the_equipment.tool_name = self.admin_item_tool_ID_name_entry.get()
        the_equipment.barcode = self.admin_item_tool_ID_barcode_entry.get()
        
        tempDate1 = self.admin_item_tool_ID_date_acquired_calendar.date_entry.get()
        the_equipment.date_of_acquisition = self.convert_to_date( tempDate1 )
        tempDate2 = self.admin_item_tool_ID_date_calibrated_calendar.date_entry.get()
        the_equipment.calibration_date = self.convert_to_date( tempDate2 )
        
        the_equipment.description = self.admin_item_tool_ID_description_box.get( "0.0", "end" )
        the_equipment.description = the_equipment.description + '.'
        e_index = the_equipment.description.rfind('.')
        the_equipment.description = the_equipment.description.replace('\n', ' ')
        the_equipment.description = the_equipment.description[:e_index-1]
        print( self.db_actions.search_key( self.admin_item_tool_ID_barcode_entry.get() ) )
        print( self.db_actions.search_equipment( self.admin_item_tool_ID_barcode_entry.get()) )
        if self.db_actions.search_key( self.admin_item_tool_ID_barcode_entry.get() ) == False and self.db_actions.search_equipment( self.admin_item_tool_ID_barcode_entry.get()) == False :
                if the_equipment.ncr_equipment_accepted():
                        self.clear_window()
                        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
                        self.admin_item_tool_end.place(relx=0.5, rely=0.3, anchor='center')
                        if self.db_actions.add_item_equipment( the_equipment ):
                                print("Successful")
                else:
                        print("TABAAAAAANG")
        else:
                print('EXISTING NA')
                
    def convert_to_date(self, theDate):
        try:
                DI = parser.parse( theDate )
                dateSplit = theDate.split(' ')
                print(f"hehe {dateSplit[0]}")
                DI = datetime.strptime( dateSplit[0], "%m/%d/%Y" )
                print( DI )
                print( type(DI))
                return DI
        except ParserError:
                print( 'Unable to parse date time' )

    def show_tool_register_batch_end(self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
        
        self.admin_item_tool_end.place(relx=0.5, rely=0.3, anchor='center')

