import tkinter as tk
from tkinter import ttk
import random
import string

COMMON_PASSWORDS = {"123456", "password", "123456789", "qwerty", "12345", "12345678", "abc123", "password1", "1234567"}
THEMES = {
    "Cyberpunk": {"bg": "#1a1a2e", "entry_bg": "#0f3460", "entry_fg": "white", "meter_style": "Cyberpunk.Horizontal.TProgressbar"},
    "Dark Mode": {"bg": "#121212", "entry_bg": "#242424", "entry_fg": "white", "meter_style": "Dark.Horizontal.TProgressbar"},
    "Pastel": {"bg": "#f0e6ff", "entry_bg": "#d4c2fc", "entry_fg": "black", "meter_style": "Pastel.Horizontal.TProgressbar"}
}

LIGHT_FEEDBACK_BG = "#f9f9f9"

def check_password_strength(*args):
    password = password_var.get()
    strength = 0
    conditions = {
        "✔️ At least 8 characters": len(password) >= 8,
        "✔️ Contains numbers": any(char.isdigit() for char in password),
        "✔️ Contains special characters": any(char in string.punctuation for char in password)
    }
    
    strength = sum(conditions.values())
    
    meter_bar.config(value=strength * 33, 
                     style=['Weak.Horizontal.TProgressbar', 'Medium.Horizontal.TProgressbar', 'Medium.Horizontal.TProgressbar', 'Strong.Horizontal.TProgressbar'][strength])
    feedback_label.config(text=["😡 Weak", "😬 Medium", "😬 Medium", "💪 Strong"][strength], 
                          fg=["red", "orange", "orange", "green"][strength])
    
    feedback_listbox.delete(0, tk.END)
    for condition, met in conditions.items():
        feedback_listbox.insert(tk.END, condition if met else "❌ " + condition[2:])

def suggest_password():
    digits = random.randint(10, 16)
    password = ""
    for i in range(1, digits):
        password += str(chr(random.randint(33,126)))
    password_var.set(password)


def toggle_theme():
    global current_theme
    themes = list(THEMES.keys())
    current_index = themes.index(current_theme)
    next_theme = themes[(current_index + 1) % len(themes)]
    theme_settings = THEMES[next_theme]
    
    root.config(bg=theme_settings["bg"])
    frame.config(bg=theme_settings["bg"])
    password_entry.config(bg=theme_settings["entry_bg"], fg=theme_settings["entry_fg"])
    meter_bar.config(style=theme_settings["meter_style"])
    toggle_button.config(text=f"Switch to {themes[(current_index + 2) % len(themes)]}")
    theme_label.config(text=f"Current Theme: {next_theme}")
    feedback_listbox.config(bg=LIGHT_FEEDBACK_BG)
    current_theme = next_theme

def toggle_password_visibility():
    if password_entry.cget('show') == '•':
        password_entry.config(show='')
        toggle_visibility_button.config(text='Hide Password')
    else:
        password_entry.config(show='•')
        toggle_visibility_button.config(text='Show Password')

root = tk.Tk()
root.title('Password Strength Checker')
root.geometry('500x600')
current_theme = 'Cyberpunk'

frame = tk.Frame(root, bg=THEMES[current_theme]["bg"])
frame.pack(expand=True, fill='both', padx=20, pady=20)

theme_label = tk.Label(frame, text=f"Current Theme: {current_theme}", font=('Arial', 12), bg=THEMES[current_theme]["bg"], fg='white')
theme_label.pack()

password_var = tk.StringVar()
password_var.trace_add('write', check_password_strength)

password_entry = tk.Entry(frame, textvariable=password_var, font=('Arial', 16), bg=THEMES[current_theme]["entry_bg"], fg=THEMES[current_theme]["entry_fg"], insertbackground='white', show='•', width=25)
password_entry.pack(pady=15, padx=20, ipadx=5, ipady=8, fill='x')

toggle_visibility_button = tk.Button(frame, text='Show Password', command=toggle_password_visibility, font=('Arial', 12), bg='#ffffff', fg='black', relief='flat', padx=12, pady=8, width=20)
toggle_visibility_button.pack(pady=5)

meter_bar = ttk.Progressbar(frame, length=250, mode='determinate')
meter_bar.pack(pady=10)

feedback_label = tk.Label(frame, text='😡 Weak', font=('Arial', 16, 'bold'), fg='red', bg=THEMES[current_theme]["bg"], padx=12, pady=8)
feedback_label.pack()

feedback_listbox = tk.Listbox(frame, height=5, font=('Arial', 12), bg=LIGHT_FEEDBACK_BG, fg='black', bd=2, relief='solid', highlightthickness=0, selectbackground='#cccccc')
feedback_listbox.pack(pady=5, padx=10, fill='x')

suggest_button = tk.Button(frame, text='Suggest Password', command=suggest_password, font=('Arial', 14), bg='#ffffff', fg='black', relief='flat', padx=12, pady=8, width=20)
suggest_button.pack(pady=10)

toggle_button = tk.Button(frame, text='Switch to Dark Mode', command=toggle_theme, font=('Arial', 14), bg='#ffffff', fg='black', relief='flat', padx=12, pady=8, width=20)
toggle_button.pack(pady=10)

style = ttk.Style()
style.theme_use('clam')
style.configure('Cyberpunk.Horizontal.TProgressbar', background='yellow', troughcolor='black', thickness=20)
style.configure('Medium.Horizontal.TProgressbar', background='orange', troughcolor='black', thickness=20)
style.configure('Weak.Horizontal.TProgressbar', background='red', troughcolor='black', thickness=20)
style.configure('Strong.Horizontal.TProgressbar', background='green', troughcolor='black', thickness=20)
style.configure('Pastel.Horizontal.TProgressbar', background='#8ecae6', troughcolor='#f0e6ff', thickness=20)
style.configure('Dark.Horizontal.TProgressbar', background='#4CAF50', troughcolor='#121212', thickness=20)

root.config(bg=THEMES[current_theme]["bg"])
frame.config(bg=THEMES[current_theme]["bg"])

root.mainloop()


