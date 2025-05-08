# ~ All front end is here
# ~ Back end is in separate python files each with their corresponding names

from customtkinter import *
from CTkDatePicker import CTkDatePicker
from CTkMessagebox import CTkMessagebox
from CTkListbox import CTkListbox

import sys
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Hardware_Services')
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Database_Services')
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Models')
import NcrEquipments as ncr_equipments
import NcrKeys as ncr_keys
import NcrEmployees as ncr_employees
import ReturnLogs as ncr_return_logs
import BorrowLogs as ncr_borrow_logs
import HardwareOperations as hardware_operations
import DatabaseOperations as database_operations
import BorrowedItem as borrowed_item
from dateutil import parser
from datetime import datetime
from dateutil.parser import ParserError
import pandas


#from PIL import Imageadmin_file_upload_tool

class MainMenu:
    def __init__(self, root, db_actions, hardware_actions):
        #initialize the root for showing in CTK
        self.root = root
        
        #initialize instance members, ready for dependency injection however this does not support dependency injection
        self.db_actions = db_actions
        self.hdw_actions = hardware_actions
        
        # initialize instance list
        self.to_borrow_dict = {}
        self.not_returned_logs_dict = {}
        self.to_return_list = []
        self.clear_not_returned_dict = {}
        self.batch_add = []
        
        #instance member
        self.selected_log = StringVar()
        
        # line after this is the initialization of buttons and widgets

        #main buttons
        self.lab_inventory = CTkLabel(self.root, text='NCR Laboratory Inventory System',font=("Sora", 20))
        self.borrow_button = CTkButton(self.root, text='Borrow', font=("Sora", 15),height=80,width=170, hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2 ,command=self.borrow_pressed)
        self.return_button = CTkButton(self.root, text='Return', font=("Sora", 15),height=80,width=170, hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2 ,command=self.return_pressed)
        self.user_info_button = CTkButton(self.root, text='User Information', font=("Sora", 15),height=80,width=170, hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2 ,command=self.user_info_pressed)
        self.admin_button = CTkButton(self.root, text='Admin', font=("Sora", 15),height=80,width=170, hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2 ,command=self.admin_pressed)


        #back buttons
        self.main_back = CTkButton(self.root, text='Back to Menu', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=80,height=50,command=self.go_to_main)
        self.borrow_back = CTkButton(self.root, text='Back',font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=80,height=50,command=self.show_borrow_selection_menu)
        self.admin_back = CTkButton(self.root, text='Back', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12, border_color="#005142", border_width=2,width=80,height=50, command=self.show_admin_selection_menu)
        self.admin_main_back = CTkButton(self.root, text='Back', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12, border_color="#005142", border_width=2,width=80, height=50, command=self.show_admin_menu)

        #borrow_buttons
        # first part buttons and labels
        self.borrow_scan_id = CTkLabel(self.root, text='Scan your ID', font=("Sora", 20))
        self.borrow_scan_entry = CTkEntry(self.root, width=280)
        self.borrow_scan_entry.bind('<Return>', lambda event: self.login_authentication(1, event))
        
        self.borrow_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=lambda: self.login_authentication(1))

        self.borrow_keys = CTkButton(self.root, text='Keys', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=lambda: self.show_borrow_menu('keys'))
        self.borrow_tools = CTkButton(self.root, text='Tools', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=lambda: self.show_borrow_menu('equipments'))

        # second part main function
        self.borrow_items = CTkLabel(self.root, text='Scan the items you want to borrow')
        self.borrow_text_label = CTkLabel(self.root, text='Items to be borrowed')
        self.borrow_entry = CTkEntry(self.root, width=180)
        self.borrow_submit = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",  corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=self.borrow_add_entry)
        self.borrow_continue = CTkButton(self.root, text='Continue', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",  corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=self.borrow_end)
        self.borrow_text = CTkListbox(self.root, width=250, height=200)

        # End part
        self.borrow_end_text = CTkLabel(self.root, text='Thank you!, Please return the items soon', font=("Sora", 20))

        self.borrow_entry.bind('<Return>', self.borrow_add_entry)


        #return_buttons
        #first part
        self.return_scan_id = CTkLabel(self.root, text='Scan your ID', font=("Sora", 20))
        self.return_scan_entry = CTkEntry(self.root, width=300)
        self.return_scan_entry.bind('<Return>', lambda event: self.login_authentication(2, event))
        
        self.return_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=lambda: self.login_authentication(2))

        # second part main function
        self.return_items = CTkLabel(self.root, text='What would you like to return?', font=("Sora", 20))
        self.return_items_entry = CTkEntry(self.root, width=130, placeholder_text='Enter Borrowed items')
        self.return_drop_box = CTkComboBox(self.root, width=280, height=30,command=self.show_return_borrow_logs, variable=self.selected_log)
        self.return_borrow_list = CTkTextbox(self.root, width=300, height=150)
        self.return_to_return_list = CTkTextbox(self.root, width=300, height=150)
        self.return_continue = CTkButton(self.root, text='Continue',font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=self.return_end)
        self.return_pending_label = CTkLabel(self.root, text='Pending Items to be returned', font=("Sora", 10, "bold"))
        self.return_log_label = CTkLabel(self.root, text='Items to be returned', font=("Sora", 10, "bold"))
        
        #binding for return buttons
        self.return_items_entry.bind('<Return>', self.verify_return_entry )
        self.return_drop_box.bind( "<<ComboboxSelected>>", self.selected_return_log) # Combobox event for that 
        
        self.return_end_text = CTkLabel(self.root, text='Thank you for returning the items!', font=("Sora", 20))
        # End part
        
        
        #User Info Buttons
        #first part
        self.user_info_main = CTkLabel(self.root, text = 'NCR Key-Tool Logging User Information', font=("Sora", 20))
        self.user_info_search = CTkButton(self.root, text='Search',font=("Sora", 15), hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,width=120,height=50, command=self.show_user_info_search_menu)
        self.user_info_register = CTkButton(self.root, text='Register', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=120,height=50,command=self.show_user_info_register_menu)

        #search part
        self.user_info_search_label = CTkLabel(self.root, text='Enter your QLID or RFID', font=("Sora", 20))
        self.user_info_search_entry = CTkEntry(self.root, width=200)
        self.user_info_search_entry.bind('<Return>', self.show_user_info_credentials)
        self.user_info_search_submit = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.show_user_info_credentials)
        

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
        self.user_info_register_submit = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command= self.user_registered_end)

#############################################
        #Admin part
        #first part
        self.admin_scan_id = CTkLabel(self.root, text='Admin Password', font=("Sora", 20))
        self.admin_scan_entry = CTkEntry(self.root, width=300)
        self.admin_scan_next = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command=self.show_admin_menu)


        self.admin_label = CTkLabel(self.root, text='Admin configurations', font=('Sora', 30))
        self.admin_register_item_button = CTkButton(self.root, text='Register New Item', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.show_admin_selection_menu)
        self.admin_log_reports_button = CTkButton(self.root, text="Logs and Reports", font=("Sora", 15), hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.logs_reports_menu)


        #Register Item part
        self.admin_item_label = CTkLabel(self.root, text='What would you like to register?', font=('Sora', 20))
        
        #batch logic
        self.admin_keys = CTkButton(self.root, text='Keys', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.show_admin_key_decision_menu)
        self.admin_key_individual_add = CTkButton(self.root, text='Single Add', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.admin_register_key_menu)
        self.admin_key_batch_add = CTkButton(self.root, text='Batch Add', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50,command= self.admin_register_key_batch)

        
        self.admin_tools = CTkButton(self.root, text='Tools', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.show_admin_tool_decision_menu)
        self.admin_tool_individual_add = CTkButton(self.root, text='Single Add', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.admin_register_tool_menu)
        self.admin_tool_batch_add = CTkButton(self.root, text='Batch Add', font=("Sora", 15), hover_color="#005142",fg_color="#00291d", corner_radius=12,border_color="#005142", border_width=2,width=100,height=50, command=self.admin_register_tool_batch)
 
        
        self.admin_item_frame = CTkFrame(master=root, border_color="#00291d", border_width=2, width=250, height=370)
        self.admin_item_tool_frame = CTkFrame(master=root, border_color="#00291d", border_width=2, width=550, height=400)

        #batch add key frames
        self.admin_key_frame_ulabel = CTkLabel(self.root, text='Unit', font=('Sora', 15))
        self.admin_key_frame_unit = CTkFrame(master=root, border_color="#00291d", border_width=2, width=170, height=300)
        self.admin_key_frame_ubox = CTkTextbox(master=self.admin_key_frame_unit, width =150, height = 280)
        
        
        self.admin_key_frame_blabel = CTkLabel(self.root, text='Barcode', font=('Sora', 15))
        self.admin_key_frame_barcode = CTkFrame(master=root, border_color="#00291d", border_width=2, width=170, height=300)
        self.admin_key_frame_bbox = CTkTextbox(master=self.admin_key_frame_barcode, width =150, height = 280)
        
        self.admin_key_frame_dlabel = CTkLabel(self.root, text='Description', font=('Sora', 15))
        self.admin_key_frame_desc = CTkFrame(master=root, border_color="#00291d", border_width=2, width=170, height=300)
        self.admin_key_frame_dbox = CTkTextbox(master=self.admin_key_frame_desc, width =150, height = 280)
        
        #batch add tool frames
        self.admin_equipment_frame_nlabel = CTkLabel(self.root, text='Tool Name', font=('Sora', 15))
        self.admin_equipment_frame_name = CTkFrame(master=root, border_color="#00291d", border_width=2, width=110, height=300)
        self.admin_equipment_frame_nbox = CTkTextbox(master=self.admin_equipment_frame_name, width =90, height = 280)
        
        self.admin_equipment_frame_blabel = CTkLabel(self.root, text='Barcode', font=('Sora', 15))
        self.admin_equipment_frame_barcode = CTkFrame(master=root, border_color="#00291d", border_width=2, width=110, height=300)
        self.admin_equipment_frame_bbox = CTkTextbox(master=self.admin_equipment_frame_barcode, width =90, height = 280)
        
        self.admin_equipment_frame_dalabel = CTkLabel(self.root, text='Date Acquired', font=('Sora', 15))
        self.admin_equipment_frame_dateacq = CTkFrame(master=root, border_color="#00291d", border_width=2, width=110, height=300)
        self.admin_equipment_frame_dabox = CTkTextbox(master=self.admin_equipment_frame_dateacq, width =90, height = 280)
        
        self.admin_equipment_frame_dclabel = CTkLabel(self.root, text='Date Calibrated', font=('Sora', 15))
        self.admin_equipment_frame_datecal = CTkFrame(master=root, border_color="#00291d", border_width=2, width=110, height=300)
        self.admin_equipment_frame_dcbox = CTkTextbox(master=self.admin_equipment_frame_datecal, width =90, height = 280)
        
        #Key part
        self.admin_item_key_ID_label = CTkLabel(master=self.admin_item_frame, text='Unit', font=('Sora', 15))
        self.admin_item_key_ID_entry = CTkEntry(master=self.admin_item_frame, width=200)
        self.admin_item_key_ID_barcode = CTkLabel(master=self.admin_item_frame, text='Barcode:', font=('Sora', 15))
        self.admin_item_key_ID_barcode_entry = CTkEntry(master=self.admin_item_frame, width=200)
        self.admin_item_key_ID_description = CTkLabel(master=self.admin_item_frame, text='Description', font=('Sora', 15))
        self.admin_item_key_ID_description_box = CTkTextbox(master=self.admin_item_frame, width=200, height=180)

        self.admin_item_key_ID_submit = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",bg_color="transparent", corner_radius=12,border_color="#005142", border_width=2,height=50,command=self.show_key_register_end)
        self.admin_item_key_end = CTkLabel(self.root, text='Key registered!', font=("Sora", 30))
        
        self.admin_item_key_batch_submit = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",bg_color="transparent", corner_radius=12,border_color="#005142", border_width=2,height=50,command=self.show_key_register_batch_end)
        self.admin_item_tool_batch_submit = CTkButton(self.root, text='Submit', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",bg_color="transparent", corner_radius=12,border_color="#005142", border_width=2,height=50,command=self.show_tool_register_batch_end)

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

        self.admin_item_tool_ID_submit = CTkButton(self.root, text='Submit', font=("Sora", 15),hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,height=50, command=self.show_tool_register_end)
        self.admin_item_tool_end = CTkLabel(self.root, text='Equipment/s registered!', font=("Sora", 20))

        self.admin_item_tool_ID_barcode_entry.bind('<Return>', self.admin_item_tool_batch_add_entry)
        
        
        #Logs and Reports part
        self.admin_config_borrowed_items = CTkButton(self.root, text='Borrowed Items Config ', font=("Sora", 15),hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,height=50, command=self.borrow_items_config_menu)        
        self.admin_config_print_logs = CTkButton(self.root, text='Print Logs', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12, border_color="#005142", border_width=2,height=50, command=self.return_logs_config_menu)
        
        
        #Borrowed items part
        self.admin_config_search_ulabel = CTkLabel(self.root, text='Search User ID', font=('Sora', 15))
        self.admin_config_search_user_entry = CTkEntry(self.root, width=300)
        self.admin_config_search_user_submit =  CTkButton(self.root, text='Submit', font=("Sora", 15),hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,height=50, command= lambda: self.login_authentication(3))
        self.admin_rlogs_label= CTkLabel(self.root, text='Items not Returned', font=('Sora', 15))
        self.admin_rlogs_box= CTkListbox(self.root, width=450, height=300)
        self.admin_rlogs_reset= CTkButton(self.root, text='Reset user returned items', font=("Sora", 15),hover_color="#005142", fg_color="#00291d",corner_radius=12,border_color="#005142", border_width=2,height=50, command=self.reset_all_box)
        
        #Print Logs part
        self.print_logs_label = CTkLabel(self.root, text='Set Range to print', font=("Sora",20))
        self.print_logs_start_date = CTkDatePicker(self.root)
        self.print_logs_end_date =  CTkDatePicker(self.root)
        self.print_logs_button = CTkButton(self.root, text='Print as PDF', font=("Sora", 15), hover_color="#005142", fg_color="#00291d", corner_radius=12, border_color="#005142", border_width=2,height=50, command=self.print_to_pdf)
        
        
        #file upload 
        self.admin_file_upload_key = CTkButton(self.root, text='Upload file', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",bg_color="transparent", corner_radius=12,border_color="#005142", border_width=2,height=30,command=self.file_upload)
        self.admin_file_upload_tool = CTkButton(self.root, text='Upload file', font=("Sora", 15), hover_color="#005142", fg_color="#00291d",bg_color="transparent", corner_radius=12,border_color="#005142", border_width=2,height=30,command=self.file_upload_tools)
        
       
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
        self.borrow_text.delete(0, "end")
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
        self.admin_scan_entry.delete(0,'end')
        self.admin_item_tool_ID_date_calibrated_calendar.date_entry.delete(0, 'end')
        self.admin_item_tool_ID_date_acquired_calendar.date_entry.delete(0,'end')
        self.admin_item_key_ID_entry.delete(0, 'end')
        self.admin_item_tool_ID_barcode_entry.delete(0, 'end')
        self.admin_item_key_ID_description_box.delete("0.0", "end")
        self.admin_item_tool_ID_name_entry.delete(0, 'end')
        self.admin_item_tool_ID_barcode_entry.delete(0, 'end')
        self.admin_item_tool_ID_description_box.delete("0.0", "end")
        
        self.admin_config_search_user_entry
        self.print_logs_start_date.date_entry.delete(0,'end')
        self.print_logs_end_date.date_entry.delete(0, 'end')
        

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
        if valueType == 1 :
                res = self.db_actions.search_employee( self.borrow_scan_entry.get(), self.borrow_scan_entry.get())
        elif valueType == 2:
                res = self.db_actions.search_employee( self.return_scan_entry.get(), self.return_scan_entry.get())                
        else:
                res = self.db_actions.search_employee( self.admin_config_search_user_entry.get(), self.admin_config_search_user_entry.get())

        if not res is None:
                self.current_qlid = res[ 0 ]
                if valueType == 1:
                        self.show_borrow_selection_menu()
                elif valueType == 2:
                        self.return_drop_box.set( 'Select To Return')
                        self.not_returned_logs_dict.clear()
                        self.to_return_list.clear()
                        self.show_return_menu()
                elif valueType == 3:
                        self.clear_not_returned_dict.clear()
                        self.admin_rlogs_menu()
        else:
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Unsuccessful Login", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)

    def show_borrow_selection_menu(self):
        self.to_borrow_dict.clear()
        self.clear_window()
        self.show_main_back()
        self.hdw_actions.stepper_off()
        
        
        self.borrow_keys.place(relx=0.4, rely=0.4, anchor= 'center')
        self.borrow_tools.place(relx=0.6, rely=0.4, anchor= 'center')

    def show_borrow_menu(self, valueType): # use this command to change position of buttons
        if valueType == 'equipments':
                self.indicator = 1
                self.hdw_actions.stepper_on()
        elif valueType == 'keys':
                self.indicator = 2
                # ~ self.message_box_test = CTkMessagebox(master=self.root, title="Information", message="Opening Keybox", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
                self.hdw_actions.solenoid_on()
        
        self.clear_window()
        self.clear_all_entry()
        self.remove_back_buttons()
        
        self.borrow_back.place(relx=0.5, rely=0.8, anchor="center")
        self.borrow_items.place(relx=0.2, rely=0.15, anchor="center")
        self.borrow_text_label.place(relx=0.8, rely=0.15, anchor="center")
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
                        self.hdw_actions.deactivate_stepper()
                        if not temp is None:
                                temp_list = [ temp[ 2 ], temp[ 0 ], temp[ 3 ] ]
                elif self.indicator == 2:
                        temp = self.db_actions.get_key_details( self.borrow_entry.get() )
                        if not temp is None:
                                temp_list = [ temp[ 1 ], temp[ 0 ], temp[ 3 ] ]
                if not temp is None and self.to_borrow_dict.get( self.borrow_entry.get(), 'False') == 'False':
                        entry_text = temp_list[ 0 ]
                        self.borrow_text.insert('end', entry_text + '\n')
                        self.to_borrow_dict[ self.borrow_entry.get() ] = temp_list # put inside dictionary
                else:
                        self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Item does not exist", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100) 
                        
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
                the_borrow_log.set_borrow_logs( self.current_qlid, borrow_list, 'key' if self.indicator == 2 else 'equipment' )
                if self.db_actions.borrow_log_db(the_borrow_log) == True:
                        print( 'SUCCESSFUL LOG' ) 
                
                self.clear_window()
                self.show_main_back()
                if self.indicator == 1:
                        self.hdw_actions.deactivate_stepper()
                self.borrow_end_text.place(relx=0.5, rely=0.4, anchor='center')
                
                
                # clear all values needed
                self.current_qlid = ''
                self.to_borrow_dict.clear()
        else:
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Borrow something to proceed", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora',12), fade_in_duration=100)
 
        
    #End of Borrow Section

#################################################################################################################################################################################################

    #Return Section
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
        self.return_pending_label.place(relx=0.25, rely=0.31, anchor='center')
        self.return_log_label.place(relx=0.75, rely=0.31, anchor='center')
        
        res = self.db_actions.get_not_returned_items_db( self.current_qlid )
        if res == None:
                print( 'empty')
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Nothing has been borrowed yet", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100) 
        else:
                for i in res:
                        list_of_items = {}
                        employee_borrow_log = ncr_borrow_logs.BorrowLogs()
                        item_result = self.db_actions.get_return_items_db( i [ 0 ] )    #database query 
                        for k in item_result:
                                ncr_item = borrowed_item.BorrowedItem()
                                ncr_item.set_item( k[ 0 ], k[ 1 ], k[ 2 ], k[ 3 ])
                                list_of_items.update( {ncr_item.barcode : ncr_item} )  # this list is now converted into a dictionary 
                        if len(item_result) != 0:
                                employee_borrow_log.set_borrow_logs_view( i[ 0 ], i[ 1 ], i[ 2 ], i[ 3 ], i[4], list_of_items)
                                        
                        self.not_returned_logs_dict[ f"{i[ 0 ]} {i[ 2 ]}" ] = employee_borrow_log
                self.return_drop_box.configure( values = self.not_returned_logs_dict )
        
    def selected_return_log(self):
        print('hehe')

    def show_return_borrow_logs(self, value = ''):
        if not value == 'update':
                self.return_to_return_list.delete('0.0', 'end')
                self.to_return_list.clear()
        self.return_borrow_list.delete("0.0", "end")
        temp = self.not_returned_logs_dict[ self.selected_log.get() ] # assign to temp the borrow log
        
        for i, j in temp.borrow_list.items():
                if value == 'update' and any( j.barcode == x.barcode for x in self.to_return_list ): # check if value is update and check if the an item is in scanned return list
                        print('norwin')
                else:
                        self.return_borrow_list.insert( '0.0', j.name + '\n' )                        
    
    def verify_return_entry(self, event = None):
        res = self.not_returned_logs_dict.get( self.selected_log.get(), 'None' )
        
        if not res == 'None':
                # find the barcode, inputted by the user
                employee_borrow_details = res.borrow_list.get( self.return_items_entry.get(), 'None' )       # get the borrow list dict 
                if not employee_borrow_details == 'None':
                        return_item = borrowed_item.BorrowedItem()
                        return_item.set_item( employee_borrow_details.log_id, employee_borrow_details.item_id, employee_borrow_details.name, employee_borrow_details.barcode )
                        print(self.to_return_list)
                        if not any( x.barcode == self.return_items_entry.get() for x in self.to_return_list): 
                                self.to_return_list.append(return_item)
                                self.return_to_return_list.insert( '0.0', employee_borrow_details.name + "\n")
                                print('appended')
                        else:
                                print('Item already logged')
                        self.show_return_borrow_logs('update')
                else:
                        print( 'Item not in this log' )


    def return_end(self):
        if len(self.to_return_list) == 0:
                print( 'Please add an item to return' )
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Please add an Item to return!", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)

        else:                
                self.clear_window()
                self.show_main_back()
                self.return_end_text.place(relx=0.5, rely=0.4, anchor='center')
                
                retrieve_log = self.not_returned_logs_dict.get( self.selected_log.get(), 'None' )
                employee_return_log = ncr_return_logs.ReturnLogs()
                
                temp = {}
                for i in self.to_return_list:
                        temp[ i.barcode ] = i
                        print( f"{i.barcode}, {i.name}, {retrieve_log.borrow_type}")
                employee_return_log.set_borrow_logs( retrieve_log.q_lid, retrieve_log.borrow_type, temp, retrieve_log.log_id )
                print( '===============')
                print( employee_return_log.return_date)
                
                for k in temp:
                        print(k)
                        
                print('------------')
                for key in employee_return_log.return_dict:
                        print(key)
                if self.db_actions.return_log_db( employee_return_log ) == True:
                        print('marrr')
                        self.selected_log.set( '' ) 
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

    def show_user_info_credentials(self, event = None):
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
        else:
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Invalid User", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)


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
                        self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Please fill up all boxes", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
        
        else: # create an error message for existing
                        self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="User already exists", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
        
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
        self.clear_all_entry()
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
        self.batch_add.clear()
        self.clear_window()
        self.admin_back.place(relx=0.4, rely=0.93, anchor='center')
        
        self.admin_key_frame_ulabel.place(relx=0.2, rely=0.1, anchor='center')
        self.admin_key_frame_unit.place(relx=0.2, rely=0.45, anchor='center')
        self.admin_key_frame_ubox.place(relx=0.5, rely=0.5, anchor='center')
        
        self.admin_key_frame_blabel.place(relx=0.8, rely=0.1, anchor='center')
        self.admin_key_frame_barcode.place(relx=0.5, rely=0.45, anchor='center')
        self.admin_key_frame_bbox.place(relx=0.5, rely=0.5, anchor='center') 
        
        self.admin_key_frame_dlabel.place(relx=0.5, rely=0.1, anchor='center')
        self.admin_key_frame_desc.place(relx=0.8, rely=0.45, anchor='center')
        self.admin_key_frame_dbox.place(relx=0.5, rely=0.5, anchor='center')
        
        self.admin_file_upload_key.place(relx=0.5, rely=0.83, anchor='center')
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
        try:
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
                                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Invalid Key", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12))
                else:
                        self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Barcode already exists for this unit", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
        except:
                print('An error occurred in registering keys')

    def show_key_register_batch_end(self):
        if len(self.batch_add) != 0:
                self.clear_window()
                self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
                self.admin_item_key_end.place(relx=0.5, rely=0.3, anchor='center')
                for row in self.batch_add:
                        unit, description, barcode = row
                        init_key = ncr_keys.NcrKeys()
                        init_key.set_ncr_key(barcode, unit, description )
                        self.db_actions.add_item_key( init_key )
                self.batch_add.clear()
        else:
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="You must upload a file", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
                
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
        print( 'UNDER INVESTIGATION')
        self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="UNDER INVESTIGATION daw ana kenet", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100) 
        #batch_text = self.admin_item_tool_ID_barcode_entry.get()
        #self.admin_item_tool_ID_batch_box.insert('end', batch_text + '\n')
        #self.admin_item_tool_ID_barcode_entry.delete(0, 'end')
        
    def file_upload(self):
        try:
                file_path = filedialog.askopenfilename()
                if file_path:
                        print( f"File selected: {file_path} " )
                self.batch_add.clear()
                get_data = pandas.read_csv(file_path, engine='python')
                print(get_data)
                print( f"The length of the csv is {len(get_data)} and the number of columns {len(get_data.columns)}")
                
                # check if the csv being read is empty 
                if get_data.empty:
                        self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV File", message="The CSV file is empty", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)  
                        return
                print('1')
                
                # drop all the empty rows through this function
                get_data = get_data.dropna(how='all')
                get_data = get_data.reset_index(drop=True)
                print(get_data)
                        
                # this function checks if there are duplicates in barcodes
                if get_data['BARCODE'].duplicated().any():
                        self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV File", message="Barcodes should have no duplicates", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)  
                        return
                
                if not len(get_data.columns) == 3:
                        self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV", message="CSV file should contain 3 columns only", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)                        
                        return
                print('[DEBUG] after testing types')
                for index, row in get_data.iterrows():
                        if not isinstance( row['UNIT'], str) and not isinstance(row['DESCRIPTION'], str) and not isinstance(row['BARCODE'], str):
                                self.message_box_test = CTkMessagebox(master=self.root, title="Error", message="An error occurred, values should be string", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)    
                                return
                        self.admin_key_frame_ubox.insert('0.0', row['UNIT'] + '\n')
                        self.admin_key_frame_bbox.insert('0.0', row['DESCRIPTION'] + '\n')
                        self.admin_key_frame_dbox.insert('0.0', row['BARCODE'] + '\n' )
                        self.batch_add.append((row['UNIT'], row['BARCODE'], row['DESCRIPTION']))
        except UnicodeDecodeError:
                self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV", message="Please upload a CSV file", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)      
                self.batch_add.clear()                      
        except ValueError:
                self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV", message="Please upload a CSV file", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)       
                self.batch_add.clear()               
        except:
                self.message_box_test = CTkMessagebox(master=self.root, title="Invalid Column Name", message="Please check column names, it must match with the documentation", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)                    
                self.admin_key_frame_ubox.delete( '0.0', 'end' )
                self.admin_key_frame_bbox.delete('0.0', 'end')
                self.admin_key_frame_dbox.delete('0.0', 'end')
                self.batch_add.clear()        
                
    def file_upload_tools(self):
        try:
                print('Tools area')
                file_path = filedialog.askopenfilename()
                if file_path:
                        print( f"File selected: {file_path} " )
                self.batch_add.clear()
                get_data = pandas.read_csv(file_path, engine='python')
                print(get_data)
                print( f"The length of the csv is {len(get_data)} and the number of columns {len(get_data.columns)}")
                if get_data.empty:
                        self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV File", message="The CSV file is empty", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)  
                        return
                print('1')
                
                # drop all the empty rows through this function
                get_data = get_data.dropna(how='all')
                get_data = get_data.reset_index(drop=True)
                print(get_data)
                        
                # this function checks if there are duplicates in barcodes
                if get_data['BARCODE'].duplicated().any():
                        self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV File", message="Barcodes should have no duplicates", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)  
                        return
                
                print('2')
                # this checks the length of the columns 
                if not len(get_data.columns) == 5:
                        self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV", message="CSV file should contain 5 columns only", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)                        
                        return
                
                # convert the strings into datetime
                
                get_data['D_ACQUISITION'] = pandas.to_datetime(get_data['D_ACQUISITION'], format = '%m/%d/%Y')
                get_data['D_CALIBRATION'] = pandas.to_datetime(get_data['D_CALIBRATION'], format = '%m/%d/%Y')
                
                print('[DEBUG] after testing types')
                for index, row in get_data.iterrows():
                        if not isinstance( row['NAME'], str) and not isinstance(row['DESCRIPTION'], str) and not isinstance(row['BARCODE'], str) and not isinstance(row['D_ACQUISITION'], str) and not isinstance(row['D_CALIBRATION'], str):
                                self.message_box_test = CTkMessagebox(master=self.root, title="Error", message="An error occurred, values should be string", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)    
                                return
                        
                        self.admin_equipment_frame_nbox.insert('0.0', row['NAME'] + '\n')
                        self.admin_equipment_frame_bbox.insert('0.0', row['BARCODE'] + '\n')
                        self.admin_equipment_frame_dabox.insert('0.0', str(row['D_ACQUISITION']) + '\n' )
                        self.admin_equipment_frame_dcbox.insert('0.0', str(row['D_CALIBRATION']) + '\n' )
                        self.batch_add.append((row['NAME'], row['BARCODE'], str(row['D_ACQUISITION']), str(row['D_CALIBRATION']), row['DESCRIPTION']))
                        print( type(row['D_ACQUISITION']) )
        except UnicodeDecodeError:
                self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV", message="Please upload a CSV file", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)      
                self.batch_add.clear()                      
        except ValueError:
                self.message_box_test = CTkMessagebox(master=self.root, title="Invalid CSV", message="Please upload a CSV file", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)       
                self.batch_add.clear()   
        
        except:
                self.message_box_test = CTkMessagebox(master=self.root, title="Invalid Column Name", message="Please check column names, it must match with the documentation", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)                    
                self.admin_key_frame_ubox.delete( '0.0', 'end' )
                self.admin_key_frame_bbox.delete('0.0', 'end')
                self.admin_key_frame_dbox.delete('0.0', 'end')
                self.batch_add.clear()       
        
    
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
        
        self.admin_file_upload_tool.place(relx=0.5, rely=0.83, anchor='center')
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
                        self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Invalid Equipment", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
        else:
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="Barcode already exists for this equipment", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
                
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
        if len(self.batch_add) != 0:
                self.clear_window()
                self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
                self.admin_item_tool_end.place(relx=0.5, rely=0.3, anchor='center')
                for row in self.batch_add:
                        name, barcode, da, dc, desc = row
                        init_tool = ncr_equipments.NcrEquipments()
                        init_tool.set_ncr_equipment(name, barcode, da, dc, desc)
                        init_tool.date_of_acquisition = datetime.strptime(init_tool.date_of_acquisition, "%Y-%m-%d %H:%M:%S")
                        init_tool.calibration_date = datetime.strptime(init_tool.calibration_date, "%Y-%m-%d %H:%M:%S")
                        self.db_actions.add_item_equipment( init_tool )
                self.batch_add.clear()
        else:
                self.message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="You must upload a file", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)


    def logs_reports_menu(self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
        self.admin_config_borrowed_items.place(relx=0.5, rely=0.3, anchor='center')
        self.admin_config_print_logs.place(relx=0.5, rely = 0.55, anchor='center')
   
    def borrow_items_config_menu(self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
        self.admin_config_search_ulabel.place(relx=0.5,rely=0.2, anchor='center')
        self.admin_config_search_user_entry.place(relx=0.5, rely=0.4, anchor='center')
        self.admin_config_search_user_submit.place(relx=0.5, rely=0.6, anchor = 'center')

    def admin_rlogs_menu(self):
        self.admin_rlogs_box.delete(0, END)
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.9, anchor='center')
        self.admin_rlogs_label.place(relx=0.35, rely=0.1, anchor='center')
        self.admin_rlogs_box.place(relx=0.35, rely = 0.45, anchor='center')
        self.admin_rlogs_reset.place(relx=0.8, rely = 0.2, anchor='center')
        res = self.db_actions.get_employee_unreturned_items(self.current_qlid)
        k = 0
        if not res == None:
                self.clear_not_returned_dict = res
                for i in res:
                        self.admin_rlogs_box.insert(k, i)
                        k = k + 1
                print(res)
        else:
                print( 'Not unreturned' )
                
        
            
    def reset_all_box(self):
        log_result = self.db_actions.search_return_log_dict(self.current_qlid)
        
        admin_message_box = CTkMessagebox(master=self.root, title="ERROR", message="Are you sure you want to reset all returned logs of this user?", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100, option_1 = 'Confirm', option_2 = 'Cancel')
        answer_to_log = admin_message_box.get()
        if answer_to_log == 'Confirm' and len(self.clear_not_returned_dict.keys()) != 0:
                message_box_test = CTkMessagebox(master=self.root, title="ERROR", message="All items returned for this user", button_color ="#00291d", border_width = 2, button_hover_color="#005142", font=('Sora', 12), fade_in_duration=100)
                for key, value in self.clear_not_returned_dict.items():
                        for k in value:
                                return_log = log_result.get(k.log_id, 'None')
                                if not return_log == 'None':
                                        if return_log[ 4 ] == 'key':
                                                self.db_actions.return_key_db( k.log_id, k.item_id, k.name, k.barcode )
                                        elif return_log[ 4 ] == 'equipment':
                                                self.db_actions.return_equipment_db( k.log_id, k.item_id, k.name, k.barcode )
                self.admin_rlogs_box.delete(0, END )
        else:
                print( 'Not to return' )

    def return_logs_config_menu (self):
        self.clear_window()
        self.admin_main_back.place(relx=0.5, rely=0.8, anchor='center')
        
        self.print_logs_label.place(relx=0.5, rely=0.2, anchor='center') 
        self.print_logs_start_date.place(relx=0.3,rely=0.4, anchor='center') 
        self.print_logs_end_date.place(relx=0.7,rely=0.4, anchor='center')
        self.print_logs_button.place(relx=0.5, rely=0.6, anchor='center')

    def print_to_pdf(self):
        print("yeah put the export thing here")
        
            
