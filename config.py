import json

class Config():
	def __init__(self, namefile:str) -> None:
		self.namefile = namefile
		try:
			with open(namefile, 'r', encoding='utf-8') as file:
				self.data = json.load(file)
		except json.decoder.JSONDecodeError:
			with open(namefile, 'w', encoding='utf-8') as file:
				file.write("[]")
				self.data = []

	def to_dict(self) -> dict:
		return self.data
		
	def to_str(self) -> str:
		with open(self.namefile, "r", encoding='utf-8') as temp_file: return temp_file.read()

	def get(self, key:str) -> str:
		return f"{self.data[key]}"
	
	def rewrite_from_str(self, str_data:str) -> None:
		dict_data = json.loads(str_data)
		with open(self.namefile, 'w', encoding='utf-8') as f:
			json.dump(dict_data, f, ensure_ascii=False, indent=4)

	def rewrite(self, dict_data:dict) -> None:
		with open(self.namefile, 'w', encoding='utf-8') as f:
			json.dump(dict_data, f, ensure_ascii=False, indent=4)

	def resave(self) -> None:
		with open(self.namefile, 'w', encoding='utf-8') as f:
			json.dump(self.data, f, ensure_ascii=False, indent=4)

	def rewrite_user_category(self, id_user:str, category:str) -> None:
		c = 0
		for user in self.data:
			if str(self.data[c]["chat_id"]) == str(id_user):
				self.data[c]["category"] = category
				self.resave()
				self.rewrite(self.data)
			c+=1




