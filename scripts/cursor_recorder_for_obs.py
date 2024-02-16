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
from pathlib import Path

file_handler = logging.FileHandler(filename=Path.home() / 'obs_cursor_recorder.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
	level=logging.DEBUG,
	format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
	handlers=handlers
)
logger = logging.getLogger('obs_cursor_recorder_logger')

p = sys.platform
PY_EXECUTABLE = "python.exe"
if p in ("linux", "linux2", "darwin"):
	PY_EXECUTABLE = str((Path("bin") / "python3"))
elif p in ("win32", "win64"):
	PY_EXECUTABLE = "python.exe"
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
py_interpreter = os.path.join(py_dir, PY_EXECUTABLE)
logger.info(f'py_interpreter: {py_interpreter}')

output = obs.obs_frontend_get_recording_output()

CUSTOM_FPS_SHOULD_EXIT = False

name = 'obs_cursor_recorder.txt'
path = Path.home()
file = None


def install_pip_then_multiple(packages):
	logger.info('Import pip then multiple modules.')
	assert (os.path.isdir(py_dir))

	def install(c: List, name: str = ""):
		logger.info(name)
		p = Popen(
			c,
			stdout=PIPE,
			stderr=PIPE,
			executable=py_interpreter,
			cwd=py_dir
		)
		print(py_dir, c)
		out, err = p.communicate()
		logging.info(f"{name=} {out=} {err=} {p.returncode=}")

	cmd_line_update = [
		PY_EXECUTABLE, '-m', 'pip', 'install', '--upgrade', 'pip', '--user'
	]

	cmd_line_install = [
		PY_EXECUTABLE, '-m', 'pip', 'install'
	] + packages

	logger.debug(f'Python interpreter location: {py_interpreter}')
	logger.debug(f'Python interpreter location directory: {py_dir}')
	install(cmd_line_update, "Upgrading your pip version: ")
	install(cmd_line_install, "Installing packages: ")


def install_modules_button_click(*args):
	install_pip_then_multiple(['pyautogui'])


try:
	import pyautogui
except ModuleNotFoundError:
	logger.error("PyAutoGui and or keyboard are not installed.\n\
I'm installing them for you if you don't mind.\n")
	install_pip_then_multiple(['pyautogui'])
	import pyautogui


def save_to_file(seconds: float, x: int, y: int):
	if not file.closed:
		file.write(f'{round(seconds, 3)} {x} {y}\n')

x = -1
y = -1
prev_x = -1
prev_y = -1
seconds = 0
skipping = False

def init_tick_globals():
	global x, y, prev_x, prev_y, seconds, skipping
	x = -1
	y = -1
	prev_x = -1
	prev_y = -1
	seconds = 0
	skipping = False


def script_tick(time_passed):
	"""
	Called on each frame by OBS. Should only run when is in default_fps. Needs to be checked.
	"""
	if not is_being_recorded or not cached_settings["use_default_fps"]:
		return

	global x,y,prev_x,prev_y,seconds,skipping

	seconds += time_passed

	# Get cursor position
	x, y = pyautogui.position()

	# If previous position same as current
	# no need to add same data
	if prev_x == x and prev_y == y:
		skipping = True
		return

	if skipping:
		# If previously was skipping
		# create a keyframe that will stop sliding
		save_to_file(seconds - time_passed, prev_x, prev_y)

	skipping = False

	prev_x = x
	prev_y = y

	save_to_file(seconds, x, y)


def cursor_recorder():
	"""
	Recording of cursor that takes place from custom_fps option. Started in handler of start of recording.
	"""
	custom_fps = cached_settings["custom_fps"]
	refresh_rate = 1 / custom_fps
	def should_exit():
		"""
		Whether cursor_recorder should exit in a given iteration.
		"""
		if CUSTOM_FPS_SHOULD_EXIT:
			logger.info('should exit!')
			return True
		return False

	x = -1
	y = -1
	prev_x = -1
	prev_y = -1
	skipping = False

	start_time: float = time.time()
	print(f"{refresh_rate=} {start_time=} {custom_fps=}")

	while True:
		time.sleep(refresh_rate)
		time_ = time.time() - start_time

		# Get cursor position
		x, y = pyautogui.position()

		# If previous position same as current
		# no need to add same data
		if prev_x == x and prev_y == y:
			skipping = True

			if should_exit():
				break
			continue

		if skipping:
			# If previously was skipping
			# create a keyframe that will stop sliding
			save_to_file(time_ - refresh_rate, prev_x, prev_y)

			if should_exit():
				break

		skipping = False

		prev_x: int = x
		prev_y: int = y

		save_to_file(time_, x, y)

		if should_exit():
			break


# Registering callbacks:
# Docs:
# - https://obsproject.com/docs/reference-outputs.html#output-signal-handler-reference
# - https://obsproject.com/docs/frontends.html#signals


def recording_start_handler(_):
	"""
	Called by OBS when recording is started
	"""

	logger.info(f'recording started ({now()})')
	output_settings = obs.obs_output_get_settings(output)
	logger.debug(obs.obs_data_get_json(output_settings))

	# Example path: "C:/Users/Admin/Documents/2019-04-04 16-02-28.flv"
	# After `os.path.split(path)`: ('C:/Users/Admin/Documents', '2019-04-04 16-02-28.flv')
	raw_path = obs.obs_data_get_string(output_settings, "path")
	print(f"Raw path: '{raw_path}'")
	if raw_path == "":
		logging.info('Path is empty when starting recording, trying to use "url" if you\'re using FFmpeg!')
		raw_path = obs.obs_data_get_string(output_settings, "url")
		print(f"Raw path: '{raw_path}'")
		if raw_path == "":
			logging.error('Switched to "url" when "path" was not working, but still didn\'t get anything!')

	global path
	global name
	global file
	path = os.path.split(raw_path)[0]
	# Convert extension to txt from .flv /mkv
	name = os.path.splitext(raw_path)[0] + '.txt'
	print(f"{path=} {name=}")
	file = open(name, 'a+', encoding='UTF-8')
	if cached_settings["use_default_fps"]:
		init_tick_globals()

	global is_being_recorded
	if not cached_settings["use_default_fps"] and not is_being_recorded:
		is_being_recorded = True
		logger.info('Starting recording using custom FPS settings.')
		threading.Thread(target=cursor_recorder).start()

	# Only set is_being_recorder after the path and name have been set so that the script_tick saves to correct file from the start
	is_being_recorded = True
	global CUSTOM_FPS_SHOULD_EXIT
	CUSTOM_FPS_SHOULD_EXIT = False


def recording_stopped_handler(_):
	"""
	Called by OBS when recording stops
	"""
	global is_being_recorded
	global CUSTOM_FPS_SHOULD_EXIT
	CUSTOM_FPS_SHOULD_EXIT = True
	is_being_recorded = False
	logger.info(f'recording stopped ({now()})')

	if file is not None and not file.closed:
		file.close()


def script_description():
	logger.debug('script_description')
	return '<img src="data:image/png;base64,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 "/><h1>OBS Cursor Recorder</h1><b>Lets you save your cursor movement to a file.</b>' \
		'<br/><br/>©2019-2024 Jakub Koralewski. ' \
		'<a href="' \
		'https://github.com/JakubKoralewski/cursor-recorder-for-afterfx"' \
		'target="_blank">Open-source on GitHub.</a> <hr />'


def script_properties():
	logger.debug('script_properties')
	props = obs.obs_properties_create()
	enabled = obs.obs_properties_add_bool(props, "enabled", "Enabled")
	obs.obs_property_set_long_description(enabled, "Whether to save the cursor recorder file when recording or not.")

	long_default_fps_description = "Use this option to achieve higher accuracy than every video frame (larger than video fps) or to save text file space (lower than video fps)."

	default_fps = obs.obs_properties_add_bool(props, "use_default_fps", "Use video's FPS to capture cursor")
	obs.obs_property_set_long_description(default_fps, long_default_fps_description)

	custom_fps = obs.obs_properties_add_int_slider(props, "custom_fps", "Custom FPS", 1, 200, 1)
	obs.obs_property_set_long_description(custom_fps, long_default_fps_description)

	default_fps_enabled = cached_settings.get("use_default_fps", True)
	obs.obs_property_set_enabled(custom_fps, not default_fps_enabled)

	def on_default_fps_clicked(props, prop, settings):
		default_fps_enabled = obs.obs_data_get_bool(settings, "use_default_fps")
		print(f"on_default_fps_clicked {default_fps_enabled=}")
		obs.obs_property_set_enabled(custom_fps, not default_fps_enabled)
		return True

	obs.obs_property_set_modified_callback(default_fps, on_default_fps_clicked)

	def on_enabled_clicked(props, prop, settings):
		enabled = obs.obs_data_get_bool(settings, "enabled")
		default_fps_enabled = obs.obs_data_get_bool(settings, "use_default_fps")
		if enabled:
			obs.obs_property_set_enabled(custom_fps, not default_fps_enabled)
		else:
			obs.obs_property_set_enabled(custom_fps, False)

		obs.obs_property_set_enabled(default_fps, enabled)

		return True


	obs.obs_property_set_modified_callback(enabled, on_enabled_clicked)

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
