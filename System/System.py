import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import datetime
import mysql.connector
import sys
import subprocess

class AppointmentScheduler:
    def __init__(self, master, user_info):
        self.master = master
        self.user_info = user_info
        self.master.title("Appointment Scheduler")
        self.master.resizable(False, False)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (746 / 2))
        y_coordinate = int((screen_height / 2) - (550 / 2))

        self.master.geometry(f"746x550+{x_coordinate}+{y_coordinate}")

        self.appointments = {}

        self.calendar_frame = tk.Frame(master)
        self.calendar_frame.pack(pady=20, expand=True, fill=tk.BOTH)

        self.style = ttk.Style()
        self.style.layout('TFrame', [('Calendar.Treeview', {'sticky': 'nswe'})])
        self.style.configure('TFrame', background='white')
        self.calendar = Calendar(self.calendar_frame, selectmode="day", date_pattern="yyyy-mm-dd",
                                 foreground="black", selectforeground="white", selectbackground="blue",
                                 background="light gray", headersbackground="gray", bordercolor="black",
                                 normalforeground="black", normalbackground="white", othermonthforeground="gray",
                                 othermonthbackground="white", weekendforeground="red", showweeknumbers=False)
        self.calendar.pack(expand=True, fill=tk.BOTH, padx=50, pady=10)

        self.time_label = tk.Label(master, text="Select Time:")
        self.time_label.pack()

        self.time_combobox = ttk.Combobox(master, values=[
            "8:00 AM - 10:00 AM",
            "1:00 PM - 3:00 PM",
            "3:00 PM - 5:00 PM",
            "5:00 PM - 7:00 PM"
        ], state="readonly")
        self.time_combobox.pack()

        self.schedule_button = tk.Button(master, text="Schedule Appointment", command=self.check_appointments)
        self.schedule_button.pack(pady=10)

        self.fetch_data()
        self.calendar.bind("<<CalendarSelected>>", self.check_for_sunday)

        self.user_info_label = tk.Label(master, text=f"Logged in as: {user_info[0]} {user_info[1]}", anchor="e")
        self.user_info_label.place(relx=1, rely=1, x=-10, y=-10, anchor="se")

        self.logout_button = tk.Button(master, text="Logout", command=self.logout)
        self.logout_button.place(relx=1, rely=1, x=-10, y=-40, anchor="se")

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Enter your MySQL password
                database="registration"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT a.appointment_date, a.appointment_time, u.email FROM appointments a JOIN users u ON a.name = CONCAT(u.name, ' ', u.surname)")
            self.appointments = {}
            for date, time, email in cursor.fetchall():
                if date not in self.appointments:
                    self.appointments[date] = {}
                if time not in self.appointments[date]:
                    self.appointments[date][time] = set()
                self.appointments[date][time].add(email)
            conn.close()
        except mysql.connector.Error as err:
            print("Error:", err)

    def check_appointments(self):
        date = self.calendar.get_date()
        time = self.time_combobox.get()

        if not time:
            messagebox.showinfo("Invalid Time", "Please select a time.")
            return

        selected_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if selected_date < datetime.date.today():
            messagebox.showinfo("Invalid Date", "You cannot schedule appointments on past dates.")
            return

        if self.is_time_slot_taken(date, time):
            messagebox.showinfo("Time Already Booked", f"The selected time slot ({time}) is already booked for {date}. Please choose another time.")
        else:
            confirm_scheduling = messagebox.askyesno("Final Confirmation", f"Confirm scheduling appointment for {date} at {time}?")
            if confirm_scheduling:
                self.schedule_appointment(date, time, self.user_info[0], self.user_info[2])  # Passing user's name and email

    def is_time_slot_taken(self, date, time):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Enter your MySQL password
                database="registration"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = %s AND appointment_time = %s", (date, time))
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except mysql.connector.Error as err:
            print("Error:", err)
            return False

    def schedule_appointment(self, date, time, name, email):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Enter your MySQL password
                database="registration"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO appointments (appointment_date, appointment_time, name, email) VALUES (%s, %s, %s, %s)", (date, time, name, email))
            conn.commit()
            conn.close()
            if date not in self.appointments:
                self.appointments[date] = {}
            if time not in self.appointments[date]:
                self.appointments[date][time] = set()
            self.appointments[date][time].add(email)
            messagebox.showinfo("Success", f"Appointment scheduled for {date} at {time}.")
        except mysql.connector.Error as err:
            print("Error:", err)

    def check_for_sunday(self, event=None):
        selected_date = self.calendar.get_date()
        selected_datetime = datetime.datetime.strptime(selected_date, "%Y-%m-%d")

        if selected_datetime.weekday() == 6:
            messagebox.showinfo("Rest Day", "You have selected a Sunday. Today is a rest day.")
            self.time_combobox.set('')
            self.time_combobox.config(state='disabled')
        else:
            self.time_combobox.config(state='readonly')

    def logout(self):
        self.master.destroy()
        subprocess.Popen(['python', 'D:\\IPTCSYSTEM\\login\\build\\gui.py'])

def main():
    root = tk.Tk()
    if len(sys.argv) == 4:
        user_info = (sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        user_info = ("Unknown", "User", "unknown@example.com")
    app = AppointmentScheduler(root, user_info)
    root.mainloop()

if __name__ == "__main__":
    main()
