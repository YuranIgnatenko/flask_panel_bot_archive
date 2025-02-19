
import telebot
from telebot import types 
from parserservice import *

def key(text):return types.KeyboardButton(text)

def key_status(a,b,c,d,name):
	a,b,c,d = int(a),int(b),int(c),int(d)
	ks = [
		key(f"Папка: {name}"),
		key(f"Получено: {c} из {d} ( {int(((c-1)/d)*100)} %)"),
		key(f"Файл в папке: {a} из {b}"),
	]
	return ks


def key_short_info(a,b,name):
	a,b = int(a),int(b)
	ks = [
		key(f"Папка: {name}"),
		key(f"Файл: {a} из {b}"),
	]
	return ks	

def panel_status(a,b,c,d,name):
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for k in key_status(a,b,c,d,name):
		table.row(k)
	return table
	
	
def panel_status_short(a,b,name):
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for k in key_short_info(a,b,name):
		table.row(k)
	return table

def panel_control_visit(a,b,c,d,name):
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for k in key_short_info(a,b,name):
		table.row(k)
	table.row(key("Случайная online"))	
	table.row(key("Случайная offline"))
	table.row(key("-15"),key("+15"))
	table.row(key("-5"),key("+5"))
	table.row(key("-1"),key("+1"))

	table.row(key("Меню"))
	return table

def panel_category_list():
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for key in category:
		table.row(types.KeyboardButton(key))
	table.row(types.KeyboardButton('Меню'))
	return table     
 
		   
def panel_menu():
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("Запуск сендера"))
	table.row(key("Online подборка"))
	table.row(key("Offline подборка"))
	table.row(key("Папки с файлами"))
	table.row(key("Настройки бота"))
	return table                      
		   
def panel_settings_bot():
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("Обновление (последнее)"))
	table.row(key("Обновление (случайный день)"))
	table.row(key("Обновление (случайная неделя)"))
	table.row(key("Отчет по хранилищу"))
	table.row(key("Форматировать хранилище"))
	table.row(key("Меню"))
	return table   
	
	
def panel_status_update(a,b,c,d,name,count_all):
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key(f"Обновление: (получено: {count_all})"))
	table.row(key(f"Файлов: {a} из {b} ( {int(((a-1)/b)*100)} %)"))
	table.row(key(f"Папка ({name}): {c} из {d} ( {int(((c-1)/d)*100)} %)"))
	return table	
	
def panel_status_storage(sum_u,sum_f,sum_c,datefile,sizefile,updateflag):
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key(f"Сумма пользователей: {sum_u}"))
	table.row(key(f"Сумма файлов базы: {sum_f}"))
	table.row(key(f"Кол-во разделов в базе: {sum_c}"))
	table.row(key(f"Дата последнего обновления: {datefile}"))
	table.row(key(f"Размер обновления: {sizefile} Кбайт"))
	table.row(key(f"Наличие обновления: {updateflag}"))
	table.row(key(f'Меню'))
	
	return table	
	
	
def panel_control_visit_online(name,rp,rh):
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key(f"Папка online: {name}"))
	table.row(key(f"Адрес файла: {rp}.{rh}"))
	table.row(key("Следующая"))
	table.row(key("Меню"))
	return table                      
		   	
	
	
def panel_control_pack_online(name,rp,rh,i,j):
	percent = round(i/j*100,2)
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key(f"Папка online: {name}"))
	table.row(key(f"Адрес файла: {rp}.{rh}"))
	table.row(key(f"Получено: {i}/{j} ({percent}%)"))
	return table        	


def panel_no_access_menu():
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("Отправить заявку"))
	return table    		
		
				
def panel_user_menu():
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("Запустить"))
	table.row(key("Остановить"))
	table.row(key("Помощь и связь"))
	return table    			
	
def panel_admin_menu():
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("Запустить"))
	table.row(key("Остановить"))
	table.row(key("Управление доступом"))
	table.row(key("Отчет логи"))
	table.row(key("Отчет по ссылкам"))
	table.row(key("Отчет пользователи"))
	return table    

def panel_admin_users(storage_users):
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for user in storage_users:
		table.row(key(f"ID:{str(user.chat_id)}:{user.category}"))
	table.row("Меню")
	return table  

def panel_admin_set_value():
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("+Люди"))
	table.row(key("+Аниме"))
	table.row(key("+Обои ПК"))
	table.row(key("+Юмор"))
	table.row(key("+Абстракции"))
	table.row(key("+Архитектура"))
	table.row(key("+Космос"))
	table.row(key("+AI арт"))
	table.row(key("+Звезды"))
	table.row("+Ограничить доступ")
	table.row(key("Сохранить"))
	table.row(key("Меню"))
	return table    		
	
	
"+Юмор и Мемы",
"+Разное",
"+Обои ПК",
"+Абстрактное",
"+Аниме",
"+Архитектура",
"+Космос",
"+Животные",
"+AI арт",
"+Люди",	
	