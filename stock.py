import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import threading
import time
from datetime import datetime
import webbrowser

# Main Window
root = tk.Tk()
root.title("Stock Market Assistant")
root.geometry("800x750")
root.configure(bg="#222222")

dark_mode = True

# Toggle Theme
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#222222" if dark_mode else "#f0f0f0"
    fg_color = "white" if dark_mode else "black"
    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        try:
            widget.configure(bg=bg_color, fg=fg_color)
        except:
            pass

# Date and Time Display
date_time_label = tk.Label(root, text=datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S"),
                           font=("Arial", 16, "bold"), fg="white", bg="#222222")
date_time_label.pack(pady=5)

def update_time():
    while True:
        date_time_label.config(text=datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S"))
        time.sleep(1)

threading.Thread(target=update_time, daemon=True).start()

# AI Stock Recommendation
recommendations_frame = tk.Frame(root, bg="#222222")
recommendations_frame.pack(pady=10)

def ai_stock_recommendation():
    recommendations = []
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "AMD", "ORCL", "IBM", "JPM", "BAC", "GS", "V", "MA", "JNJ", "PFE", "UNH", "XOM", "CVX", "BA", "WMT", "KO", "PG", "NKE"]
    for stock in stocks:
        recent_trend = np.random.choice(["Bullish", "Bearish", "Neutral"])
        news_sentiment = np.random.choice(["Positive", "Negative", "Neutral"])
        if recent_trend == "Bullish" and news_sentiment == "Positive":
            action, color = "BUY", "green"
        elif recent_trend == "Bearish" and news_sentiment == "Negative":
            action, color = "SELL", "red"
        else:
            action, color = "HOLD", "blue"
        recommendations.append((f"{stock}: {action} (Trend: {recent_trend}, News: {news_sentiment})", color))
    return recommendations

def update_ai_recommendations():
    recommendations = ai_stock_recommendation()
    for widget in recommendations_frame.winfo_children():
        widget.destroy()
    
    cols = 2
    for i, (rec, color) in enumerate(recommendations):
        label = tk.Label(recommendations_frame, text=rec, fg=color, bg="#222222", font=("Arial", 12))
        label.grid(row=i // cols, column=i % cols, sticky="w", padx=10, pady=2)

threading.Thread(target=lambda: (update_ai_recommendations(), time.sleep(60)), daemon=True).start()
update_ai_recommendations()

# Stock Search and Analysis
frame_top = tk.Frame(root, bg="#222222")
frame_top.pack(pady=10)

stock_entry = tk.Entry(frame_top, width=20)
stock_entry.pack(side=tk.LEFT, padx=5)

time_range = tk.StringVar(value="1mo")
time_options = [("1 Month", "1mo"), ("6 Months", "6mo"), ("1 Year", "1y")]
for text, value in time_options:
    tk.Radiobutton(frame_top, text=text, variable=time_range, value=value, bg="#222222", fg="white").pack(side=tk.LEFT, padx=5)

fetch_button = tk.Button(frame_top, text="Fetch Stock", command=lambda: threading.Thread(target=fetch_stock_data).start())
fetch_button.pack(side=tk.LEFT, padx=5)

price_label = tk.Label(root, text="Current Price: N/A", font=("Arial", 12))
price_label.pack()

def fetch_stock_data():
    stock_symbol = stock_entry.get().upper()
    if not stock_symbol:
        return
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1d")
        price = data["Close"].iloc[-1]
        price_label.config(text=f"Current Price: ${price:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch data: {e}")

# Graphs & AI Prediction
def plot_stock_graph():
    stock_symbol = stock_entry.get().upper()
    if not stock_symbol:
        messagebox.showerror("Error", "Please enter a stock symbol")
        return

    period = time_range.get()
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period=period)
    graph_frame = tk.Frame(root, bg="#222222")
    graph_frame.pack(pady=10)

    if data.empty:
        messagebox.showerror("Error", "No data available for selected period")
        return

    data['SMA'] = data['Close'].rolling(window=10).mean()

    # Create a new figure for the graph
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]})

    # Ensure previous canvas is removed before plotting new one
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Plot Candlestick Chart
    mpf.plot(data, type='candle', style='charles', ax=ax1, volume=ax2)
    ax1.set_title(f"Candlestick Chart for {stock_symbol} ({period})")

    # Embed Matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()



def ai_prediction():
    stock_symbol = stock_entry.get().upper()
    if not stock_symbol:
        return
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1mo")
    if len(data) < 10:
        messagebox.showerror("Error", "Not enough data for AI prediction")
        return
    days = np.arange(len(data)).reshape(-1, 1)
    prices = data["Close"].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(days, prices)
    future_days = np.arange(len(data) + 5).reshape(-1, 1)
    future_prices = model.predict(future_days)
    plt.figure(figsize=(8, 5))
    plt.plot(days, prices, marker="o", linestyle="-", label="Historical Prices")
    plt.plot(future_days, future_prices, linestyle="--", color="orange", label="AI Prediction")
    plt.xlabel("Days")
    plt.ylabel("Stock Price")
    plt.title(f"AI Predicted Trend for {stock_symbol}")
    plt.legend()
    plt.show()

def open_link(url):
    webbrowser.open(url)

links = [
    ("Yahoo Finance", "https://finance.yahoo.com"),
    ("Google Finance", "https://www.google.com/finance"),
    ("TradingView", "https://www.tradingview.com"),
    ("MarketWatch", "https://www.marketwatch.com"),
]

def update_stock_price():
    while True:
        fetch_stock_data()
        time.sleep(60)
threading.Thread(target=update_stock_price, daemon=True).start()

# Buttons
btn_frame = tk.Frame(root, bg="#222222")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Show Stock Graph", command=plot_stock_graph, bg="#3498db", fg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="AI Prediction", command=ai_prediction, bg="#e74c3c", fg="white").grid(row=0, column=1, padx=5, pady=5)

# Quick Links for Stock Market
quick_links_frame = tk.Frame(root, bg="#222222")
quick_links_frame.pack(pady=10)
for name, url in links:
    btn = tk.Button(quick_links_frame, text=name, command=lambda u=url: open_link(u), bg="#1abc9c", fg="white")
    btn.pack(side=tk.LEFT, padx=5, pady=5)
# Toggle Button at Bottom
toggle_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_theme, bg="#444", fg="white")
toggle_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
