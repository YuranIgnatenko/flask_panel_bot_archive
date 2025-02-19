class Conf():
	def __init__(self, namefile="config.txt"):
		self.namefile_config = namefile
		self.namefile_users = "users.txt"
		self.namefile_historylogs = "historylogs.txt"

		access_keys = ['bot_token', "bot_admin_password", "bot_name", "bot_last_started", "bot_status"]
		
		with open(namefile, "r") as file:
			data = file.read().split("\n")
		for row in data:
			param, value = row.split("---")[0],row.split("---")[1]
			if param not in access_keys:
				print(f"error key: {param} from file: {namefile} in line: {row}")
				continue
			if param == "bot_token":
				self.bot_token = value
			elif param == "bot_name":
				self.bot_name = value
			elif param == "bot_last_started":
				self.bot_last_started = value
			elif param == "bot_status":
				self.bot_status = value
			elif param == "bot_admin_password":
				self.bot_admin_password = value
	def save(self):
		data = f"""bot_token---{self.bot_token}
bot_name---{self.bot_name}
bot_last_started---{self.bot_last_started}
bot_status---{self.bot_status}
bot_admin_password---{self.bot_admin_password}"""

		with open(self.namefile, "w") as file:
			file.write(data)

	def reset(self):
		self.bot_token = "8165343589:AAE_GUvzzXA1u-JOV4WK0SUanzryndnbVnc"
		self.bot_name = "@name_bot"
		self.bot_last_started = "00:00:00"
		self.bot_status = "off"
		self.bot_admin_password = "1234@"


