import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
import requests
import threading
import time

# Initialize Text-to-Speech Engine[cite: 1]
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

def speak(text):
    """Text-to-speech feedback for all responses[cite: 1]."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input using speech_recognition[cite: 1]."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        # Graceful error handling[cite: 1]
        speak("I didn't quite catch that. Could you please repeat?")
        return "None"
    except sr.RequestError:
        speak("My speech recognition service is currently unavailable.")
        return "None"

def send_email(to_address, subject, message):
    """Send an email via voice command using smtplib."""
    try:
        # Dummy credentials - replace with your actual test account details
        sender_email = "your_dummy_email@gmail.com"
        sender_password = "your_app_password"
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_body = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_address, email_body)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("I was unable to send the email.")

def get_weather(city):
    """Fetch and read out live weather updates using OpenWeatherMap[cite: 2]."""
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url).json()
        if response["cod"] != "404":
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The current temperature in {city} is {temp} degrees Celsius with {desc}.")
        else:
            speak("I could not find weather details for that city.")
    except Exception as e:
        speak("I am having trouble fetching the weather right now.")

def set_reminder(duration_seconds, message):
    """Set a timed reminder that triggers an audible alert[cite: 2]."""
    time.sleep(duration_seconds)
    speak(f"Reminder alert: {message}")

def parse_intent(query):
    """Basic Natural Language Understanding to parse intent[cite: 1]."""
    if any(word in query for word in ["hello", "hi", "hey"]):
        return "greeting"
    elif any(word in query for word in ["time", "date"]):
        return "datetime"
    elif "search" in query:
        return "search"
    elif "weather" in query:
        return "weather"
    elif "email" in query:
        return "email"
    elif "remind" in query:
        return "reminder"
    else:
        return "unknown"

def main():
    speak("Voice assistant activated. How can I help you?")
    while True:
        query = listen()
        if query == "None":
            continue

        intent = parse_intent(query)

        if intent == "greeting":
            # Respond to "Hello" with a predefined greeting[cite: 1]
            speak("Hello there! I am ready to assist you.")
            
        elif intent == "datetime":
            # Tell the current time and date on request[cite: 1]
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")
            current_date = now.strftime("%B %d, %Y")
            speak(f"The current time is {current_time} on {current_date}.")
            
        elif intent == "search":
            # Perform a web search on a user-specified topic[cite: 1]
            speak("What would you like me to search for?")
            search_term = listen()
            if search_term != "None":
                url = f"https://www.google.com/search?q={search_term}"
                webbrowser.open(url)
                speak(f"Here are the search results for {search_term}.")
                
        elif intent == "weather":
            speak("Which city's weather would you like to know?")
            city = listen()
            if city != "None":
                get_weather(city)

        elif intent == "email":
            speak("Who should I send the email to? Please provide the email address manually for accuracy.")
            to_address = input("Enter recipient email: ") # Hard to parse email via voice reliably
            speak("What is the subject of the email?")
            subject = listen()
            speak("What is the message?")
            message = listen()
            if subject != "None" and message != "None":
                send_email(to_address, subject, message)
                
        elif intent == "reminder":
            speak("What should I remind you about?")
            message = listen()
            speak("In how many seconds should I remind you?")
            try:
                seconds_str = listen()
                # Extremely basic conversion for example purposes
                seconds = int(''.join(filter(str.isdigit, seconds_str)))
                threading.Thread(target=set_reminder, args=(seconds, message)).start()
                speak(f"Reminder set for {seconds} seconds from now.")
            except ValueError:
                speak("I did not understand the duration.")

        elif "exit" in query or "stop" in query:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()