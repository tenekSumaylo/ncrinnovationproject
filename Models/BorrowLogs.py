import datetime

class BorrowLogs:
	def __init__(self):
		self.log_id = 0
		self.q_lid = ''
		self.borrow_date = datetime.datetime.now().strftime('%x')
		self.borrow_time = datetime.datetime.now().strftime('%I:%M:%S %p')
		
	def set_borrow_logs(self, q_lid, borrow_date, borrow_time, log_id = 0):
		self.q_lid = q_lid
		self.borrow_date = borrow_date
		self.borrow_time = borrow_time
		self.log_id = log_id
		
		
