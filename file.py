import os
import re
from recognize import speak, command
from words import find_word
import shutil


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
        os.startfile(file_path)
    else:
        speak(f"{filename} not found.")


