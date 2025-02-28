from telebot import types, TeleBot

import os,sys,random,time,queue

from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pyshorteners, requests

import logging

from config import Config
from parser_service import ParserSpcs
from storage import StorageJson, StorageTxt
from telegram_bot_markup import *

class TelegramBotService():
	def __init__(self, chan:queue.Queue, conf:Config) -> None:
		self.chan = chan
		self.conf_base = conf
		self.conf_categories = Config(self.conf_base.get("file_categories"))
		self.conf_users = Config(self.conf_base.get("file_users"))
		self.name_categories = self.conf_categories.data.keys()
		self.conf_base.bot_token = self.conf_base.get("bot_token")

		self.parser = ParserSpcs(self.conf_base)

		self.storage_users = StorageJson(self.conf_base.get("file_users"))
		self.flagSelectedID = 0
		self.flagSelectedValue = ""
		self.flagFileUsers = self.conf_base.get("file_users")
		self.flagFileHistoryLogs = self.conf_base.get("file_log")
		self.flagPswdAdmin = self.conf_base.get("bot_admin_password")
		self.flagAdminID = 0
		self.flagStarted = False

		bot = TeleBot(self.conf_base.bot_token)
		self.bot = bot

		@bot.message_handler(commands=['start'])
		def start(message) -> None:
			self.chan.put("start")
			msg_chat_id = int(message.chat.id)
			msg_user_name = message.from_user.first_name

			logging.info(f"started user:{msg_chat_id}")

			if self.storage_users.find_item_as_str("chat_id", msg_chat_id) == False:
				self.storage_users.add_user(msg_user_name, msg_chat_id, "none")

			self.bot.send_message(msg_chat_id,text="Управление",reply_markup=panel_user_menu())

					
		@bot.message_handler(content_types=['text'])
		def func(message) -> None:			
			msg_chat_id = message.chat.id
			mt = message.text
			mn = message.from_user.first_name
				
			if mt == "Запустить":
				for user_dict in self.storage_users.conf.data:
					if str(user_dict["chat_id"]) == str(msg_chat_id):
						self.flagStarted = True
						self.run_sender(user_dict, msg_chat_id)   
					
			if mt == "Остановить" or mt == "/abort":
				for user in self.storage_users.conf.data:
					if str(user["chat_id"]) == str(msg_chat_id):
						self.flagStarted = False
						logging.info("aborted")				
						
			if mt == self.flagPswdAdmin:
				self.flagAdminID = msg_chat_id  
				logging.info("admin mode is ok")
				self.bot.send_message(msg_chat_id,text="Режим Администратора",reply_markup=panel_admin_menu())    	
			
			
			if str(mt).startswith("ID:"):
				val_id = int(mt.split("ID:")[1].split(':')[0])
				self.flagSelectedID = val_id
				self.bot.send_message(msg_chat_id,text=val_id,reply_markup=panel_admin_set_value(self.name_categories))
				
			if str(mt) in self.name_categories:
				val_set = mt
				self.flagSelectedValue = val_set
				t = f"Применить ?\n\nID:{self.flagSelectedID}\n{self.flagSelectedValue}"
				logging.info(f"{msg_chat_id} изменил доступ на: {self.flagSelectedValue}")
				self.bot.send_message(msg_chat_id,text=t,reply_markup=panel_admin_ask_yes_no())
					

			if mt == "Для разработчика":
				for user in self.storage_users.conf.data: 
					if str(user["chat_id"]) == str(msg_chat_id) and str(user["admin"] == "1"):
						self.flagAdminID = msg_chat_id  
						logging.info("admin mode is ok")
						self.bot.send_message(msg_chat_id,text="Вы используете доп меню",reply_markup=panel_admin_menu())
						return
					else:
						self.bot.send_message(msg_chat_id,text="Требуется ключ",reply_markup=panel_admin_menu()) 
				return   

			if mt == "Меню":
				self.bot.send_message(msg_chat_id,text="ок",reply_markup=panel_admin_menu())    	
			if mt == "Управление доступом":
				self.bot.send_message(msg_chat_id,text="Список Users ID",reply_markup=panel_admin_users(self.conf_users.to_dict()))      	
			if mt == "yes":
				self.conf_users.rewrite_user_category(self.flagSelectedID,self.flagSelectedValue)					

				logging.info(f"{msg_chat_id},сохранен с задачей {self.flagSelectedValue}")
				self.bot.send_message(msg_chat_id,text="Выполнено !",reply_markup=panel_admin_menu())  
				
			
			if mt == "Отчет пользователи":
				data = self.conf_users.to_str()
				self.bot.send_message(msg_chat_id,text=f"{data}",reply_markup=panel_admin_menu())
			if mt == "Отчет категории":
				data = self.conf_categories.to_str()
				self.bot.send_message(msg_chat_id,text=f"{data}",reply_markup=panel_admin_menu())
			if mt == "Отчет конфигурация":
				data = self.conf_base.to_str()
				self.bot.send_message(msg_chat_id,text=f"{data}",reply_markup=panel_admin_menu())

	def add_log(self, record):
		with open(self.flagFileHistoryLogs, 'a')as file:
			file.write(f"{record}\n")

	def read_logs(self):
		try:
			with open(self.flagFileHistoryLogs, 'r')as file:
				data = file.read().split("\n")
				return data[-20:-1]
		except FileNotFoundError as e:
			logging.error(e)
			open(self.flagFileHistoryLogs, 'w')
			return


	def save_userdb(self,users):
		with open(self.flagFileUsers, 'w')as file:
			for user in users:
				file.write(f"{user.username}---{user.chat_id}---{user.category}---{user.date}\n")

	def read_userdb(self):
		try:
			with open(self.flagFileUsers, 'r')as file:
				data = file.read().split("\n")
				return data
		except FileNotFoundError:
			open(self.flagFileUsers, 'w')
			return

	def run_sender(self, user_dict, msg_chat_id):
		logging.info("run sender")
		tmp_b = 0
		tmp_a = random.randint(0,tmp_b)
		tc = 0
		iter_c = 10000
		name = user_dict["category"]
		for i in range(iter_c):
			if self.flagStarted == False:
				return 1
			tc += 1
			out = self.parser.get_url_random_page_from_category(name)
			try:		        	
				self.bot.send_photo(user_dict["chat_id"],urlopen(out, timeout=5))	 
			except Exception as e:
				logging.error(e)

	### commands /Any*


	
	def polling(self):
		self.bot.polling(none_stop=True)


def main() -> None:
	if len(sys.argv) > 1:
		arg_namefile_config = sys.argv[1]
		conf_base = Config(sys.argv[1])

		logging.basicConfig(filename=conf_base.get("file_log"), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

		chan_signal_work_status = queue.Queue()
		
		bot_service = TelegramBotService(chan_signal_work_status, conf_base)
		bot_service.polling()


if __name__ == "__main__":main()