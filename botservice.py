''' 
Dev : G E O R G 

''' 

import telebot,random,time
from telebot import types 

import requests
from bs4 import BeautifulSoup

import pyshorteners

import os,sys
from datetime import datetime
from parserservice import *
from urllib.request import urlopen

import queue
from models import *
import logger
import bd
import config
################################

msgcode1 = "вход как админ"
msgcode2 = "запуск сендера"
msgcode3 = "запуск бота"
msgcode4 = "не найден в базе"
msgcode5 = "остановка бота"

class BotService():
	def __init__(self, chan:queue.Queue, conf:config.Config, log:logger.Logger, ctrl_bd:bd.ControlBD, storage_users:StorageRowRecordUsers) -> None:
		self.conf = conf
		self.log = log
		self.ctrl_bd = ctrl_bd
		self.chan = chan
		self.conf.bot_token = self.conf.get("bot_token")
		self.flagSelectedID = 0
		self.flagSelectedValue = ""
		self.storage_users = storage_users
		self.flagFileUsers = self.conf.get("file_users")
		self.flagFileHistoryLogs = self.conf.get("file_log")
		self.flagPswdAdmin = self.conf.get("bot_admin_password")
		self.flagAdminID = 0

		bot = telebot.TeleBot(self.conf.bot_token)
		self.bot = bot

		@bot.message_handler(commands=['start'])
		def start(message) -> None:
			self.chan.put("start")

			msg_chat_id = int(message.chat.id)
			msg_user_name = message.from_user.first_name
			# self.add_log(self.rec_event(msg_chat_id,msgcode3))
			for user in self.storage_users.data:
				if str(msg_chat_id) == str(user.chat_id):
					return

			self.add_log(self.rec_event(msg_chat_id,msgcode4))
			self.storage_users.data.append(RowRecordUser(len(self.storage_users.data),msg_user_name,msg_chat_id,"Люди",str(datetime.now())))
			self.save_userdb(self.storage_users.data)
			self.bot.send_message(msg_chat_id,text="Управление",reply_markup=panel_user_menu())

					
		@bot.message_handler(content_types=['text'])
		def func(message) -> None:			

			msg_chat_id = message.chat.id
			mt = message.text
			mn = message.from_user.first_name
				
			if mt == "Запустить":
				for user in self.storage_users.data:
					if str(user.chat_id) == str(msg_chat_id):
						user.flagStarted = True
						self.run_sender(user, msg_chat_id)   
					
			if mt == "Остановить" or mt == "/abort":
				for user in self.storage_users.data:
					if str(user.chat_id) == str(msg_chat_id):
						user.flagStarted = False
				self.add_log(self.rec_event(msg_chat_id,msgcode5))
						
			if mt == self.flagPswdAdmin:
				self.flagAdminID = msg_chat_id  
				self.add_log(self.rec_event(msg_chat_id,msgcode1))
				self.bot.send_message(msg_chat_id,text="Режим Администратора",reply_markup=panel_admin_menu())    	
			
			if self.flagAdminID != msg_chat_id: return
			
			if str(mt).startswith("ID:"):
				val_id = int(mt.split("ID:")[1].split(':')[0])
				self.flagSelectedID = val_id
				self.bot.send_message(msg_chat_id,text=val_id,reply_markup=panel_admin_set_value())
				
			elif str(mt).startswith("+"):
				val_set = mt
				self.flagSelectedValue = val_set
				t = f"Применить ?\n\nID:{self.flagSelectedID}\n{self.flagSelectedValue}"
				self.add_log(self.rec_event(msg_chat_id,"изменил доступ на:"+self.flagSelectedValue))
				self.bot.send_message(msg_chat_id,text=t,reply_markup=panel_admin_set_value())
		
				
			elif mt == "Меню":
				self.bot.send_message(msg_chat_id,text="ок",reply_markup=panel_admin_menu())    	
			elif mt == "Управление доступом":
				self.bot.send_message(msg_chat_id,text="Список Users ID",reply_markup=panel_admin_users(self.storage_users.data))      	
			elif mt == "Сохранить":
				for user in self.storage_users.data:
					if str(user.chat_id) == str(self.flagSelectedID):
						user.category = self.flagSelectedValue
				self.save_userdb(self.storage_users.data)
				self.add_log(self.rec_event(msg_chat_id,"сохранен с задачей"+self.flagSelectedValue))
				self.bot.send_message(msg_chat_id,text="Выполнено !",reply_markup=panel_admin_users(self.storage_users.data))  
				
			elif mt == "Отчет логи":
				data = self.read_logs() 
				c = 0
				s = ""
				for line in data:
					c+=1
					if c >= 30: break
					s += line+"\n"  	
				self.bot.send_message(msg_chat_id,text=f"{s}",reply_markup=panel_admin_menu())
			elif mt == "Отчет пользователи":
				data = self.read_userdb() 
				s = ""
				for line in data:
					s += line+"\n\n"  	
				self.bot.send_message(msg_chat_id,text=f"{s}",reply_markup=panel_admin_menu())
			elif mt == "Отчет по ссылкам":
				self.bot.send_message(msg_chat_id,text=f"{self.about_links()}",reply_markup=panel_admin_menu())    


	def about_links(self):
		s = ""
		for c in category_links():
			s += f"{c} {get_count_pages(category_links()[c])} x 10\n\n"		
		return s


	def rec_event(self, msg_chat_id,log):
		return f"[{datetime.now()}] [{msg_chat_id}] [{log}]" 

	def add_log(self, record):
		with open(self.flagFileHistoryLogs, 'a')as file:
			file.write(f"{record}\n")

	def read_logs(self):
		try:
			with open(self.flagFileHistoryLogs, 'r')as file:
				data = file.read().split("\n")
				return data
		except FileNotFoundError:
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

	def run_sender(self, user, msg_chat_id):
		self.add_log(self.rec_event(user.chat_id,msgcode2))
		tmp_b = 0
		tmp_a = random.randint(0,tmp_b)
		tc = 0
		iter_c = 10000
		name = user.category
		for i in range(iter_c):
			if user.flagStarted == False:
				return 1
			tc += 1  	
			db_visit_name[user.chat_id] = name
			url,r_page,r_href = get_r_page_href(name)
			out = get_href_content_online(url,r_page,r_href)
			try:		        	
				self.bot.send_photo(user.chat_id,urlopen(out, timeout=5))	 
			except Exception as e:
				pass

	### commands /Any*


	
	def polling(self):
		self.bot.polling(none_stop=True)

print('launch server')
print("bot listen")
