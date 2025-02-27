import telethon
import os
import config
import json
import models

class ControlBD():
	def __init__(self, conf:config.Config) -> None:
		self.namefile_bd = conf.get("file_log")

	def ping_connection_bd(self) -> None:
		if self.is_exists_file() == False:
			with open(self.namefile_bd, "w") as bd:
				bd.close()
	
	def is_exists_file(self) -> bool:
		return os.path.isfile(self.namefile_bd)

	# def json_dump_array_dialogs(self, temp_array_dialogs_json:list[models.ModelDialog]) -> None:
	# 	with open(self.namefile_bd, 'w', encoding='utf-8') as file:
	# 		json.dump(temp_array_dialogs_json, file, ensure_ascii=False, indent=4)

	def rename_image(self, old_name_image:str, new_name_image:str) -> None:
		try:os.rename(old_name_image, new_name_image)
		except Exception as e: print(e)

	def remove_cache_image(self) -> None:
		try:os.remove(self.path_image_cache)
		except Exception as e: print(e)
		try:os.makedirs(self.path_image_cache)
		except Exception as e: print(e)
		try:os.remove(self.namefile_bd)
		except Exception as e: print(e)
		try:open(self.namefile_bd, "w").close()
		except Exception as e: print(e)
	
