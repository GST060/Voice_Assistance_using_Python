import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import time
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "bc0804194af44a28a3e42ec4061a0810"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()
    
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    # Initialize Pygame mixer
    pygame.mixer.init()
    
    #Load the MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace 'your_file.mp3' with the path to your MP3 file
    
    # Play the MP3 file
    pygame.mixer.music.play()
    
    # Keep the script running until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.music.unload()    
    os.remove("temp.mp3")

    
def aiProcess(command):
    client = OpenAI(api_key="sk-proj-WxSl7ehGk2PnwzCHcDwT3BlbkYFJFMj6bYTk9G1bqZaFTcj",
                    )
    
    completion = client.chat.completions.create(
        # model="gpt-4o-mini",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant name jarvis skilled in general tasks like Alex and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
            ]
        )
    return completion.choices[0].message.content
 
def processCommand(c):  
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the article
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
                
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)
        
 
if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    
    while True:
        # Listen for the wake word "Jarvis"
        # # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening.....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Bolo")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processCommand(command)
                
                
        except Exception as e:
            print("Error; {0}".format(e))
