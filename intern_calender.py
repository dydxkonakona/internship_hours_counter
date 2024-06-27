import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

def validate_inputs(working_hours, total_hours, start_date, end_date):
    try:
        working_hours = int(working_hours)
        total_hours = int(total_hours)
        if working_hours <= 0 or total_hours <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Working hours and total required hours must be positive integers.")
        return False

    if start_date > end_date:
        messagebox.showerror("Invalid Input", "Start date must be before or equal to end date.")
        return False

    return True

def calculate_hours(working_hours, total_hours, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    total_workdays = 0
    total_workhours = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday are 0 to 4
            total_workdays += 1
            total_workhours += working_hours
        current_date += timedelta(days=1)

    can_complete_internship = total_workhours >= total_hours

    return total_workdays, total_workhours, can_complete_internship

def on_submit():
    working_hours = working_hours_entry.get()
    total_hours = total_hours_entry.get()
    start_date = start_date_entry.get_date().strftime("%Y-%m-%d")
    end_date = end_date_entry.get_date().strftime("%Y-%m-%d")

    if validate_inputs(working_hours, total_hours, start_date, end_date):
        working_hours = int(working_hours)
        total_hours = int(total_hours)
        total_workdays, total_workhours, can_complete_internship = calculate_hours(working_hours, total_hours, start_date, end_date)
        display_calendar(total_workdays, total_workhours, total_hours, can_complete_internship)

def display_calendar(total_workdays, total_workhours, total_required_hours, can_complete_internship):
    calendar_window = tk.Toplevel()
    calendar_window.title("Internship Hours Calendar")

    ttk.Label(calendar_window, text="Total Workdays:").grid(column=0, row=0, padx=10, pady=5)
    ttk.Label(calendar_window, text=total_workdays).grid(column=1, row=0, padx=10, pady=5)

    ttk.Label(calendar_window, text="Total Work Hours:").grid(column=0, row=1, padx=10, pady=5)
    ttk.Label(calendar_window, text=total_workhours).grid(column=1, row=1, padx=10, pady=5)

    ttk.Label(calendar_window, text="Total Required Hours:").grid(column=0, row=2, padx=10, pady=5)
    ttk.Label(calendar_window, text=total_required_hours).grid(column=1, row=2, padx=10, pady=5)

    if can_complete_internship:
        ttk.Label(calendar_window, text="You can complete your internship within the given duration.").grid(column=0, row=3, columnspan=2, pady=10)
    else:
        ttk.Label(calendar_window, text="You cannot complete your internship within the given duration.").grid(column=0, row=3, columnspan=2, pady=10)

def create_gui():
    global working_hours_entry, total_hours_entry, start_date_entry, end_date_entry

    root = tk.Tk()
    root.title("Internship Hours Calendar")

    ttk.Label(root, text="Working Hours per Day:").grid(column=0, row=0, padx=10, pady=5)
    working_hours_entry = ttk.Entry(root)
    working_hours_entry.grid(column=1, row=0, padx=10, pady=5)

    ttk.Label(root, text="Total Required Hours:").grid(column=0, row=1, padx=10, pady=5)
    total_hours_entry = ttk.Entry(root)
    total_hours_entry.grid(column=1, row=1, padx=10, pady=5)

    ttk.Label(root, text="Start Date:").grid(column=0, row=2, padx=10, pady=5)
    start_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd")
    start_date_entry.grid(column=1, row=2, padx=10, pady=5)

    ttk.Label(root, text="End Date:").grid(column=0, row=3, padx=10, pady=5)
    end_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd")
    end_date_entry.grid(column=1, row=3, padx=10, pady=5)

    submit_button = ttk.Button(root, text="Generate Calendar", command=on_submit)
    submit_button.grid(column=0, row=4, columnspan=2, pady=10)

    root.mainloop()

create_gui()
