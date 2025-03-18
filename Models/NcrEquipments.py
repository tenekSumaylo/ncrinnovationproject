class NcrEquipments:
	def __init__(self):
		self.equipment_id = 0
		self.tool_name = ''
		self.barcode = ''
		self.date_of_acquisition = ''
		self.calibration_date = '' 
		self.description = ''
		self.is_deleted = 0
		
	def set_ncr_equipment(self, tool_name, barcode, date_of_acquisiton, calibration_date, description, equipment_id = 0, is_deleted = 0):
		self.equipment_id = equipment_id
		self.tool_name = tool_name
		self.barcode = barcode
		self.date_of_acquisition = date_of_acquisition
		self.calibration_date = calibration_date
		self.description = description
		self.is_delete = is_deleted
		
	def deactivate_equipment(self):
		self.is_deleted = 1
	
	def activate_equipment(self):
		self.is_deleted = 0
		
	def ncr_equipment_accepted(self):
		return self.tool_name != '' and self.barcode != ''
