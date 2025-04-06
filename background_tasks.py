import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image,ImageTk

TASKS_FILE = "tasks.json"
UNDO_STACK = []

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def save_state():
    tasks = load_tasks()
    UNDO_STACK.append(tasks)

def undo_last_action():
    if UNDO_STACK:
        previous_state = UNDO_STACK.pop()
        save_tasks(previous_state)
        refresh_task_list()
        messagebox.showinfo("Undo", "Last action undone.")
    else:
        messagebox.showwarning("Undo", "No actions to undo.")

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def add_task():
    task = task_entry.get()
    category = category_entry.get()
    priority = priority_var.get()
    due_date = due_date_entry.get()
    recurrence = recurrence_var.get()

    if not task or not category or not validate_date(due_date):
        messagebox.showwarning("Invalid Input", "Please enter valid task details.")
        return

    save_state()
    tasks = load_tasks()
    tasks.append({
        "task": task,
        "category": category,
        "priority": priority,
        "due_date": due_date,
        "finished": False,
        "recurrence": recurrence
    })
    save_tasks(tasks)
    refresh_task_list()
    messagebox.showinfo("Success", "Task added successfully!")

def remove_task():
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showwarning("Remove Task", "Please select a task to remove.")
        return

    save_state()
    tasks = load_tasks()
    index = int(task_list.item(selected_item, "text"))
    del tasks[index]
    save_tasks(tasks)
    refresh_task_list()
    messagebox.showinfo("Success", "Task removed successfully!")

def toggle_task_status():
    selected_item = task_list.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a task to toggle its status.")
        return

    tasks = load_tasks()

    for item in selected_item:
        try:
            # Get the task name from the selected row
            task_name = task_list.item(item, "values")[0]  # First column: Task Name
        except IndexError:
            messagebox.showerror("Error", "Could not retrieve task information.")
            return

        # Find the corresponding task in the task list
        for task in tasks:
            if task["task"] == task_name:
                task["finished"] = not task.get("finished", False)

    save_tasks(tasks)
    refresh_task_list()
    messagebox.showinfo("Task Updated", "Selected task(s) status toggled successfully.")

    save_state()
    tasks = load_tasks()
    index = int(task_list.item(selected_item, "text"))
    tasks[index]["finished"] = not tasks[index]["finished"]
    save_tasks(tasks)
    refresh_task_list()

def refresh_task_list():
    task_list.delete(*task_list.get_children())
    tasks = load_tasks()

    # Sort tasks by due date
    tasks.sort(key=lambda x: x.get("due_date", "9999-12-31"))

    for idx, task in enumerate(tasks):
        status = "✅" if task.get("finished", False) else "❌"
        tag = "next_task" if idx == 0 else ""

        task_list.insert("", "end", text=str(idx), values=(
            task.get("task", "Unnamed Task"),
            task.get("category", "Uncategorized"),
            task.get("priority", "Unknown"),
            task.get("due_date", "No Due Date"),
            status,
            task.get("recurrence", "None")
        ), tags=(tag,))

    task_list.tag_configure("next_task", foreground="red", font=("Arial", 10, "bold"))

def show_reminders():
    tasks = load_tasks()
    today = datetime.date.today().strftime("%Y-%m-%d")
    upcoming_tasks = [task for task in tasks if task.get("due_date", "9999-12-31") >= today and not task.get("finished", False)]

    if not upcoming_tasks:
        messagebox.showinfo("Reminders", "No upcoming tasks.")
        return

    reminder_text = "\n".join([f"{task.get('task', 'Unnamed')} (Due: {task.get('due_date', 'N/A')})" for task in upcoming_tasks])
    messagebox.showinfo("Upcoming Reminders", reminder_text)

def show_statistics():
    tasks = load_tasks()
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    completed = sum(1 for task in tasks if task.get("finished", False))
    overdue = sum(1 for task in tasks if task.get("due_date", "9999-12-31") < today and not task.get("finished", False))
    total_tasks = len(tasks)

    stats_text = f"Total Tasks: {total_tasks}\nCompleted: {completed}\nOverdue: {overdue}"
    messagebox.showinfo("Task Statistics", stats_text)

def show_help():
    help_text = (
        "1. Add Task: Enter details and click 'Add Task'.\n"
        "2. Remove Task: Select a task and click 'Remove Task'.\n"
        "3. Toggle Status: Select a task and click 'Toggle Status'.\n"
        "4. Show Reminders: Click 'Show Reminders'.\n"
        "5. View Stats: Click 'Task Statistics'.\n"
        "6. Undo Last Action: Click 'Undo'."
    )
    messagebox.showinfo("Help", help_text)
def exit_application():
    root.quit()
# GUI Setup
root = tk.Tk()
root.title("Potato Task Manager")
root.geometry("500x500")
root.resizable(False, False)

# Load and set background image
bg_image = Image.open("C:\\Users\\Laxman\\Desktop\\chatbot\\chatbotbg123.jpg")  # Update path
bg_image = bg_image.resize((500, 500), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Input Fields
frame = tk.Frame(root, bg="white")
frame.place(relx=0.5, rely=0.05, anchor="n")

tk.Label(frame, text="Task:", bg="white").grid(row=0, column=0, sticky="w")
task_entry = tk.Entry(frame, width=25)
task_entry.grid(row=0, column=1)

tk.Label(frame, text="Category:", bg="white").grid(row=1, column=0, sticky="w")
category_entry = tk.Entry(frame, width=25)
category_entry.grid(row=1, column=1)

tk.Label(frame, text="Priority:", bg="white").grid(row=2, column=0, sticky="w")
priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(frame, textvariable=priority_var, values=["Low", "Medium", "High"], width=22)
priority_menu.grid(row=2, column=1)

tk.Label(frame, text="Due Date (YYYY-MM-DD):", bg="white").grid(row=3, column=0, sticky="w")
due_date_entry = tk.Entry(frame, width=25)
due_date_entry.grid(row=3, column=1)

tk.Label(frame, text="Recurrence:", bg="white").grid(row=4, column=0, sticky="w")
recurrence_var = tk.StringVar(value="None")
recurrence_menu = ttk.Combobox(frame, textvariable=recurrence_var, values=["None", "Daily", "Weekly", "Monthly"], width=22)
recurrence_menu.grid(row=4, column=1)

# Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.place(relx=0.5, rely=0.3, anchor="n")

btn_colors = {"fg": "white", "width": 15}

tk.Button(button_frame, text="Add Task", command=add_task, bg="green", **btn_colors).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Remove Task", command=remove_task, bg="red", **btn_colors).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Toggle Status", command=toggle_task_status, bg="blue", **btn_colors).grid(row=1, column=0, padx=5)
tk.Button(button_frame, text="Show Reminders", command=show_reminders, bg="orange", **btn_colors).grid(row=1, column=1, padx=5)
tk.Button(button_frame, text="Task Statistics", command=show_statistics, bg="purple", **btn_colors).grid(row=2, column=0, padx=5)
tk.Button(button_frame, text="Undo", command=undo_last_action, bg="gray", **btn_colors).grid(row=2, column=1, padx=5)
tk.Button(button_frame, text="Help", command=show_help, bg="brown", **btn_colors).grid(row=3, column=0, columnspan=2, pady=5)

# Task List
task_list_frame = tk.Frame(root, bg="white")
task_list_frame.place(relx=0.5, rely=0.5, anchor="n")

columns = ("Task", "Category", "Priority", "Due Date", "Status", "Rec")
task_list = ttk.Treeview(task_list_frame, columns=columns, show="headings", height=6)
for col, width in zip(columns, [150, 60, 50, 90, 50, 50]):  # Adjust column widths
    task_list.column(col, width=width)
    task_list.heading(col, text=col)
task_list.pack(pady=10)
# Exit Button
tk.Button(root, text="Exit", command=exit_application, bg="black", fg="white", width=20).place(relx=0.5, rely=0.9, anchor="s")

refresh_task_list()
root.mainloop()
