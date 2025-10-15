import requests
import datetime
import json
import os

# File to store previous results
CACHE_FILE = "weather_cache.json"

# Default location (London)
DEFAULT_LAT = 51.5074
DEFAULT_LON = -0.1278

def load_cache():
    """Read cached data if it exists."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_cache(cache):
    """Write cache data to the file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def get_weather(lat, lon, date):
    """Request precipitation data from Open-Meteo."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=precipitation_sum&timezone=Europe%2FLondon"
        f"&start_date={date}&end_date={date}"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("daily", {}).get("precipitation_sum", [None])[0]
    except Exception as e:
        print("Error while fetching data:", e)
        return None

def check_weather(date, lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """Check and display rain info for the given date."""
    cache = load_cache()

    # Use cached result if available
    if date in cache:
        precipitation = cache[date]
        print(f"Data loaded from cache for {date}")
    else:
        precipitation = get_weather(lat, lon, date)
        cache[date] = precipitation
        save_cache(cache)

    # Print appropriate message
    if precipitation is None or precipitation < 0:
        print(f"{date}: I don't know.")
    elif precipitation == 0.0:
        print(f"{date}: It will not rain.")
    else:
        print(f"{date}: It will rain ({precipitation} mm).")

def main():
    print("Weather Checker")
    user_input = input("Enter a date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()

    # If user leaves date empty, use tomorrow
    if not user_input:
        date_to_check = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        try:
            datetime.datetime.strptime(user_input, "%Y-%m-%d")
            date_to_check = user_input
        except ValueError:
            print("Invalid date format. Use YYYY-mm-dd.")
            return

    # Optional: custom location
    custom = input("Do you want to enter coordinates? (y/n): ").strip().lower()
    if custom == "y":
        try:
            lat = float(input("Latitude: ").strip())
            lon = float(input("Longitude: ").strip())
        except ValueError:
            print("Invalid coordinates. Using default location (London).")
            lat, lon = DEFAULT_LAT, DEFAULT_LON
    else:
        lat, lon = DEFAULT_LAT, DEFAULT_LON

    check_weather(date_to_check, lat, lon)

if __name__ == "__main__":
    main()
