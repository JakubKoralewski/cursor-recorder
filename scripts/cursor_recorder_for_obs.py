# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. 
# Copyright 2019 (c) Jakub Koralewski
import obspython as obs
import datetime
import os
from subprocess import Popen, PIPE
from typing import List
import time
import threading

import logging
import sys

file_handler = logging.FileHandler(filename='obs_cursor_recorder.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
	level=logging.DEBUG,
	format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
	handlers=handlers
)
logger = logging.getLogger('obs_cursor_recorder_logger')

p = sys.platform
py_executable = "python.exe"
if p == "linux" or p == "linux2":
	py_executable = "python3.6"
elif p == "win32" or p == "win64":
	py_executable = "python.exe"
else:
	logging.error(f"Unsupported platform: {p}\nWindows or Linux.")
del p

import_succeeded = False
cached_settings = {}
properties = {}
is_being_recorded = False


def now():
	return datetime.datetime.now().time()


logger.info(f"{now()}: refresh")
py_dir = os.__file__.split("lib")[0]
py_interpreter = os.path.join(py_dir, py_executable)
logger.info(f'py_interpreter: {py_interpreter}')

output = obs.obs_frontend_get_recording_output()

SHOULD_EXIT = False

name = 'obs_cursor_recorder.txt'
path = 'C:/Users/Admin/Documents'


def install_pip_then_multiple(packages):
	logger.info('Import pip then multiple modules.')
	assert (os.path.isdir(py_dir))

	"""
	:param name - name of action you are doing, for logging 
	"""

	def install(c: List, name: str = ""):
		logger.info(name)
		p = Popen(
			' '.join(c),
			stdout=PIPE,
			stderr=PIPE,
			stdin=PIPE,
			executable=py_interpreter,
			cwd=py_dir[:-1]
		)
		print(f"Stdout writable: {p.stdout.writable()}")
		print(p.args)
		out, err = p.communicate()
		if len(err) != 0:
			logging.error(f"{name} Error:\n {err}")
		logging.info(f"{name} Output:\n {out}")

	cmd_line_update = [
		py_executable, '-m', 'pip', 'install', '--upgrade', 'pip', '--user'
	]

	cmd_line_install = [
		py_executable, '-m', 'pip', 'install'
	] + packages

	logger.debug(f'Python interpreter location: {py_interpreter}')
	logger.debug(f'Python interpreter location directory: {py_dir}')
	install(cmd_line_update, "Upgrading your pip version: ")
	install(cmd_line_install, "Installing packages: ")


def install_modules_button_click():
	install_pip_then_multiple(['pyautogui', 'keyboard'])


try:
	import pyautogui
	import keyboard
except ModuleNotFoundError:
	logger.error("PyAutoGui and or keyboard are not installed.\n\
I'm installing them for you if you don't mind.\n")
	install_pip_then_multiple(['pyautogui', 'keyboard'])
	import pyautogui
	import keyboard


def save_to_file(seconds, x, y):
	full_path = os.path.join(path, name) if path and name else "cursor-recorder.txt"
	logger.info(f'Saving file to {full_path}')

	with open(full_path, "a+") as file:
		file.write(f'{seconds} {x} {y}\n')


x = -1
y = -1
prev_x = -1
prev_y = -1
seconds = 0
skipping = False


def script_tick(time_passed):
	if not is_being_recorded or not cached_settings["use_default_fps"]:
		return

	global x
	global y
	global prev_x
	global prev_y
	global seconds
	global skipping

	seconds += time_passed

	# Get cursor position
	x, y = pyautogui.position()

	# If previous position same as current
	# no need to add same data
	if prev_x == x and prev_y == y:
		skipping = True
		return
	else:
		if skipping == True:
			# If previously was skipping
			# create a keyframe that will stop sliding
			save_to_file(seconds - time_passed, prev_x, prev_y)

		skipping = False

	prev_x = x
	prev_y = y

	save_to_file(seconds, x, y)


def should_exit():
	if SHOULD_EXIT:
		logger.info('should exit!')
		return True
	return False


def cursor_recorder():
	refresh_rate = 1 / cached_settings["custom_fps"]

	x = -1
	y = -1
	prev_x = -1
	prev_y = -1
	skipping = False

	startTaim: int = time.time()

	while True:
		time.sleep(refresh_rate)
		taim = time.time() - startTaim

		# Get cursor position
		x, y = pyautogui.position()

		# If previous position same as current
		# no need to add same data
		if prev_x == x and prev_y == y:
			skipping = True

			if should_exit():
				break
			continue
		else:
			if skipping == True:
				# If previously was skipping
				# create a keyframe that will stop sliding
				save_to_file(round(taim - refresh_rate, 3), prev_x, prev_y)

				if should_exit():
					break

			skipping = False

		prev_x: int = x
		prev_y: int = y

		save_to_file(taim, x, y)

		if should_exit():
			break


""" Registering callbacks:
Docs:
	- https://obsproject.com/docs/reference-outputs.html#output-signal-handler-reference
	- https://obsproject.com/docs/frontends.html#signals 
"""


def recording_start_handler(_):
	global is_being_recorded
	global path
	global name
	is_being_recorded = True

	logger.info(f'recording started ({now()})')
	output_settings = obs.obs_output_get_settings(output)
	logger.debug(obs.obs_data_get_json(output_settings))

	""" Example path: "C:/Users/Admin/Documents/2019-04-04 16-02-28.flv"
	After `os.path.split(path)`: ('C:/Users/Admin/Documents', '2019-04-04 16-02-28.flv')"""
	video_path_tuple = os.path.split(obs.obs_data_get_string(output_settings, "path"))
	video_name = video_path_tuple[-1]

	path = video_path_tuple[0]
	# Convert extension to txt from .flv
	name = os.path.splitext(video_name)[0] + '.txt'

	if not cached_settings["use_default_fps"]:
		global SHOULD_EXIT
		SHOULD_EXIT = False
		logger.info('Starting recording using custom FPS settings.')
		threading.Thread(target=cursor_recorder).start()


def recording_stopped_handler(_):
	global is_being_recorded
	global SHOULD_EXIT
	SHOULD_EXIT = True
	is_being_recorded = False
	logger.info(f'recording stopped ({now()})')


def script_description():
	logger.debug('script_description')
	return '<h1>OBS Cursor Recorder</h1><b>Lets you save your cursor movement to a file.</b>' \
		'<br/><br/>©2019 Jakub Koralewski. ' \
		'<a href="' \
		'https://github.com/JakubKoralewski/cursor-recorder-for-afterfx"' \
		'target="_blank">Open-source on GitHub.</a> <hr />'


def script_properties():
	logger.debug('script_properties')
	props = obs.obs_properties_create()
	enabled = obs.obs_properties_add_bool(props, "enabled", "Enabled")
	obs.obs_property_set_long_description(enabled, "Whether to save the file when recording or not.")

	long_default_fps_description = "Use this option to achieve higher accuracy than every video frame."

	default_fps = obs.obs_properties_add_bool(props, "use_default_fps", "Use video's FPS to capture cursor")
	obs.obs_property_set_long_description(default_fps, long_default_fps_description)

	custom_fps = obs.obs_properties_add_int_slider(props, "custom_fps", "Custom FPS", 1, 200, 1)
	obs.obs_property_set_long_description(custom_fps, long_default_fps_description)

	install_modules = obs.obs_properties_add_button(
		props,
		"install_modules",
		"Install Python modules",
		install_modules_button_click
	)

	obs.obs_property_set_long_description(
		install_modules,
		"Installs pip, pyautogui and keyboard Python modules in your specified Python interpreter."
	)

	return props


def script_save(settings):
	logger.debug('script_save')
	script_update(settings)


def script_update(settings):
	logger.debug('script_update')

	cached_settings["use_default_fps"] = obs.obs_data_get_bool(settings, "use_default_fps")
	cached_settings["custom_fps"] = obs.obs_data_get_int(settings, "custom_fps")
	cached_settings["enabled"] = obs.obs_data_get_bool(settings, "enabled")

	if cached_settings["enabled"]:
		logger.info('Registering start and stop handlers.')
		signal_handler = obs.obs_output_get_signal_handler(output)
		try:
			obs.signal_handler_connect(signal_handler, 'start', recording_start_handler)
			obs.signal_handler_connect(signal_handler, 'stop', recording_stopped_handler)
		except RuntimeError as e:
			logger.critical(f'Disregarding error when connecting start and stop handlers: {e}')
	else:
		logger.info('Disconnecting start and stop handlers.')
		signal_handler = obs.obs_output_get_signal_handler(output)
		obs.signal_handler_disconnect(signal_handler, 'start', recording_start_handler)
		if not is_being_recorded:
			obs.signal_handler_disconnect(signal_handler, 'stop', recording_stopped_handler)

	logger.debug(f'cached_settings: {cached_settings}')


def script_defaults(settings):
	logger.debug('script_defaults')
	obs.obs_data_set_default_bool(settings, "enabled", True)
	obs.obs_data_set_default_bool(settings, "use_default_fps", True)
	obs.obs_data_set_default_int(settings, "custom_fps", 30)
