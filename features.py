import os
import tkinter as tk
from tkinter import Label, Button, messagebox
import subprocess
from datetime import datetime
import sys
from PIL import Image, ImageTk

def set_background(root, image_path):
    """Set a background image in Tkinter window without being garbage collected."""
    img = Image.open(image_path)
    img = img.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    
    # Store reference in `root` to prevent garbage collection
    root.bg_photo = ImageTk.PhotoImage(img)  

    bg_label = tk.Label(root, image=root.bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Paths to scripts (Ensure names match exactly with button labels)
SCRIPTS = {
    "Chatbot": "C:\\Users\\Laxman\\Desktop\\chatbot\\chatbot.py",
    "Home (Commands)": "C:\\Users\\Laxman\\Desktop\\chatbot\\commands.py",
    "Emergency": "C:\\Users\\Laxman\\Desktop\\chatbot\\emergency1.py",
    "To-Do List": "C:\\Users\\Laxman\\Desktop\\chatbot\\background_tasks.py",
    "Time Manager": "C:\\Users\\Laxman\\Desktop\\chatbot\\calender.py",
    "Weather": "C:\\Users\\Laxman\\Desktop\\chatbot\\weather.py",
    "Shopping": "C:\\Users\\Laxman\\Desktop\\chatbot\\shopping.py",
    "File Manager": "C:\\Users\\Laxman\\Desktop\\chatbot\\file manager.py",  # Fixed underscore
    "News": "C:\\Users\\Laxman\\Desktop\\chatbot\\news.py",
    "Stock": "C:\\Users\\Laxman\\Desktop\\chatbot\\stock.py"
}

def update_time():
    """Update date and time dynamically."""
    now = datetime.now().strftime("%A, %B %d, %Y - %H:%M:%S")
    time_label.config(text=now)
    time_label.after(1000, update_time)  # Refresh every second

def run_script(script_name):
    """Execute the selected Python script."""
    script_path = SCRIPTS.get(script_name)

    print(f"[DEBUG] Button clicked: {script_name}")
    print(f"[DEBUG] Looking for script: {script_path}")

    if not script_path or not os.path.exists(script_path):
        print(f"[❌ ERROR] Script not found: {script_path}")
        messagebox.showerror("Error", f"Script '{script_name}' not found!")
        return

    print(f"[✅ CHECK] Found script: {script_path}")

    try:
        print(f"[⏳ RUNNING] Executing {script_name}...\n")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=True)
        print(f"[✅ SUCCESS] Script Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"[❌ ERROR] Script execution failed:\n{e}")
        messagebox.showerror("Script Error", f"Error running {script_name}: {e}")
    except Exception as e:
        print(f"[❌ ERROR] Unexpected error:\n{e}")
        messagebox.showerror("Script Error", f"Unexpected error: {e}")

def show_feature_page():
    """Display the chatbot's feature selection page."""
    global time_label
    feature_window = tk.Tk()
    feature_window.title("Chatbot Features")
    feature_window.geometry("600x600")

    feature_window.resizable(False, False)  # Prevent window resizing
    
    # Load and set background image
    try:
        bg_image = Image.open("C:\\Users\\Laxman\\Desktop\\chatbot\\chatbotbg123.jpg")  # Update path
        bg_image = bg_image.resize((600, 600), Image.LANCZOS)  # Resize image to fit the window
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        print(f"Error loading background image: {e}")
        bg_photo = None  # Set a fallback if image doesn't load
    
    canvas = tk.Canvas(feature_window, width=600, height=600)
    canvas.pack(fill="both", expand=True)
    
    if bg_photo:
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    
    # Dynamic Time Label
    time_label = Label(feature_window, text="", font=("Arial", 12), fg="yellow", bg="black")
    time_label.place(x=150, y=10)  # Positioned near the top-left corner
    update_time()  # Start updating time dynamically

    # Title
    title = Label(feature_window, text="Welcome to Your AI Chatbot", font=("Arial", 16, "bold"), bg="#f5f5f5")
    title.place(x=150, y=50)  # Positioned centrally in the window

    # Frame for buttons (2-column layout)
    script_frame = tk.Frame(feature_window, bg="#f5f5f5")
    script_frame.place(x=50, y=100)  # Position the frame slightly below the title

    # Button configuration: (Text, Color)
    buttons = [
        ("🤖 Chatbot", "#3498db"),
        ("🏠 Home (Commands)", "#2ecc71"),
        ("📝 To-Do List", "#ff9900"),  # Orange
        ("⏳ Time Manager", "#8e44ad"),  # Purple
        ("📂 File Manager", "#16a085"),  # Teal
        ("🌦 Weather", "#2980b9"),  # Sky Blue
        ("🛒 Shopping", "#c0392b"),  # Dark Red   
        ("📰 News", "#d35400"),
        ("📈 Stock", "#f1c40f"),
        ("🚨 Health & Emergency", "#e74c3c")
    ]

    # Create buttons in 2 columns
  # Create a row frame for the first two buttons
    row_frame0 = tk.Frame(script_frame, bg="#e6e6e6")
    row_frame0.pack(pady=5)
    btn_todo = tk.Button(row_frame0, text="🤖 Chatbot", command=lambda: run_script("Chatbot"),
                     bg="#4169E1", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_todo.pack(side="left", padx=10, ipadx=10, ipady=5)
    btn_time_manager = tk.Button(row_frame0, text="🏠 Home (Commands)", command=lambda: run_script("Home (Commands)"),
                             bg="#C70039", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_time_manager.pack(side="left", padx=10, ipadx=10, ipady=5)
    # Create a row frame for the first two buttons
    row_frame1 = tk.Frame(script_frame, bg="#e6e6e6")
    row_frame1.pack(pady=5)
    btn_todo = tk.Button(row_frame1, text="📝 To-Do List", command=lambda: run_script("To-Do List"),
                     bg="#ff9900", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_todo.pack(side="left", padx=10, ipadx=10, ipady=5)
    btn_time_manager = tk.Button(row_frame1, text="⏳ Time Manager", command=lambda: run_script("Time Manager"),
                             bg="#8e44ad", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_time_manager.pack(side="left", padx=10, ipadx=10, ipady=5)
    # Create a row frame for the next two button
    row_frame2 = tk.Frame(script_frame, bg="#e6e6e6")
    row_frame2.pack(pady=5)
    btn_file_manager = tk.Button(row_frame2, text="📂 File Manager", command=lambda: run_script("File Manager"),
                             bg="#16a085", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_file_manager.pack(side="left", padx=10, ipadx=10, ipady=5)
    btn_weather = tk.Button(row_frame2, text="🌦 Weather", command=lambda: run_script("Weather"),
                        bg="#2980b9", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_weather.pack(side="left", padx=10, ipadx=10, ipady=5)
     # Create a row frame for two buttons
    row_frame4 = tk.Frame(script_frame, bg="#e6e6e6")
    row_frame4.pack(pady=5)
    btn_shopping = tk.Button(row_frame4, text="📰 News", command=lambda: run_script("News"),
                         bg="#00bfff", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_shopping.pack(side="left", padx=10, ipadx=10, ipady=5)
    btn_emergency = tk.Button(row_frame4, text="📉 stock market", command=lambda: run_script("Stock"),
                          bg="#dc143c", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_emergency.pack(side="left", padx=10, ipadx=10, ipady=5)
    # Create a row frame for the last two buttons
    row_frame3 = tk.Frame(script_frame, bg="#e6e6e6")
    row_frame3.pack(pady=5)
    btn_shopping = tk.Button(row_frame3, text="🛒 Shopping", command=lambda: run_script("Shopping"),
                         bg="#c0392b", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_shopping.pack(side="left", padx=10, ipadx=10, ipady=5)
    btn_emergency = tk.Button(row_frame3, text="🚨 Emergency", command=lambda: run_script("Emergency"),
                          bg="#d35400", fg="white", font=("Arial", 14), relief="raised", width=18)
    btn_emergency.pack(side="left", padx=10, ipadx=10, ipady=5)
       

    # Close button
    row_frame_exit = tk.Frame(script_frame, bg="#e6e6e6")
    row_frame_exit.pack(pady=30)  # Add some padding to give space above and below
    btn_exit = tk.Button(row_frame_exit, text="EXIT", command=feature_window.destroy,bg="red", fg="white", font=("Arial", 12), relief="raised", width=20)
    btn_exit.pack()

    feature_window.mainloop()

if __name__ == "__main__":
    show_feature_page()
