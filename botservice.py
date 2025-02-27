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

import config
from models import *
################################

msgcode1 = "вход как админ"
msgcode2 = "запуск сендера"
msgcode3 = "запуск бота"
msgcode4 = "не найден в базе"
msgcode5 = "остановка бота"

class BotService():
	def __init__(self, conf, chan, storage_users):
		self.conf = conf
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
		def start(message):
			self.chan.put("start")
			mcid = message.chat.id
			username = message.from_user.first_name
			self.add_log(self.rec_event(mcid,msgcode3))
			mcid = int(mcid) 
			for user in self.storage_users.data:
				if str(mcid) == str(user.chat_id):
					return

			self.add_log(self.rec_event(mcid,msgcode4))
			self.storage_users.data.append(RowRecordUser(len(self.storage_users.data),username,mcid,"Люди",str(datetime.now())))
			self.save_userdb(self.storage_users.data)
			self.bot.send_message(mcid,text="Управление",reply_markup=panel_user_menu())

					
		@bot.message_handler(content_types=['text'])
		def func(message):			

			mcid = message.chat.id
			mt = message.text
			mn = message.from_user.first_name
				
			if mt == "Запустить":
				for user in self.storage_users.data:
					if str(user.chat_id) == str(mcid):
						user.flagStarted = True
						self.run_sender(user, mcid)   
					
			if mt == "Остановить" or mt == "/abort":
				for user in self.storage_users.data:
					if str(user.chat_id) == str(mcid):
						user.flagStarted = False
				self.add_log(self.rec_event(mcid,msgcode5))
						
			if mt == self.flagPswdAdmin:
				self.flagAdminID = mcid  
				self.add_log(self.rec_event(mcid,msgcode1))
				self.bot.send_message(mcid,text="Режим Администратора",reply_markup=panel_admin_menu())    	
			
			if self.flagAdminID != mcid: return
			
			if str(mt).startswith("ID:"):
				val_id = int(mt.split("ID:")[1].split(':')[0])
				self.flagSelectedID = val_id
				self.bot.send_message(mcid,text=val_id,reply_markup=panel_admin_set_value())
				
			elif str(mt).startswith("+"):
				val_set = mt
				self.flagSelectedValue = val_set
				t = f"Применить ?\n\nID:{self.flagSelectedID}\n{self.flagSelectedValue}"
				self.add_log(self.rec_event(mcid,"изменил доступ на:"+self.flagSelectedValue))
				self.bot.send_message(mcid,text=t,reply_markup=panel_admin_set_value())
		
				
			elif mt == "Меню":
				self.bot.send_message(mcid,text="ок",reply_markup=panel_admin_menu())    	
			elif mt == "Управление доступом":
				self.bot.send_message(mcid,text="Список Users ID",reply_markup=panel_admin_users(self.storage_users.data))      	
			elif mt == "Сохранить":
				for user in self.storage_users.data:
					if str(user.chat_id) == str(self.flagSelectedID):
						user.category = self.flagSelectedValue
				self.save_userdb(self.storage_users.data)
				self.add_log(self.rec_event(mcid,"сохранен с задачей"+self.flagSelectedValue))
				self.bot.send_message(mcid,text="Выполнено !",reply_markup=panel_admin_users(self.storage_users.data))  
				
			elif mt == "Отчет логи":
				data = self.read_logs() 
				c = 0
				s = ""
				for line in data:
					c+=1
					if c >= 30: break
					s += line+"\n"  	
				self.bot.send_message(mcid,text=f"{s}",reply_markup=panel_admin_menu())
			elif mt == "Отчет пользователи":
				data = self.read_userdb() 
				s = ""
				for line in data:
					s += line+"\n\n"  	
				self.bot.send_message(mcid,text=f"{s}",reply_markup=panel_admin_menu())
			elif mt == "Отчет по ссылкам":
				self.bot.send_message(mcid,text=f"{self.about_links()}",reply_markup=panel_admin_menu())    


	def about_links(self):
		s = ""
		for c in category_links():
			s += f"{c} {get_count_pages(category_links()[c])} x 10\n\n"		
		return s


	def rec_event(self, mcid,log):
		return f"[{datetime.now()}] [{mcid}] [{log}]" 

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

	def run_sender(self, user, mcid):
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
