import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia

# Function to take commands and recognize speech
def takeCommand():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print("Command:", query)
            
        except Exception as e:
            print(e)
            print("Say that again, please.")
            return "None"
        
        return query

def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def tellDay():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    
    if day in day_dict.keys():
        day_of_the_week = day_dict[day]
        print(day_of_the_week)
        speak("Today is " + day_of_the_week)

def tellTime():
    time = str(datetime.datetime.now())
    hour = time[11:13]
    minutes = time[14:16]
    speak("The time is " + hour + " hours and " + minutes + " minutes.")

def hello():
    speak("Hello! I am your Cozmo Virtual Assistant. How may I assist you?")

def takeQuery():
    hello()
    
    while True:
        query = takeCommand().lower()
        
        if "open google" in query:
            speak("Opening Google...")
            # Open Google website
            # (You can modify this as per your requirement)
            continue
        
        elif "which day is it" in query:
            tellDay()
            continue
        
        elif "tell me the time" in query:
            tellTime()
            continue
        
        elif "bye" in query:
            speak("Goodbye! Have a nice day!")
            exit()
        
        elif "from wikipedia" in query:
            speak("Searching on Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=4)
            speak("According to Wikipedia")
            speak(result)
        
        elif "tell me your name" in query:
            speak("I am your Cozmo Virtual Assistant.")
    
if __name__ == '__main__':
    takeQuery()
