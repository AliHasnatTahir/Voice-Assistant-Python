import cv2
import psutil
import time
import pyautogui as py
import os
import datetime
import screen_brightness_control as sbc
import re
from file import search_all
from words import find_word
from recognize import speak, command


def open_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("I cannot open the camera")

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow('Camera', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def get_open_applications():
    apps = []
    for p in psutil.process_iter(['pid', 'name']):
        if p.info['name'].lower() in ['explorer.exe', 'taskmgr.exe']:
            continue
        if p.info['name'].lower().endswith('.exe'):
            apps.append(p.info['name'])
    return apps


def check_app_open(app_name):
    open_apps = get_open_applications()
    for word in open_apps:
        if app_name in word.lower():
            return True
    return None


def close_application(app_name):
    for proc in psutil.process_iter(['name', 'pid']):
        if app_name in proc.info['name'].lower():
            proc.kill()
            speak(f"{proc.info['name'].lower()} has been closed")
            break
    else:
        speak(f"Application is not open")


def open_app(app_name):
    py.hotkey('winleft', 's')

    time.sleep(1)

    py.write(app_name)

    time.sleep(1)

    py.press('enter')

    time.sleep(1)


def volume_up(percentage):
    for _ in range(percentage):
        py.press('volumeup')


def volume_down(percentage):
    for _ in range(percentage):
        py.press('volumedown')


def volume_mute():
    py.press('volumemute')


def brightness():
    speak("How much brightness do you want")

    text = command()

    level = re.findall(r'\d+', text)

    sbc.set_brightness(level)


def get_properties(path):
    if ":\\" in path:
        file_path = path
    else:
        word = find_word(path, "properties")
        file_path = search_all(word)
    stat = os.stat(file_path)

    file_size_mb = stat.st_size / (1024 * 1024)

    created_time = datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    modified_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    accessed_time = datetime.datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')

    is_file = os.path.isfile(path)
    is_dir = os.path.isdir(path)

    print(f"Size: {file_size_mb:.2f} MB")
    print(f"Created time: {created_time}")
    print(f"Last modified time: {modified_time}")
    print(f"Last accessed time: {accessed_time}")
    print(f"Is file: {is_file}")
    print(f"Is directory: {is_dir}")


def battery():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    if int(percentage) == 100:
        speak("Battery is full")
    else: 
        speak(f"{percentage} % battery left")
    charger_plugged = battery.power_plugged
    if charger_plugged == True:
        speak("and charger is plugged in")
    else:
        speak("and charger is not plugged")
    sec_left = int(battery.secsleft) / 60
    if sec_left >= 0:
        speak(f"and the estimated time remaining of battery is {sec_left} minutes")
    else:
        speak("The charger is plugged in so you can use it for long time so enjoy.")


def remember(query):

    remember_text = query.split("remember", 1)[1].strip()

    with open("remember.txt", "a") as file:
        file.write(remember_text + "\n")
        print("Ok I will remember it.")
        speak("Ok I will remember it.") 