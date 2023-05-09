import pyttsx3
import speech_recognition as sr
from vosk import Model,KaldiRecognizer
import screen_brightness_control as sbc
import pandas as pd
import pyaudio
import os
import shutil
import re
import subprocess
import webbrowser
import nltk
from nltk.corpus import stopwords
import datetime
import pyautogui as py
import time
from googlesearch import search
from twilio.rest import Client
import openai
import pywikihow
import psutil
import speedtest
import cv2
import geocoder
import requests




api_key = "46aa6862ecbf867fb74ed0f2fb590fd6"
account_sid = "ACf5a1538ff0a529f02bce0c5a376f727f"
auth_token = "d429f578fe7315fc23e535a80337eb4f"
openai.api_key = "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"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

def command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print("You said: " + query)
    except sr.UnknownValueError:
        print("Say again...")
        return "None"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "None"
    return query


def vosk():
    model = Model("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Vosk\\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)
        if len(data) == 0:
            print("Mic not working")
            break
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result()[14:-3])


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def find_link(text):
    pattern1 = re.compile("(?P<url>www[^\s]+)")
    match1 = re.findall(pattern1, text)
    pattern2 = re.compile("(?P<url>https://[^\s]+)")
    match2 = re.findall(pattern2, text)
    pattern3 = re.compile("\\b\w*\.com\\b")
    match3 = re.findall(pattern3, text)
    
    match = match1 + match2 + match3
    if match == []:
        return None
    else:
        return match[0]


def get_url(query):
    for url in search(query, num_results=1):
        return url
    

def chatgpt_ai(input_text):
    output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user",
    "content": input_text}]
    )
    answer = output.choices[0].message.content.replace('"', '')
    if "sorry" in answer or "?" in answer or "but" in answer or "AI language model" in answer:
        print("I cannot understand")
        speak("I cannot understand")
        return False
    else:
        print(answer)
        speak(answer)
        return True
    

def msg_send():
    while True:
        speak("Please speak the number to whom you want to send the message")
        text = command.lower()
        num = re.findall(r'\d+', text)
        number = ''.join(num)
        number = number.replace(' ', '')
        if number.startswith("92"):
            number = "+" + number
        elif not number.startswith("+92"):
            number = "+92" + number

        if len(number) == 13:
            speak(f"Do you want to send a message to this number {number}")
            check = command.lower()
            if check == "yes" or check == "yeah":
                speak("what do you want to send")
                msg = command()

                client = Client(account_sid, auth_token)
                message = client.messages.create(
                body=msg,
                from_="+19593350437",
                to=number
                )
                speak("Message successfully sent")
                break
        else:
            speak(f"Phone Number is not correct : {number}")


def speed_test():
    speed = speedtest.Speedtest()
    download_speed = round(float(speed.download()) * 0.000000125, 2)
    upload_speed = round(float(speed.upload()) * 0.000000125, 2)

    print(f"the downloading speed is {download_speed} megabytes and uploading speed is {upload_speed} megabytes")
    speak(f"the downloading speed is {download_speed} megabytes and uploading speed is {upload_speed} megabytes")


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
        if app in word.lower():
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


def how_question(query):
    searched = pywikihow.search_wikihow(query, max_results=1)
    assert len(searched) == 1
    print(searched[0].summary)


def removal_words(sentence):
    tokens = nltk.word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if not word.lower() in stop_words]
    return(filtered_tokens)


def find_word(text, name):
    if name in text:
        index = text.index(name)
        word = text[index+1]
        return(word)
    else:
        speak("I cannot understand")
        return None


def get_myweather():
    g = geocoder.ip('me')

    weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={g.lat}&lon={g.lng}&appid={api_key}'

    response = requests.get(weather_url)

    weather_data = response.json()

    if weather_data["cod"] != "404":

        main = weather_data["main"]
        temperature = main["temp"]
        description = weather_data["weather"][0]["description"]
        wind = weather_data["wind"]["speed"]

        temperature = temperature - 273.15

        print(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
        speak(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
    else:
        print("Location not found.")
        speak("Location not found.")


def get_otherweather(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + location

    response = requests.get(complete_url)

    weather_data = response.json()

    if weather_data["cod"] != "404":

        main = weather_data["main"]
        temperature = main["temp"]
        description = weather_data["weather"][0]["description"]
        wind = weather_data["wind"]["speed"]

        temperature = temperature - 273.15

        print(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
        speak(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
        
    else:
        print("Location not found.")
        speak("Location not found.")


def get_search(file_or_folder_name):
    drives = ["%s:\\" % d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists("%s:\\" % d)]
    results = []
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for name in files + dirs:
                if file_or_folder_name.lower() in name.lower():
                    print(os.path.join(root, name))
                    results.append(os.path.join(root, name))

    return results


def search_all(filename):
    results = get_search(filename)
    if len(results) == 0:
        speak("No results found")
        return None
    elif len(results) == 1:
        return results[0]
    else:
        speak("Multiple results found:")
        for i, path in enumerate(results):
            print(f"{i+1}. {path}")
        while True:
            choice = input("Enter the number of the file or folder you want to select: ")
            try:
                choice = int(choice)
                if choice >= 1 and choice <= len(results):
                    print(f"Selected the {results[choice-1]}")
                    speak(f"Selected the {results[choice-1]}")
                    return results[choice-1]
            except:
                pass
            speak("Invalid choice")


def delete_file(filename):
    if ":\\" in filename:
        filepath = filename
    else:
        file = find_word(filename, "delete")
        filepath = search_all(file)

    if filepath is not None:
        speak("Do you really want to delete it?")
        confirm = command().lower()
        if confirm == "yes" or confirm == "Yes" or confirm == "yeah":
            if os.path.isfile(filepath):
                os.remove(filepath)
                speak("File removed successfully!") 
            elif os.path.isdir(filepath):
                if not os.listdir(filepath):
                    os.rmdir(filepath)
                    speak("Directory removed successfully!")
                else:
                    shutil.rmtree(filepath)
                    speak("Directory and its contents removed successfully!")
        else:
            speak("Deletion cancelled by user.")
    else:
        speak("File or folder not found in disk.")


def cut_paste(name):
    if ":\\" in name:
        filepath = name
    else:
        file = find_word(name, "cut")
        filepath = search_all(file)

    if filepath is not None:
        speak("where do you want to paste it.")
        destination_path = command().lower()
        if "drive" in destination_path or "disk" in destination_path:
            drives = ["%s:\\" % d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists("%s:\\" % d)]
            match = re.search(r'drive\s+([a-zA-Z])', destination_path)
            match2 = re.search(r'disk\s+([a-zA-Z])', destination_path)
            if match:
                letter = match.group(1).upper()
                drive = letter + ":\\"
                if drive in drives:
                    try:
                        shutil.move(filepath, drive)
                        speak(f"{filepath} has been cut and pasted to {drive}.")
                    except:
                        speak("Error occurred while moving the file/folder.")
            elif match2:
                letter = match2.group(1).upper()
                drive = letter + ":\\"
                if drive in drives:
                    try:
                        shutil.move(filepath, drive)
                        speak(f"{filepath} has been cut and pasted to {drive}.")
                    except:
                        speak("Error occurred while moving the file/folder.")
            else:
                speak("Enter a write drive letter")
        elif "in" in destination_path:
            words = destination_path.split()
            index = words.index("in")
            word= words[index+1]
            if word:
                letter = word.capitalize()
                folder = search_all(letter)
                if folder:
                    try:
                        shutil.move(filepath, folder)
                        speak(f"{filepath} has been cut and pasted to {folder}.")
                    except:
                        speak("Error occurred while moving the file/folder.")
                else:
                    letter = word.lower()
                    folder_lower = search_all(letter)
                    if folder_lower:
                        try:
                            shutil.move(filepath, folder_lower)
                            speak(f"{filepath} has been cut and pasted to {folder_lower}.")
                        except:
                            speak("Error occurred while moving the file/folder.")
                    else:
                        speak("Cannot find it")
        else:
            speak("Cannot find the destination where you want to paste it.")
    else:
        speak(f"{name} do not found.")


def copy_paste(name):
    if ":\\" in name:
        filepath = name
    else:
        file = find_word(name, "copy")
        filepath = search_all(file)

    if filepath is not None:
        speak("where do you want to paste it.")
        destination_path = command().lower()
        if "drive" in destination_path or "disk" in destination_path:
            drives = ["%s:\\" % d for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists("%s:\\" % d)]
            match = re.search(r'drive\s+([a-zA-Z])', destination_path)
            match2 = re.search(r'disk\s+([a-zA-Z])', destination_path)
            if match:
                letter = match.group(1).upper()
                drive = letter + ":\\"
                if drive in drives:
                    try:
                        if os.path.isfile(filepath):
                            shutil.copy2(filepath, drive)
                            speak(f"{filepath} copied to '{drive}'")
                        elif os.path.isdir(filepath):
                            shutil.copytree(filepath, f"{drive}\\{name}")
                            speak(f"{filepath} copied to '{drive}'")
                    except:
                        speak("Error occurred while moving the file/folder.")
            elif match2:
                letter = match2.group(1).upper()
                drive = letter + ":\\"
                if drive in drives:
                    try:
                        if os.path.isfile(filepath):
                            shutil.copy2(filepath, drive)
                            speak(f"{filepath} copied to '{drive}'")
                        elif os.path.isdir(filepath):
                            shutil.copytree(filepath, f"{drive}\\{name}")
                            speak(f"{filepath} copied to '{drive}'")
                    except:
                        speak("Error occurred while moving the file/folder.")
            else:
                speak("Enter a right drive letter")
        elif "in" in destination_path:
            words = destination_path.split()
            index = words.index("in")
            word= words[index+1]
            if word:
                letter = word.capitalize()
                folder = search_all(letter)
                if folder:
                    try:
                        if os.path.isfile(filepath):
                            shutil.copy2(filepath, folder)
                            speak(f"{filepath} copied to '{folder}'")
                        elif os.path.isdir(filepath):
                            shutil.copytree(filepath, f"{folder}\\{name}")
                            speak(f"{filepath} copied to '{folder}'")
                    except:
                        speak("Error occurred while moving the file/folder.")
                else:
                    letter = word.lower()
                    folder_lower = search_all(letter)
                    if folder_lower:
                        try:
                            if os.path.isfile(filepath):
                                shutil.copy2(filepath, folder_lower)
                                speak(f"{filepath} copied to '{folder_lower}'")
                            elif os.path.isdir(filepath):
                                shutil.copytree(filepath, f"{folder}\\{name}")
                                speak(f"{filepath} copied to '{folder_lower}'")
                        except:
                            speak("Error occurred while moving the file/folder.")
                    else:
                        speak("Cannot find it")
        else:
            speak("Enter a right folder name")
    else:
        speak(f"{name} do not found.")


def rename_file(filename):
    if ":\\" in filename:
        file_path = filename
    else:
        word = find_word(filename, "rename")
        file_path = search_all(word)
    if file_path:
        new_name = input("Enter a new name of file or folder")
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        speak(f"{filename} has been renamed to {new_name}.")
    else:
        speak(f"{filename} not found.")


def open_file(filename):
    if ":\\" in filename:
        file_path = filename
    else:
        word = find_word(filename, "open")
        file_path = search_all(word)
    if file_path is not None:
        file = os.startfile(file_path)
    else:
        speak(f"{filename} not found.")


def is_internet_on():
    try:
        response = subprocess.check_output(['ping', '-n', '1', '-w', '5000', 'google.com'])
        return True
    except subprocess.CalledProcessError:
        return False


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



def add(query, result):
    number = re.findall(r'\d+', query)
    for num in number:
        result = result + int(num)
    print("Answer: ", result)
    speak(f"Answer is {result}")
    return(result)


def subtract(query, result):
    number = re.findall(r'\d+', query)
    for num in number:
        result = result - int(num)
    print("Answer: ", result)
    speak(f"Answer is {result}")
    return(result)


def multiply(query, result):
    number = re.findall(r'\d+', query)
    for num in number:
        result = result * int(num)
    print("Answer: ", result)
    speak(f"Answer is {result}")
    return(result)


def divided(query, result):
    number = re.findall(r'\d+', query)
    result = int(number[0])
    for num in number[1:]:
        result = float(result / int(num))
    print("Answer: ", result)
    speak(f"Answer is {result}")
    return(result)


def divide(query, result):
    number = re.findall(r'\d+', query)
    for num in number:
        result = float(result / int(num))
    print("Answer: ", result)
    speak(f"Answer is {result}")
    return(result)


def remaining_calculation(result):
    while True:
        speak("Do you want to perform other calculations with answer?")
        text = command().lower()
        if "yes" in text or "Yeah" in text:
            speak("What do you want to do?")
            sentence = command().lower()
            if "add" in sentence or "plus" in sentence or "+" in sentence:
                result = add(sentence, result)
            elif "subtract" in sentence or "minus" in sentence or "-" in sentence:
                result = subtract(sentence, result)
            elif "multiply" in sentence or "*" in sentence or "multiplied" in sentence:
                result = multiply(sentence, result)
            elif "divide" in sentence or "/" in sentence or "divided" in sentence or "division" in sentence:
                result = divide(sentence, result)
            else:
                speak("i cannot understand it") 
        else:
            break


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


def write_error(error):
    timestamp = datetime.datetime.now()
    df = pd.DataFrame({"Errors": [error], "Time": [timestamp]})

    try:
        existing_data = pd.read_excel("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Errors.xlsx")
        updated_data = pd.concat([existing_data, df], ignore_index=True)
        updated_data.to_excel("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Errors.xlsx", index=False)
        
    except FileNotFoundError:
        df.to_excel("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Errors.xlsx", index=False)


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Boss!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Boss!")   

    else:
        speak("Good Evening Boss!")  

    assname=("Red Sword version 1.0")
    speak("I am your Assistant")
    speak(assname)


def takeCommandname():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Username...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Trying to Recognizing Name...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)    
        print("Unable to Recognizing your name.")
        takeCommandname()  
        return "None"
    return query


def usrname():
    speak("What should i call you sir")
    uname=takeCommandname()
    speak("Welcome")
    speak(uname)  






wishMe()
# usrname()
while True:
    internet = is_internet_on()
    if internet:
        speak("What can i do for you? Boss!")
        # query = command().lower()
        query = "exit"
        work = removal_words(query)
        if "open" in work and ("file manager" in work or "file explorer" in work or "this pc" in work):
            # TO OPEN THE FILE MANAGER
            os.startfile("::{20D04FE0-3AEA-1069-A2D8-08002B30309D}")
        elif "open" in work and "c" in work and ("drive" in work or "disk" in work):
            path = "C:/"
            os.startfile(path)
        elif "open" in work and "e" in work and ("drive" in work or "disk" in work):
            path = "E:/"
            os.startfile(path)       
        elif "open" in work and ("power shell" in work or "powershell" in work):
            # Open Powershell
            os.startfile("C:\Windows\WinSxS\wow64_microsoft-windows-powershell-exe_31bf3856ad364e35_10.0.22621.1_none_d50074ba2a5195be\powershell.exe")
        elif "open" in work and ("terminal" in work or "command prompt" in work):
            # Open CMD
            os.startfile("C:\Windows\System32\cmd.exe")
        elif "open" in work and ("search" in work or "search bar" in work):
            # Open Search
            os.system("start ms-search:")
        elif "open" in work and "control panel" in work:
            # Open Control Panel
            os.system('control')
        elif "open" in work and ("settings" in work or "computer settings" in work):
            # Open Windows Settings
            os.system("start ms-settings:")
        elif "open" in work and ("network connection" in work or "network connections" in work):
            # Open Network Connections
            os.system("ncpa.cpl")
        elif "open" in work and ("computer manage" in work or "computer management" in work):
            # Open Computer Management
            os.system("compmgmt.msc")
        elif "open" in work and ("disk manage" in work or "disk management" in work):
            # Open Disk Management
            os.system("diskmgmt.msc")
        elif "open" in work and ("drive manage" in work or "drive management" in work):
            # Open Disk Management
            os.system("diskmgmt.msc")
        elif "open" in work and ("system properties" in work or "properties" in work):
            # Open System Properties
            os.system("sysdm.cpl")
        elif "open" in work and ("event viewer" in work or "event" in work or "events viewer" in work or "events" in work):
            # Open Event Viewer
            os.system("eventvwr.msc")
        elif "open" in work and ("power options" in work or "power option" in work):
            # Open Power Options
            os.system("powercfg.cpl")
        elif "open" in work and ("mobility center" in work or "center" in work):
            # Open Mobility Center
            os.system("mblctr")
        elif "open" in work and ("installed app" in work or "installed apps" in work):
            # Open Installed Apps
            os.system("start ms-settings:appsfeatures")
        elif "show" in work and ("installed app" in work or "installed apps" in work):
            # Open Installed Apps
            os.system("start ms-settings:appsfeatures")
        elif "open" in work and ("device manage" in work or "device manager" in work or "device management" in work):
            # Open Device Manager
            os.system("devmgmt.msc")
        elif "open" in work and ("task manage" in work or "task management" in work or "task manager" in work):
            # Open Task Manager
            os.system("taskmgr")
        elif "open" in work and ("note" in work or "pad" in work or "notepad" in work):
            # Open Notepad
            os.startfile("notepad.exe")
        elif ("increase" in work and ("brightness" in work or "bright" in work)) or ("decrease" in work and ("brightness" in work or "bright" in work)):
            brightness()
        elif ("show" in work or "what" in work) and ("brightness" in work or "brightness level" in work or "bright level" in work):
            print(sbc.get_brightness())
        elif "open" in work and "browser" in work:
            webbrowser.open("https://www.google.com")
        elif "search" in work and ("file" in work or "folder" in work):
            name = find_word(work, "search")
            if name is not None:
                file = search_all(name)
                speak("What do you want to do with it?")
                answer = command().lower()
                if "rename" in answer:
                    rename_file(file)
                elif "open" in answer:
                    open_file(file)
                elif "delete" in answer:
                    delete_file(answer)
                elif "copy" in answer:
                    copy_paste(answer)
                elif "cut" in answer:
                    cut_paste(answer)
                elif "properties" in answer:
                    get_properties(answer)
                else:
                    pass
        elif "rename" in work and ("file" in work or "folder" in work):
            rename_file(work)
        elif "open" in work and ("file" in work or "folder" in work):
            open_file(work)
        elif "delete" in work and ("file" in work or "folder" in work):
            delete_file(work)
        elif "copy" in work and ("file" in work or "folder" in work):
            copy_paste(work)
        elif "cut" in work and ("file" in work or "folder" in work):
            cut_paste(work)
        elif "show" in work and "properties" in work:
            get_properties(work)
        elif "increase volume" in query or "increasevolume" in query or "volume up" in query or "volumeup" in query:
            level = re.findall(r'\d+', query)
            if level:
                volume = int(int(level[0]) / 2)
                volume_up(volume)
            else:
                speak("how many volume do you want to increase?")
                sound = command()
                volume = re.findall(r'\d+', sound)
                up = int(int(volume[0]) / 2)
                volume_up(up)
        elif "decrease volume" in query or "decreasevolume" in query or "volume down" in query or "volumedown" in query:
            level = re.findall(r'\d+', query)
            if level:
                volume = int(int(level[0]) / 2)
                volume_down(volume)
            else:
                speak("how many volume do you want to decrease?")
                sound = command()
                volume = re.findall(r'\d+', sound)
                up = int(int(volume[0]) / 2)
                volume_down(up)
        elif "mute" in query:
            volume_mute()
        elif "unmute" in query:
            volume_up(1)
        elif "show" in query and ("notification" in query or "notification panel" in query or "notifications" in query):
            py.hotkey("win", "n")
        elif ("open" in query or "show" in query) and ("action center" in query or "action centre" in query or "action" in query):
            py.hotkey("win", "a")
        elif ("open" in query or "show" in query) and ("clip board" in query or "clipboard" in query):
            py.hotkey("win", "v")
        elif "add" in query or "plus" in query or "+" in query:
            result = add(query, 0)
            remaining_calculation(result)
        elif "subtract" in query or "minus" in query or "-" in query:
            number = re.findall(r'\d+', query)
            result = subtract(query, 2*int(number[0]))
            remaining_calculation(result)
        elif "multiply" in query or "*" in query or "multiplied" in query:
            result = multiply(query, 1)
            remaining_calculation(result)
        elif "divide" in query or "/" in query  or "divided" in query or "division" in query:
            result = divided(query, 1)
            remaining_calculation(result)
        elif "open" in query and "website" in query:
            word = work.index("open")
            if work[word+1] == "website" or work[word+1] == "webite":
                website = work[word+2]
            else:
                website = work[word+1]
            url = get_url(website)
            webbrowser.open(url)
        elif ("battery" in query and "percentage" in query) or "how much battery left" in query or "how much power left" in query or "what is battery percentage" in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            if int(percentage) == 100:
                speak("Battery is full")
            else: 
                speak(f"{percentage} % battery left")
        elif "battery" in query or "status of battery" in query:
            battery()
        elif "internet" in query and "speed" in query:
            speed_test()
        elif ("open" in query or "show" in query) and "camera" in query:
            open_camera()
        elif "open" in query and ("app" in query or "application" in query or "apps" in query or "applications" in query):
            word = work.index("open")
            if work[word+1] == "app" or work[word+1] == "application" or work[word+1] == "apps" or work[word+1] == "applications":
                app = work[word+2]
            else:
                app = work[word+1]
            open_app(app)
            app_check = check_app_open(app)
            if app_check == True:
                speak("Application is opened successfully")
            else:
                speak("I cannot find the application")
        elif "close" in query and ("app" in query or "application" in query or "apps" in query or "applications" in query):
            word = work.index("close")
            if work[word+1] == "app" or work[word+1] == "application" or work[word+1] == "apps" or work[word+1] == "applications":
                app = work[word+2]
            else:
                app = work[word+1]
            close_application(app)
        elif "close" in query and "it" in query:
            py.hotkey("alt", "f4")
        elif "copy" in query and "it" in query:
            py.hotkey("ctrl", "c")
        elif "paste" in query and "it" in query:
            py.hotkey("ctrl", "v")
        elif "delete" in query and "it" in query:
            py.press("delete")
        elif "cut" in query and "it" in query:
            py.hotkey("ctrl", "x")
        elif "send" in query and ("message" in query or "msg" in query):
            msg_send()
        elif "weather" in query and "of" in query:
            city = find_word(query, "of")
            if city is not None:
                get_otherweather(city)
            else:
                speak("Which City weather do you want to see")
                city = command().lower()
                if "of" in city:
                    city = city.replace("of", "")
                    get_otherweather(city)
                else:
                    get_otherweather(city)
        elif "weather" in query:
            get_myweather()
        elif "how are you" in query:
            speak("i am fine, what about you?")
            text = command().lower()
            if "fine" in text or "good" in text:
                speak("That's good")
            else:
                speak("That's not good please take care yourself")
        elif "what" in query or "how" in query:
            answer = chatgpt_ai(query)
            while True:
                if answer == True:
                    break
                else:
                    speak("i cannot understand it please say again")
                    input_query = command().lower()
                    answer = chatgpt_ai(input_query)
        elif "time" in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")
            print("The current time is:", current_time)
            speak(f"Time is {current_time}")
        elif "date" in query:
            current_date = datetime.date.today()
            print("Today date is:", current_date)
            speak(f"Today date is {current_date}")
        elif "change my name to" in query:
            query=query.replace("change my name to","")
            assname=query
        elif "change name" in query or "change my name" in query:
            speak("What would you like to call me ,Boss ")
            assname = command()
            speak("Thanks for naming me")
        elif "what's your name" in query or "what is your name" in query or "tell your name" in query or "tell me your name" in query:
            speak("My Name is")
            speak(assname)
            print("My Name is ",assname)
        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()
        else:
            if "open" in query:
                speak("Please specify the what do you want to open")
            elif "close" in query:
                speak("Please specify the what do you want to close")
            elif "search" in query:
                speak("Please specify the what do you want to search")
            else:
                write_error(query)
                speak("i cannot understand it")









