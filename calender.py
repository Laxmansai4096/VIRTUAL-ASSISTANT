import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import time
import threading
import datetime
import os
import subprocess

# File to store events
events_file = "time.json"
diary_folder = "diary"

# Ensure diary folder exists
if not os.path.exists(diary_folder):
    os.makedirs(diary_folder)

def load_data():
    """Load saved events from time.json."""
    if os.path.exists(events_file):
        try:
            with open(events_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"tasks": {}, "important_dates": {}}
    return {"tasks": {}, "important_dates": {}}

def save_data():
    """Save the events to time.json."""
    try:
        with open(events_file, "w") as f:
            json.dump(events, f, indent=4)
        print("Data successfully saved.")
    except Exception as e:
        print(f"Error saving data: {e}")

def check_events():
    """Continuously check for due or missed events."""
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")

        for task, details in list(events["tasks"].items()):
            if details["time"] <= current_time and details["date"] <= current_date:
                show_popup(task, details, "task")

        for event, details in list(events["important_dates"].items()):
            if details["time"] <= "08:00" and details["date"] <= current_date:
                show_popup(event, details, "important_dates")

        time.sleep(60)

def show_popup(name, details, event_type):
    """Show popup reminder with Snooze and Remove buttons."""
    popup = tk.Toplevel()
    popup.title("Reminder")
    popup.geometry("350x200")

    tk.Label(popup, text=f"{name}: {details['message']}", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(popup, text="Snooze (5 min)", command=lambda: snooze_event(name, details, event_type, popup)).pack(pady=5)
    tk.Button(popup, text="Remove", command=lambda: dismiss_event(name, event_type, popup)).pack(pady=5)

def snooze_event(name, details, event_type, popup):
    """Snooze the event by 5 minutes."""
    new_time = (datetime.datetime.strptime(details["time"], "%H:%M") + datetime.timedelta(minutes=5)).strftime("%H:%M")
    events[event_type][name]["time"] = new_time
    save_data()
    popup.destroy()

def dismiss_event(name, event_type, popup):
    """Remove the event."""
    del events[event_type][name]
    save_data()
    update_event_list()
    popup.destroy()

def add_task():
    """Add a new task."""
    task_name = task_entry.get()
    task_time = task_time_entry.get()
    task_date = task_date_entry.get()
    task_message = task_message_entry.get()
    
    if task_name and task_time and task_date and task_message:
        events["tasks"][task_name] = {"time": task_time, "date": task_date, "message": task_message}
        save_data()
        update_event_list()
        clear_fields()

def update_task():
    """Update a selected task."""
    selected_index = task_list.curselection()
    if selected_index:
        task_name = sorted(events["tasks"].keys(), key=lambda x: events["tasks"][x]['date'], reverse=True)[selected_index[0]]
        new_time = simpledialog.askstring("Update Task", "Enter new time (HH:MM):", initialvalue=events["tasks"][task_name]["time"])
        new_date = simpledialog.askstring("Update Task", "Enter new date (YYYY-MM-DD):", initialvalue=events["tasks"][task_name]['date'])
        new_message = simpledialog.askstring("Update Task", "Enter new message:", initialvalue=events["tasks"][task_name]['message'])
        
        if new_time and new_date and new_message:
            events["tasks"][task_name] = {"time": new_time, "date": new_date, "message": new_message}
            save_data()
            update_event_list()
    else:
        messagebox.showerror("Error", "Please select a task to update!")

def add_important_date():
    """Add a new important date."""
    event_name = imp_date_entry.get()
    event_date = imp_date_date_entry.get()
    event_message = imp_date_message_entry.get()

    if event_name and event_date and event_message:
        events["important_dates"][event_name] = {"time": "08:00", "date": event_date, "message": event_message}
        save_data()
        update_event_list()
        clear_fields()

def update_event_list():
    """Update the task and important date lists."""
    task_list.delete(0, tk.END)
    sorted_tasks = sorted(events["tasks"].items(), key=lambda x: x[1]["date"], reverse=True)
    for index, (event, details) in enumerate(sorted_tasks):
        task_list.insert(tk.END, f"{index + 1}. {event} on {details['date']} at {details['time']}")

    important_date_list.delete(0, tk.END)
    sorted_dates = sorted(events["important_dates"].items(), key=lambda x: x[1]["date"], reverse=True)
    for index, (event, details) in enumerate(sorted_dates):
        important_date_list.insert(tk.END, f"{index + 1}. {event} on {details['date']} at {details['time']}")

def clear_fields():
    """Clear input fields."""
    task_entry.delete(0, tk.END)
    task_time_entry.delete(0, tk.END)
    task_date_entry.delete(0, tk.END)
    task_message_entry.delete(0, tk.END)
    imp_date_entry.delete(0, tk.END)
    imp_date_date_entry.delete(0, tk.END)
    imp_date_message_entry.delete(0, tk.END)
def update_important_date():
    """Update a selected important date."""
    selected_index = important_date_list.curselection()
    if selected_index:
        event_name = sorted(events["important_dates"].keys())[selected_index[0]]
        new_date = simpledialog.askstring("Update Date", "Enter new date (YYYY-MM-DD):", initialvalue=events["important_dates"][event_name]['date'])
        new_message = simpledialog.askstring("Update Message", "Enter new message:", initialvalue=events["important_dates"][event_name]['message'])
        
        if new_date and new_message:
            events["important_dates"][event_name] = {"time": "08:00", "date": new_date, "message": new_message}
            save_data()
            update_event_list()
    else:
        messagebox.showerror("Error", "Please select an important date to update!")

import tkinter as tk
from tkinter import messagebox
import json
import time
import threading
import datetime
import os
import subprocess
from PIL import Image,ImageTk

# File to store events
events_file = "time.json"
diary_folder = "diary"

# Ensure diary folder exists
if not os.path.exists(diary_folder):
    os.makedirs(diary_folder)

def load_data():
    """Load saved events from time.json."""
    if os.path.exists(events_file):
        try:
            with open(events_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"tasks": {}, "important_dates": {}}
    return {"tasks": {}, "important_dates": {}}

def save_data():
    """Save the events to time.json."""
    try:
        with open(events_file, "w") as f:
            json.dump(events, f, indent=4)
        print("Data successfully saved.")
    except Exception as e:
        print(f"Error saving data: {e}")

def open_diary(filename=None):
    """Open Notepad with the selected or today's diary file."""
    if not filename:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{date}.txt"
    file_path = os.path.join(diary_folder, filename)
    subprocess.run(["notepad.exe", file_path])
    update_diary_list()

def delete_diary():
    """Delete the selected diary entry."""
    selected_index = diary_listbox.curselection()
    if selected_index:
        filename = diary_listbox.get(selected_index)
        file_path = os.path.join(diary_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            messagebox.showinfo("Success", "Diary entry deleted.")
            update_diary_list()
        else:
            messagebox.showinfo("Info", "No entry to delete.")
    else:
        messagebox.showwarning("Warning", "Please select a diary entry to delete.")

def update_diary_list():
    """Update the listbox with available diary entries."""
    diary_listbox.delete(0, tk.END)
    files = sorted(os.listdir(diary_folder), reverse=True)
    for file in files:
        if file.endswith(".txt"):
            diary_listbox.insert(tk.END, file)

def delete_diary():
    """Delete today's diary entry."""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(diary_folder, f"{date}.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
        messagebox.showinfo("Success", "Diary entry deleted.")
    else:
        messagebox.showinfo("Info", "No entry to delete.")
events = load_data()
threading.Thread(target=check_events, daemon=True).start()

root = tk.Tk()
root.title("Task & Important Dates Manager")
root.geometry("600x550")
root.configure(bg="black")

# Task Management Section
task_frame = tk.LabelFrame(root, text="Task Management")
task_frame.pack(pady=5, padx=5, fill="both")

# Task Entry Row
task_input_frame = tk.Frame(task_frame)
task_input_frame.pack(pady=2, padx=2)

tk.Label(task_input_frame, text="Task:").grid(row=0, column=0)
task_entry = tk.Entry(task_input_frame, width=15)
task_entry.grid(row=0, column=1, padx=2)

tk.Label(task_input_frame, text="Time:").grid(row=0, column=2)
task_time_entry = tk.Entry(task_input_frame, width=8)
task_time_entry.grid(row=0, column=3, padx=2)

tk.Label(task_input_frame, text="Date:").grid(row=0, column=4)
task_date_entry = tk.Entry(task_input_frame, width=10)
task_date_entry.grid(row=0, column=5, padx=2)

tk.Label(task_input_frame, text="Message:").grid(row=0, column=6)
task_message_entry = tk.Entry(task_input_frame, width=20)
task_message_entry.grid(row=0, column=7, padx=2)

# Buttons
button_frame = tk.Frame(task_frame)
button_frame.pack()

tk.Button(button_frame, text="Add Task", command=add_task, bg="green", fg="white").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Task", command=update_task, bg="blue", fg="white").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Remove Task", command=lambda: dismiss_event(task_list.get(tk.ACTIVE).split(". ")[1].split(" on ")[0], "tasks", None), bg="red", fg="white").grid(row=0, column=2, padx=5)

task_list = tk.Listbox(task_frame, height=5, width=50)
task_list.pack()

#Important Dates Section
important_date_frame = tk.LabelFrame(root, text="Important Dates")
important_date_frame.pack(pady=5, padx=5, fill="both")

important_date_input_frame = tk.Frame(important_date_frame)
important_date_input_frame.pack(pady=2, padx=2)

tk.Label(important_date_input_frame, text="Event Name:").grid(row=0, column=0)
imp_date_entry = tk.Entry(important_date_input_frame, width=15)
imp_date_entry.grid(row=0, column=1, padx=2)

tk.Label(important_date_input_frame, text="Date:").grid(row=0, column=2)
imp_date_date_entry = tk.Entry(important_date_input_frame, width=10)
imp_date_date_entry.grid(row=0, column=3, padx=2)

tk.Label(important_date_input_frame, text="Message:").grid(row=0, column=4)
imp_date_message_entry = tk.Entry(important_date_input_frame, width=20)
imp_date_message_entry.grid(row=0, column=5, padx=2)

button_frame = tk.Frame(important_date_frame)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Add Date", command=add_important_date, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Update Date", command=update_important_date, bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Delete Date", command=lambda: dismiss_event(important_date_list.get(tk.ACTIVE).split(". ")[1].split(" on ")[0], "important_dates", None), bg="red", fg="white").pack(side=tk.LEFT, padx=5)

important_date_list = tk.Listbox(important_date_frame, height=5, width=50)
important_date_list.pack()

update_event_list()
# Diary Section
# Diary Section
diary_frame = tk.LabelFrame(root, text="Personal Diary")
diary_frame.pack(pady=5, padx=5, fill="both", expand=True)

diary_button_frame = tk.Frame(diary_frame)
diary_button_frame.pack(pady=5)

tk.Button(diary_button_frame, text="Create Note", command=lambda: open_diary(), bg="green", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(diary_button_frame, text="Update Note", command=lambda: open_diary(diary_listbox.get(tk.ACTIVE)), bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(diary_button_frame, text="View Note", command=lambda: open_diary(diary_listbox.get(tk.ACTIVE)), bg="yellow", fg="black").pack(side=tk.LEFT, padx=5)
tk.Button(diary_button_frame, text="Delete Note", command=delete_diary, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

diary_listbox = tk.Listbox(diary_frame, height=10, width=50)
diary_listbox.pack(pady=5)

update_diary_list()
root.mainloop()
