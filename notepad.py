from recognize import speak, command
import os


def notepad():
    while True:
        speak("Do you want to write to an existing file or create a new file?")
        response = command().lower()
        if 'existing' in response:
            # Ask for file name
            while True:
                speak("What is the name of the file you want to write to?")
                file_name = command().lower()
                # Check if file already exists
                if os.path.isfile(file_name):
                    # Ask user if they want to append to existing file or overwrite it
                    while True:
                        speak("Do you want to overwrite or append to the file?")
                        write_mode = command().lower()
                        if 'overwrite' in write_mode:
                            with open(file_name, 'w') as file:
                                speak("Say what you want to write:")
                                while True:
                                    text = command().lower()
                                    if 'write' in text:
                                        file.write(text + '\n')
                                    elif 'stop' in text:
                                        return None
                        elif 'append' in write_mode:
                            with open(file_name, 'a') as file:
                                speak("Say what you want to write:")
                                while True:
                                    text = command().lower()
                                    if 'write' in text:
                                        file.write(text + '\n')
                                    elif 'stop' in text:
                                        return None
                        else:
                            speak("Sorry, I didn't understand. Please say 'overwrite' or 'append'.")
                else:
                    speak("Sorry, that file doesn't exist. Please try again.")
        elif 'new' in response:
            # Ask for file name
            speak("What do you want to name the new file?")
            file_name = command().lower()
            with open(file_name, 'w') as file:
                speak("Say what you want to write:")
                while True:
                    text= command().lower()
                    if 'write' in text:
                        file.write(text + '\n')
                    elif 'stop' in text:
                        return None