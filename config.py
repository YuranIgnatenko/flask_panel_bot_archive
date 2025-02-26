import json

class Config():
	def __init__(self, namefile:str) -> None:
		with open(namefile, 'r') as f:
			self.data = json.load(f)
	def to_dict(self) -> dict:
		return self.data
	def get(self, key:str) -> str:
		return f"{self.to_dict()[key]}"
