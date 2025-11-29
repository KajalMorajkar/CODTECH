
"""
weather_data_plot.py
Fetches past 7 days of daily average temperature for Mumbai (India)
from the Open-Meteo API (no key required) and plots it.
"""

import requests
from datetime import date, timedelta
import matplotlib.pyplot as plt

def fetch_weather_data(lat, lon, start_date, end_date):
    """Fetch daily mean temperature data from Open-Meteo API."""
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&daily=temperature_2m_mean"
        "&timezone=auto"
    )

    print(f"Fetching weather data for {start_date} → {end_date} ...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Extract dates and temperatures
    dates = data["daily"]["time"]
    temps = data["daily"]["temperature_2m_mean"]

    return dates, temps

def plot_weather(dates, temps, city_name):
    """Plot temperature vs date."""
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker="o", color="tab:orange")
    plt.title(f"Average Daily Temperature – {city_name}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    city_name = "Mumbai"
    latitude = 19.0760
    longitude = 72.8777

    end = date.today()
    start = end - timedelta(days=7)

    start_str = start.isoformat()
    end_str = end.isoformat()

    dates, temps = fetch_weather_data(latitude, longitude, start_str, end_str)
    print("Received data points:", len(dates))

    plot_weather(dates, temps, city_name)

if __name__ == "__main__":
    main()
