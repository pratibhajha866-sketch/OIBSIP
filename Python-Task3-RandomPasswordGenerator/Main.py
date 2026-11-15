import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("450x600")
        
        # History storage (in-memory only, no persistence)[cite: 5]
        self.history = []

        # GUI Elements[cite: 5]
        tk.Label(root, text="Password Length (Min 8):").pack(pady=5)
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = tk.Spinbox(root, from_=8, to=128, textvariable=self.length_var, width=5)
        self.length_spinbox.pack()

        self.var_upper = tk.BooleanVar(value=True)
        self.var_lower = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_symbols = tk.BooleanVar(value=True)
        self.var_exclude = tk.BooleanVar(value=False)

        tk.Checkbutton(root, text="Include Uppercase", variable=self.var_upper).pack(anchor='w', padx=50)
        tk.Checkbutton(root, text="Include Lowercase", variable=self.var_lower).pack(anchor='w', padx=50)
        tk.Checkbutton(root, text="Include Numbers", variable=self.var_digits).pack(anchor='w', padx=50)
        tk.Checkbutton(root, text="Include Symbols", variable=self.var_symbols).pack(anchor='w', padx=50)
        tk.Checkbutton(root, text="Exclude Ambiguous (e.g., O, 0, l, 1)", variable=self.var_exclude).pack(anchor='w', padx=50, pady=10) # Option to exclude ambiguous characters[cite: 5]

        self.btn_generate = tk.Button(root, text="Generate & Copy", command=self.generate_password)
        self.btn_generate.pack(pady=10)

        self.lbl_password = tk.Label(root, text="--", font=("Courier", 14, "bold"), wraplength=400)
        self.lbl_password.pack(pady=10)

        self.lbl_strength = tk.Label(root, text="Strength: --", font=("Helvetica", 10))
        self.lbl_strength.pack(pady=5)

        tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5) # Copy button using pyperclip[cite: 5]

        tk.Label(root, text="Recent History (Session Only):", font=("Helvetica", 10, "underline")).pack(pady=10)
        self.lbl_history = tk.Label(root, text="", font=("Courier", 10))
        self.lbl_history.pack()

    def generate_password(self):
        length = self.length_var.get()
        
        # Enforce minimum 8 characters[cite: 5]
        if length < 8:
            messagebox.showerror("Error", "Password length must be at least 8 characters.")
            return

        pools = []
        ambiguous = "Il1O0"

        if self.var_upper.get():
            upper_pool = string.ascii_uppercase
            if self.var_exclude.get():
                upper_pool = ''.join([c for c in upper_pool if c not in ambiguous])
            pools.append(upper_pool)
            
        if self.var_lower.get():
            lower_pool = string.ascii_lowercase
            if self.var_exclude.get():
                lower_pool = ''.join([c for c in lower_pool if c not in ambiguous])
            pools.append(lower_pool)
            
        if self.var_digits.get():
            digit_pool = string.digits
            if self.var_exclude.get():
                digit_pool = ''.join([c for c in digit_pool if c not in ambiguous])
            pools.append(digit_pool)
            
        if self.var_symbols.get():
            pools.append(string.punctuation)

        # Enforce at least 2 types selected[cite: 5]
        if len(pools) < 2:
            messagebox.showerror("Error", "Please select at least 2 character types.")
            return

        password_chars = []
        all_chars = ""

        # Enforce security rule: at least one character from each selected type[cite: 5]
        for pool in pools:
            password_chars.append(secrets.choice(pool)) # Use secrets module for cryptographically secure generation[cite: 5]
            all_chars += pool

        # Fill the rest of the password length
        while len(password_chars) < length:
            password_chars.append(secrets.choice(all_chars))

        # Shuffle to ensure the guaranteed characters aren't always at the beginning
        secrets.SystemRandom().shuffle(password_chars)
        password = ''.join(password_chars)

        self.lbl_password.config(text=password)
        self.evaluate_strength(length, len(pools))
        
        # Password copies automatically on generation[cite: 5]
        pyperclip.copy(password) 
        
        self.update_history(password)

    def evaluate_strength(self, length, types_count):
        # Display a visual label showing strength[cite: 5]
        if length >= 14 and types_count == 4:
            self.lbl_strength.config(text="Strength: Strong", fg="green")
        elif length >= 10 and types_count >= 3:
            self.lbl_strength.config(text="Strength: Medium", fg="orange")
        else:
            self.lbl_strength.config(text="Strength: Weak", fg="red")

    def copy_to_clipboard(self):
        password = self.lbl_password.cget("text")
        if password != "--":
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")

    def update_history(self, password):
        # Display the last 5 generated passwords in the session[cite: 5]
        self.history.insert(0, password)
        if len(self.history) > 5:
            self.history.pop()
            
        history_text = "\n".join(self.history)
        self.lbl_history.config(text=history_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()