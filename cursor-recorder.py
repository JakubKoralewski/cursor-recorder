import atexit
import ctypes
import json
import msvcrt
import os
import time
import re
from decimal import Decimal, ROUND_HALF_UP  # pylint: disable=unused-import

import pyautogui
import keyboard

# awareness = ctypes.c_int()
# ctypes.windll.shcore.SetProcessDpiAwareness(2)

refreshRate = 0.1  # Gap between saving cursor position to JSON in seconds

fetchAmount = int(1 / refreshRate)


def startMenu():
    print(
        "The cursor position will be fetched {} time{} a second.".format(
            fetchAmount, "" if fetchAmount == 1 else "s"
        )
    )
    input("ENTER to start recording.")
    os.system("cls")
    # Will be fixed with GUI
    # Every way of getting an ESC press had a problem
    print("Close script to end recording.")
    print("Consider setting cursor in TOP-LEFT corner.")


startMenu()
startText = "{{\n".format(refreshRate=refreshRate)


def exiting(taim):
    file.write('"lastTaim": {taim}\n}}'.format(taim=taim))


id = taim = 0
# impossible position, quick fix for undeclared variable error
previousData = [-1, -1]

with open("cursor-recorder.json", "w+") as file:
    file.write(startText)
    atexit.register(exiting, taim)
    while True:
        # sleep for refreshRate seconds
        time.sleep(refreshRate)
        # calculate current time
        taim = Decimal(id * refreshRate)
        # convert float to decimal using decimal module
        taim = Decimal(taim.quantize(
            Decimal(str(refreshRate)), rounding=ROUND_HALF_UP))

        # Get cursor position from pyautogui
        x, y = pyautogui.position()

        # Print current cursor position on screen
        positionStr = (
            "X: "
            + str(x).rjust(4)
            + " Y: "
            + str(y).rjust(4)
            + " | Duration: {}".format(taim)
        )
        print(positionStr, end="")
        print("\b" * len(positionStr), end="", flush=True)

        # save cursor positions to list
        data = [x, y]

        # if cursor doesn't move
        if previousData == data:
            id += 1  # don't write data, but add id
            continue

        previousData = data

        # save taim to file
        file.write('"{}":\n'.format(taim))

        # dump list to json
        json.dump(data, file, indent=4)

        id += 1

        # add comma and newline in between ids
        file.write(",\n")
    exiting(taim)
print("File saved in " + str(os.getcwd()) + "\\cursor-recorder.json.")
print("Duration of recording: {duration}".format(duration=taim))
atexit.unregister(exiting)
