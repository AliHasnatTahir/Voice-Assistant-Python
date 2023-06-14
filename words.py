import nltk
from nltk.corpus import stopwords
import datetime
from recognize import speak


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
    

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Boss!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Boss!")   

    else:
        speak("Good Evening Boss!")

    speak("I am your Assistant Red Sword")