class NcrKeys:
	def __init__(self):
		self.key_id = 0
		self.barcode = ''
		self.unit = ''
		self.description = ''
		self._isDeleted = 0
		
	def read_barcode(self, barcode):
		if self.barcode == barcode:
			return true
		else:
			return false
	
	def set_ncr_key(self, barcode, unit, description = '', key_id = 0):
		self.barcode = barcode
		self.unit = unit
		self.key_id = key_id
		self.description = description
		
	def deactivate_key(self):
		self._isDeleted = 1
		
	def activate_key(self):
		self._isDeleted = 0
	
	def ncr_key_accepted(self):
		return self.barcode != '' and self.unit != ''
