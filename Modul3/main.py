import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from microdot import Microdot, Response, send_file
import requests
import random

app = Microdot()
Response.default_content_type = 'application/json'

# API Cuaca (Gantilah API_KEY dengan API dari OpenWeatherMap)
API_KEY = "3f5c97ba51c98cb66a97c7fd54f105fa"
CITY = "Malang"
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

@app.route('/sensor/data')
def get_sensor_data(request):
    data = {
        "temp": round(random.uniform(20, 35), 1),  # Suhu dalam °C
        "humidity": round(random.uniform(40, 90), 1),  # Kelembaban dalam %
        "air_pressure": round(random.uniform(980, 1050), 1),  # Tekanan dalam hPa
        "altitude": round(random.uniform(0, 500), 1),  # Ketinggian dalam meter

        "temp2": round(random.uniform(20, 35), 1),  # Suhu dalam °C
        "humidity2": round(random.uniform(40, 90), 1),  # Kelembaban dalam %
        "air_pressure2": round(random.uniform(980, 1050), 1),  # Tekanan dalam hPa
        "altitude2": round(random.uniform(0, 500), 1)  # Ketinggian dalam meter
    }
    return data

@app.route('/')
def index(request):
    return send_file('templates/index.html')

@app.route('/static/<path:path>')
def static_files(request, path):
    return send_file('static/' + path)

@app.route('/api/weather')
def get_weather(request):
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()

        # Ambil parameter yang diperlukan
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
        return weather_data

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/sensor/temperature')
def get_temperature(request):
    temperature = round(random.uniform(20, 35), 1)  # Random suhu antara 20°C - 35°C
    return {"temperature": temperature}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
