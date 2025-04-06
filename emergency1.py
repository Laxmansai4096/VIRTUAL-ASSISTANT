import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import webbrowser
import time
import requests
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import ttk
import os
import json
import subprocess
DATA_FILE = "diet_data.json"
diet_entries = []  # Initialize an empty list for diet entries
notes_text = None 
# Function to save notes
def save_notes(note_text):
    with open("diet_notes.txt", "w") as file:
        file.write(note_text.get("1.0", tk.END))
    messagebox.showinfo("Saved", "Notes saved successfully!")

# Function to load notes
def load_notes(note_text):
    if os.path.exists("diet_notes.txt"):
        with open("diet_notes.txt", "r") as file:
            note_text.insert(tk.END, file.read())
            
def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        if "loc" in data:
            latitude, longitude = data["loc"].split(",")
            location_url = f"https://www.google.com/maps?q={latitude},{longitude}"
            return f"{data['city']}, {data['region']}, {data['country']} ({location_url})"
        else:
            return "Location not available"
    except Exception:
        return "Location not available"

def call_emergency_service(number):
    confirmation = messagebox.askyesno("Confirm Call", f"Are you sure you want to call {number}?")
    if confirmation:
        webbrowser.open(f"tel:{number}")

def compose_gmail():
    location_url = get_location()
    subject = "🚨 Emergency Alert!"
    body = f"I need help immediately! This is an emergency.\n\nMy location: {location_url}"
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=emergency@example.com&su={subject}&body={body}"
    webbrowser.open(gmail_url)

def compose_whatsapp():
    location_url = get_location()
    message = f"🚨 Emergency! I need help immediately!\nMy location: {location_url}"
    webbrowser.open(f"https://web.whatsapp.com/send?phone=+911234567890&text={message}")

def emergency_alert():
    confirmation = messagebox.askyesno("Confirm", "Are you sure you want to send the emergency alert?")
    if confirmation:
        compose_gmail()
        compose_whatsapp()

def open_first_aid():
    webbrowser.open("https://www.mayoclinic.org/first-aid")
# Function to save calorie intake
def open_calorie_tracker():
    exitb= tk.Toplevel(root)
    script_path = r"C:\\Users\\Laxman\\Desktop\\chatbot\\calorietrckr.py"

    if os.path.exists(script_path):
        subprocess.run(["python", script_path], check=True)
    else:
        messagebox.showerror("Error", f"File not found: {script_path}")
    # Exit Button
    tk.Button(exitb, text="Exit", bg="#424242", fg="white", command=exitb.destroy).pack(pady=10)
def open_doctor_details():
    doc_win = tk.Toplevel(root)
    doc_win.title("Doctor Details")
    tk.Label(doc_win, text="Doctor Details", font=("Arial", 14, "bold")).pack()
    
    doctor_data = {
        "Name": "Dr. Tejaswini chary",
        "Specialization": "General Physician",
        "Contact": "9032264096",
        "Hospital": "City Medical Center",
        "Medical History": "Diabetes, Hypertension"
    }
    
    for field, value in doctor_data.items():
        tk.Label(doc_win, text=f"{field}: {value}", font=("Arial", 12)).pack()
    
    def upload_profile_pic():
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg;*.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            profile_pic_label.config(image=img)
            profile_pic_label.image = img
    
    profile_pic_label = tk.Label(doc_win)
    profile_pic_label.pack()
    tk.Button(doc_win, text="Upload Profile Picture", command=upload_profile_pic).pack()

def save_prescription():
    os.makedirs("HealthRecords", exist_ok=True)
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg")])
    if file_path:
        date_str = datetime.now().strftime("%Y-%m-%d")
        existing_files = [f for f in os.listdir("HealthRecords") if f.startswith(date_str)]
        file_name = f"{date_str}_{len(existing_files) + 1}.jpg"
        dest_path = os.path.join("HealthRecords", file_name)
        with open(file_path, 'rb') as fsrc, open(dest_path, 'wb') as fdst:
            fdst.write(fsrc.read())
        messagebox.showinfo("Success", f"Prescription saved as {file_name}")

def view_prescriptions():
    os.makedirs("HealthRecords", exist_ok=True)
    files = os.listdir("HealthRecords")
    if not files:
        messagebox.showinfo("No Records", "No prescriptions found!")
    else:
        webbrowser.open(os.path.abspath("HealthRecords"))

def open_fitness_section():
    fitness_win = tk.Toplevel(root)
    fitness_win.title("Fitness & Wellness")
    tk.Label(fitness_win, text="Choose an option:", font=("Arial", 12, "bold")).pack()
    tk.Button(fitness_win, text="Exercise Videos", bg="#FFC107", command=lambda: webbrowser.open("https://www.youtube.com/results?search_query=exercise+workout")).pack(fill='x')
    tk.Button(fitness_win, text="Yoga Videos", bg="#FF9800", command=lambda: webbrowser.open("https://www.youtube.com/results?search_query=yoga")).pack(fill='x')
    tk.Button(fitness_win, text="Meditation Guide", bg="#4CAF50", command=lambda: webbrowser.open("https://www.youtube.com/results?search_query=meditation")).pack(fill='x')

def open_health_section():
    health_win = tk.Toplevel(root)
    health_win.title("Health Section")
    tk.Button(health_win, text="First Aid", bg="#FFC107", command=open_first_aid).pack(fill='x')
    tk.Button(health_win, text="Doctor Details", bg="#FF9800", command=open_doctor_details).pack(fill='x')
    tk.Button(health_win, text="Save Prescription", bg="#4CAF50", command=save_prescription).pack(fill='x')
    tk.Button(health_win, text="View Prescriptions", bg="#3F51B5", command=view_prescriptions).pack(fill='x')
# Diet Section
# Function to open the Diet Section
def open_diet_section():
    diet_win = tk.Toplevel(root)
    diet_win.title("Diet Plan & Calorie Tracker")
    diet_win.geometry("500x500")  # Set window size

    # Sample diet data
    diet_data = [
        ["Day", "Breakfast", "Lunch", "Snacks", "Dinner"],
        ["Monday", "Oats & Fruits", "Grilled Chicken", "Nuts", "Brown Rice & Veggies"],
        ["Tuesday", "Smoothie", "Fish & Salad", "Yogurt", "Quinoa & Beans"],
        ["Wednesday", "Boiled Eggs", "Lentil Soup", "Seeds", "Whole Wheat Pasta"],
        ["Thursday", "Avocado Toast", "Chicken Wrap", "Dark Chocolate", "Stir-fried Tofu"],
        ["Friday", "Pancakes", "Paneer Curry", "Hummus & Veggies", "Rice & Dal"],
        ["Saturday", "Poha", "Grilled Fish", "Popcorn", "Khichdi"],
        ["Sunday", "Paratha", "Rajma Chawal", "Energy Bar", "Vegetable Soup"],
    ]

    # Create table
    table = ttk.Treeview(diet_win, columns=[f"col{i}" for i in range(5)], show="headings")
    for i, col in enumerate(diet_data[0]):
        table.heading(f"col{i}", text=col)
        table.column(f"col{i}", width=100)
    for row in diet_data[1:]:
        table.insert("", tk.END, values=row)
    table.pack(pady=10, padx=10)

    # Function to edit a selected row
    def edit_diet():
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a row to edit!")
            return
        values = table.item(selected_item, "values")
        new_values = []
        for i, val in enumerate(values[1:]):
            new_val = simpledialog.askstring("Edit Meal", f"Enter new {diet_data[0][i+1]}:", initialvalue=val)
            if new_val:
                new_values.append(new_val)
            else:
                new_values.append(val)
        table.item(selected_item, values=[values[0]] + new_values)

    # Function to save changes
    def save_diet():
        messagebox.showinfo("Save", "Diet Plan Saved Successfully!")

    # Function to add a new diet plan
    def new_diet():
        for item in table.get_children():
            table.delete(item)
        messagebox.showinfo("New Plan", "New Diet Plan Created!")

   # Notes Section
    tk.Label(diet_win, text="Notes:", font=("Arial", 12, "bold")).pack()
    note_text = tk.Text(diet_win, height=3, width=50)
    note_text.pack(pady=5)

    # Load existing notes
    load_notes(note_text)

    # Buttons (Centered)
    button_frame = tk.Frame(diet_win)
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Edit", bg="#FFC107", command=edit_diet).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Save Diet", bg="#4CAF50", command=save_diet).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="New", bg="#FF5722", command=new_diet).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Save Notes", bg="#3F51B5", command=lambda: save_notes(note_text)).pack(side=tk.LEFT, padx=10)

    # Exit Button
    tk.Button(diet_win, text="Exit", bg="#424242", fg="white", command=diet_win.destroy).pack(pady=10)
# Exit Application
def exit_application():
    root.quit()
def load_diet_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"diet": [], "notes": ""}

def save_diet_data():
    data = {"diet": diet_entries, "notes": notes_text.get("1.0", tk.END).strip()}
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)
def edit_diet(diet_list):
    selected = diet_list.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Select an item to edit.")
        return

    index = selected[0]
    old_value = diet_list.get(index)
    new_value = simpledialog.askstring("Edit Entry", "Modify entry:", initialvalue=old_value)
    
    if new_value:
        diet_entries[index]["food"] = new_value.split(" - ")[0]
        diet_list.delete(index)
        diet_list.insert(index, new_value)
        save_diet_data()

def remove_diet_item(diet_list):
    selected = diet_list.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Select an item to remove.")
        return
    
    index = selected[0]
    del diet_entries[index]
    diet_list.delete(index)
    save_diet_data()

# Fetch Nutrition Data from API
def fetch_nutrition_data(food_name):
    api_url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={food_name}&app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "parsed" in data and data["parsed"]:
            food_info = data["parsed"][0]["food"]["nutrients"]
            return {
                "calories": int(food_info.get("ENERC_KCAL", 0)),
                "protein": int(food_info.get("PROCNT", 0)),
                "fiber": int(food_info.get("FIBTG", 0)),
                "carbs": int(food_info.get("CHOCDF", 0)),
                "fats": int(food_info.get("FAT", 0)),
            }
    return None  # Return None if no data found

import tkinter as tk

import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Initialize main window
root = tk.Tk()
root.title("Emergency Alert System")
root.geometry("500x680")
root.resizable(False, False)

# Load and Set Background Image
bg_image = Image.open("C:\\Users\\Laxman\\Desktop\\chatbot\\chatbotbg123.jpg")  # Update path
bg_image = bg_image.resize((500, 680), Image.LANCZOS)  # Resize image
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=500, height=680)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

frame = tk.Frame(root)
frame.pack(pady=20)

buttons = [
    ("Diet Chart", "#3F51B5", open_diet_section),
    ("Calorie Tracker", "#FF7043", open_calorie_tracker), 
    ("Health Section", "#4CAF50", open_health_section),
    ("Fitness ", "#FF9800", open_fitness_section),
    ("🚨 Emergency Alert", "#D32F2F", emergency_alert),
    ("Call Ambulance (108)", "#F44336", lambda: call_emergency_service("108")),
    ("Call Police (100)", "#1976D2", lambda: call_emergency_service("100")),
    ("Call Fire Station (101)", "#FF5722", lambda: call_emergency_service("101")),
    ("Call SHE Team (1098)", "#7B1FA2", lambda: call_emergency_service("1098"))
]


# Create Button Frame
frame = tk.Frame(root, bg="#ffffff")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Create Buttons in Two Columns
for i, (text, color, command) in enumerate(buttons):
    row, col = divmod(i, 2)  # Distribute buttons into two columns
    tk.Button(frame, text=text, font=("Arial", 12, "bold"), bg=color, fg="white",
              width=20, height=2, command=command).grid(row=row, column=col, padx=10, pady=5)

# Centered Exit Button at Bottom
exit_button = tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="#424242", fg="white",
                        width=25, height=2, command=exit_application)
exit_button.place(relx=0.5, rely=0.95, anchor="s")

root.mainloop()
