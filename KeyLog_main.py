from customtkinter import *
from main_menu import MainMenu
import sys
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Hardware_Services')
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Database_Services')
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Models')
import HardwareOperations as hardware_operations
import DatabaseOperations as database_operations
import mariadb
import BorrowLogs as borrow

#initialize services
try:
	conn = mariadb.connect(
	user = "ncr",
	password = "1234",
	host = "127.0.0.1",
	port = 3306,
	database = "ncrinnovationproject")
#initialization of objects for hardware and db operations
	cur = conn.cursor()
	hardware_actions = hardware_operations.HardwareActions()
	db_actions = database_operations.DatabaseOperations( conn, cur )
	root = CTk()
	root.title("Laboratory Inventory")
	root.geometry("800x480")

	set_appearance_mode("light")

	main_menu = MainMenu(root, db_actions, hardware_actions)
	root.mainloop()

	conn.close()
	cur.close()
	hardware_actions.gpio_clean_all()
except:
	print( 'Error in initializing' )



#445-0753129


#alter table for notes in description that accepts a key that is empty
# report generation 

"""
Admin can see unreturned 
Makita ang tanan transactions na unresolved
	- for instance wala nauli
	- clear unreturned status
	- admin time 
"""
###
