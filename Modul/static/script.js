//   API
async function fetchWeather() {
    try {
        const response = await fetch('/api/weather');
        const data = await response.json();
        console.log("Data cuaca diterima:", data);

        if (data.error) {
            throw new Error(data.error);
        }

        // Tentukan ikon cuaca berdasarkan deskripsi
        let weatherIconClass = "bi bi-question-circle"; // Default
        if (data.description.includes("clear")) {
            weatherIconClass = "bi bi-sun";
        } else if (data.description.includes("cloud")) {
            weatherIconClass = "bi bi-cloud-fill";
        } else if (data.description.includes("rain")) {
            weatherIconClass = "bi bi-cloud-rain";
        } else if (data.description.includes("thunderstorm")) {
            weatherIconClass = "bi bi-cloud-lightning-rain";
        } else if (data.description.includes("snow")) {
            weatherIconClass = "bi bi-snow";
        }

        // Perbarui elemen HTML
        document.getElementById('city').textContent = data.city;
        document.getElementById('weather-desc').textContent = data.description;
        document.getElementById('temperature').textContent = data.temperature;
        document.getElementById('wind-speed').textContent = data.wind_speed;
        document.getElementById('weather-icon').className = weatherIconClass;

    } catch (error) {
        console.error('Gagal mengambil data cuaca:', error);
        document.getElementById('weather-info').innerHTML = `<i class="bi bi-exclamation-triangle"></i> Cuaca tidak tersedia`;
    }
}

// Panggil saat halaman dimuat
fetchWeather();

var detik = 10; // Masukkan detik yang di ingin kan
var refresh_time = detik * 1000; // Konversi ke milidetik

setInterval(fetchWeather, refresh_time); // Perbarui setiap detik yang di setting



// LOCAL
function fetchSensorData() {
    fetch('/sensor/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById("temp").textContent = data.temp;
            document.getElementById("humidity").textContent = data.humidity;
            document.getElementById("air_pressure").textContent = data.air_pressure;
            document.getElementById("altitude").textContent = data.altitude;

            document.getElementById("temp2").textContent = data.temp;
            document.getElementById("humidity2").textContent = data.humidity;
            document.getElementById("air_pressure2").textContent = data.air_pressure;
            document.getElementById("altitude2").textContent = data.altitude;
        })
        .catch(error => console.error('Error fetching sensor data:', error));
}

// Perbarui setiap 5 detik
setInterval(fetchSensorData, 5000);

// Ambil data pertama kali saat halaman dimuat
fetchSensorData();


