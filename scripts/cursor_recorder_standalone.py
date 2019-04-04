# OBSOLETE! Please use the OBS script.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright 2019 (c) Jakub Koralewski


__version__ = "0.2"

import json
import os
import sys
import time
IS37 = True

try:
	time.time_ns()
except AttributeError as e:
	IS37 = False

import pyautogui
import keyboard
from typing import List, Tuple
from enum import Enum

class EXIT_TYPES(Enum): 
	""" Should exit using Escape key or manually. """
	KEYBOARD = 0
	SCRIPT = 1

refreshAmount = 60

EXIT_TYPE = EXIT_TYPES.SCRIPT
# Set to True to exit main loop
SHOULD_EXIT = False

def exit_loop():
	global SHOULD_EXIT
	SHOULD_EXIT = True

def startMenu(refreshAmount):
	print(
		"The cursor position will be fetched {} time{} a second.".format(
			refreshAmount, "" if refreshAmount == 1 else "s"
		)
	)
	input("ENTER to start recording.")
	os.system("cls")
	print("RECORDING! Press ESC to stop.")
	print("Consider setting cursor in TOP-LEFT corner.")

def should_exit() -> bool:
	if EXIT_TYPE == EXIT_TYPES.KEYBOARD:
		if keyboard.is_pressed("esc"):
			return True
	elif EXIT_TYPE == EXIT_TYPES.SCRIPT:
		if should_exit == True:
			return True
	return False

def save_to_file(seconds, x, y):
	full_path = "cursor-recorder.txt"

	with open(full_path, "a+") as file:
		file.write(f'{seconds} {x} {y}\n')
	#sys.stdout.write("%d% %d% %d% \r" % (seconds, x, y) )
	#sys.stdout.flush()
	print(seconds, x, y, flush=True, end='\r')


def main(path = None, name = None):
	global refreshAmount
	refreshRate: float = 1 / refreshAmount
	taim: int = 0
	skipping: bool = False

	# Cursor positions
	x: int
	y: int
	prev_x: int = -1
	prev_y: int = -1

	startTaim: int = time.time_ns() if IS37 else time.time()

	while True:
		time.sleep(refreshRate)
		if IS37:
			taim = (time.time_ns() - startTaim) / (10 ** 9)
		else:
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
				save_to_file(round(taim - refreshRate, 3), prev_x, prev_y)

				if should_exit():
					break

			skipping = False

		prev_x: int = x
		prev_y: int = y

		save_to_file(taim, x, y)

		if should_exit():
			break

	print(f"File saved in {str(os.getcwd())}\\cursor-recorder.json.")
	print(f"Duration of recording: {taim}")

if __name__ == "__main__":
	# If called directly ( not imported )
	# then exit from loop using Escape Key
	EXIT_TYPE = EXIT_TYPES.KEYBOARD
	
	# Display start screen
	startMenu(refreshAmount)
	main()

