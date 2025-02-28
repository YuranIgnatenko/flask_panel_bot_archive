from flask import Flask, request, render_template

import logging
import threading
import queue
import sys

from telegram_bot_service import TelegramBotService, ParserSpcs
from parser_service import ParserSpcs
from config import Config

class WebApp():
	def __init__(self, chan:queue.Queue, conf:Config, bot_service:TelegramBotService, parser_service:ParserSpcs) -> None:
		self.app = Flask(__name__)
		
		self.conf_base = conf_base
		self.conf_log = read_file_log()
		self.conf_users = config.Config(self.conf_base.get("file_users"))

		self.conf_categories = config.Config(self.conf_base.get("file_categories"))
		self.parser_service = parser_service
		self.bot_service = bot_service
		self.collect_images = []
		self.category_value = self.conf_base.get("category_value")
		self.count_pic_value = self.conf_base.get("count_pic_value")
		self.flagLaunchBot = False

		self.setup_routes()

	def read_file_log(self):
		with open(self.conf_base.get("file_log")) as file:
			return file.read()

	def receiver_chan_status_bot(self, chan:queue.Queue) -> None:
		logging.info("start receiver channel")
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
		var_api_key_bot = self.conf_base.get("bot_token"),
		var_name_bot = self.conf_base.get("bot_name"),
		var_status_bot = self.flagLaunchBot,
		var_last_started_bot = self.conf_base.get("bot_last_started"))

	def setup_routes(self) -> str:

		@self.app.route('/settings')
		def settings() -> str:
			return self.render_settings()

		# @self.app.route('/settings_apply', methods=['POST'])
		# def settings_apply():
		# 		self.conf_base.bot_token = request.form['bot_token']
		# 		self.conf_base.bot_name = request.form['bot_name']
		# 		self.conf_base.bot_last_started = request.form['bot_last_started']
		# 		self.conf_base.bot_status = request.form['bot_status']
		# 		self.conf_base.save()
		# 		return self.render_settings()

		@self.app.route('/dash_panel')
		def dash_panel() -> str:
			return render_template('dash_panel.html')

		@self.app.route('/')
		def app_root() -> str:
			return render_template('desk_space.html')

		@self.app.route('/desk_space_random_pic')
		def desk_space_random_pic() -> str:
			return render_template('desk_space.html', dt=self.get_image()[::-1], category_value=self.category_value, count_pic_value=self.count_pic_value)


		# @self.app.route('/desk_space_clear_conf')
		# def desk_space_clear_conf():
		# 	self.new_out, self.data_out = [],[]
		# 	category_value = "+Люди"
		# 	count_pic_value = "1"
		# 	return desk_space()

		@self.app.route('/desk_space_apply_conf', methods=['POST'])
		def desk_space_apply_conf():
			form = request.form
			self.category_value = form['category_value']
			self.count_pic_value = form['count_pic_value']	
			return render_template('desk_space.html', dt=self.get_image()[::-1], category_value=self.category_value, count_pic_value=self.count_pic_value)

		@self.app.route('/desk_space')
		def desk_space() -> str:
			return render_template('desk_space.html', dt=self.get_image()[::-1], category_value=self.category_value, count_pic_value=self.count_pic_value)

		@self.app.route('/logs')
		def logs():
			# self.storage_logs.update()
			return render_template('logs.html', dt=self.conf_log)

		@self.app.route('/users')
		def users():
			# self.storage_users.update()
			return render_template('users.html', dt=self.conf_users.to_dict())

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
			return render_template('parser.html',conf_parser=self.conf_categories.to_str())

		# @self.app.route('/parser_apply', methods=['POST'])
		# def parser_apply():
		# 	data = request.form['text']
		# 	self.parser_service.conf_write("parser.txt", data)
		# 	return render_template('parser.html',conf_parser=self.parser_service.conf_read())

		# @self.app.route('/parser_reset')
		# def parser_reset():
		# 	self.parser_service.conf_reset()
		# 	return render_template('parser.html',conf_parser=self.parser_service.conf_read())

	def get_image(self) -> list[DataImage]:
		for index in range(int(self.count_pic_value)):
			url_image = self.parser_service.get_url_random_page_from_category(self.category_value)
			self.collect_images.append(DataImage(index,url_image))
		return self.collect_images


	def start_app(self, chan:queue.Queue) -> None:
		logging.info("start web app")
		self.app.run(debug=False)

	def start_bot(self, chan:queue.Queue) -> None:
		logging.info("start bot telegram")
		self.bot_service.polling()


def main() -> None:
	if len(sys.argv) > 1:
		arg_namefile_config = sys.argv[1]
		conf_base = config.Config(sys.argv[1])

		logging.basicConfig(filename=conf_base.get("file_log"), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

		chan_signal_work_status = queue.Queue()
		
		bot_service = TelegramBotService(chan_signal_work_status, conf_base)
		parser_service = parser_service.ParserSpcs(conf_base)

		webapp = WebApp(chan_signal_work_status, conf_base, bot_service, parser_service)

		def launch_threads() -> None:
			thread_web_app = threading.Thread(target=webapp.start_app, args=(chan_signal_work_status,))
			thread_tg_bot = threading.Thread(target=webapp.start_bot, args=(chan_signal_work_status,))
			thread_receiver_chan = threading.Thread(target=webapp.receiver_chan_status_bot, args=(chan_signal_work_status,))

			thread_web_app.start()
			thread_tg_bot.start()
			thread_receiver_chan.start()

			thread_web_app.join()
			thread_tg_bot.join()
			thread_receiver_chan.join()

		launch_threads()
	else:
		logging.error("Enter name file base config for setup params WebApp !")
		return


if __name__ == "__main__":main()