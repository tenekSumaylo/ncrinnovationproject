import sys
sys.path.append('/home/keyloggerpi/ncr_innovation_project/PythonProject/Database_Services')
sys.path.append('/home/keyloggerpi/ncr_innovation_project/PythonProject/Models')
import DatabaseOperations as database_operations
import NcrEmployees as ncr_employees
import NcrEquipments as ncr_equipments
import NcrKeys as ncr_keys
import mariadb

class DatabaseOperations:
	def __init__(self, conn, cur):
		self.conn = conn
		self.cur = cur
	
	def register_employee(self, employee): # this function is used to register an employee
		if employee.employee_is_acceptable:
			self.cur.execute( "INSERT INTO NcrEmployees( q_lid, firstName, lastName, rfid) VALUES(?, ?, ?, ?)", (employee.q_lid, employee.first_name, employee.last_name, employee.rfid) )
			self.conn.commit()
			return True
		else:
			return False
			
	def search_employee(self, q_lid = None, rfid = None): # this searches for a specific employee
		self.cur.execute( "SELECT * FROM NcrEmployees WHERE q_lid = ? OR rfid = ?", (q_lid, rfid))
		searched = self.cur.fetchone()
		if searched == None:
			return None
		return searched
	
	def add_item_key(self, the_key): 
		if self.search_key( the_key.barcode ) != True:
			self.cur.execute( "INSERT INTO NcrKeys ( unitID, key_description,barcode ) VALUES ( ?, ?, ?)", 
							( the_key.unit, the_key.description, the_key.barcode )) 
			self.conn.commit()
		return True
		
	def search_key(self, barcode):
		self.cur.execute( "SELECT barcode FROM NcrKeys WHERE barcode = ?", ( barcode, ))
		result = self.cur.fetchone()
		if not result == None:
			return True
		return False
		
		
	def add_item_equipment(self, the_equipment):
		if self.search_equipment( the_equipment.barcode ) !=True:
			self.cur.execute( "INSERT INTO NcrEquipments ( itemDescription, toolName, barcode, dateOfAcquisition, calibrationDate ) VALUES ( ?, ?, ?, ?, ?)", 
							( the_equipment.description, the_equipment.tool_name, the_equipment.barcode, the_equipment.date_of_acquisition, the_equipment.calibration_date ))
			self.conn.commit()
		return True
		
	def search_equipment(self, barcode):
		#Add a comma in the second parameter because python will error with Tuple
		self.cur.execute( "SELECT barcode FROM NcrEquipments WHERE barcode = ?", (barcode, ))
		result = self.cur.fetchone()
		if not result == None:
			return True
		return False
		
	def get_equipments(self):
		self.cur.execute(  "SELECT * FROM NcrEquipments" )
		result = self.cur.fetchall()
		if result is []:
			return []
		else:
			return result
			
	def get_keys(self):
		self.cur.execute( "SELECT * FROM NcrKeys" )
		result = self.cur.fetchall()
		if result is []:
			return []
		else:
			return result
			
	def get_equipment_details(self, barcode):
		#Add a comma in the second parameter because python will error with Tuple
		self.cur.execute( "SELECT * FROM NcrEquipments WHERE barcode = ?", (barcode, ))
		result = self.cur.fetchone()
		if not result == None:
			return result
		return None
		
	def get_key_details(self, barcode):
		self.cur.execute( "SELECT * FROM NcrKeys WHERE barcode = ?", ( barcode, ))
		result = self.cur.fetchone()
		if not result == None:
			return result
		return None		
		
		
		
	
