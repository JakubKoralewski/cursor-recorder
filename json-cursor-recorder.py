import win32api
import time
import json
import os
import sys
import msvcrt
import ctypes

awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)

refreshRate = 0.1  # Gap between saving cursor position to JSON
waitTime = 3  # Countdown timer

""" def timeOut():
    t = waitTime
    while t > 0:
        print("{}s".format(t), end="\r")
        time.sleep(1)
        t -= 1 """


def getRefreshRate():
    input("ENTER to start recording.")
    os.system("cls")
    print("Press ESC to stop recording.")
    print("Consider setting cursor in TOP-LEFT corner.")


getRefreshRate()

with open("json-cursor-recorder.json", "w+") as file:
    startText = '{{\n"refreshRate": {refreshRate},\n'.format(refreshRate=refreshRate)
    file.write(startText)
    id = 0
    while True:
        x, y = win32api.GetCursorPos()  # Get cursor position from win32 api
        print(
            "x: {} y: {}".format(x, y), end="\r"
        )  # Print current cursor position on screen
        file.write('"{}":\n'.format(id))  # write current id to JSON
        data = [x, y]  # save cursor positions to list
        time.sleep(refreshRate)
        json.dump(data, file, indent=4)
        if (
            msvcrt.kbhit() and msvcrt.getch() == chr(27).encode()
        ):  # Get ESCAPE # On EXIT:
            file.write(",\n")  # end file #add newline and } in the end of the file
            file.write('\n"lastId": {id}\n'.format(id=id))
            file.write("}")
            break
        id += 1
        file.write(",\n")  # add comma and newline in between ids


print("File saved in " + str(os.getcwd()) + "\\python-cursor-recorder.json.")
print("Press anything to exit.")
input()
