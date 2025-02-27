import os
import time
import config

class Logger():
	def __init__(self, conf:config.Config) -> None:
		self.namefile = conf.get("file_log")
		self.connect_file()

	def is_exists_file(self) -> bool:
		return os.path.isfile(self.namefile)

	def connect_file(self) -> None:
		if self.is_exists_file == False:
			with open(self.namefile, "w+") as file:
				file.read() 
	
	def add(self, line:any) -> None:
		try:
			with open(self.namefile, "a") as file:
				file.write(f"{time.asctime()} [{line}]\n")
		except:
			with open(self.namefile, "a") as file:
				file.write(f"{time.asctime()} [indef move]\n")