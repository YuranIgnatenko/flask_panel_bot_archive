from flask import Flask, request
from flask import render_template

from  service import Service, StorageLogs, StorageUsers, RowUser, StorageImages
import parserservice
import threading
import queue
import config
from random import randint
import sys

class WebApp():
	def __init__(self, conf:config.Config, service:Service, storage_images:StorageImages, 
		storage_logs:StorageLogs, storage_users:StorageUsers) -> None:

		self.app = Flask(__name__)
		self.conf = conf
		self.service = service
		self.storage_images, self.storage_logs, self.storage_users = storage_images, storage_logs, storage_users
		self.new_out = []
		self.data_out = []
		self.category_value = self.conf.get("category_value")
		self.count_pic_value = self.conf.get("count_pic_value")
		self.flagLaunchBot = False

		self.setup_routes()


	def receiver_chan_status_bot(self, chan:queue.Queue) -> None:
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


	def render_settings(self) -> str:
			return render_template('settings.html', 
		var_api_key_bot = self.conf.get("bot_token"),
		var_name_bot = self.conf.get("bot_name"),
		var_status_bot = self.flagLaunchBot,
		var_last_started_bot = self.conf.get("bot_last_started"))

	def setup_routes(self) -> str:

		@self.app.route('/settings')
		def settings() -> str:
			return self.render_settings()

		# @self.app.route('/settings_apply', methods=['POST'])
		# def settings_apply():
		# 		self.conf.bot_token = request.form['bot_token']
		# 		self.conf.bot_name = request.form['bot_name']
		# 		self.conf.bot_last_started = request.form['bot_last_started']
		# 		self.conf.bot_status = request.form['bot_status']
		# 		self.conf.save()
		# 		return self.render_settings()

		# @self.app.route('/settings_reset')
		# def settings_reset():
		# 	self.conf.reset()
		# 	return self.render_settings()

		# @self.app.route('/settings_launch_bot')
		# def settings_launch_bot():
		# 	return self.render_settings()

		# @self.app.route('/settings_stop_bot')
		# def settings_stop_bot():
		# 	return self.render_settings()

		# @self.app.route('/settings_launch_parser')
		# def settings_launch_parser():
		# 	return self.render_settings()

		# @self.app.route('/settings_stop_parser')
		# def settings_stop_parser():
		# 	return self.render_settings()

		# @self.app.route('/settings_restart_app')
		# def settings_restart_app():
		# 	return self.render_settings()

		# @self.app.route('/settings_send_test_notify')
		# def settings_send_test_notify():
		# 	return self.render_settings()


		@self.app.route('/dash_panel')
		def dash_panel() -> str:
			return render_template('dash_panel.html')

		@self.app.route('/')
		def app_root() -> str:
			return render_template('desk_space.html')

		@self.app.route('/desk_space_random_pic')
		def desk_space_random_pic() -> str:
			class DataImage():
				def __init__(self, index,link):
					self.index = index
					self.link = link

			dict_category = parserservice.category_links()
			def run_scrap():
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



		# @self.app.route('/desk_space_clear_conf')
		# def desk_space_clear_conf():
		# 	self.new_out, self.data_out = [],[]
		# 	category_value = "+Люди"
		# 	count_pic_value = "1"
		# 	return desk_space()

		# @self.app.route('/desk_space_apply_conf', methods=['POST'])
		# def desk_space_apply_conf():
		# 	form = request.form
		# 	category_value = form['category_value']
		# 	count_pic_value = form['count_pic_value']	
		# 	return desk_space()

		@self.app.route('/desk_space')
		def desk_space() -> str:

			class DataImage():
				def __init__(self, index,link):
					self.index = index
					self.link = link

			dict_category = parserservice.category_links()
			def run_scrap() -> list[DataImage]:
				iter_c = int(self.count_pic_value)
				for i in range(iter_c):
					url,r_page,r_href = parserservice.get_r_page_href(self.category_value)
					out = parserservice.get_href_content_online(url,r_page,r_href)
					try:		        	
						data_out.append(DataImage(i,out))
					except Exception as e:pass
				return data_out

			new_out = run_scrap()
			
			return render_template('desk_space.html', dt=new_out[::-1], category_value=category_value, count_pic_value=count_pic_value)

		@self.app.route('/logs')
		def logs():
			storage_logs.update()
			return render_template('logs.html', dt=storage_logs.data)

		@self.app.route('/users')
		def users():
			self.storage_users.update()
			return render_template('users.html', dt=storage_users.data)

		# @self.app.route('/users_apply', methods=['POST'])
		# def users_apply():
		# 	form = request.form
		# 	for i in form:
		# 		for u in storage_users.data:
		# 			if str(u.chat_id) == str(i):
		# 				u.category = form[i]
		# 	storage_users.save()
		# 	return render_template('users.html', dt=storage_users.data)


		@self.app.route('/parser')
		def parser():
			return render_template('parser.html',conf_parser=parserservice.conf_read())

		# @self.app.route('/parser_apply', methods=['POST'])
		# def parser_apply():
		# 	data = request.form['text']
		# 	parserservice.conf_write("parser.txt", data)
		# 	return render_template('parser.html',conf_parser=parserservice.conf_read())

		# @self.app.route('/parser_reset')
		# def parser_reset():
		# 	parserservice.conf_reset()
		# 	return render_template('parser.html',conf_parser=parserservice.conf_read())


	def start_app(self, chan:queue.Queue) -> None:
		self.app.run(debug=False)

	def start_bot(self, chan:queue.Queue) -> None:
		self.service.polling()


def main() -> None:
	if len(sys.argv)>1:
		arg_namefile_config = sys.argv[1]
		conf = config.Config(sys.argv[1])

		chan = queue.Queue()
		chan_images = queue.Queue()
		
		storage_images = StorageImages()
		storage_logs = StorageLogs(conf)
		storage_users = StorageUsers()
		service = Service(conf, chan, storage_users)

		webapp = WebApp(conf, service, storage_images, storage_logs, storage_users)

		def launch_threads() -> None:
			thread_web_app = threading.Thread(target=webapp.start_app, args=(chan,))
			thread_tg_bot = threading.Thread(target=webapp.start_bot, args=(chan,))
			thread_receiver_chan = threading.Thread(target=webapp.receiver_chan_status_bot, args=(chan,))

			thread_web_app.start()
			thread_tg_bot.start()
			thread_receiver_chan.start()

			thread_web_app.join()
			thread_tg_bot.join()
			thread_receiver_chan.join()

		launch_threads()
	else:
		print("enter setup-params for file")
		return

main()