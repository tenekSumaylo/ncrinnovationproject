import datetime
from datetime import time 
class ReturnLogs:
	def __init__(self):
		self.log_id = 0
		self.q_lid = ''
		self.return_date = datetime.datetime.now()
		self.return_time = time( self.return_date.hour, self.return_date.minute, self.return_date.second )
		self.borrow_type = ''
		self.return_dict = {}
		
	def set_borrow_logs(self, q_lid, borrow_type, return_dict, log_id = 0):
		self.q_lid = q_lid
		self.log_id = log_id
		self.borrow_type = borrow_type
		self.return_dict = return_dict
		
	def set_borrow_logs_view(self, q_lid, return_date, return_time, borrow_type, return_dict, log_id = 0):
		self.q_lid = q_lid
		self.return_date = return_date
		self.return_time = return_time
		self.log_id = log_id
		self.borrow_type = borrow_type
		self.return_dict = return_dict
