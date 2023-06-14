This voice Assistant do many things like open all the things of the windows like control panel, Disk Manager etc.
open all apps installed in the windows and can check the installed apps.
this voice assistant open any website by saying open (website name) website.
like this you can also open the any apps saying like open (app name) app.
you can search any file any open it by saying open it and close it by saying close it.
this also can do the all the calculations.
it have its own notepad.
it also store the all the history.
if also can remember anything by saying RedSword Remember this.
This voice assistant can answer any question you said.
voice assistant also do the copy, paste, and delete files or folders.
voice assistant also can control the brightness, volume, mute, unmute.
also open the weather which is used by the api.
Also store the all the Errors in the excel file with time.
this voice assistant also use the face recognition and can add the new user by saying "Add new User".



Firstly you have to install these libraries

use the voice assistant by running the RedSword.py

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




After installing these libraries then you have to replace the api, account_sid, auth_token with your's

and then you can run it.
