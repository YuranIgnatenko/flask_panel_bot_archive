from telebot import types 
from parser_service import *

def key(text:str) -> types.KeyboardButton:
	return types.KeyboardButton(text)

def key_status(name_category:str, index_element:int, all_count_element:int) -> list[types.KeyboardButton]:
	array_keys = [
		key(f"Папка: {name_category}"),
		key(f"Получено: {index_element} из {all_count_element} ( {int(((index_element-1)/all_count_element)*100)} %)"),
	]
	return array_keys

def key_short_info(name_category:str, index_element:int, all_count_element:int) -> list[types.KeyboardButton]:
	array_keys = [
		key(f"Папка: {name_category}"),
		key(f"Файл: {index_element} из {all_count_element}"),
	]
	return array_keys	
				
def panel_user_menu() -> types.ReplyKeyboardMarkup:
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("Запустить"))
	table.row(key("Остановить"))
	table.row(key("Для разработчика"))
	table.row(key("Помощь и связь"))
	return table    			
	
def panel_admin_menu() -> types.ReplyKeyboardMarkup:
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("Запустить"))
	table.row(key("Остановить"))
	table.row(key("Управление доступом"))
	table.row(key("Отчет категории"))
	table.row(key("Отчет пользователи"))
	table.row(key("Отчет конфигурация"))
	return table    

def panel_admin_ask_yes_no() -> types.ReplyKeyboardMarkup:
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	table.row(key("yes"))
	table.row(key("no"))
	return table    

def panel_admin_users(dict_users:dict) -> types.ReplyKeyboardMarkup:
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for user in dict_users:
		table.row(key(f"({user["name"]}) ID: {str(user["chat_id"])} : {user["category"]}"))
	table.row("Меню")
	return table  

def panel_admin_set_value(array_categories:list[str]) -> types.ReplyKeyboardMarkup:
	table = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for name_category in array_categories:
		table.row(key(f"{name_category}"))
	return table    		
