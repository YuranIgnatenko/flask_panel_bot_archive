import requests
from bs4 import BeautifulSoup
import pyshorteners	
from panel import *
import panel
from random import randint
from urllib.request import urlopen
import threading

default_value = """+Юмор---https://world79.spcs.bio/sz/foto-i-kartinki/jumor-prikoly/new/
+Разное---https://world79.spcs.bio/sz/foto-i-kartinki/raznoe/new/
+Обои ПК---https://world79.spcs.bio/sz/foto-i-kartinki/oboi-dlja-pk/new/
+Абстрактное---https://world79.spcs.bio/sz/foto-i-kartinki/abstraktnye/new/
+Аниме---https://world79.spcs.bio/sz/foto-i-kartinki/anime/new/
+Архитектура---https://world79.spcs.bio/sz/foto-i-kartinki/arhitektura-goroda/new/
+Животные---https://world79.spcs.bio/sz/foto-i-kartinki/zhivotnyj-mir/new/
+AI арт---https://world79.spcs.bio/sz/foto-i-kartinki/ai-art/new/
+Космос---https://world79.spcs.bio/sz/foto-i-kartinki/kosmos/new/
+Люди---https://world79.spcs.bio/sz/foto-i-kartinki/ljudi/new/
+Звезды---https://world79.spcs.bio/sz/foto-i-kartinki/znamenitosti/"""

def category_links(namefile="parser.txt"):
	dt = {}
	with open(namefile, "r") as file:
		data = file.read().split('\n')
	for row in data:
		k,v = row.split("---")
		dt[k] = v
	return dt
		
def category(namefile="parser.txt"):
	dt = category_links(namefile)
	return dt.keys()

def conf_read(namefile="parser.txt"):
	with open(namefile, "r") as file:
		return file.read()

def conf_write(namefile, data):
	with open(namefile, "w") as file:
		file.write(data)

def conf_reset(namefile="parser.txt", data=default_value):
	conf_write(namefile,default_value)


category_db = {}

def shorten_url(url):
	try:
		return pyshorteners.Shortener().clckru.short(url)
	except:
		return url


def get_count_pages(url):
	try:
		response= requests.get(url, timeout=5)
	except Exception:
		return 10


	soup = BeautifulSoup(response.text, 'html.parser')
	tmp = []
	for link in soup.find_all('a'):
		href = link.get('href')
		if href and href.startswith('http'):
			if href.find('/p') != -1:
				tmp.append(href)
	t = tmp[-1].split('/')[-2][1:]
	t = int(t)
	
	return t

def get_r_page_href(name):
	url = category_links()[name]
	max_page = get_count_pages(url)-1
	try:
		r_page = randint(1,max_page)
		r_href = randint(1,20)
		return url,r_page,r_href
	except Exception:
		return url, randint(1,max_page),randint(1,10)

def get_href_content_online(url,r_page,r_href):
	url = f"{url}p{r_page}/"
	response= requests.get(url, timeout=5)
	soup = BeautifulSoup(response.text, 'html.parser')
	tmp = []
	t = 0
	for link in soup.find_all('a'):
		href = link.get('href')
		if href and href.startswith('http'):
			if href.find('/view') != -1:
				if t != r_href: 
					t+=1
					continue
				response = requests.get(href, timeout=5)
				soup = BeautifulSoup(response.text, 'html.parser')
				tmp_d = []
				for link in soup.find_all('a'):
					href = link.get('href')
					if href and href.startswith('http'):
						if href.find("download") != -1:
							tmp_d.append(href) 
									  
				if len(tmp_d) == 0: continue
				t+=1
				tmp.append(tmp_d[-1].replace("jpg","png"))
	
	res = tmp[0]         	
	return res

def get_href_content_online_process(chan_images,url,r_page,r_href):
	url = f"{url}p{r_page}/"
	try:
		response= requests.get(url, timeout=5)
	except Exception as e:
		return

	soup = BeautifulSoup(response.text, 'html.parser')
	tmp = []
	t = 0
	for link in soup.find_all('a'):
		href = link.get('href')
		if href and href.startswith('http'):
			if href.find('/view') != -1:
				if t != r_href: 
					t+=1
					continue
				try:
					response = requests.get(href, timeout=5)
				except Exception as e:
					continue

				soup = BeautifulSoup(response.text, 'html.parser')
				tmp_d = []
				for link in soup.find_all('a'):
					href = link.get('href')
					if href and href.startswith('http'):
						if href.find("download") != -1:
							tmp_d.append(href)
				
				if len(tmp_d) == 0: continue
				t+=1
				tmp_last_link = tmp_d[-1].replace("jpg","png")
				try:
					chan_images.put(tmp_last_link) 
				except Exception as e:
					pass
	return 



def get_href_content_online_list(chan_images, url,r_page,r_href):
	out_links = []
	name = url

	url,r_page,r_href = get_r_page_href(name)
	get_href_content_online_process(chan_images, url,r_page,r_href)

	return 




def get_href_content(url,bot,mcid,c,d,name,count_all):
	response= requests.get(url, timeout=5)
	soup = BeautifulSoup(response.text, 'html.parser')
	tmp = []
	t = 0
	for link in soup.find_all('a'):
		href = link.get('href')
		if href and href.startswith('http'):
			if href.find('/view') != -1:
				response = requests.get(href, timeout=5)
				soup = BeautifulSoup(response.text, 'html.parser')
				tmp_d = []
				for link in soup.find_all('a'):
					href = link.get('href')
					if href and href.startswith('http'):
						if href.find("download") != -1:
							
							
							tmp_d.append(href)

				if len(tmp_d) == 0: continue
				t+=1
				tmp.append(tmp_d[-1].replace("jpg","png"))
  	
	return tmp

def get_href_content_range(url,start,stop,bot,mcid,c,d,name):
	tmp = []
	for i in range(start,stop+1):
		link = f"{url}p{i}/"
		count_all = len(tmp)
		tmp += get_href_content(link,bot,mcid,c,d,name,count_all)
		bot.send_message(mcid,text='Выполняется обновление',reply_markup=panel.panel_status_update(len(tmp),len(tmp),c,d,name,count_all))
	return tmp


def save_file_href(category_db):
	with open("category_db.txt", "w") as file:
		for key in category_db:
			file.write(key+"\n")
			for link in category_db[key]:
				file.write(link+'\n')

def load_file_href():
	tmp_db = {}
	with open('category_db.txt','r')as file:
		data = file.read().split("\n")
	tmp_key=""
	for line in data:
		if not line.startswith("https"):
			tmp_key = line
			tmp_db[tmp_key] = []
		else:
			tmp_db[tmp_key].append(line)
	return tmp_db
			


print('init cache db content')

category_db = load_file_href()

print('finish init cache')

db_visit_index ={}
db_visit_name={}
