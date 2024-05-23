import tkinter as tk
from tkinter import Canvas, Entry, Checkbutton, PhotoImage, IntVar, Button, Label, messagebox
from pathlib import Path
import mysql.connector
import subprocess

# General setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_entry_click(event, entry):
    if entry.cget("fg") == "#808080":
        entry.delete(0, "end")
        entry.config(fg="#000000")

def on_focus_out(event, entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)
        entry.config(fg="#808080")

def toggle_password_visibility():
    if show_password_var.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

def login():
    email = entry_email.get()
    password = entry_password.get()

    # Check for admin credentials
    if email == "ADMIN123" and password == "1234":
        # Launch the admin system application
        subprocess.Popen(['python', 'D:\\IPTCSYSTEM\\admin\\ADMIN.py'])
        # Close the login window
        window.destroy()
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Adjust as per your settings
            database="registration"
        )
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if result:
            # Launch the user system application and pass user information as command-line arguments
            subprocess.Popen(['python', 'D:\\IPTCSYSTEM\\System\\System.py', result[0], result[1], result[3]])  # Pass name, surname, and email
            # Close the login window
            window.destroy()
        else:
            messagebox.showerror("Login Status", "Invalid email or password. Please try again.")

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")

def open_registration():
    subprocess.Popen(['python', 'D:\\IPTCSYSTEM\\registration\\build\\gui.py'])
    window.destroy()  # Close the login window after opening registration

# Create the main window
window = tk.Tk()
window.geometry("746x470")  # Adjusted height to accommodate new label
window.configure(bg="#ADD8E6")

canvas = Canvas(window, bg="#ADD8E6", height=430, width=746, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

login_label = canvas.create_text(373.0, 30, anchor="n", text="Login", fill="#000000", font=("Inter", 30, "bold"))

# Email Entry
email_placeholder = "Enter your email"
entry_email = Entry(bd=0, bg="white", fg="#808080", highlightthickness=0)
entry_email.insert(0, email_placeholder)
entry_email.bind("<FocusIn>", lambda event, entry=entry_email: on_entry_click(event, entry))
entry_email.bind("<FocusOut>", lambda event, entry=entry_email, placeholder=email_placeholder: on_focus_out(event, entry, placeholder))
entry_email.place(x=400, y=115, width=296, height=44)

# Password Entry
password_placeholder = "Enter your password"
show_password_var = IntVar(value=0)
entry_password = Entry(bd=0, bg="white", fg="#808080", highlightthickness=0, show="*")
entry_password.insert(0, password_placeholder)
entry_password.bind("<FocusIn>", lambda event, entry=entry_password: on_entry_click(event, entry))
entry_password.bind("<FocusOut>", lambda event, entry=entry_password, placeholder=password_placeholder: on_focus_out(event, entry, placeholder))
entry_password.place(x=400, y=220, width=296, height=44)

# Checkbox for password visibility
show_password_checkbutton = Checkbutton(window, text="Show Password", variable=show_password_var, onvalue=1, offvalue=0, command=toggle_password_visibility, bg="#ADD8E6")
show_password_checkbutton.place(x=400, y=270)

# Login Button
login_button = Button(window, text="Login", bg="white", fg="#000000", font=("Inter", 14), command=login)
login_button.place(x=400, y=320, width=296, height=44)

# Registration Link Label
register_label = Label(window, text="Don't have an account? Click here", bg="#ADD8E6", fg="blue", cursor="hand2", font=("Inter", 10))
register_label.place(x=400, y=380)
register_label.bind("<Button-1>", lambda e: open_registration())

# Adding Image on the Left Side
image_path = r"D:\IPTCSYSTEM\login\build\images.png"
image = PhotoImage(file=image_path)
canvas.create_image(50, 195, anchor="w", image=image)  # Adjust x coordinate for positioning

window.resizable(False, False)
window.mainloop()
