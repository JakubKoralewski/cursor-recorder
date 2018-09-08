import ctypes
import json
import msvcrt
import os
import time
import re
from decimal import *  # pylint: disable=unused-import

import pyautogui

awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)

refreshRate = 0.1  # Gap between saving cursor position to JSON

# calculate the amount of digits printed after .
# ex.: 0.3 -> 1, 1 -> 1, 0.001 -> 3
# useful when refreshRate will be subject to change
rerefreshRate = re.findall(r"\.(\d+)", (str(refreshRate)))
if rerefreshRate:
    precision = len(rerefreshRate[0])
else:
    precision = 1
context = Context(prec=precision + 1)
print("precision: {}".format(precision))


def startMenu():
    print(
        "The cursor position will be fetched {} times a second.".format(
            int(1 / refreshRate)
        )
    )
    input("ENTER to start recording.")
    os.system("cls")
    print("Press ESC to stop recording.")
    print("Consider setting cursor in TOP-LEFT corner.")


startMenu()
startText = "{{\n".format(refreshRate=refreshRate)
id = 0
taim = 0
previousData = [-1, -1]  # impossible position, quick fix for undeclared variable error

with open("cursor-recorder.json", "w+") as file:
    file.write(startText)

    while True:
        # sleep for refreshRate seconds
        time.sleep(refreshRate)
        taim = context.create_decimal_from_float(id * refreshRate)

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

        if previousData == data:
            id += 1  # don't write data, but add id
            continue

        previousData = data

        # save id to file
        file.write('"{}":\n'.format(taim))

        # dump list to json
        json.dump(data, file, indent=4)

        # if ESCAPE pressed:
        if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
            # end file
            print("ESC HIT")
            file.write(',\n"lastTaim": {taim}\n}}'.format(taim=taim))
            break

        id += 1

        # add comma and newline in between ids
        file.write(",\n")

print("File saved in " + str(os.getcwd()) + "\\cursor-recorder.json.")
print("Duration of recording: {duration}".format(duration=taim))
