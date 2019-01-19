"""cursor-recorder"""
__version__ = "0.1"

import json
import os
import time
import atexit

import pyautogui
import keyboard

import asyncio


def cleanup():
    with open("cursor-recorder.json", "r+") as file:
        print(file.read())


atexit.register(cleanup)


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


def main():
    ajdi = 0
    taim = 0
    skipping = False
    previousData = []
    refreshAmount = 60
    refreshRate = 1 / refreshAmount

    startMenu(refreshAmount)

    with open("cursor-recorder.json", "w+") as file:
        startTaim = time.time_ns()
        file.write(f'{{"refreshAmount":{refreshAmount},"data":[')
        while True:

            # TODO: because of this exit doesn't work!!!
            # FIXEDTODO because of this after a while it may get unsynchronized
            #await asyncio.sleep(refreshRate)
            time.sleep(refreshRate)

            ajdi += 1
            taim = (time.time_ns() - startTaim) / (10 ** 9)
            # Get cursor position from pyautogui
            x, y = pyautogui.position()

            # save cursor positions to list
            data = [x, y]

            if previousData == data:
                skipping = True
                continue
            else:
                if skipping == True:
                    # writeData(previousData[0], previousData[1], taim - ( 1/refreshAmount ))
                    previousData = (
                        f'{{"t":{taim - ( refreshRate ):.3f},"x":{x},"y":{y}}}'
                    )
                    file.write(previousData)
                    if keyboard.is_pressed("esc"):
                        break
                    file.write(",")
                skipping = False

            previousData = data
            data = f'{{"t":{taim:.3f},"x":{x},"y":{y}}}'
            file.write(data)

            if keyboard.is_pressed("esc"):
                break

            # add comma, newline in between ids
            # but don't add it in the last one
            file.write(",")
        file.write("]}")

        """ lastTaim(taim) """
    print("File saved in " + str(os.getcwd()) + "\\cursor-recorder.json.")
    print("Duration of recording: {duration}".format(duration=taim))

main()
""" async def listenToExit():
    while True:
        yield keyboard.is_pressed("esc")


async def main():
    await asyncio.gather(main(), listenToExit())


asyncio.run(main()) """
