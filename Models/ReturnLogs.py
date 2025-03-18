class ReturnLogs:
	def __init__(self):
		self.log_id = 0
		self.q_lid = ''
		self.return_date = datetime.datetime.now().strftime('%x')
		self.return_time = datetime.datetime.now().strftime('%I:%M:%S %p')
		
	def set_borrow_logs(self, q_lid, return_date, return_time, log_id = 0):
		self.q_lid = q_lid
		self.return_date = return_date
		self.return_time = return_time
		self.log_id = log_id
