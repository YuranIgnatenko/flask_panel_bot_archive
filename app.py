from flask import Flask, request
from flask import render_template

from  service import Service, StorageLogs, StorageUsers, RowUser, StorageImages
import parserservice
import threading
import queue
import time
import config
from random import randint

new_out = []
data_out = []
category_value = "+Люди"
count_pic_value = "1"

flagLaunchBot = False

chan = queue.Queue()
chan_images = queue.Queue()
conf = config.Conf("config.txt")
app = Flask(__name__)
storage_images = StorageImages()
storage_logs = StorageLogs()
storage_users = StorageUsers()
service = Service(conf,chan, storage_users)



def receiver_chan(chan):
	global flagLaunchBot
	while True:
		try:
			chan_vlaue = chan.get()
		except Exceptiona as e:
			continue
		else:
			if chan_vlaue == "start":
				flagLaunchBot = True
			elif chan_vlaue == "abort":
				flagLaunchBot = False
			chan.task_done()


def render_settings():
		return render_template('settings.html', 
	var_api_key_bot=conf.bot_token,
	var_name_bot = conf.bot_name,
	var_status_bot = flagLaunchBot,
	var_last_started_bot = conf.bot_last_started)

@app.route('/settings')
def settings():
	return render_settings()

@app.route('/settings_apply', methods=['POST'])
def settings_apply():
		conf.bot_token = request.form['bot_token']
		conf.bot_name = request.form['bot_name']
		conf.bot_last_started = request.form['bot_last_started']
		conf.bot_status = request.form['bot_status']
		conf.save()
		return render_settings()


@app.route('/settings_reset')
def settings_reset():
	conf.reset()
	return render_settings()

@app.route('/settings_launch_bot')
def settings_launch_bot():
	return render_settings()

@app.route('/settings_stop_bot')
def settings_stop_bot():
	return render_settings()

@app.route('/settings_launch_parser')
def settings_launch_parser():
	return render_settings()

@app.route('/settings_stop_parser')
def settings_stop_parser():
	return render_settings()

@app.route('/settings_restart_app')
def settings_restart_app():
	return render_settings()

@app.route('/settings_send_test_notify')
def settings_send_test_notify():
	return render_settings()


@app.route('/dash_panel')
def dash_panel():
	return render_template('dash_panel.html')
@app.route('/')
def app_root():
	return render_template('desk_space.html')

@app.route('/desk_space_random_pic')
def desk_space_random_pic():
	global new_out,data_out, category_value,count_pic_value
	class DataImage():
		def __init__(self, index,link):
			self.index = index
			self.link = link

	dict_category = parserservice.category_links()
	def run_scrap():
		global new_out,data_out, category_value,count_pic_value
		parserservice.category_links()
		iter_c = 5
		for i in range(iter_c):
			random_category = list(dict_category)[randint(0,len(list(dict_category))-1)]
			url,r_page,r_href = parserservice.get_r_page_href(random_category)
			out = parserservice.get_href_content_online(url,r_page,r_href)
			try:		        	
				data_out.append(DataImage(i,out))
			except Exception as e:
				pass
		return data_out

	new_out = run_scrap()
	
	return render_template('desk_space.html', dt=new_out[::-1], category_value=category_value, count_pic_value=count_pic_value)



@app.route('/desk_space_clear_conf')
def desk_space_clear_conf():
	global category_value, count_pic_value, new_out, data_out
	new_out,data_out = [],[]
	category_value = "+Люди"
	count_pic_value = "1"
	return desk_space()

@app.route('/desk_space_apply_conf', methods=['POST'])
def desk_space_apply_conf():
	global category_value, count_pic_value,data_out,new_out
	form = request.form
	category_value = form['category_value']
	count_pic_value = form['count_pic_value']	
	return desk_space()

@app.route('/desk_space')
def desk_space():
	global new_out,data_out, category_value,count_pic_value

	class DataImage():
		def __init__(self, index,link):
			self.index = index
			self.link = link

	dict_category = parserservice.category_links()
	def run_scrap():
		global new_out,data_out, category_value,count_pic_value
		iter_c = int(count_pic_value)
		for i in range(iter_c):
			url,r_page,r_href = parserservice.get_r_page_href(category_value)
			out = parserservice.get_href_content_online(url,r_page,r_href)
			try:		        	
				data_out.append(DataImage(i,out))
			except Exception as e:pass
		return data_out

	new_out = run_scrap()
	
	return render_template('desk_space.html', dt=new_out[::-1], category_value=category_value, count_pic_value=count_pic_value)

@app.route('/logs')
def logs():
	storage_logs.update()
	return render_template('logs.html', dt=storage_logs.data)

@app.route('/users')
def users():
	storage_users.update()
	return render_template('users.html', dt=storage_users.data)

@app.route('/users_apply', methods=['POST'])
def users_apply():
	form = request.form
	for i in form:
		for u in storage_users.data:
			if str(u.chat_id) == str(i):
				u.category = form[i]

	storage_users.save()
	return render_template('users.html', dt=storage_users.data)


@app.route('/parser')
def parser():
	return render_template('parser.html',conf_parser=parserservice.conf_read())

@app.route('/parser_apply', methods=['POST'])
def parser_apply():
	data = request.form['text']
	parserservice.conf_write("parser.txt", data)
	return render_template('parser.html',conf_parser=parserservice.conf_read())

@app.route('/parser_reset')
def parser_reset():
	parserservice.conf_reset()
	return render_template('parser.html',conf_parser=parserservice.conf_read())


@app.route('/cache')
def cache():
	return render_template('cache.html')


@app.route('/tables')
def tables():
	return render_template('tables.html')



def start_app(ch):
	app.run(debug=False)

def start_bot(ch):
	service.polling()



t1 = threading.Thread(target=start_app, args=(chan,))
t2 = threading.Thread(target=start_bot, args=(chan,))
t3 = threading.Thread(target=receiver_chan, args=(chan,))


t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()