class LogsViewModel:
	def __init__(self, log_id, borrowed_date, returned_date, first_name, last_name):
		self.log_id = log_id
		self.borrowed_date = borrowed_date
		self.returned_date = returned_date
		self.borrowed_item = []
		self.returned_item = []
		self.first_name = first_name
		self.last_name = last_name

