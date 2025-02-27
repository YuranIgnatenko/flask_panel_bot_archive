import json

class Config():
	def __init__(self, namefile:str) -> None:
		self.namefile = namefile
		with open(namefile, 'r') as f:
			self.data = json.load(f)

	def to_dict(self) -> dict:
		return self.data
		
	def to_str(self) -> str:
		with open(self.namefile, "r") as temp_file: return temp_file.read()

	def get(self, key:str) -> str:
		return f"{self.to_dict()[key]}"

	# def replace_save(self, key:str, value:str) -> None:
	# 	self.data[key] = value
	# 	with open(namefile, 'w') as f:
	# 		self.data = json.load(f)


