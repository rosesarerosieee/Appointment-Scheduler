import tkinter as tk
from tkinter import ttk
import mysql.connector
import subprocess

def fetch_appointments():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Adjust as per your settings
            database="registration"
        )
        cursor = conn.cursor()
        query = "SELECT id, name, email, appointment_date, appointment_time FROM appointments"
        cursor.execute(query)
        appointments = cursor.fetchall()
        conn.close()
        return appointments
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def open_login_page():
    subprocess.Popen(['python', 'D:\\IPTCSYSTEM\\login\\build\\gui.py'])  # Adjust path as needed

def create_admin_page():
    root = tk.Tk()
    root.title("Admin Page")
    root.geometry("800x600")

    # Admin Label
    admin_label = tk.Label(root, text="Logged in as Admin", font=("Arial", 12))
    admin_label.pack(side=tk.TOP, pady=10)

    # Frame for Logout Button
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Logout Button
    logout_button = tk.Button(button_frame, text="Logout", command=lambda: [root.destroy(), open_login_page()])
    logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Frame for the appointments
    appointments_frame = tk.Frame(root)
    appointments_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    # Create a canvas inside the frame
    canvas = tk.Canvas(appointments_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(appointments_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Another frame inside the canvas
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def delete_appointment(appointment_id, appointment_frame):
        # Delete appointment from the database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Adjust as per your settings
                database="registration"
            )
            cursor = conn.cursor()
            query = "DELETE FROM appointments WHERE id = %s"
            cursor.execute(query, (appointment_id,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        # Remove the frame from the UI
        appointment_frame.destroy()
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    appointments = fetch_appointments()  # Fetch appointments
    columns = 2
    for index, appointment in enumerate(appointments):
        row = index // columns
        col = index % columns
        appointment_id, name, email, appointment_date, appointment_time = appointment
        appointment_frame = tk.Frame(inner_frame, bd=2, relief=tk.SOLID, padx=10, pady=10)
        appointment_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        name_label = tk.Label(appointment_frame, text=f"Name: {name}", font=("Arial", 12))
        name_label.pack(anchor="w")
        email_label = tk.Label(appointment_frame, text=f"Email: {email}", font=("Arial", 12))
        email_label.pack(anchor="w")
        date_time_label = tk.Label(appointment_frame, text=f"Date and Time: {appointment_date} {appointment_time}", font=("Arial", 12))
        date_time_label.pack(anchor="w")

        # Adding the "Done" button
        done_button = tk.Button(appointment_frame, text="Done", command=lambda appt_id=appointment_id, appt_frame=appointment_frame: delete_appointment(appt_id, appt_frame))
        done_button.pack(anchor="e", pady=5)

    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()

if __name__ == "__main__":
    create_admin_page()  # Start directly with the admin window for testing
