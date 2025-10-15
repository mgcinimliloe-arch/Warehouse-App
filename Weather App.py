import requests
import datetime
import json
import os

CACHE_FILE = "weather_cache.json"
DEFAULT_LAT = 51.5074
DEFAULT_LON = -0.1278


class WeatherForecast:
    """Handles reading, writing, and accessing weather forecasts."""

    def __init__(self, cache_file=CACHE_FILE):
        self.cache_file = cache_file
        self._data = self._load_cache()

    # --- File handling -----------------------------------------------------
    def _load_cache(self):
        """Load previously saved weather data from file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_cache(self):
        """Save current weather data to file."""
        with open(self.cache_file, "w") as f:
            json.dump(self._data, f, indent=4)

    # --- Dunder methods ----------------------------------------------------
    def __setitem__(self, date, weather_value):
        """Allows setting a forecast using [] notation."""
        self._data[date] = weather_value
        self._save_cache()

    def __getitem__(self, date):
        """Allows getting a forecast using [] notation."""
        if date not in self._data:
            raise KeyError(f"No forecast found for {date}")
        return self._data[date]

    def __iter__(self):
        """Allows iterating over known dates."""
        return iter(self._data.keys())

    def items(self):
        """Generator yielding (date, weather_value) tuples."""
        for date, value in self._data.items():
            yield (date, value)

    # --- Weather API -------------------------------------------------------
    def fetch_weather(self, date, lat=DEFAULT_LAT, lon=DEFAULT_LON):
        """Fetch precipitation data from Open-Meteo API."""
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
            precipitation = data.get("daily", {}).get("precipitation_sum", [None])[0]
            return precipitation
        except requests.RequestException as e:
            print("Error fetching weather data:", e)
            return None


# --------------------------------------------------------------------------
# Main program
# --------------------------------------------------------------------------
def main():
    print("=== Weather Forecast (OOP Version) ===")
    weather_forecast = WeatherForecast()

    user_input = input("Enter a date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()
    if not user_input:
        date_to_check = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        try:
            datetime.datetime.strptime(user_input, "%Y-%m-%d")
            date_to_check = user_input
        except ValueError:
            print("Invalid date format. Use YYYY-mm-dd.")
            return

    use_custom = input("Do you want to enter custom coordinates? (y/n): ").strip().lower()
    if use_custom == "y":
        try:
            lat = float(input("Latitude: "))
            lon = float(input("Longitude: "))
        except ValueError:
            print("Invalid coordinates. Using default (London).")
            lat, lon = DEFAULT_LAT, DEFAULT_LON
    else:
        lat, lon = DEFAULT_LAT, DEFAULT_LON

    # --- Check cache or API ---
    if date_to_check in weather_forecast._data:
        precipitation = weather_forecast[date_to_check]
        print(f"Loaded from cache for {date_to_check}")
    else:
        precipitation = weather_forecast.fetch_weather(date_to_check, lat, lon)
        weather_forecast[date_to_check] = precipitation

    # --- Interpret result ---
    if precipitation is None or precipitation < 0:
        print(f"{date_to_check}: I don't know.")
    elif precipitation == 0.0:
        print(f"{date_to_check}: It will not rain.")
    else:
        print(f"{date_to_check}: It will rain ({precipitation} mm).")

    # --- Example usage of iteration and items() ---
    print("\nSaved forecasts so far:")
    for date, value in weather_forecast.items():
        print(f"{date} -> {value}")


if __name__ == "__main__":
    main()
