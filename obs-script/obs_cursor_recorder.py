# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. 
# 
# Copyright 2019 (c) Jakub Koralewski
#

import obspython as obs
import datetime
import os
import atexit

print(f"{datetime.datetime.now().time()}: refresh")

import cursor_recorder

description = (
    open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "obs-script",
            "description.html",
        ),
        encoding="utf-8",
        newline="",
    )
    .read()
    .replace("\n", "")
)
def script_description():
    return description

def script_properties():
	now = datetime(2018,1,1,0,0)
	props = obs.obs_properties_create()
	obs.obs_properties_add_bool(props, "enabled", "Enabled")
	obs.obs_properties_add_int(props, "duration", "Recording Duration (Minutes)", 1, 120, 1)
	st = obs.obs_properties_add_list(props, "start_time", "Record Start Time", obs.OBS_COMBO_TYPE_LIST , obs.OBS_COMBO_FORMAT_STRING)
	obs.obs_property_list_add_string(st, "None", "None")
	et = obs.obs_properties_add_list(props, "end_time", "Record End Time", obs.OBS_COMBO_TYPE_LIST , obs.OBS_COMBO_FORMAT_STRING)
	for x in range(96):
		obs.obs_property_list_add_string(st, str(datetime.time(now).strftime( "%I:%M %p")), str(datetime.time(now)))
		obs.obs_property_list_add_string(et, str(datetime.time(now).strftime( "%I:%M %p")), str(datetime.time(now)))
		now += timedelta(minutes=15)	

	obs.obs_properties_add_bool(props, "enabled_stream", "Include Streaming")
	obs.obs_properties_add_bool(props, "debug_mode", "Debug Mode")
	return props

def script_save(settings):
	script_update(settings)

def script_update(settings):
	global Enabled_Recording
	global Enabled_Streaming
	global Pause_Time
	global Recording_Start
	global Recording_Timer
	global Recording_End
	global Time_To_Record

	if obs.obs_data_get_bool(settings, "enabled") is not Enabled_Recording:
		if obs.obs_data_get_bool(settings, "enabled") is True:
			if Debug_Mode: print("Loading Timer")

			Enabled_Recording = True
			obs.timer_add(timer_check_recording,30000)
		else:
			if Debug_Mode: print("Unloading Timer")

			Enabled_Recording = False
			obs.timer_remove(timer_check_recording)

	if obs.obs_data_get_int(settings, "duration") == 0:
		Recording_Timer = 30 * 60
	else:
		Recording_Timer = obs.obs_data_get_int(settings, "duration") * 60

	Time_To_Record = time.time() + Recording_Timer
	if obs.obs_data_get_string(settings, "start_time") == "" or obs.obs_data_get_string(settings, "start_time") == "None" or obs.obs_data_get_string(settings, "start_time") == obs.obs_data_get_string(settings, "end_time"):
		Recording_Start = "None"
		obs.obs_data_set_bool(settings, "enabled_stream", False)
		Enabled_Streaming = False
	else:
		Recording_Start = obs.obs_data_get_string(settings, "start_time")

	if obs.obs_data_get_string(settings, "end_time") == "":
		Recording_Start = "None"
		obs.obs_data_set_bool(settings, "enabled_stream", False)
		Enabled_Streaming = False
	else:
		Recording_End = obs.obs_data_get_string(settings, "end_time")
	Debug_Mode = obs.obs_data_get_bool(settings, "debug_mode")
	Enabled_Streaming = obs.obs_data_get_bool(settings, "enabled_stream")



