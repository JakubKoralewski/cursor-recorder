# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. 
# Copyright 2019 (c) Jakub Koralewski

import obspython as obs
import datetime
import os
from subprocess import call

import logging
import sys

import pyautogui
import keyboard

file_handler = logging.FileHandler(filename='obs_cursor_recorder.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)
logger = logging.getLogger('obs_cursor_recorder_logger')

import_succeeded = False
cached_settings = {}
is_being_recorded = False

def now():
	return datetime.datetime.now().time()

logger.info(f"{now()}: refresh")

py_interpreter = os.path.join(os.__file__.split("lib")[0], "python.exe")
logger.info(f'py_interpreter: {py_interpreter}')

output = obs.obs_frontend_get_recording_output()

# Cursor positions
x = -1
y = -1
prev_x = -1
prev_y = -1
seconds = 0
skipping = False

name = 'obs_cursor_recorder.txt'
path = 'C:/Users/Admin/Documents'

def save_to_file(seconds, x, y):
	full_path = os.path.join(path, name) if path and name else "cursor-recorder.txt"
	logger.info(f'Saving file to {full_path}')

	with open(full_path, "a+") as file:
		file.write(f'{seconds} {x} {y}\n')
	
	logger.debug(seconds, x, y)
	

def script_tick(time_passed):
	if not is_being_recorded:
		return
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


""" Registering callbacks:
Docs:
	- https://obsproject.com/docs/reference-outputs.html#output-signal-handler-reference
	- https://obsproject.com/docs/frontends.html#signals 
"""

def recording_start_handler(x):
	global is_being_recorded
	global path
	global name
	is_being_recorded = True

	logger.info(f'recording started ({now()})')
	output_settings = obs.obs_output_get_settings(output)

	""" Example path: "C:/Users/Admin/Documents/2019-04-04 16-02-28.flv"
	After `os.path.split(path)`: ('C:/Users/Admin/Documents', '2019-04-04 16-02-28.flv')"""
	video_path_tuple = os.path.split(obs.obs_data_get_string(output_settings, "path"))
	video_name = video_path_tuple[-1]

	path = video_path_tuple[0]
	# Convert extension to txt from .flv
	name = os.path.splitext(video_name)[0] + '.txt'

def install_modules_button_click(x,y):
	for module in ['pyautogui', 'keyboard']:
		install(module)

def recording_stopped_handler(x):
	global is_being_recorded
	is_being_recorded = False
	logger.info(f'recording stopped ({now()})')

def install_pip():
	call([py_interpreter, '-m', 'pip', 'install', '--upgrade', 'pip'])

def install(package: str):
	call([py_interpreter, '-m', 'pip', 'install', package])

def script_description():
	logger.debug('script_description')
	return '<h1>OBS Cursor Recorder</h1><b>Lets you save your cursor movement to a file.</b><br/><br/>©2019 Jakub Koralewski. <a href="https://github.com/JakubKoralewski/cursor-recorder-for-afterfx" target="_blank">Open-source on GitHub.</a> <hr />  '

def script_properties():
	logger.debug('script_properties')
	props = obs.obs_properties_create()
	obs.obs_properties_add_bool(props, "enabled", "Enabled")
	obs.obs_properties_add_button(props, "install_modules", "Install Python modules", install_modules_button_click)
	return props

def script_save(settings):
	logger.debug('script_save')
	script_update(settings)

def script_update(settings):
	logger.debug('script_update')
	cached_settings["python_path"] = obs.obs_data_get_string(settings, "python_path")
	cached_settings["enabled"] = obs.obs_data_get_bool(settings, "enabled")
	logger.info(f'cached_settings["enabled"]: {cached_settings["enabled"]}')
	if cached_settings["enabled"]:
		logger.info('Registering start and stop handlers.')
		signal_handler = obs.obs_output_get_signal_handler(output)
		obs.signal_handler_connect(signal_handler, 'start', recording_start_handler)
		obs.signal_handler_connect(signal_handler, 'stop', recording_stopped_handler)
	else:
		logger.info('Disconnecting start and stop handlers.')
		signal_handler = obs.obs_output_get_signal_handler(output)
		obs.signal_handler_disconnect(signal_handler, 'start', recording_start_handler)
		if not is_being_recorded:
			obs.signal_handler_disconnect(signal_handler, 'stop', recording_stopped_handler)

def script_defaults(settings):
	logger.debug('script_defaults')
	obs.obs_data_set_default_bool(settings, "enabled", True)



