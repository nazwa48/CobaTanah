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

#API Flask
FLASK_API_URL = "http://192.168.58.113:5002/api/bengkel"  # Sesuaikan dengan URL Flask kamu

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

#CHECK API DARI FLASK
@app.route('/api/inventory')
def get_inventory(request):
    try:
        response = requests.get(FLASK_API_URL)  # Mengambil data dari API Flask
        data = response.json()  # Ubah ke format JSON
        response.close()  # Tutup request

        print("\n📦 Data dari Flask API:")
        for item in data:
            print(f"ID: {item['id']}, Kode: {item['kode_barang']}, Nama: {item['nama']}, Jumlah: {item['jumlah']}, Kondisi: {item['kondisi']}")

        return data  # Mengembalikan data supaya bisa diakses di Microdot

    except Exception as e:
        print("❌ Error mengambil data:", e)
        return {"error": str(e)}, 500

#TAMPILKAN API dari FLASK
@app.route('/api/inventory')
def get_inventory(request):
    try:
        response = requests.get(FLASK_API_URL)  # Ambil dari Flask
        data = response.json()  # Ubah ke JSON
        response.close()  # Tutup request
        return data  # Kirim ke frontend

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
