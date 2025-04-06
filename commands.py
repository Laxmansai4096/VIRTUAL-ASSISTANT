import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import os
import json

# File to store commands
COMMANDS_FILE = "home.json"

def load_commands():
    """Load commands from home.json file."""
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "r") as file:
            return json.load(file)
    return []

def save_commands(commands):
    """Save commands to home.json file."""
    with open(COMMANDS_FILE, "w") as file:
        json.dump(commands, file, indent=4)

def show_commands():
    """Display all commands in a professional UI with management buttons."""
    commands = load_commands()
    
    command_window = tk.Tk()
    command_window.title("Command Manager")
    command_window.geometry("600x450")

    # Treeview Frame
    frame = tk.Frame(command_window)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("Task", "Command"), show="headings")
    tree.heading("Task", text="Task")
    tree.heading("Command", text="Command")
    tree.column("Task", width=200)
    tree.column("Command", width=350)

    # Insert commands into the tree
    for cmd in commands:
        tree.insert("", tk.END, values=(cmd['task'], cmd['command']))

    tree.pack(fill=tk.BOTH, expand=True)

    # Buttons Frame
    button_frame = tk.Frame(command_window)
    button_frame.pack(pady=10)

    add_btn = tk.Button(button_frame, text="Add", command=lambda: add_command(tree), bg="#28a745", fg="white", font=("Arial", 12))
    add_btn.grid(row=0, column=0, padx=5)

    edit_btn = tk.Button(button_frame, text="Edit", command=lambda: edit_command(tree), bg="#ffc107", fg="black", font=("Arial", 12))
    edit_btn.grid(row=0, column=1, padx=5)

    remove_btn = tk.Button(button_frame, text="Remove", command=lambda: remove_command(tree), bg="#dc3545", fg="white", font=("Arial", 12))
    remove_btn.grid(row=0, column=2, padx=5)

    close_btn = tk.Button(command_window, text="Close", command=command_window.destroy, bg="#6c757d", fg="white", font=("Arial", 12))
    close_btn.pack(pady=10)

    command_window.mainloop()

def add_command(tree):
    """Add a new command."""
    task = simpledialog.askstring("Add Command", "Enter task name:")
    command = simpledialog.askstring("Add Command", "Enter command:")

    if task and command:
        commands = load_commands()
        commands.append({"task": task, "command": command})
        save_commands(commands)
        messagebox.showinfo("Success", "New command added successfully!")
        refresh_tree(tree)

def edit_command(tree):
    """Edit selected command."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a command to edit.")
        return

    item = tree.item(selected_item)
    old_task, old_command = item["values"]

    new_task = simpledialog.askstring("Edit Command", "Enter new task name:", initialvalue=old_task)
    new_command = simpledialog.askstring("Edit Command", "Enter new command:", initialvalue=old_command)

    if new_task and new_command:
        commands = load_commands()
        for cmd in commands:
            if cmd["task"] == old_task and cmd["command"] == old_command:
                cmd["task"] = new_task
                cmd["command"] = new_command
                break
        save_commands(commands)
        messagebox.showinfo("Success", "Command updated successfully!")
        refresh_tree(tree)

def remove_command(tree):
    """Remove selected command."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a command to remove.")
        return

    item = tree.item(selected_item)
    task, command = item["values"]

    commands = load_commands()
    commands = [cmd for cmd in commands if not (cmd["task"] == task and cmd["command"] == command)]
    save_commands(commands)

    messagebox.showinfo("Success", "Command removed successfully!")
    refresh_tree(tree)

def refresh_tree(tree):
    """Refresh the treeview after changes."""
    tree.delete(*tree.get_children())  # Clear tree
    for cmd in load_commands():
        tree.insert("", tk.END, values=(cmd['task'], cmd['command']))  # Reload data

if __name__ == "__main__":
    show_commands()
