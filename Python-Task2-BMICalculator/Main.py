import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database setup using sqlite3 as specified in the tech stack
def setup_db():
    try:
        conn = sqlite3.connect('bmi_records.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {e}") # Error handling for DB failures[cite: 3]

def calculate_bmi():
    user = entry_user.get().strip()
    weight_str = entry_weight.get().strip()
    height_str = entry_height.get().strip()

    if not user:
        messagebox.showerror("Input Error", "Please enter a username.")
        return

    try:
        # Input validation: reject non-numeric and negative values[cite: 3]
        weight = float(weight_str)
        height = float(height_str)
        if weight <= 0 or height <= 0:
            raise ValueError("Values must be positive.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid positive numbers for weight and height.")
        return

    # Calculate BMI: BMI = weight / (height^2)[cite: 3]
    bmi = weight / (height ** 2)
    bmi = round(bmi, 2) # Display BMI rounded to 2 decimal places[cite: 3]

    # Classify result into standard categories[cite: 3]
    if bmi < 18.5:
        category = "Underweight"
        color = "blue"
    elif 18.5 <= bmi <= 24.9:
        category = "Normal"
        color = "green"
    elif 25.0 <= bmi <= 29.9:
        category = "Overweight"
        color = "orange"
    else:
        category = "Obese"
        color = "red"

    # Display colour-coded feedback[cite: 3]
    lbl_result.config(text=f"BMI: {bmi} ({category})", fg=color)

    # Save to database
    try:
        conn = sqlite3.connect('bmi_records.db')
        c = conn.cursor()
        c.execute("INSERT INTO records (username, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
                  (user, weight, height, bmi, category))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to save record: {e}")

def show_graph():
    user = entry_user.get().strip()
    if not user:
        messagebox.showerror("Input Error", "Please enter a username to view history.")
        return

    try:
        conn = sqlite3.connect('bmi_records.db')
        c = conn.cursor()
        c.execute("SELECT bmi FROM records WHERE username=?", (user,))
        records = c.fetchall()
        conn.close()
        
        if not records:
            messagebox.showinfo("No Data", "No historical records found for this user.")
            return

        bmis = [row[0] for row in records]
        
        # Display a line chart of a user's BMI trend over time using matplotlib[cite: 3]
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(range(1, len(bmis) + 1), bmis, marker='o', linestyle='-')
        ax.set_title(f"BMI Trend for {user}")
        ax.set_xlabel("Entry Number")
        ax.set_ylabel("BMI")
        
        graph_window = tk.Toplevel(root)
        graph_window.title("BMI Trend")
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to retrieve records: {e}")

setup_db()

# GUI window built with tkinter[cite: 3]
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("350x350")

tk.Label(root, text="Username:").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack()

# Input fields with labels for weight and height[cite: 3]
tk.Label(root, text="Weight (kg):").pack(pady=5)
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Height (m):").pack(pady=5)
entry_height = tk.Entry(root)
entry_height.pack()

# "Calculate" button[cite: 3]
tk.Button(root, text="Calculate", command=calculate_bmi).pack(pady=10)

lbl_result = tk.Label(root, text="BMI: --", font=("Helvetica", 12, "bold"))
lbl_result.pack(pady=10)

tk.Button(root, text="Show Trend Graph", command=show_graph).pack(pady=10)

root.mainloop()