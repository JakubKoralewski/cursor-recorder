"""cursor-recorder"""
__version__ = '0.1'

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
    print("RECORDING! Press ESC to stop.")
    print("Consider setting cursor in TOP-LEFT corner.")


startMenu()
startText = '{{\n"refreshRate": {refreshRate},\n'.format(
    refreshRate=refreshRate)
# objId = objective Id, as in independent
id = taim = objId = 0
isEscHit = False


def lastTaim(taim):
    # add }, newline, "lastTaim": 0.1, newline }
    file.write('}},\n"lastTaim": {taim}\n}}'.format(taim=taim))


def writeData(x, y, taim):
    global objId
    objId += 1
    data = '"{id}": {{\n"taim": {taim},\n"x": {x},\n"y":{y} }}'.format(
        id=objId, taim=taim, x=x, y=y
    )
    file.write(data)


previousData = []
with open("cursor-recorder.json", "w+") as file:
    file.write(startText)
    file.write('"recording":\n{\n')
    while True:

        # sleep for refreshRate seconds
        time.sleep(refreshRate)
        id += 1

        # Get cursor position from pyautogui
        x, y = pyautogui.position()

        # save cursor positions to list
        data = [x, y]

        if previousData == data:
            continue

        previousData = data

        taim = id * refreshRate
        # write data:
        writeData(x, y, taim)

        if keyboard.is_pressed("esc"):
            break

        # add comma, newline in between ids
        # but don't add it in the last one
        file.write(",\n")

    lastTaim(taim)
print("File saved in " + str(os.getcwd()) + "\\cursor-recorder.json.")
print("Duration of recording: {duration}".format(duration=taim))
