class NcrEmployees:
	def __init__(self):
		self.q_lid = ''
		self.first_name = ''
		self.last_name = ''
		self.is_active = 1
		self.rfid = ''
		
	def set_ncr_employee(self, q_lid, first_name, last_name, is_active, rfid ):
		self.q_lid = q_lid
		self.first_name = first_name
		self.last_name = last_name
		self.is_active = is_active
		self.rfid = rfid
	
	def deactivate_employee(self):
		self.is_active = 0
	
	def activate_employee(self):
		self.is_active = 1
		
	def employee_is_acceptable(self):
		return self.q_lid != '' and self.first_name != '' and self.last_name != '' and self.rfid != '' 
	
