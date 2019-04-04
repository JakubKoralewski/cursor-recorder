# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. 
# 
# Copyright 2019 (c) Jakub Koralewski
#

import obspython as obs
import datetime
import os
#import atexit

print(f"{datetime.datetime.now().time()}: refresh")

#import sys
#sys.path.insert(1, os.path.join(sys.path[0], "..", "python-script"))

import_succeeded = False
cursor_recorder = None

cached_settings = {}

from pprint import pprint
from subprocess import call


#import pip
""" def install(package: str, upgrade = False):
	arguments = ['install', '--upgrade', package] if upgrade else ['install', package]
	print(f'install arguments: {arguments}')
	if hasattr(pip, 'main'):
		pip.main(arguments)
	else:
		#FIXME: DOES NOT WORK
		from pip._internal import main as pipmain
		pipmain(arguments) """
#install('pip', upgrade=True)

py_interpreter = os.path.join(os.__file__.split("lib")[0], "python.exe")
print(f'py_interpreter: {py_interpreter}')

def install_pip():
	global py_interpreter
	call([py_interpreter, '-m', 'pip', 'install', '--upgrade', 'pip'])

def install(package: str):
	call([py_interpreter, '-m', 'pip', 'install', package])


def import_cursor_recorder(path: str):
	global cursor_recorder
	install_pip()
	import importlib.util
	spec = importlib.util.spec_from_file_location("cursor_recorder", path)
	too_many_tries = False
	many_tries = 5
	i = 0
	last_missing_import = ''
	while not too_many_tries:
		try:
			cursor_recorder = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(cursor_recorder)
		except ImportError as e:
			""" May happen when the cursor_recorder.py has modules that aren't present. """
			if last_missing_import == e.name:
				print('ERROR: Tried to import same module twice!')
				break
			last_missing_import = e.name
			print(f'ERROR: No module named: {e.name}!')
			install(e.name)
		finally:
			if i > many_tries:
				too_many_tries = True
			i += 1
	if too_many_tries:
		return False
	return True

#pprint(vars(obs._obspython), indent=4)


def script_description():
	print('script_description')
	return "<h1>OBS Cursor Recorder</h1><b>Lets you save your cursor movement to a JSON formatted file.</b><br/><br/>©2019 Jakub Koralewski. Open-source on GitHub.<hr />"

def script_properties():
	print('script_properties')
	props = obs.obs_properties_create()
	obs.obs_properties_add_bool(props, "enabled", "Enabled")
	obs.obs_properties_add_path(props, "cursor_recorder", "Cursor Recorder Python Script", obs.OBS_PATH_FILE, "*.py", "")
	#obs.obs_properties_add_path(props, "file", "Directory to save JSON file", obs.OBS_PATH_DIRECTORY, None, "")
	#obs.obs_properties_add_path(props, "python_path", "Copy Python Path from Python Settings", obs.OBS_PATH_DIRECTORY, '.exe', py_interpreter)
	return props

def script_save(settings):
	print('script_save')
	script_update(settings)

def script_update(settings):
	print('script_update')
	#cached_settings["file"] = obs.obs_data_get_string(settings, "file")
	cached_settings["python_path"] = obs.obs_data_get_string(settings, "python_path")
	#print("file directory: ", cached_settings["file"])
	cached_settings["cursor_recorder"] = obs.obs_data_get_string(settings, "cursor_recorder")
	cached_settings["enabled"] = obs.obs_data_get_int(settings, "enabled")
	print(f'cached_settings: {cached_settings}')
	global import_succeeded
	if cached_settings["cursor_recorder"] != '' and not import_succeeded:
		if import_cursor_recorder(cached_settings["cursor_recorder"]):
			import_succeeded = True
			#pprint(vars(cursor_recorder), indent=2)

def script_defaults(settings):
	print('script_defaults')
	""" config = obs.obs_frontend_get_profile_config() """
	obs.obs_data_set_default_bool(settings, "enabled", True)
	#obs.obs_data_set_default_string(settings, "python_path", sys.executable)



