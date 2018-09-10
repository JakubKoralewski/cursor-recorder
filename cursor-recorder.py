# import atexit
import json
import os
import time
from decimal import Decimal, ROUND_HALF_UP  # pylint: disable=unused-import

import pyautogui
import keyboard

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
    print("RECORDING! Press ESC to stop.")
    print("Consider setting cursor in TOP-LEFT corner.")


startMenu()
startText = '{{\n"refreshRate": {refreshRate},\n'.format(refreshRate=refreshRate)


def lastTaim(taim):
    # add }, newline, "lastTaim": 0.1, newline }
    file.write('}},\n"lastTaim": {taim}\n}}'.format(taim=taim))


def writeData(x, y, id, taim):
    data = '"{id}": {{\n "taim": {taim},\n"x": {x},\n"y":{y} }}'.format(
        id=id, taim=taim, x=x, y=y
    )
    file.write(data)


id = taim = idAll = 0
# impossible position, quick fix for undeclared variable error
previousData = [-1, -1]

with open("cursor-recorder.json", "w+") as file:
    file.write(startText)
    file.write('"recording":\n{\n')
    # atexit.register(lastTaim, taim)
    while True:
        # sleep for refreshRate seconds
        time.sleep(refreshRate)
        idAll += 1

        taim = id * refreshRate
        # Get cursor position from pyautogui
        x, y = pyautogui.position()

        # save cursor positions to list
        data = [x, y]

        if previousData == data:
            # id += 1  # don't write data, but add id
            continue

        previousData = data

        # write data:
        writeData(x, y, idAll, taim)

        id += 1

        if keyboard.is_pressed("esc"):
            break
        # add comma and newline in between ids
        file.write(",\n")
    lastTaim(taim)
print("File saved in " + str(os.getcwd()) + "\\cursor-recorder.json.")
print("Duration of recording: {duration}".format(duration=taim))
# atexit.unregister(lastTaim)
