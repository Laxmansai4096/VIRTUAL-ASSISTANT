import geocoder
import requests
import time
import webbrowser
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import Label, Button
from geopy.geocoders import Nominatim


def get_device_location():
    """Fetch the device's location (latitude, longitude)"""
    print("Requesting location access... Please wait.")
    
    g = geocoder.ip('me')  # Get location using IP
    latitude = g.latlng[0]
    longitude = g.latlng[1]
    
    time.sleep(3)  # Simulate location access wait
    
    print(f"Device location: Latitude={latitude}, Longitude={longitude}")
    return latitude, longitude

def get_location_details(latitude, longitude):
    """Reverse geocode latitude & longitude to get address details"""
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.reverse((latitude, longitude), language='en', addressdetails=True)
    
    if location:
        address_details = location.raw.get('address', {})
        location_name = address_details.get('city', address_details.get('town', 'Unknown City'))
        country = address_details.get('country', 'Unknown Country')
        pincode = address_details.get('postcode', 'Unknown Pincode')

        print(f"Location Name: {location_name}, Country: {country}, Pincode: {pincode}")
        return location_name, country, pincode
    else:
        print("Unable to retrieve location details.")
        return "Unknown", "Unknown", "Unknown"

def get_icao_code(location_name):
    """Retrieve ICAO airport code for the given city"""
    icao_code_mapping = {
        "Hyderabad": "VOHS",
        "Mumbai": "VABB",
        "Delhi": "VIDP",
        "Bangalore": "VOBL",
        "Chennai": "VOMM"
    }
    return icao_code_mapping.get(location_name, "Unknown ICAO")

def generate_weather_links(latitude, longitude, location_name, country):
    """Generate Weather Underground and Windy map URLs"""
    country_code = country[:2].lower()  # Extract first two letters of country code
    icao_code = get_icao_code(location_name)

    weather_report_url = f"https://www.wunderground.com/hourly/{country_code}/{location_name.lower()}/{icao_code}"
    windy_map_url = f"https://www.windy.com/-Radar+-radarPlus?radarPlus,{latitude},{longitude},5"

    return weather_report_url, windy_map_url

def open_weather_report():
    webbrowser.open(weather_report_url)

def open_windy_map():
    webbrowser.open(windy_map_url)

def main():
    global weather_report_url, windy_map_url
    
    # Step 1: Get device location
    latitude, longitude = get_device_location()
    
    # Step 2: Retrieve location details
    location_name, country, pincode = get_location_details(latitude, longitude)
    
    # Step 3: Generate Weather URLs
    weather_report_url, windy_map_url = generate_weather_links(latitude, longitude, location_name, country)
    
    root = tk.Tk()
    root.title("Weather Information")
    root.geometry("500x550")
    
    # Load and set background image
    bg_image = Image.open("C:\\Users\\Laxman\\Desktop\\chatbot\\chatbotbg123.jpg")
    bg_image = bg_image.resize((500, 550), Image.Resampling.LANCZOS)  # Resize to fit window
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Set to cover the entire window
    
    # Header
    Label(root, text="🌍 Weather Information", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

    # Location Details
    Label(root, text=f"📍 Latitude  : {latitude}", font=("Arial", 12), bg="#34495e", fg="white").pack(fill="x")
    Label(root, text=f"📍 Longitude : {longitude}", font=("Arial", 12), bg="#2c3e50", fg="white").pack(fill="x")
    Label(root, text=f" 🏙️ City       : {location_name}", font=("Arial", 12, "bold"), bg="#34495e", fg="lightgreen").pack(fill="x")
    Label(root, text=f"🌎 Country   : {country}", font=("Arial", 12), bg="#2c3e50", fg="white").pack(fill="x")
    Label(root, text=f"📮 Pincode   : {pincode}", font=("Arial", 12), bg="#34495e", fg="white").pack(fill="x")
    
    # Buttons with hover effect
    def on_enter(e, btn):
        btn.config(bg="#f1c40f", fg="black")

    def on_leave(e, btn):
        btn.config(bg="#e67e22", fg="white")
    
    btn1 = Button(root, text="📊 Open Weather Report", command=open_weather_report, font=("Arial", 14, "bold"), 
                  bg="#e67e22", fg="white", relief="raised")
    btn1.pack(pady=10, ipadx=10, ipady=5)
    
    btn2 = Button(root, text="🌪️ Open Windy Map", command=open_windy_map, font=("Arial", 14, "bold"), 
                  bg="#e67e22", fg="white", relief="raised")
    btn2.pack(pady=5, ipadx=10, ipady=5)
    
    # Add hover effect
    btn1.bind("<Enter>", lambda e: on_enter(e, btn1))
    btn1.bind("<Leave>", lambda e: on_leave(e, btn1))
    btn2.bind("<Enter>", lambda e: on_enter(e, btn2))
    btn2.bind("<Leave>", lambda e: on_leave(e, btn2))
    
    root.mainloop()

main()
