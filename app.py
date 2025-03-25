from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "4b1e12bdb3d078c18a60d9f332dc7db1"  # Replace with your API key

def fetch_aqi_data(city):
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geocode_url).json()
    
    if not geo_response:
        return None, "City not found"
    
    lat, lon = geo_response[0]["lat"], geo_response[0]["lon"]
    
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(aqi_url).json()
    
    if "list" in response and len(response["list"]) > 0:
        aqi_value = response["list"][0]["main"]["aqi"]
        return aqi_value, None
    else:
        return None, "Error fetching AQI data"

def get_aqi_category(aqi):
    categories = {
        1: ("Good", "Air quality is satisfactory."),
        2: ("Fair", "Acceptable, but some pollutants may affect sensitive groups."),
        3: ("Moderate", "May cause discomfort for sensitive individuals."),
        4: ("Poor", "Health warnings for everyone."),
        5: ("Very Poor", "Emergency conditions, serious health effects."),
    }
    return categories.get(aqi, ("Unknown", "AQI data unavailable"))

@app.route("/", methods=["GET", "POST"])
def index():
    city = "Pune"  # Default city
    aqi, category, alert = None, None, None
    
    if request.method == "POST":
        city = request.form["city"]
        aqi, error = fetch_aqi_data(city)
        if error:
            return render_template("index.html", error=error)
        category, alert = get_aqi_category(aqi)
    
    return render_template("index.html", city=city, aqi=aqi, category=category, alert=alert)

if __name__ == "__main__":
    app.run(debug=True)
