Objective: A Python-based voice assistant that listens to spoken commands, parses user intent, and automates useful actions.

This project goes beyond simple keyword matching by implementing basic Natural Language Understanding (NLU) to deduce intent from free-form spoken sentences. It integrates with third-party APIs and system libraries to perform real-world tasks.

Tech Stack:

Python

speech_recognition (Microphone input capture)

pyttsx3 (Text-to-speech feedback)

smtplib (Email automation)

requests (REST API calls)

Optional: MySQL (For storing custom commands)

Key Features:

Intent Recognition: Parses natural language to determine if the user wants to search the web, check the weather, send an email, or set a reminder.

Live Weather Updates: Fetches and reads out current weather conditions for user-specified cities using the OpenWeatherMap API.

Voice-Activated Email: Collects email subjects and messages via dictation and securely sends them using an SMTP server.

Asynchronous Reminders: Uses multi-threading to set timed reminders that trigger audible alerts without blocking the main application loop.

Graceful Error Handling: Automatically prompts the user to repeat themselves if ambient noise prevents clear speech recognition.
