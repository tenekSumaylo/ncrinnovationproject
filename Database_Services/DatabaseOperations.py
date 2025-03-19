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
		try:
			if employee.employee_is_acceptable:
				self.cur.execute( "INSERT INTO NcrEmployees( q_lid, firstName, lastName, rfid) VALUES(?, ?, ?, ?)", (employee.q_lid, employee.first_name, employee.last_name, employee.rfid) )
				self.conn.commit()
				return True
		except mariadb.InterfaceError:
			print( 'Disconnection with the server' )
			return False
			
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
		if self.search_equipment( the_equipment.barcode ) != True:
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
		self.cur.execute(  "SELECT * FROM NcrEquipments WHERE is_deleted = 0" )
		result = self.cur.fetchall()
		if result is []:
			return []
		else:
			return result
			
	def get_keys(self):
		self.cur.execute( "SELECT * FROM NcrKeys WHERE is_deleted = 0" )
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
		
	def borrow_log_db(self, the_borrow_log ):
		try:
			self.cur.execute( "INSERT INTO BorrowLogs ( q_lid, borrowDate, borrowTime, borrow_type ) VALUES ( ?, ?, ?, ?)", ( the_borrow_log.q_lid, the_borrow_log.borrow_date, the_borrow_log.borrow_time, the_borrow_log.borrow_type) )
			self.cur.execute( "SELECT * FROM BorrowLogs ORDER BY log_id DESC LIMIT 1" )
			get_val = self.cur.fetchone()
			print( 'JGH' )
			if the_borrow_log.borrow_type == 'equipment' and get_val != None: # changes to equipment
				for list_val in the_borrow_log.borrow_list:
					if not self.borrow_equipment_db( get_val[ 0 ], list_val[ 1 ], list_val[ 0 ], list_val[ 2 ] ) == True:
						return False  # handle if db errors
			elif the_borrow_log.borrow_type == 'key': # changes to key
				for list_val in the_borrow_log.borrow_list:
					if not self.borrow_key_db( get_val[ 0 ], list_val[ 1 ], list_val[ 0 ], list_val[ 2 ] ) == True:
						return False # handle if db errors 
			return True
		except mariadb.InterfaceError:
			print( 'Borrow item connection Error' )
		return False
		
	def borrow_key_db(self, logID, keyID, name, barcode):
		try:	
			self.cur.execute( "INSERT INTO BorrowedKeys (log_id, keyID, name, barcode) VALUES ( ?, ?, ?, ? )", (logID, keyID, name, barcode ) )
			self.conn.commit()
			return True
		except mariadb.InterfaceError:
			print( 'Connection Error' )
		return False
			
	def borrow_equipment_db(self, logID, equipmentID, name, barcode ):
		try:
			self.cur.execute( "INSERT INTO BorrowedEquipment (log_id, equipmentID, name, barcode) VALUES ( ?, ?, ?, ? )", (logID, equipmentID, name, barcode ) )
			self.conn.commit()
			return True
		except mariadb.InterfaceError:
			print( 'Connection Error' )
		return False
		
	def get_borrow_log_db(self, q_lid, rfid ):
		try:
			self.cur.execute( "SELECT * FROM BorrowLogs WHERE q_lid = ?", ( q_lid,) )
			res = self.cur.fetchall()
			if len(res) == 0:
				return None
			return res
		except:
			print( 'Possible error in fetching database borrow logs' )
			
	def get_return_log_db(self, q_lid, rfid):
		try:
			self.cur.execute( "SELECT * FROM ReturnLogs WHERE q_lid = ?", ( q_lid,) )
			res = self.cur.fetchall()
			if len(res) == 0:
				 return None
			return res
		except:
			print( 'Possible error in fetching database return logs' )
			
	def get_not_returned_items_db(self, q_lid):
		try:
			self.cur.execute( "SELECT BorrowLogs.log_id, BorrowLogs.q_lid, BorrowLogs.borrowDate, BorrowLogs.borrowTime, BorrowLogs.borrow_type FROM BorrowLogs LEFT JOIN ReturnLogs USING(log_id) WHERE ReturnLogs.log_id IS NULL AND BorrowLogs.q_lid = ?", ( q_lid, ) )
			res = self.cur.fetchall()
			
			if len(res) == 0:
				return None
			return res
		except mariadb.InterfaceError:
			print( 'Possible error in fetching database borrow logs' )
			
	def get_return_items_db(self, log_id):
		# this checks for both borrowed keys or borrowed items
		self.cur.execute( "SELECT * FROM BorrowedKeys WHERE log_id = ?", (log_id,) )
		res = self.cur.fetchall()
		if len(res) != 0:
			return res
		else:
			self.cur.execute( "SELECT * FROM BorrowedEquipment WHERE log_id = ?", (log_id, ) )
			res = self.cur.fetchall()
			if res == 0:
				return None
			else:
				return res
		
	
		
		
		
		
	
