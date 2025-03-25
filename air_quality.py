import tkinter as tk
import requests

API_KEY = "4b1e12bdb3d078c18a60d9f332dc7db1"
LAT = 18.5204
LON = 73.8567
URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

def analyze_aqi(aqi):
    if aqi == 1:
        return ("Good", "Air quality is satisfactory.")
    elif aqi == 2:
        return ("Fair", "Air quality is acceptable; sensitive individuals take note.")
    elif aqi == 3:
        return ("Moderate", "Moderate air quality: Some health concern for sensitive individuals.")
    elif aqi == 4:
        return ("Poor", "Poor air quality: Health alert for everyone.")
    elif aqi == 5:
        return ("Very Poor", "Very poor air quality: Emergency conditions, everyone at risk.")
    else:
        return ("Unknown", "AQI value is not recognized.")

def fetch_data():
    try:
        response = requests.get(URL)
        data = response.json()
        if "list" in data:
            aqi = data["list"][0]["main"]["aqi"]
            category, message = analyze_aqi(aqi)
            return aqi, category, message
        else:
            return None, None, "Error fetching data"
    except Exception as e:
        return None, None, f"Error: {e}"

def update_gui():
    aqi, category, message = fetch_data()
    if aqi is not None:
        aqi_label.config(text=f"AQI: {aqi}")
        category_label.config(text=f"Category: {category}")
        message_label.config(text=f"Alert: {message}")
    else:
        aqi_label.config(text="AQI: N/A")
        category_label.config(text="Category: N/A")
        message_label.config(text=message)
    # Refresh every 10 minutes (600000 milliseconds)
    root.after(600000, update_gui)

# Set up the GUI window
root = tk.Tk()
root.title("Smart Air Quality Monitor")

# Create labels to display the data
city_label = tk.Label(root, text="City: Pune", font=("Helvetica", 16))
city_label.pack(pady=10)

aqi_label = tk.Label(root, text="AQI: Loading...", font=("Helvetica", 14))
aqi_label.pack(pady=5)

category_label = tk.Label(root, text="Category: Loading...", font=("Helvetica", 14))
category_label.pack(pady=5)

message_label = tk.Label(root, text="Alert: Loading...", font=("Helvetica", 12), wraplength=300)
message_label.pack(pady=10)

# Initial update of data
update_gui()

# Start the GUI loop
root.mainloop()
