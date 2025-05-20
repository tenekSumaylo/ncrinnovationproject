import sys
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Hardware_Services')
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Database_Services')
sys.path.append('/home/keylog/ncr_innovation_project/PythonProject/Models')
import DatabaseOperations as database_operations
import NcrEmployees as ncr_employees
import NcrEquipments as ncr_equipments
import NcrKeys as ncr_keys
import BorrowedItem as borrowed_item
import mariadb
from collections import defaultdict

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
			
	def search_employee(self, q_lid = None, rfid = None): # this searches for a specific 
		print(q_lid)
		self.cur.execute( "SELECT * FROM NcrEmployees WHERE q_lid = ? OR rfid = ?", (q_lid, rfid))
		searched = self.cur.fetchone()
		if searched == None:
			return None
		return searched
	
	def add_item_key(self, the_key):
		try:
			if self.search_key( the_key.barcode ) != True:
				self.cur.execute( "INSERT INTO NcrKeys ( unit_ID, keyDescription,barcode ) VALUES ( ?, ?, ?)", 
								( the_key.unit, the_key.description, the_key.barcode )) 
				self.conn.commit()
			return True
		except:
			print( 'An error occurred in item key addition')
		
	def search_key(self, barcode):
		self.cur.execute( "SELECT barcode FROM NcrKeys WHERE barcode = ?", ( barcode, ))
		result = self.cur.fetchone()
		if not result == None:
			return True
		return False
		
		
	def add_item_equipment(self, the_equipment):
		if self.search_equipment( the_equipment.barcode ) != True:
			self.cur.execute( "INSERT INTO NcrEquipments ( itemDescription, toolName, barcode, date_of_acquisition, calibration_date ) VALUES ( ?, ?, ?, ?, ?)", 
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
		if not result:
			return []
		else:
			return result
			
	def get_keys(self):
		self.cur.execute( "SELECT * FROM NcrKeys WHERE is_deleted = 0" )
		result = self.cur.fetchall()
		if not result:
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
			#self.conn.commit()
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
			self.cur.execute( "INSERT INTO BorrowedKey (log_id, key_ID, name, barcode) VALUES ( ?, ?, ?, ? )", (logID, keyID, name, barcode ) )
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
		     
	def return_log_db(self, the_return_log):
		try: 
			self.cur.execute( "INSERT INTO ReturnLogs ( log_id, q_lid, returnDate, returnTime, borrow_type ) VALUES ( ?, ?, ?, ?, ?)", ( the_return_log.log_id, the_return_log.q_lid, the_return_log.return_date, the_return_log.return_time, the_return_log.borrow_type) )
			#self.conn.commit()
			print(f"the return type: {the_return_log.borrow_type}")
			if the_return_log.borrow_type == 'equipment': # changes to equipment
				for list_val, val in the_return_log.return_dict.items():
					print('equip')
					if not self.return_equipment_db( the_return_log.log_id, val.item_id, val.name, val.barcode) == True:
						return False  # handle if db errors
			elif the_return_log.borrow_type == 'key': # changes to key
				for list_val, val in the_return_log.return_dict.items():
					print( 'key' )
					if not self.return_key_db( the_return_log.log_id, val.item_id, val.name, val.barcode) == True:
						return False # handle if db errors 
			return True
		except mariadb.InterfaceError:
			print( 'Borrow item connection error' )
		return False
		
	def return_key_db(self, logID, keyID, name, barcode):
		try:	
			self.cur.execute( "INSERT INTO ReturnedKey (log_id, key_ID, name, barcode) VALUES ( ?, ?, ?, ? )", (logID, keyID, name, barcode ) )
			self.conn.commit()
			return True
		except mariadb.InterfaceError:
			print( 'Connection Error' )
		return False
			
	def return_equipment_db(self, logID, equipmentID, name, barcode ):
		try:
			self.cur.execute( "INSERT INTO ReturnedEquipment (log_id, equipmentID, name, barcode) VALUES ( ?, ?, ?, ? )", (logID, equipmentID, name, barcode ) )
			self.conn.commit()
			return True
		except mariadb.InterfaceError:
			print( 'Connection Error' )
		return False
			
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
		self.cur.execute( "SELECT * FROM BorrowedKey WHERE log_id = ?", (log_id,) )
		res = self.cur.fetchall()
		if len(res) != 0:
			return res
		else:
			self.cur.execute( "SELECT * FROM BorrowedEquipment WHERE log_id = ?", (log_id, ) )
			res = self.cur.fetchall()
			if len(res) == 0:
				return None
			else:
				return res
				
	def get_all_not_returned_items(self):
		try:
			self.cur.execute( "SELECT BorrowLogs.log_id, BorrowLogs.q_lid, BorrowLogs.borrowDate, BorrowLogs.borrowTime, BorrowLogs.borrow_type FROM BorrowLogs LEFT JOIN ReturnLogs USING(log_id) WHERE ReturnLogs.log_id IS NULL")
			res = self.cur.fetchall()
			if len(res) == 0:
				return []
			return res
		except mariadb.InterfaceError:
			print( 'Possible error in fetching database borrow logs' )		
			
	def get_all_not_returned_keys(self, log_id):
		self.cur.execute( "SELECT * FROM BorrowedKey WHERE log_id = ?", ( log_id, ) )
		borrow_result = self.cur.fetchall()
		self.cur.execute( "SELECT * FROM ReturnedKey WHERE log_id = ?", (log_id, ) )
		return_result = self.cur.fetchall()
		temp_list = []
		
		if len(return_result) == 0:
			return borrow_result
		else:
			for element in borrow_result:
				if not element in return_result:
					temp_list.append( element )
					print( 'appended get' )
				else:
					print('Already here')
			return temp_list
		"""
		try:
			self.cur.execute( "SELECT BorrowedKey.log_id, BorrowedKey.key_ID, BorrowedKey.name, BorrowedKey.barcode  FROM BorrowedKey LEFT JOIN ReturnedKey USING (key_ID) WHERE ReturnedKey.log_id IS NULL AND BorrowedKey.log_id = ?", ( log_id,) )
			res = self.cur.fetchall()
			if res == None:
				return []
			return res
		except mariadb.InterfaceError:
			print( 'Database error in fetching database in borrow key' )
		"""
		
	def get_all_not_returned_equipments(self, log_id):
		self.cur.execute( "SELECT * FROM BorrowedEquipment WHERE log_id = ?", ( log_id, ) )
		borrow_result = self.cur.fetchall()
		self.cur.execute( "SELECT * FROM ReturnedEquipment WHERE log_id = ?", (log_id, ) )
		return_result = self.cur.fetchall()
		temp_list = []
		
		if len(return_result) == 0:
			return borrow_result
		else:
			for element in borrow_result:
				if not element in return_result:
					temp_list.append( element )
					print( 'appended get' )
				else:
					print('Already here')
			return temp_list
		"""
		try:																											#FROM BorrowedEquipment LEFT JOIN ReturnedEquipment USING(log_id) WHERE ReturnedEquipment.log_id IS NULL AND BorrowedEquipment.log_id = ?
			self.cur.execute("SELECT BorrowedEquipment.log_id, BorrowedEquipment.equipmentID, BorrowedEquipment.name, BorrowedEquipment.barcode FROM BorrowedEquipment LEFT JOIN ReturnedEquipment USING (key_ID) WHERE ReturnedEquipment.log_id IS NULL AND BorrowedEquipment.log_id = ?", (log_id,) )
			res = self.cur.fetchall()
			if res == None:
				return None
			return res
		except mariadb.InterfaceError:
			print( "Database error in equipments" )
		"""
			
	def check_not_returned(self, log_id): # this returns true if the item log is not in the returned db
		try:
			self.cur.execute(  "SELECT log_id, borrow_type FROM BorrowLogs LEFT JOIN ReturnLogs WHERE ReturnLogs.log_id IS NULL and BorrowLogs.log_id = ?", (log_id, ) )
			res = self.cur.fetchone()
			if res == None:
				return False
			return True
		except mariadb.InterfaceError:
			print( 'Database error in checking not returned' )
		
	def search_return_log(self, q_lid):
		try:
			 self.cur.execute( "SELECT * FROM ReturnLogs WHERE q_lid = ?", (q_lid,) )
			 res = self.cur.fetchall()
			 if len(res) == 0:
				 return None
			 return res
		except mariadb.InterfaceError:
			print( 'Database noir noir Error' )
	
	def search_return_log_dict(self, q_lid):
		try:
			res = self.search_return_log( q_lid )
			if res != None:
				log_dict = {}
				for log in res:
					log_dict[ log[ 0 ] ] = log
				return log_dict
			return {}
				
		except mariadb.InterfaceError:
			print( 'Database connection loss' )
		

	def get_employee_unreturned_items(self, q_lid):
		try:
			items_dict = defaultdict(list)
			res = self.search_return_log( q_lid )
			if res != None:
				for log in res:
					if log[4] == 'equipment':
						temp_items = self.get_all_not_returned_equipments( log[ 0 ] )
						for item in temp_items:
							item_details = borrowed_item.BorrowedItem()
							item_details.set_item( item[ 0 ], item[ 1 ], item[ 2 ], item[ 3 ] )
							items_dict[ f"{item[ 2 ]} {item[ 3 ]}" ].append( item_details )
								
					elif log[4] == 'key':
						temp_items = self.get_all_not_returned_keys( log[ 0 ] )
						for item in temp_items:
							item_details = borrowed_item.BorrowedItem()
							item_details.set_item( item[ 0 ], item[ 1 ], item[ 2 ], item[ 3 ] )
							items_dict[f"{item[ 2 ]} {item[ 3 ]}"].append( item_details )

				for k, val in items_dict.items():
					for j in val:
						print( f"{j.barcode} {j.name}" )
				
				return items_dict
			else:
				return None
		except mariadb.InterfaceError:
			print( 'Database error/timeout' )
			
	def get_all_logs_range(self, start_date, end_date):
		try:
			self.cur.execute('SELECT * FROM BorrowLogs WHERE borrowDate BETWEEN (?) and (?)', (start_date, end_date))
			res = self.cur.fetchall()
			if len(res) == 0:
				return None
			else:
				return res
		except:
			print('An error occurred in getting the logs range')
			
	def search_return_log_by_id(self, log_id):
		try:
			self.cur.execute('SELECT * FROM ReturnLogs WHERE log_id = (?)', (log_id,))
			res = self.cur.fetchone()
			if res is None:
				return None
			else:
				return res
		except:
			print('An error occurred in retrieving return logs')
	
	def get_borrowed_keys_by_id(self, log_id):
		try:
			self.cur.execute('SELECT * FROM BorrowedKey WHERE log_id = ?', (log_id,))
			res = self.cur.fetchall()
			if len(res) == 0:
				return None
			else:
				return res
		except:
			print('An error occurred while retrieved borrowed keys')
			
	def get_returned_keys_by_id(self, log_id):
		try:
			self.cur.execute('SELECT * FROM ReturnedKey WHERE log_id = ?', (log_id,))
			res = self.cur.fetchall()
			if len(res) == 0:
				return None
			else:
				return res
		except:
			print('An error occurred while retrieved borrowed keys')
			
	def get_borrowed_equipment_by_id(self, log_id):
		try:
			self.cur.execute('SELECT * FROM BorrowedEquipment WHERE log_id = ?', (log_id,))
			res = self.cur.fetchall()
			if len(res) == 0:
				return None
			else:
				return res
		except:
			print('An error occurred while retrieved borrowed keys')
			
	def get_returned_equipment_by_id(self, log_id):
		try:
			self.cur.execute('SELECT * FROM ReturnedEquipment WHERE log_id = ?', (log_id,))
			res = self.cur.fetchall()
			if len(res) == 0:
				return None
			else:
				return res
		except:
			print('An error occurred while retrieved borrowed keys')
			
	def search_borrow_log_by_id(self, log_id):
		try:
			self.cur.execute('SELECT * FROM BorrowLogs WHERE log_id = (?)', (log_id,))
			res = self.cur.fetchone()
			if res is None:
				return None
			else:
				return res
		except:
			print('An error occurred in retrieving return logs')
			
	
			
	
	
