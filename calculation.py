import re
from recognize import speak, command


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