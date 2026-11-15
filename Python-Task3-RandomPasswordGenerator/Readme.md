Objective: A cryptographically secure password generation tool with a user-friendly GUI, designed to create strong, highly customizable passwords.

Unlike basic random string generators, this tool utilizes Python's secrets module to ensure the generated passwords meet cryptographic security standards, making it suitable for generating actual account credentials.

Tech Stack:

Python

tkinter (Graphical User Interface)

secrets (Cryptographically strong random number generator)

pyperclip (Clipboard integration)

string (Character sets)

Key Features:

Strict Security Rules: Enforces a minimum length of 8 characters and guarantees that at least one character from every selected type (uppercase, lowercase, numbers, symbols) is included in the final output.

Ambiguous Character Exclusion: Offers a toggle to remove easily confused characters (like O, 0, l, 1) to improve password readability.

Strength Indicator: Dynamically evaluates and displays password strength (Weak, Medium, Strong) based on length and character diversity.

Frictionless UX: Automatically copies newly generated passwords to the system clipboard using pyperclip.

Secure Session History: Displays the last 5 generated passwords in the current session for convenience, intentionally avoiding file persistence to maintain strict security.
