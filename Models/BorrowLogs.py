import datetime
from datetime import time

class BorrowLogs:
	def __init__(self):
		self.log_id = 0
		self.q_lid = ''
		self.borrow_date = datetime.datetime.now()
		self.borrow_time = time(self.borrow_date.hour, self.borrow_date.minute, self.borrow_date.second )
		self.borrow_list = []
		
	def set_borrow_logs(self, q_lid, borrow_list, log_id = 0):
		self.q_lid = q_lid
		self.log_id = log_id
		self.borrow_list = borrow_list
	
	def set_borrow_logs_view( self, log_id, q_lid, borrow_date, borrow_time, borrow_list ):
		self.log_id = log_id
		self.q_lid = q_lid
		self.borrow_date = borrow_date
		self.borrow_time = borrow_time
		self.borrow_list = borrow_list
		
		
