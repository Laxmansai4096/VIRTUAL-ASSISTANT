import cv2
import numpy as np
import mediapipe as mp
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import json
import hashlib
from PIL import Image, ImageTk

# Initialize Mediapipe for face detection & mesh
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5)

# Path to store user data
USER_DATA_FILE = "users.json"
#Login attempt tracking
MAX_ATTEMPTS = 3
attempts = 0

# Dark Mode UI Colors
BG_COLOR = "#121212"
FG_COLOR = "white"
BUTTON_COLOR = "#1f1f1f"
HIGHLIGHT_COLOR = "#ff5733"

# ---------------- Helper Functions ----------------

def hash_password(password):
    """Hashes a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    """Loads user credentials from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {"users": []}

def save_data(data):
    """Saves user credentials to JSON file"""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load user data
user_data = load_data()

def extract_face_landmarks(image, bbox):
    """Extracts facial landmarks"""
    x, y, w, h = bbox
    face_roi = image[y:y + h, x:x + w]
    rgb_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_face)
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]
        return np.array([(lm.x, lm.y, lm.z) for lm in landmarks.landmark])
    return None

def compute_face_embedding(landmarks):
    """Computes face embedding as the mean of landmarks"""
    return np.mean(landmarks, axis=0)

def recognize_face(embedding):
    """Recognizes the face using stored embeddings"""
    for user in user_data["users"]:
        known_embedding = np.array(user.get("face_embedding", []))
        if known_embedding.size > 0 and np.linalg.norm(embedding - known_embedding) < 0.6:
            return user["username"]
    return None

# ------------------- User Registration -------------------

def register_user():
    """Registers a new user with a username and password"""
    def submit_registration():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return
        
        for user in user_data["users"]:
            if user["username"] == username:
                messagebox.showerror("Error", "Username already exists.")
                return
        
        password_hash = hash_password(password)
        new_user = {
            "username": username,
            "password": password_hash,
            "face_embedding": []
        }
        user_data["users"].append(new_user)
        save_data(user_data)
        messagebox.showinfo("Success", "User registered successfully!")
        registration_window.destroy()

        if messagebox.askyesno("Face Registration", "Would you like to register your face now?"):
            register_face(username)

    registration_window = tk.Toplevel()
    registration_window.title("User Registration")

    tk.Label(registration_window, text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(registration_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(registration_window, text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(registration_window, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(registration_window, text="Register", command=submit_registration).grid(row=2, columnspan=2, pady=10)

# ------------------- Face Registration -------------------

def register_face(username):
    """Captures and registers a face for a user"""
    user = next((u for u in user_data["users"] if u["username"] == username), None)
    if not user:
        messagebox.showerror("Error", "User not found!")
        return

    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                bbox = (x, y, w, h)

                face_landmarks = extract_face_landmarks(rgb_frame, bbox)
                if face_landmarks is not None:
                    embedding = compute_face_embedding(face_landmarks)
                    user["face_embedding"] = embedding.tolist()
                    save_data(user_data)
                    messagebox.showinfo("Success", "Face registered successfully!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

        cv2.imshow('Register Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ------------------- Face Login -------------------

import cv2
import numpy as np
import subprocess  # For opening the chatbot script

def login_face():
    """Login using face recognition with limited attempts."""
    global attempts
    cap = cv2.VideoCapture(0)

    while attempts < MAX_ATTEMPTS:
        success, frame = cap.read()
        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                bbox = (x, y, w, h)

                face_landmarks = extract_face_landmarks(rgb_frame, bbox)
                if face_landmarks is not None:
                    embedding = compute_face_embedding(face_landmarks)
                    username = recognize_face(embedding)  # Match against stored embeddings

                    if username:
                        cv2.putText(frame, f"Face ID: {username}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.imshow('Face Recognition', frame)
                        cv2.waitKey(2000)

                        messagebox.showinfo("Login", f"Welcome to Virtual Assistant, {username}!")

                        cap.release()
                        cv2.destroyAllWindows()

                        # Redirect user to chatbot system
                        os.system(f"python C:\\Users\\Laxman\\Desktop\\chatbot\\features.py")
                        return
                    else:
                        attempts += 1
                        messagebox.showwarning("Login Failed", f"Attempt {attempts}/{MAX_ATTEMPTS}. Try again.")

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    messagebox.showerror("Login Blocked", "Too many failed attempts. Please try again later.")
    cap.release()
    cv2.destroyAllWindows()

# ------------------- Credentials Login -------------------

def login_credentials():
    """Authenticates user using username and password with separate input fields"""
    def authenticate():
        username = entry_username.get()
        password = entry_password.get()
        
        if username and password:
            password_hash = hash_password(password)
            if any(u["username"] == username and u["password"] == password_hash for u in user_data["users"]):
                messagebox.showinfo("Login", f"Welcome, {username}!")
                login_window.destroy()  # Close the login window after successful login
            else:
                messagebox.showerror("Error", "Invalid credentials.")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
    # Create a new window for login
     # Create a new window for login
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")
    
    # Background color
    login_window.configure(bg="#2E3B4E")  # Dark blue color for the background

    # Username input (above background)
    label_username = tk.Label(login_window, text="Username:", fg="white", bg="#2E3B4E", font=("Arial", 14))
    label_username.pack(pady=10)
    entry_username = tk.Entry(login_window, width=30, font=("Arial", 12))
    entry_username.pack(pady=5)
    
    # Password input
    label_password = tk.Label(login_window, text="Password:", fg="white", bg="#2E3B4E", font=("Arial", 14))
    label_password.pack(pady=10)
    entry_password = tk.Entry(login_window, width=30, show='*', font=("Arial", 12))
    entry_password.pack(pady=5)
    
    # Login button (stylish with modern color)
    login_button = tk.Button(login_window, text="Login", command=authenticate, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), relief="flat")
    login_button.pack(pady=20, ipadx=10, ipady=5)

# ------------------- Main UI -------------------
root = tk.Tk()
root.title("Login/Register System")
root.geometry("500x550")  # Adjust size based on image dimensions
root.resizable(False, False)

# Load and Set Full-Screen Background Image
bg_image = Image.open("C:\\Users\\Laxman\\Desktop\\chatbot\\chatbotbg123.jpg")  # Replace with your image path
bg_image = bg_image.resize((600, 700), Image.Resampling.LANCZOS)  # Resize to match window
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # Light grey background for a modern look

# Heading Label
title_label = tk.Label(root, text="USER AUTHENTICATION", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=20)

# Button Styling
button_style = {
    "font": ("Arial", 14, "bold"),
    "width": 20,
    "height": 1,
    "bd": 3,
    "relief": "raised",
}

# Button Colors
colors = {
    "register": "#ff5733",  # Red-Orange
    "face_login": "#337ab7",  # Blue
    "password_login": "#28a745",  # Green
    "exit": "#6c757d",  # Grey
}

# Buttons
register_btn = tk.Button(root, text="📝 Register User", bg=colors["register"], fg="white", command=register_user, **button_style)
register_btn.pack(pady=10)

face_login_btn = tk.Button(root, text="📷 Login with Face", bg=colors["face_login"], fg="white", command=login_face, **button_style)
face_login_btn.pack(pady=10)

password_login_btn = tk.Button(root, text="🔑 Login with Credentials", bg=colors["password_login"], fg="white", command=login_credentials, **button_style)
password_login_btn.pack(pady=10)
#exit button
# Exit Button (Now Styled Directly)
exit_btn = tk.Button(root, text="❌ Exit", bg="#6c757d", fg="white", font=("Arial", 14, "bold"),
                     width=20, height=1, bd=3, relief="raised", command=root.destroy)
exit_btn.pack(side="bottom", padx=10, pady=10)


root.mainloop()
