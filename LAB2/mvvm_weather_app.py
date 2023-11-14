import tkinter as tk
import requests

API_KEY = "pC297hbGFOudjkPGQk7npPnkbbx9Cvph"

class WeatherModel:
    def __init__(self):
        self.data = ""

class WeatherViewModel:
    def __init__(self, model):
        self.model = model

    def get_current_weather(self, city):
        self.get_weather_data(city, "currentconditions")

    def get_forecast_12hours(self, city):
        self.get_weather_data(city, "forecasts/v1/hourly/12hour")

    def get_forecast_5days(self, city):
        self.get_weather_data(city, "forecasts/v1/daily/5day")

    def get_weather_alarm_1day(self, city):
        self.get_weather_data(city, "forecasts/v1/daily/1day")

    def get_weather_data(self, city, endpoint):
        url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
        params = {
            "apikey": API_KEY,
            "q": city,
            "language": "pl-PL"
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                self.model.data = "Wyczerpano limit zapytań do API"
                return
            data = response.json()
            location_key = data[0]["Key"]

            url = f"http://dataservice.accuweather.com/{endpoint}/{location_key}"
            params = {
                "apikey": API_KEY,
                "language": "pl-PL"
            }

            response = requests.get(url, params=params)
            data = response.json()
            self.process_weather_data(city, data, endpoint)
        except Exception as e:
            self.model.data = "Błąd podczas pobierania danych pogodowych"

    def process_weather_data(self, city, data, endpoint):
        text = ""
        if endpoint == 'forecasts/v1/hourly/12hour':
            for forecast in data:
                temperature = forecast.get("Temperature", {}).get("Metric", {}).get("Value", "")
                rain_probability = forecast.get("PrecipitationProbability", "")
                time = forecast.get("DateTime", "").split("T")[1].split("-")[0]
                weather_text = forecast.get("IconPhrase", "")
                text += f"Pogoda w {city} o {time} {temperature}°C, szansa na opady {rain_probability}%, {weather_text}\n"
        elif endpoint == 'forecasts/v1/daily/5day':
            for forecast in data.get("DailyForecasts", []):
                date = forecast.get("Date", "")
                temperature_min = forecast.get("Temperature", {}).get("Minimum", {}).get("Value", "")
                temperature_max = forecast.get("Temperature", {}).get("Maximum", {}).get("Value", "")
                icon_day = forecast.get("Day", {}).get("Icon", "")
                icon_night = forecast.get("Night", {}).get("Icon", "")
                icon_phrase_day = forecast.get("Day", {}).get("IconPhrase", "")
                icon_phrase_night = forecast.get("Night", {}).get("IconPhrase", "")
                text += f"Prognoza pogody za {date} w {city}: Minimalna temperatura: {temperature_min}°C, Maksymalna temperatura: {temperature_max}°C\n"
                text += f"Dzień: {icon_phrase_day}, Ikona: {icon_day}\n"
                text += f"Noc: {icon_phrase_night}, Ikona: {icon_night}\n\n"
        elif endpoint == 'forecasts/v1/daily/1day':
            daily_forecasts = data.get("DailyForecasts", [])
            if daily_forecasts:
                forecast = daily_forecasts[0]
                date = forecast.get("Date", "")
                temperature_min = forecast.get("Temperature", {}).get("Minimum", {}).get("Value", "")
                temperature_max = forecast.get("Temperature", {}).get("Maximum", {}).get("Value", "")
                icon_phrase_day = forecast.get("Day", {}).get("IconPhrase", "")
                icon_phrase_night = forecast.get("Night", {}).get("IconPhrase", "")
                text += f"Prognoza pogody {date} w {city}:\n"
                text += f"Minimalna temperatura: {temperature_min}°C, Maksymalna temperatura: {temperature_max}°C\n"
                text += f"Dzień: {icon_phrase_day}\n"
                text += f"Noc: {icon_phrase_night}\n\n"
        elif endpoint == 'currentconditions':
            observation = data[0]
            weather_text = observation.get("WeatherText", "")
            temperature_celsius = observation.get("Temperature", {}).get("Metric", {}).get("Value", "")
            temperature_fahrenheit = observation.get("Temperature", {}).get("Imperial", {}).get("Value", "")
            precipitation = observation.get("HasPrecipitation", "")
            precipitation_type = observation.get("PrecipitationType", "")
            
            text += f"Aktualna pogoda w {city}:\n"
            text += f"Warunki pogodowe: {weather_text}\n"
            text += f"Temperatura: {temperature_celsius}°C / {temperature_fahrenheit}°F\n"
            text += f"Czy występują opady: {precipitation}\n"
            if precipitation:
                text += f"Typ opadów: {precipitation_type}\n"
        else:
            text = "Nieobsługiwany rodzaj prognozy"
        
        self.model.data = text
        
        
class WeatherView(tk.Tk):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.instruction_label = tk.Label(self, text="Podaj miasto:")
        self.instruction_label.pack()

        self.city_entry = tk.Entry(self)
        self.city_entry.pack()

        self.get_weather_button = tk.Button(self, text="Pobierz aktualną pogodę", command=self.on_get_current_weather)
        self.get_weather_button.pack()

        self.get_forecast_12hours_button = tk.Button(self, text="Pobierz prognozę pogody (12 godzin)", command=self.on_get_forecast_12hours)
        self.get_forecast_12hours_button.pack()

        self.get_forecast_5days_button = tk.Button(self, text="Pobierz prognozę pogody (5 dni)", command=self.on_get_forecast_5days)
        self.get_forecast_5days_button.pack()

        self.get_weather_alarm_1day_button = tk.Button(self, text="Pobierz prognozę pogody na jutro", command=self.on_get_weather_alarm_1day)
        self.get_weather_alarm_1day_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def on_get_current_weather(self):
        self.view_model.get_current_weather(self.city_entry.get())
        self.update_view()

    def on_get_forecast_12hours(self):
        self.view_model.get_forecast_12hours(self.city_entry.get())
        self.update_view()

    def on_get_forecast_5days(self):
        self.view_model.get_forecast_5days(self.city_entry.get())
        self.update_view()

    def on_get_weather_alarm_1day(self):
        self.view_model.get_weather_alarm_1day(self.city_entry.get())
        self.update_view()

    def update_view(self):
        self.result_label.config(text=self.view_model.model.data)

if __name__ == "__main__":
    model = WeatherModel()
    view_model = WeatherViewModel(model)
    view = WeatherView(view_model)
    view.title("Aplikacja Pogodowa")
    view.mainloop()
