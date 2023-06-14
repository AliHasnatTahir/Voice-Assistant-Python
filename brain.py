from browser import *
from words import *
from weather import *
from calculation import *
from file import *
from system import *
from errors import *
from history import *
from notepad import notepad
from msg import msg_send
from recognize import *
from Sample_generator import sample_taken
from Model_Trainer import model_train
import webbrowser
import re
import screen_brightness_control as sbc
import pyautogui



def brain():
    # pyautogui.press('esc')
    wishMe()
    while True:
        speak("What can i do for you? Boss!")
        query = command().lower()
        check = history(query)
        if check is not None:
            query = check

        work = removal_words(query)
        if "open" in work:
            website_name = find_word(work, "open")
            search_and_open_link(website_name)
        elif "open" in work and ("file manager" in work or "file explorer" in work or "this pc" in work):
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
        elif "open" in work and ("device manage" in work or "device manager" in work or "device management" in work):
            # Open Device Manager
            os.system("devmgmt.msc")
        elif "open" in work and ("task manage" in work or "task management" in work or "task manager" in work):
            # Open Task Manager
            os.system("taskmgr")
        elif "open" in work and ("note" in work or "pad" in work or "notepad" in work):
            speak("Do you want to open system notepad or red sword notepad")
            ans = command().lower()
            if "system notepad" in ans or "system" in ans:
                os.startfile("notepad.exe")
            elif "redsword notepad" in ans or "red sword notepad" in ans or "red sword" in ans:
                notepad()
        elif ("increase" in work and ("brightness" in work or "bright" in work)) or ("decrease" in work and ("brightness" in work or "bright" in work)):
            brightness()
        elif ("show" in work or "what" in work) and ("brightness" in work or "brightness level" in work or "bright level" in work):
            print(sbc.get_brightness())
        elif "open" in work and "browser" in work:
            webbrowser.open("https://www.google.com")
        elif "search" in work and ("file" in work or "folder" in work or "image" in work or "movie" in work or "video" in work):
            name = find_word(work, "search")
            if name is not None:
                file = search_all(name)
                if file is not None:
                    speak("What do you want to do with it?")
                    answer = command().lower()
                    history(answer)
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
                else:
                    speak(f"{name} do not found")
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
                history(sound)
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
                history(sound)
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
                history(city)
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
        elif "time" in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")
            print("The current time is:", current_time)
            speak(f"Time is {current_time}")
        elif "date" in query:
            current_date = datetime.date.today()
            print("Today date is:", current_date)
            speak(f"Today date is {current_date}")
        elif "what's your name" in query or "what is your name" in query or "tell your name" in query or "tell me your name" in query:
            speak("My Name is Red Sword")
        elif "history" in query:
            display_history()
        elif "show error" in query or "show errors" in query or "show error file" in query or "show errors file" in query:
            show_error()
        elif "wikipedia" in query or "who" in query:
            wikipedia(work)
        elif "add" in work and "user" in work:
            sample_taken()
            model_train()
        elif "what" in query or "how" in query:
            answer = chatgpt_ai(query)
            while True:
                if answer == True:
                    break
                else:
                    speak("i cannot understand it please say again")
                    input_query = command().lower()
                    history(input_query)
                    answer = chatgpt_ai(input_query)
        elif "remember" in query:
            remember(query)
        elif "ok" in query:
            pass
        elif "exit" in query:
            speak("Thanks for giving me your time")
            exit()
        elif "nothing" in query or "sleep" in query:
            check = True
            while check:
                speak("Ok I will wait you can resume me by saying red sword or wakeup")
                permission = command()
                if "red sword" in permission or ("red" in permission and "sword" in permission) or "wakeup" in permission or "wake up" in permission:
                    check = False
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