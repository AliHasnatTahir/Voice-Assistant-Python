from recognize import speak


def history(query):
    if "try again" in query or "try" in query:
                # Read the second last line from the text file
        with open("history.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                second_last_value = lines[-1].strip()
                query = second_last_value
                return query
            else:
                speak("No last command found.")
                
    else:
        with open("history.txt", "a") as file:
                file.write(query + "\n")


def display_history():
    with open("history.txt", "r") as file:
        content = file.read()
        if len(content) == 0:
            speak("Nothing in history")
        else:
            print(content)