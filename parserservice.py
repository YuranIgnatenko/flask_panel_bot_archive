import requests
from bs4 import BeautifulSoup
import pyshorteners	
from botpanel import *
import botpanel
from random import randint
import config
import sys, json

class ParserService():
	def __init__(self, conf:config.Config) -> None:
		self.conf = conf
		self.conf_categories = config.Config(self.conf.get("file_categories"))

	def shorten_url(self, url:str) -> str:
		try: return pyshorteners.Shortener().clckru.short(url)
		except: return url

	def get_random_number_page(self, max_page:int) -> int:
		return randint(0, max_page)

	def build_url_page_image(self, category_name:str, num_page:int=0) -> str:
		# ex: https://world79.spcs.bio/sz/foto-i-kartinki/ljudi/p9 -- url page, not only image !
		if num_page == 0: return f"{self.conf_categories.get("prefix_url")}{self.conf_categories.get(category_name)}"
		else: return f"{self.conf_categories.get("prefix_url")}{self.conf_categories.get(category_name)}/p{num_page}"

	def get_count_pages(self, category_name:str) -> int:
		url = self.build_url_page_image(category_name)
		try: response = requests.get(url)
		except Exception: return 10
		soup = BeautifulSoup(response.text, 'html.parser')
		temp_links = []
		for link in soup.find_all('a'):
			href = link.get('href')
			if href and href.startswith('http'):
				if href.find('/p') != -1:
					temp_links.append(href)
		max_num_page = int(temp_links[-1].split('/')[-2][1:])
		return max_num_page

	def get_url_random_page_from_category(self, category_name:str) -> str:
		max_page_category = self.get_count_pages(category_name)-1
		try:
			random_page = randint(1,max_page_category)
			return self.get_image_from_params(category_name, random_page)
		except Exception:
			return self.get_image_from_params(category_name, random_page)

	def get_image_from_params(self, category_name:str, num_page:int) -> str:
		temp_url = self.build_url_page_image(category_name, num_page)
		response = requests.get(temp_url)
		soup = BeautifulSoup(response.text, 'html.parser')
		tmp = []
		for link in soup.find_all('a'):
			href = link.get('href')
			if href and href.startswith('http'):
				if href.find('/view') != -1:
					response = requests.get(href)
					soup = BeautifulSoup(response.text, 'html.parser')
					tmp_d = []
					for link in soup.find_all('a'):
						href = link.get('href')
						if href and href.startswith('http'):
							if href.find("download") != -1:
								tmp_d.append(href) 
										
					if len(tmp_d) == 0: continue
					tmp.append(tmp_d[-1].replace("jpg","png"))
		res = tmp[0]
		return res

def get_href_content_range(url,start,stop,bot,mcid,c,d,name) -> list[str]:
	tmp = []
	for i in range(start,stop+1):
		link = f"{url}p{i}/"
		count_all = len(tmp)
		tmp += get_href_content(link,bot,mcid,c,d,name,count_all)
		bot.send_message(mcid,text='Выполняется обновление',reply_markup=panel.panel_status_update(len(tmp),len(tmp),c,d,name,count_all))
	return tmp

# # single launch for file main
# ps = ParserService("../config.json", "categories.json")
# new_url_image = ps.get_url_random_page_from_category("human")
# print(new_url_image)
# sys.exit(1)