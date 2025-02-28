import requests
from bs4 import BeautifulSoup
import pyshorteners	
from random import randint

def shorten_url(url:str) -> str:
    try: return pyshorteners.Shortener().clckru.short(url)
    except: return url

def get_random_number_page(max_page:int) -> int:
    return randint(0, max_page)

def build_url_page_image(category_name:str, num_page:int=0) -> str:
		if num_page == 0: return f"{self.conf_categories.get("prefix_url")}{self.conf_categories.get(category_name)}"
		else: return f"{self.conf_categories.get("prefix_url")}{self.conf_categories.get(category_name)}/p{num_page}"