Objective: A fully-featured Desktop GUI application that calculates Body Mass Index (BMI), categorizes the health metric, and tracks historical user data over time.

This tool is designed with multi-user support in mind, allowing different users to save their records to a local database and visualize their health journey through dynamically generated line charts.

Tech Stack:

Python

tkinter (Graphical User Interface)

sqlite3 (Local database persistence)

matplotlib (Data visualization)

Key Features:

Interactive GUI: Built with Tkinter, featuring dedicated input fields, health categories, and color-coded text feedback (e.g., Green for Normal, Red for Obese).

Data Persistence: Automatically logs the username, weight, height, BMI, and category to a local SQLite database for historical tracking.

Trend Analysis: Queries historical user data to plot and display a Matplotlib line chart of a user's BMI trend over time.

Input Validation: Prevents application crashes by rejecting non-numeric inputs and negative values with helpful error dialogues.
