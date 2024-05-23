from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\IPTCSYSTEM\Mysystem\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to check for conflicting appointments
def is_conflicting(new_start, new_end):
    for appointment in appointments:
        existing_start = appointment["start"]
        existing_end = appointment["end"]
        if (new_start < existing_end and new_end > existing_start):
            return True
    return False

# Function to handle registration button click
def register_appointment():
    name = name_entry.get()
    surname = surname_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    date = datetime.strptime(date_entry.get(), "%Y-%m-%d")
    start_time = datetime.strptime(start_time_entry.get(), "%H:%M")
    end_time = datetime.strptime(end_time_entry.get(), "%H:%M")

    new_start = datetime.combine(date, start_time.time())
    new_end = datetime.combine(date, end_time.time())

    if is_conflicting(new_start, new_end):
        messagebox.showerror("Error", "This time slot is already booked. Please choose another time.")
    else:
        appointments.append({
            "name": name,
            "surname": surname,
            "contact": contact,
            "email": email,
            "password": password,
            "start": new_start,
            "end": new_end
        })
        messagebox.showinfo("Success", "Appointment registered successfully!")

# Initialize appointments list
appointments = []

window = Tk()
window.geometry("303x536")
window.configure(bg = "#808080")

canvas = Canvas(
    window,
    bg = "#808080",
    height = 536,
    width = 303,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    73.0,
    15.0,
    anchor="nw",
    text="Registration",
    fill="#FFFFFF",
    font=("Inter Bold", 20 * -1)
)

# Name entry
canvas.create_rectangle(71.999, 80.999, 237.132, 123.176, fill="#D9D9D9", outline="")
canvas.create_text(93.0, 88.0, anchor="nw", text="Name", fill="#000000", font=("Inter Bold", 20 * -1))
name_entry = Entry(window)
canvas.create_window(155, 102, window=name_entry)

# Surname entry
canvas.create_rectangle(75.0, 140.0, 240.132, 182.176, fill="#D9D9D9", outline="")
canvas.create_text(94.0, 147.0, anchor="nw", text="Surname", fill="#000000", font=("Inter Bold", 20 * -1))
surname_entry = Entry(window)
canvas.create_window(155, 162, window=surname_entry)

# Contact entry
canvas.create_rectangle(75.0, 206.0, 240.132, 248.176, fill="#D9D9D9", outline="")
canvas.create_text(94.0, 216.0, anchor="nw", text="Contact", fill="#000000", font=("Inter Bold", 20 * -1))
contact_entry = Entry(window)
canvas.create_window(155, 222, window=contact_entry)

# Email entry
canvas.create_rectangle(75.0, 267.0, 240.132, 309.176, fill="#D9D9D9", outline="")
canvas.create_text(91.0, 278.0, anchor="nw", text="Email", fill="#000000", font=("Inter Bold", 20 * -1))
email_entry = Entry(window)
canvas.create_window(155, 282, window=email_entry)

# Password entry
canvas.create_rectangle(75.028, 328.116, 240.104, 370.060, fill="#D9D9D9", outline="")
canvas.create_text(94.0, 335.0, anchor="nw", text="Password", fill="#000000", font=("Inter Bold", 20 * -1))
password_entry = Entry(window, show="*")
canvas.create_window(155, 342, window=password_entry)

# Date entry
canvas.create_text(93.0, 360.0, anchor="nw", text="Date (YYYY-MM-DD)", fill="#000000", font=("Inter Bold", 12 * -1))
date_entry = Entry(window)
canvas.create_window(155, 375, window=date_entry)

# Start time entry
canvas.create_text(93.0, 390.0, anchor="nw", text="Start Time (HH:MM)", fill="#000000", font=("Inter Bold", 12 * -1))
start_time_entry = Entry(window)
canvas.create_window(155, 405, window=start_time_entry)

# End time entry
canvas.create_text(93.0, 420.0, anchor="nw", text="End Time (HH:MM)", fill="#000000", font=("Inter Bold", 12 * -1))
end_time_entry = Entry(window)
canvas.create_window(155, 435, window=end_time_entry)

# Register button
canvas.create_rectangle(111.0, 392.0, 198.0, 424.0, fill="#D9D9D9", outline="")
register_button = Button(window, text="Register", command=register_appointment)
canvas.create_window(155, 408, window=register_button)

canvas.create_text(77.0, 450.0, anchor="nw", text="Already have an account? Click here", fill="#FFFFFF", font=("Inter Bold", 11 * -1))

window.resizable(False, False)
window.mainloop()
