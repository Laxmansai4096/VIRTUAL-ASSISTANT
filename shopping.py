import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
import webbrowser

# Updated product database with dummy data
products_db = {
    # Food Items
    "Burger": {
        "Zomato": (149, "https://www.zomato.com/hyderabad/delivery/dish-burger"),
        "Swiggy": (139, "https://www.swiggy.com/search?query=burger"),
    },
    "Pizza": {
        "Swiggy": (299, "https://www.swiggy.com/search?query=pizza"),
        "Zomato": (289, "https://www.zomato.com/hyderabad/delivery/dish-pizza"),
    },
    "Biryani": {
        "Zomato": (349, "https://www.zomato.com/hyderabad/delivery/dish-biryani"),
        "Swiggy": (329, "https://www.swiggy.com/search?query=biryani"),
    },
    "Noodles": {
        "Swiggy": (179, "https://www.swiggy.com/search?query=noodles"),
        "Zomato": (169, "https://www.zomato.com/hyderabad/delivery/dish-noodles"),
    },
    "Pasta": {
        "Swiggy": (199, "https://www.swiggy.com/search?query=pasta"),
        "Zomato": (189, "https://www.zomato.com/hyderabad/delivery/dish-pasta"),
    },

    # Snacks
    "Chips": {
        "Swiggy Instamart": (60, "https://www.swiggy.com/instamart/search?query=chips"),
        "Zepto": (55, "https://www.zeptonow.com/search?query=chips"),
    },
    "Chocolate": {
        "Swiggy Instamart": (99, "https://www.swiggy.com/instamart/search?query=chocolate"),
        "Zepto": (95, "https://www.zeptonow.com/search?query=chocolate"),
    },
    "Biscuit": {
        "Swiggy Instamart": (40, "https://www.swiggy.com/instamart/search?query=biscuit"),
        "Zepto": (35, "https://www.zeptonow.com/search?query=biscuit"),
    },
    "Popcorn": {
        "Swiggy Instamart": (50, "https://www.swiggy.com/instamart/search?query=popcorn"),
        "Zepto": (45, "https://www.zeptonow.com/search?query=popcorn"),
    },
    "Candy": {
        "Swiggy Instamart": (30, "https://www.swiggy.com/instamart/search?query=candy"),
        "Zepto": (25, "https://www.zeptonow.com/search?query=candy"),
    },

    # Accessories
    "Watches": {
        "Amazon": (2999, "https://www.amazon.in/s?k=watches"),
        "Flipkart": (2799, "https://www.flipkart.com/search?q=watches"),
        "Meesho": (2599, "https://www.meesho.com/search?q=watches"),
    },
    "Shoes": {
        "Amazon": (2499, "https://www.amazon.in/s?k=shoes"),
        "Flipkart": (2299, "https://www.flipkart.com/search?q=shoes"),
        "Meesho": (2199, "https://www.meesho.com/search?q=shoes"),
    },
    "Backpacks": {
        "Amazon": (1999, "https://www.amazon.in/s?k=backpacks"),
        "Flipkart": (1899, "https://www.flipkart.com/search?q=backpacks"),
        "Meesho": (1799, "https://www.meesho.com/search?q=backpacks"),
    },
    "Sunglasses": {
        "Amazon": (999, "https://www.amazon.in/s?k=sunglasses"),
        "Flipkart": (899, "https://www.flipkart.com/search?q=sunglasses"),
        "Meesho": (799, "https://www.meesho.com/search?q=sunglasses"),
    },
    "Headphones": {
        "Amazon": (1999, "https://www.amazon.in/s?k=headphones"),
        "Flipkart": (1799, "https://www.flipkart.com/search?q=headphones"),
        "Meesho": (1599, "https://www.meesho.com/search?q=headphones"),
    },
}

# Function to compare product prices
def compare_prices():
    query = entry.get().strip().title()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a product name!")
        return
    
    for widget in results_frame.winfo_children():
        widget.destroy()
    
    results_text.config(state=tk.NORMAL)
    results_text.delete("1.0", tk.END)
    
    if query in products_db:
        platforms = products_db[query]
        best_platform = min(platforms, key=lambda x: platforms[x][0])
        best_price = platforms[best_platform][0]
        for platform, (price, link) in platforms.items():
            price_info = f"{platform}: ₹{price}"
            if price == best_price:
                price_info += " ✅ (Best Price)"
            results_text.insert(tk.END, price_info + "\n")
            buy_button = tk.Button(results_frame, text=f"Buy on {platform}", command=lambda l=link: open_link(l), bg="#FFA500", fg="white", width=12, height=1)
            buy_button.pack(pady=4)
    else:
        results_text.insert(tk.END, "❌ Product not found. Try another item.")
    
    results_text.config(state=tk.DISABLED)

# Function to open product links
def open_link(url):
    webbrowser.open(url)
def set_background(root, image_path):
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((500, 500), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo  # Keep reference
    return bg_label

# Create GUI window
root = tk.Tk()
root.title("Shopping Assistant")
root.geometry("500x550")
# Set background image
set_background(root, "C:\\Users\\Laxman\\Desktop\\chatbot\\chatbotbg123.jpg")

# Title Label
title_label = tk.Label(root, text="🛒 Smart Shopping Assistant", font=("Arial", 14, "bold"))
title_label.pack(pady=6)

# Entry Field
entry_label = tk.Label(root, text="Enter Product Name:", font=("Arial", 12))
entry_label.pack(pady=4)
entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=2)

# Search Button
search_button = tk.Button(root, text="🔍 Compare Prices", command=compare_prices, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20, height=1)
search_button.pack(pady=6)

# Results Text Box
results_text = tk.Text(root, height=10, width=50, font=("Arial", 9), state=tk.DISABLED)
results_text.pack(pady=8)

# Results Frame for Buy Buttons
results_frame = tk.Frame(root)
results_frame.pack()

# Quick Links Section
# Quick Links Section
platforms_label = tk.Label(root, text="Quick Links:", font=("Arial", 10, "bold"))
platforms_label.pack(pady=6)

# Quick Links Frames
quick_links_frame1 = tk.Frame(root)
quick_links_frame1.pack()
quick_links_frame2 = tk.Frame(root)
quick_links_frame2.pack()
exit_frame = tk.Frame(root)
exit_frame.pack(pady=8)

# Quick Links Row 1 - Bright Colors
for platform, color in [("Amazon", "#FF5733"), ("Flipkart", "#FFBD33"), ("Meesho", "#FF33A8")]:
    tk.Button(quick_links_frame1, text=platform, command=lambda p=platform: open_link(products_db[platform][1]), bg=color, fg="white", width=12, height=1).pack(side="left", padx=4, pady=4)

# Quick Links Row 2 - Light Colors
for platform, color in [("Swiggy", "#AED6F1"), ("Zomato", "#A3E4D7"), ("Zepto", "#FAD7A0")]:
    tk.Button(quick_links_frame2, text=platform, command=lambda p=platform: open_link(products_db[platform][1]), bg=color, fg="black", width=12, height=1).pack(side="left", padx=4, pady=4)

# Spacer to move exit button further down
tk.Label(root, text="", height=4).pack()

# Exit Button centered below Quick Links
exit_btn = tk.Button(exit_frame, text="❌ Exit", bg="#6c757d", fg="white", command=root.destroy, width=12, height=1)
exit_btn.pack()
# Run the GUI
root.mainloop()
