import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from microdot import Microdot, Response, send_file
import random
import json
import requests
import os

app = Microdot()
Response.default_content_type = 'application/json'

# API Cuaca (Gantilah API_KEY dengan API dari OpenWeatherMap)
API_KEY = "3f5c97ba51c98cb66a97c7fd54f105fa"
CITY = "Malang"
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Fungsi untuk mengambil data sensor
def generate_sensor_data():
    try:
        response = requests.get(WEATHER_URL)
        weather_data = response.json()

        if "main" not in weather_data:
            print("Error: API Cuaca Bermasalah!", weather_data)
            return {}

        data = {
            "soil_moisture": round(random.uniform(10, 90), 2),
            "ph_level": round(random.uniform(4, 9), 2),
            "rainfall": round(random.uniform(0, 50), 2),
            "wind_speed": round(random.uniform(0, 30), 2),
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"]
        }

        print("Data yang dikirim:", data)
        return data

    except Exception as e:
        print("Error mengambil data cuaca:", e)
        return {}



@app.route('/')
def index(request):
    return send_file('templates/index.html')

@app.route('/data')
def data(request):
    return Response(body=json.dumps(generate_sensor_data()), headers={'Content-Type': 'application/json'})

@app.route('/static/<path:path>')
def static_files(request, path):
    return send_file('static/' + path)

if __name__ == '__main__':
    app.run(host='127.0.0.2', port=5001, debug=True)
