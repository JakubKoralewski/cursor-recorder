# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright 2019 (c) Jakub Koralewski
__version__ = "0.1"

import json
import os
import time

import pyautogui
import keyboard


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


def save_to_file(**kwargs):
    times = kwargs["times"]
    positions = kwargs["positions"]
    refreshAmount = kwargs["refreshAmount"]

    output = {"refreshAmount": refreshAmount, "times": times, "positions": positions}
    len_times = len(times)
    len_positions = len(positions)
    if len_times != len_positions:
        print(
            f"Different number of positions and times elements!\nThere is {len_positions} positions and {len_times} len_times!"
        )

    with open("cursor-recorder.json", "w+") as file:
        json.dump(output, file)


def main():
    taim = 0
    skipping: bool = False
    prev_x = -1
    prev_y = -1
    refreshAmount = 60
    refreshRate = 1 / refreshAmount

    # Display start screen
    startMenu(refreshAmount)

    times = []
    positions = []

    startTaim = time.time_ns()
    while True:
        time.sleep(refreshRate)

        taim: int = (time.time_ns() - startTaim) / (10 ** 9)

        # Get cursor position
        x, y = pyautogui.position()

        # If previous position same as current
        # no need to add same data
        if prev_x == x and prev_y == y:
            skipping = True

            if keyboard.is_pressed("esc"):
                break
            continue
        else:
            if skipping == True:
                # If previously was skipping
                # create a keyframe that will stop sliding
                times.append(round(taim - refreshRate, 3))
                positions.append([prev_x, prev_y])

                if keyboard.is_pressed("esc"):
                    break

            skipping = False

        prev_x = x
        prev_y = y

        times.append(taim)
        positions.append([x, y])

        if keyboard.is_pressed("esc"):
            break

    save_to_file(times=times, positions=positions, refreshAmount=refreshAmount)
    print(f"File saved in {str(os.getcwd())}\\cursor-recorder.json.")
    print(f"Duration of recording: {taim}")


main()

