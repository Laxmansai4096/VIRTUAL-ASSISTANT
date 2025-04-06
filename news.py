import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import feedparser
import time
from PIL import Image,ImageTk

# RSS Feeds for International & Indian News
news_sources = {
    "International": {
        "World": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
        "Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "Science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "Sports": "http://feeds.bbci.co.uk/sport/rss.xml",
    },
    "Indian": {
        "Top News": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "India": "https://www.thehindu.com/news/national/feeder/default.rss",
        "Business": "https://economictimes.indiatimes.com/rssfeeds/1977021501.cms",
        "Technology": "https://www.gadgets360.com/rss/news",
        "Sports": "https://www.espn.in/espn/rss/news",
        "Entertainment": "https://www.bollywoodhungama.com/rss/news.xml",
    }
}

# Function to fetch and display news
def fetch_news():
    category = category_var.get()
    region = region_var.get()

    if not category or not region:
        messagebox.showerror("Error", "Please select a region and category.")
        return

    rss_url = news_sources[region].get(category)
    if not rss_url:
        messagebox.showerror("Error", "Invalid Category Selected.")
        return

    # Fetch RSS Feed
    feed = feedparser.parse(rss_url)
    
    # Clear previous news
    news_display.config(state=tk.NORMAL)
    news_display.delete(1.0, tk.END)

    news_display.insert(tk.END, f"📰 {region} - {category} News\n" + "="*60 + "\n", "title")

    for index, entry in enumerate(feed.entries[:8], start=1):
        news_display.insert(tk.END, f"\n{index}. {entry.title}\n", "headline")
        news_display.insert(tk.END, f"   🔗 Read more: {entry.link}\n", "link")

    news_display.config(state=tk.DISABLED)

# Function to open e-paper link
def open_link(url):
    webbrowser.open(url)

# Function to toggle dark mode
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#2E2E2E" if dark_mode else "#F0F0F0"
    fg_color = "white" if dark_mode else "black"
    root.configure(bg=bg_color)
    time_label.configure(bg=bg_color, fg=fg_color)
    news_display.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    toggle_button.configure(bg="#666" if dark_mode else "#DDD", fg=fg_color)
    fetch_button.configure(bg="green" if not dark_mode else "darkgreen")

# Function to update time
def update_time():
    current_time = time.strftime("%A, %d %B %Y  |  %I:%M:%S %p")  # Day, Date, Time
    time_label.config(text=current_time)
    root.after(1000, update_time)  # Update every second
# Load and set background image
def set_background(image_path):
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((700, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference
    bg_label.place(relwidth=1, relheight=1)
# GUI Setup
root = tk.Tk()
root.title("News Reader - International & Indian News")
root.geometry("600x625")
set_background("C:\\Users\\Laxman\\Desktop\\chatbot\\newsbg.webp")

# Time Label (Replaces News Reader Title)
time_label = tk.Label(root, font=("Arial", 16, "bold"), fg="darkred")
time_label.pack(pady=10)
update_time()  # Start updating time

# Dropdown Frame (side-by-side)
dropdown_frame = tk.Frame(root)
dropdown_frame.pack(pady=5)

# Region Selection
region_var = tk.StringVar()
region_label = tk.Label(dropdown_frame, text="Region:", font=("Arial", 12, "bold"))
region_label.grid(row=0, column=0, padx=5)
region_dropdown = ttk.Combobox(dropdown_frame, textvariable=region_var, values=list(news_sources.keys()), state="readonly", font=("Arial", 10, "bold"))
region_dropdown.grid(row=0, column=1, padx=10)

# Category Selection
category_var = tk.StringVar()
category_label = tk.Label(dropdown_frame, text="Category:", font=("Arial", 12, "bold"))
category_label.grid(row=0, column=2, padx=5)
category_dropdown = ttk.Combobox(dropdown_frame, textvariable=category_var, state="readonly", font=("Arial", 10, "bold"))
category_dropdown.grid(row=0, column=3, padx=10)

# Update categories when region is selected
def update_categories(event):
    selected_region = region_var.get()
    if selected_region:
        category_dropdown["values"] = list(news_sources[selected_region].keys())
        category_dropdown.current(0)

region_dropdown.bind("<<ComboboxSelected>>", update_categories)

# Fetch News Button
fetch_button = tk.Button(root, text="Fetch News", font=("Arial", 12, "bold"), bg="green", fg="white", command=fetch_news)
fetch_button.pack(pady=4)

# Scrollable News Display (Increased Space)
news_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), height=18, width=80)
news_display.pack(pady=15)
news_display.tag_config("title", font=("Arial", 14, "bold"), foreground="blue")
news_display.tag_config("headline", font=("Arial", 12, "bold"), foreground="black")
news_display.tag_config("link", font=("Arial", 10, "italic"), foreground="blue")
news_display.config(state=tk.DISABLED)

# ePaper Links
epaper_frame = tk.Frame(root)
epaper_frame.pack(pady=10)

epapers = [
    ("Eenadu", "#FF5733", "https://epaper.eenadu.net"),
    ("Sakshi", "#33A1FF", "https://epaper.sakshi.com"),
    ("Andhra Jyothi", "#FFBD33", "https://epaper.andhrajyothy.com"),
    ("Namasthe Telangana", "#FF33A8", "https://epaper.ntnews.com"),
    ("The Hindu", "#4CAF50", "https://epaper.thehindu.com"),
    ("Deccan Chronicle", "#8E44AD", "https://epaper.deccanchronicle.com"),
    ("Business Standard", "#E74C3C", "https://epaper.business-standard.com")
]

for i in range(0, len(epapers), 4):
    row_frame = tk.Frame(epaper_frame)
    row_frame.pack()
    for name, color, link in epapers[i:i+4]:
        btn = tk.Button(row_frame, text=name, bg=color, fg="white", font=("Arial", 10), width=len(name)+2, command=lambda l=link: open_link(l))
        btn.pack(side="left", padx=5, pady=5)

# Theme Toggle Button
toggle_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_theme, font=("Arial", 8), bg="#DDD", fg="black")
toggle_button.pack(side="left", padx=120, pady=5)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 8, "bold"), bg="red", fg="white", width=10)
exit_button.pack(side="left", padx=100, pady=5)
root.mainloop()
