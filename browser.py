from googlesearch import search
import speedtest
from recognize import speak
import pywikihow
import wikipedia
import subprocess
import openai
import webbrowser
import csv


openai.api_key = "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"


def get_url(query):
    for url in search(query, num_results=1):
        return url
    

def speed_test():
    speed = speedtest.Speedtest()
    download_speed = round(float(speed.download()) * 0.000000125, 2)
    upload_speed = round(float(speed.upload()) * 0.000000125, 2)

    print(f"the downloading speed is {download_speed} megabytes and uploading speed is {upload_speed} megabytes")
    speak(f"the downloading speed is {download_speed} megabytes and uploading speed is {upload_speed} megabytes")


def how_question(query):
    searched = pywikihow.search_wikihow(query, max_results=1)
    assert len(searched) == 1
    print(searched[0].summary)
    

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
    

def wikipedia(querylist):
    speak("Searching wikipedia")
    string = ' '.join(querylist)
    query = string.replace("wikipedia", "")
    results = wikipedia.summary(query, sentence=2)
    print(f"according to wikipedia {results}")
    speak(f"according to wikipedia {results}")



def search_and_open_link(search_input):
    csv_file = 'C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\website_link.csv'
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if search_input in row['Name']:
                link = row['Links']
                webbrowser.open(link)
                break
        else:
            speak("No matching link found from file.")