from config import Config

class RowRecordLog():
	def __init__(self, row_data_dict:dict) -> None:
		self.key = row_data_dict['key']
		self.date = row_data_dict['date']
		self.chat_id = row_data_dict['chat_id']
		self.info = row_data_dict['info']

class RowRecordUser():
	def __init__(self, row_data_dict:dict) -> None:
		self.key = row_data_dict['key']
		self.username = row_data_dict['username']
		self.chat_id = row_data_dict['chat_id']
		self.date = row_data_dict['date']
		self.category = row_data_dict['category']
		self.flagStarted = False

class RowRecordImage():
	def __init__(self, row_data_dict:dict) -> None:
		self.category = row_data_dict["category"]
		self.link = row_data_dict["link"]

class StorageRowRecordImages():
	def __init__(self) -> None:
		self.rows = []
	def add(self, row:RowRecordImage):
		self.rows.append(row)

class StorageRowRecordUsers():
	def __init__(self) -> None:
		self.namefile = "users.txt"
		self.rows = []
	def resave(self):
		pass
	def add(self, row:RowRecordUser) -> None:
		self.rows.append(row)

class StorageRowRecordLogs():
	def __init__(self) -> None:
		self.rows = []
	def add(self, row:RowRecordLog) -> None:
		self.rows.append(row)

class DataImage():
	def __init__(self, index, link):
		self.index = index
		self.link = link
		