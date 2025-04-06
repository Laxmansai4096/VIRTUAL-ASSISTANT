import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Toplevel,Label
import pyttsx3
import speech_recognition as sr
import time
import webbrowser
import datetime
import os
import cv2
import threading
from datetime import datetime
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyautogui
import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput.keyboard import Key, Controller
from ctypes import cast, POINTER
from threading import Thread
import socket
import psutil
from comtypes import CLSCTX_ALL
from tkinter import scrolledtext, Entry, Button, Toplevel
import sys

# ----- Voice Assistant Setup -----
today = datetime.today()
recog = sr.Recognizer()


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

mc = sr.Microphone(device_index=0)
is_awake = True
video_capture_active = False

# Get the audio endpoint
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def reply(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

from pynput.keyboard import Key,Controller

from time import sleep

keyboards = Controller()
# Get the current volume level
current_volume = volume.GetMasterVolumeLevel()
# Get the volume range (min, max, increment)
volume_range = volume.GetVolumeRange()
min_volume = volume_range[0]
max_volume = volume_range[1]
def volumeup():
    # Increase volume
    volume_increment = 2.0
    new_volume = current_volume + volume_increment
    if new_volume > max_volume:
        new_volume = max_volume  # Limit to max volume
    volume.SetMasterVolumeLevel(new_volume, None)
    print(f"Volume set to: {new_volume} dB")
def volumedown():
    # Decrease volume
    volume_increment = 2.0
    new_volume = current_volume - volume_increment
    if new_volume < min_volume:
        new_volume = min_volume  # Limit to min volume
    volume.SetMasterVolumeLevel(new_volume, None)
    print(f"Volume set to: {new_volume} dB")

def schedule_action(hours, minutes, action):
    """Schedules a system action (shutdown or restart) after a given time."""
    seconds = (hours * 3600) + (minutes * 60)
    reply(f"System will {action} in {hours} hours and {minutes} minutes.")
    time.sleep(seconds)
    
    if action == "shutdown":
        reply("Shutting down the system...")
        os.system('shutdown /s /t 1')
    elif action == "restart":
        reply("Restarting the system...")
        os.system('shutdown /r /t 1')
    else:
        reply("Invalid action. Please choose 'shutdown' or 'restart'.")
        
def get_user_time_input():
    """Prompts the user for time duration in hours and minutes."""
    while True:
        try:
            hours = int(input("Enter the number of hours: "))
            minutes = int(input("Enter the number of minutes: "))
            if hours < 0 or minutes < 0:
                raise ValueError("Hours and minutes must be non-negative.")
            return hours, minutes
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter valid integers for hours and minutes.")
def wish():
    hour = int(datetime.now().hour)
    if hour < 12:
        reply("Good Morning!")
    elif hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
    reply("I am Sai, how may I help you?")

def convert_speech_to_text(model_path, max_duration):
    """Converts speech to text using the saved model with optimizations for speed."""
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()

    reply("start speaking...")

    recognized_text = ""
    start_time = time.time()
    
    while True:
        data = stream.read(2048, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            recognized_text += result.get("text", "") + " "
            break  # Stop as soon as we recognize a command
        elif time.time() - start_time > max_duration:
            break  # Stop after max_duration seconds if no command is recognized

    stream.stop_stream()
    stream.close()
    p.terminate()

    recognized_text = recognized_text.strip()
    reply(f"You said: {recognized_text}")
    return recognized_text

def start_video_capture():
    global video_capture_active
    video_capture_active = True
    cap = cv2.VideoCapture(0)

    while video_capture_active:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Capture', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_ip_address():
    # Get the local IP address of the machine
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # Prepare response with local IP
    response = f"Local IP Address: {local_ip}\n"
    
    # Get MAC address of network interfaces
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:  # AF_LINK represents MAC addresses
                response += f"Interface: {interface}, MAC Address: {addr.address}\n"
    
    # Return the response so it can be used elsewhere (e.g., chatbot response)
    print(response)
    return 

is_awake = True
video_capture_active = False
# Get the audio endpoint
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

greet=["hii","hi","hello","sai","wakeup","who are you","what u do"]
def respond(voice_data):
    global is_awake
    global video_capture_active
    global gesture_recognition_active
    voice_data = voice_data.replace('sai', '').strip()

    response = ""  # Prepare the response variable
    voice_data=voice_data.lower()

    if not is_awake and 'wake up' in voice_data:
        is_awake = True
        wish()
    elif voice_data in greet:
        response = 'My name is Sai!'
        reply(response)
        wish()
    elif 'date' in voice_data:
        response = today.strftime("%B %d, %Y")
        reply(response)
    elif 'time' in voice_data:
        response = datetime.datetime.now().strftime("%H:%M:%S")
        reply(response)
    elif 'search' in voice_data:
        query = voice_data.split('search')[-1].strip()
        response = f'Searching for {query}'
        reply(response)
        webbrowser.open(f'https://google.com/search?q={query}')
    elif 'shutdown' in voice_data:
        response = "How many hours and minutes before shutdown?"
        reply(response)
        hours, minutes = get_user_time_input()
        schedule_action(hours, minutes, "shutdown")
    elif 'restart' in voice_data:
        response = "How many hours and minutes before restart?"
        reply(response)
        hours, minutes = get_user_time_input()
        schedule_action(hours, minutes, "restart")
    elif 'location' in voice_data:
        response = 'Which place are you looking for?'
        reply(response)
        model_path = "C:\\Users\\Laxman\\Desktop\\vosk-model-en-in-0.5\\vosk-model-en-in-0.5"
        temp_audio = convert_speech_to_text(model_path, max_duration=10)
        response = 'Locating...'
        reply(response)
        webbrowser.open(f'https://google.nl/maps/place/{temp_audio}')
    elif 'quit' in voice_data or 'exit' in voice_data:
        response = "Execution stopped"
        reply(response)
        exit()
        
    elif 'open' in voice_data:
        if 'notepad' in voice_data:
            response = "Notepad opened"
            reply(response)
            os.system('notepad.exe')
        elif 'youtube' in voice_data:
            response = "Opening YouTube"
            reply(response)
            webbrowser.open('https://www.youtube.com')
        elif 'command prompt' in voice_data:
            response = "Command Prompt opened"
            reply(response)
            os.system('start cmd')
        elif 'settings' in voice_data:
            response = "Settings opened"
            reply(response)
            os.system('start ms-settings:')
        elif 'vscode' in voice_data:
            response = "Visual Studio Code opened"
            reply(response)
            os.system('code')
        elif 'chrome' in voice_data:
            response = "Google Chrome opened"
            reply(response)
            os.system('start chrome')
        elif 'brave' in voice_data:
            response = "Brave browser opened"
            reply(response)
            os.system('start brave')
        elif 'file' in voice_data:
            file_path = voice_data.split("open file")[-1].strip()
            response = f"Opening file {file_path}"
            reply(response)
            os.system(f'start {file_path}')
        elif 'paint' in voice_data:
            response = "Paint opened"
            reply(response)
            os.system('mspaint.exe')
        elif 'gallery' in voice_data:
            response = "Gallery opened"
            reply(response)
            os.system('start ms-photos:')
        elif 'msword' in voice_data:
            response = "Microsoft Word opened"
            reply(response)
            os.system('start winword')
        elif 'powerpoint' in voice_data:
            response = "PowerPoint opened"
            reply(response)
            os.system('start powerpnt')
        elif 'camera' in voice_data:
            response = "Camera opened"
            reply(response)
            os.system('start microsoft.windows.camera:')
        elif 'gmail' in voice_data:
            response = "Opening Gmail"
            reply(response)
            webbrowser.open('https://mail.google.com')
        elif 'chatgpt' in voice_data:
            response = "Opening ChatGPT"
            reply(response)
            webbrowser.open('https://chat.openai.com')
    elif 'start video' in voice_data:
        if not video_capture_active:
            response = 'Starting video capture'
            reply(response)
            t = Thread(target=start_video_capture)
            t.start()
        else:
            response = 'Video capture is already active'
            reply(response)
    elif 'stop video' in voice_data:
        if video_capture_active:
            response = 'Stopping video capture'
            reply(response)
            video_capture_active = False
        else:
            response = 'Video capture is not active'
            reply(response)
    elif "pause" in voice_data:
        pyautogui.press("k")
        response = "Video paused"
        reply(response)
    elif "play" in voice_data:
        pyautogui.press("k")
        response = "Video played"
        reply(response)
    elif "mute" in voice_data:
        pyautogui.press("m")
        response = "Video muted"
        reply(response)
    elif "volume up" in voice_data or "increase volume" in voice_data:
        response = "Turning volume up, sir"
        reply(response)
        volumeup()
    elif "volume down" in voice_data or "decrease volume" in voice_data:
        response = "Turning volume down, sir"
        reply(response)
        volumedown()
    elif "keyboard" in voice_data:
        os.system("osk")
        response = "On-screen keyboard opened"
        reply(response)
    elif "fetchip" in voice_data:
        ip_address = get_ip_address()  # Function to fetch the IP address
        response = f"Your IP address is fetched"
        reply(response)
    elif "refresh" in voice_data:
        pyautogui.press('f5')
        response=f"system refreshed"
        reply(response)
        
    elif "paste" in voice_data:
        pyautogui.hotkey('ctrl', 'v')
        response="copied text pasted"
        reply(response)
    elif "close window" in voice_data:
        pyautogui.hotkey('alt', 'f4')
        response=f"window closed"
        reply(response)
    elif "switch window" in voice_data:
        pyautogui.hotkey('alt', 'tab')
        response=f"window switched"
        reply(response)
    elif "min window" in voice_data:
        pyautogui.hotkey('win', 'down')
        response=f"window minimised"
        reply(response)
    elif "max window" in voice_data:
        pyautogui.hotkey('win', 'up')
        response=f"window maximised"
        reply(response)
    elif "file explorer"in voice_data:
        pyautogui.hotkey('win','e')
        response=f"File explorer opened"
        reply(response)
    elif 'task manager' in voice_data:
        pyautogui.hotkey('ctrl','shift','esc')
        response=f"task manager opened"
        reply(response)
    elif 'capslock' in voice_data:
        pyautogui.press('capslock')
        response=f"capslock activated"
        reply(response)
    elif "emoji" in voice_data:
        pyautogui.hotkey('win','.')
        response=f"emojis opened"
        reply(response)
    elif "clipboard" in voice_data:
        pyautogui.hotkey('win','v')
        response=f"clipboard history opened"
        reply(response)
        
    elif "lockscreen" in voice_data:
        pyautogui.hotkey('win', 'l')
        response=f"lock screen opened"
        reply(response)
    elif "show desktop" in voice_data:
        pyautogui.hotkey('win', 'd')
        response=f"Desktop screen"
        reply(response)
    elif "screenshot" in voice_data:
        pyautogui.press('printscreen')
        response=f"screenshot clicked"
        reply(response)
    elif "window screenshot" in voice_data:
        pyautogui.hotkey('alt','printscreen')
        response=f"window screenshot clicked"
        reply(response)
    elif "window" in voice_data:
        pyautogui.press('win')
        response=f"windows opened"
        reply(response)
    elif "task bar" in voice_data:
        pyautogui.hotkey('win','tab')
        response=f"taskbar opened"
        reply(response)
        
    elif "q shutdown"in voice_data:
        response=f"system shudowning now"
        reply(response)
        os.system("shutdown /s /t 1") 
    elif "q restart" in voice_data:
        response=f"system restarting now"
        reply(response)
        os.system("shutdown /r /t 1")
    elif "copy path" in voice_data:
        pyautogui.hotkey('ctrl','shift','c')
        response=f"path is copied"
        reply(response)
    elif "run command" in voice_data:
        pyautogui.hotkey('win','r')
        response=f"command is running"
        reply(response)
    elif "search" in voice_data:
        pyautogui.hotkey('win','s')
        response=f"search is opened"
        reply(response)
    elif "show notifications" in voice_data:
        pyautogui.hotkey('win','a')
        response=f"notifications are opened"
        reply(response)
    elif "firstaid"in voice_data:
        response="first aid shortcut opened"
        reply(response)
        webbrowser.open("https://www.mayoclinic.org/first-aid")
                
    elif 'bye' in voice_data or 'by' in voice_data:
        response = "Goodbye! Have a nice day."
        reply(response)
        is_awake = False

    # Return the final response for GUI display
    return response

# Global settings
is_dark_mode = False
is_vanish_mode = False
is_audio_on = True
is_mic_on = True
is_running = True  # Controls play/pause

def speak(text):
    """Function for Text-to-Speech."""
    if is_audio_on:
        engine.say(text)
        engine.runAndWait()

# Function to handle user input
def send_text_message(event=None):
    if not is_running:
        return

    message = user_input.get().strip()
    if message:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"You: {message}\n", "user_tag")
        chat_area.config(state=tk.DISABLED)
        user_input.delete(0, tk.END)

        # Get response from chatbot
        response = respond(message)

        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"Chatbot: {response}\n", "bot_tag")
        chat_area.config(state=tk.DISABLED)
        chat_area.see(tk.END)

        if is_vanish_mode:
            chat_area.after(3000, lambda: chat_area.delete("1.0", tk.END))

def toggle_dark_mode():
    """Toggle between light and dark modes."""
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    bg_color = "black" if is_dark_mode else "white"
    fg_color = "white" if is_dark_mode else "black"

    root.config(bg=bg_color)
    chat_area.config(bg=bg_color, fg=fg_color)
    user_input.config(bg=bg_color, fg=fg_color)

def toggle_clear():
    """Enable or disable vanish mode."""
    global is_vanish_mode
    is_vanish_mode = not is_vanish_mode
    if is_vanish_mode:
        chat_area.config(state=tk.NORMAL)
        chat_area.delete(1.0, tk.END)
        chat_area.config(state=tk.DISABLED)


def toggle_audio():
    """Mute or unmute chatbot voice."""
    global is_audio_on
    is_audio_on = not is_audio_on
    if not is_audio_on:
        print("Audio output is now muted.")
    else:
        print("Audio output is now unmuted.")
        reply("Audio is unmuted.")

# Function to toggle microphone (enable/disable)
def toggle_mic():
    """Enable or disable microphone input."""
    global is_mic_on
    is_mic_on = not is_mic_on
    if not is_mic_on:
        print("Microphone is now off. Audio commands will not be processed.")
        speak("Microphone is off.")
    else:
        print("Microphone is now on. Audio commands will be processed.")
        speak("Microphone is on.")

def play_pause_chatbot():
    """Pause or Resume the Chatbot."""
    global is_running
    is_running = not is_running

    if is_running:
        play_pause_button.config(text="Pause")
        threading.Thread(target=start_virtual_assistant, daemon=True).start()
    else:
        play_pause_button.config(text="Play")
        sys.exit(0)  # Stops execution when paused

def start_virtual_assistant():
    """Start the virtual assistant for voice commands."""
    speak("Welcome! I am your virtual assistant.")
    while is_running:
        try:
            if is_mic_on:
                with sr.Microphone() as source:
                    recog.adjust_for_ambient_noise(source)
                    print("Listening...")
                    audio = recog.listen(source)
                    voice_data = recog.recognize_google(audio)
                    print(f"You said: {voice_data}")

                    chat_area.config(state=tk.NORMAL)
                    chat_area.insert(tk.END, f"You: {voice_data}\n", "user_tag")
                    chat_area.config(state=tk.DISABLED)
                    chat_area.see(tk.END)

                    # Get response from chatbot
                    response = respond(voice_data)

                    chat_area.config(state=tk.NORMAL)
                    chat_area.insert(tk.END, f"Chatbot: {response}\n", "bot_tag")
                    chat_area.config(state=tk.DISABLED)
                    chat_area.see(tk.END)
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            continue

# ------------------ UI Elements ------------------
# Initialize UI
root = tk.Tk()
root.title("AI Virtual Assistant")
root.geometry("600x700")
root.configure(bg="#1E1E1E")  # Professional dark background

chat_area = scrolledtext.ScrolledText(root, width=60, height=28, bg="#2D2D2D", fg="white")
chat_area.pack(pady=10)
chat_area.config(state=tk.DISABLED)
chat_area.tag_config("user_tag", foreground="green", justify="right")  # Green for user
chat_area.tag_config("bot_tag", foreground="red", justify="left")  # Cyan for bot

# Input Frame
user_input_frame = tk.Frame(root, bg="#1E1E1E")
user_input_frame.pack(side=tk.BOTTOM, pady=(5, 10)) 

user_input = Entry(user_input_frame, width=60, bg="#333333", fg="white", insertbackground="white")
user_input.pack(side=tk.LEFT, padx=(0, 10))
user_input.bind("<Return>", send_text_message)

send_button = Button(user_input_frame, text="Send ➤", command=send_text_message, bg="#0078D7", fg="white")
send_button.pack(side=tk.LEFT)

# Controls
controls_frame = tk.Frame(root, bg="#1E1E1E")
controls_frame.pack(side=tk.BOTTOM, pady=2)

dark_mode_button = Button(controls_frame, text="Dark Mode ☾☀︎", command=toggle_dark_mode, bg="#555555", fg="white")
dark_mode_button.pack(side=tk.LEFT, padx=8)

audio_button = Button(controls_frame, text="Audio 🔊", command=toggle_audio, bg="#4CAF50", fg="white")
audio_button.pack(side=tk.LEFT, padx=8)

mic_button = Button(controls_frame, text="Mic 🎙️", command=toggle_mic, bg="#FF9800", fg="white")
mic_button.pack(side=tk.LEFT, padx=8)

play_pause_button = Button(controls_frame, text="Pause ⏯", command=play_pause_chatbot, bg="#E91E63", fg="white")
play_pause_button.pack(side=tk.LEFT, padx=8)

# Start Voice Assistant Thread
threading.Thread(target=start_virtual_assistant, daemon=True).start()

root.mainloop()
