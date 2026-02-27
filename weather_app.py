from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"
SECURITY_TOKEN = "YOUR_TOKEN"

def fetch_weather_data(location, date):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?unitGroup=metric&key={API_KEY}&contentType=json"
    
    response = requests.get(url)
    data = response.json()

    day = data["days"][0]

    return {
        "temp_c": day["temp"],
        "wind_kph": day["windspeed"],
        "pressure_mb": day["pressure"],
        "humidity": day["humidity"]
    }

@app.route("/weather", methods=["POST"])
def weather_api():
    data = request.json

    if data.get("token") != SECURITY_TOKEN:
        return jsonify({"error": "Invalid token"}), 403

    location = data.get("location")
    date = data.get("date")
    requester = data.get("requester_name")

    weather = fetch_weather_data(location, date)

    result = {
        "requester_name": requester,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": location,
        "date": date,
        "weather": weather
    }

    return jsonify(result)

@app.route("/")
def home():
    return "<h2>Weather API is running</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
