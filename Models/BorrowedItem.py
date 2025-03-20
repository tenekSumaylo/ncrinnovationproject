class BorrowedItem:
	def __init__(self):
		self.log_id = ''
		self.item_id = ''
		self.name = ''
		self.barcode = ''
		
	def set_item(self, log_id, item_id, name, barcode):
		self.log_id = log_id
		self.item_id = item_id
		self.name = name
		self.barcode = barcode
		
	def to_string(self):
		return f"{self.item_id} - {self.name} - {self.log_id}"
	
