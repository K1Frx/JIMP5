import tkinter as tk
import requests

API_KEY = "pC297hbGFOudjkPGQk7npPnkbbx9Cvph"

def get_current_weather(city, result_label):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": API_KEY,
        "q": city,
        "language": "pl-PL"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        location_key = data[0]["Key"]
        
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        params = {
            "apikey": API_KEY,
            "language": "pl-PL"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        temperature = data[0]["Temperature"]["Metric"]["Value"]
        weather_text = data[0]["WeatherText"]
        
        result_label.config(text=f"Pogoda w {city}: {temperature}°C, {weather_text}")
    except Exception as e:
        result_label.config(text="Błąd podczas pobierania danych pogodowych")

def get_forecast_12hours(city, result_label):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": API_KEY,
        "q": city,
        "language": "pl-PL"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        location_key = data[0]["Key"]
        
        url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}"
        params = {
            "apikey": API_KEY,
            "language": "pl-PL"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        text = ""
        for forecast in data:
            celcius = (forecast["Temperature"]["Value"] - 32) * 5/9
            temperature = celcius
            rain_probability = forecast["PrecipitationProbability"]
            time = forecast["DateTime"].split("T")[1].split("-")[0]
            weather_text = forecast["IconPhrase"]
            text += f"Pogoda w {city} o {time} {temperature}°C, szansa na opady {rain_probability}%, {weather_text}\n"
            
        result_label.config(text=text)
    except Exception as e:
        result_label.config(text="Błąd podczas pobierania danych pogodowych")
def get_forecast_5days(city, result_label):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": API_KEY,
        "q": city,
        "language": "pl-PL"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        location_key = data[0]["Key"]
        
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}"
        params = {
            "apikey": API_KEY,
            "language": "pl-PL"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        forecast = data["DailyForecasts"][0]["Day"]["IconPhrase"]
        result = ""
        for i,forecast in enumerate(data["DailyForecasts"]):
            forecast_spec = forecast["Day"]["IconPhrase"]
            result += f"Prognoza pogody za {i} dni w {city}: {forecast_spec}\n"
        
        result_label.config(text=result)
    except Exception as e:
        result_label.config(text="Błąd podczas pobierania danych pogodowych")

def get_weather_alarm_1day(city, result_label):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": API_KEY,
        "q": city,
        "language": "pl-PL"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        location_key = data[0]["Key"]
        
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
        params = {
            "apikey": API_KEY,
            "language": "pl-PL"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        forecast_day = data["DailyForecasts"][0]["Day"]["IconPhrase"]
        forecast_night = data["DailyForecasts"][0]["Night"]["IconPhrase"]
        
        result_label.config(text=f"Prognoza pogody na jutro w {city} \n Za dnia: {forecast_day} \n Wieczorem: {forecast_night}")
    except Exception as e:
        result_label.config(text="Błąd podczas pobierania danych pogodowych")
        

root = tk.Tk()
root.title("Aplikacja Pogodowa")

instruction_label = tk.Label(root, text="Podaj miasto:")
instruction_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Pobierz aktualną pogodę", command=lambda: get_current_weather(city_entry.get(), result_label))
get_weather_button.pack()

get_forecast_12hours_button = tk.Button(root, text="Pobierz prognozę pogody (12 godzin)", command=lambda: get_forecast_12hours(city_entry.get(), result_label))
get_forecast_12hours_button.pack()

get_forecast_5days_button = tk.Button(root, text="Pobierz prognozę pogody (5 dni)", command=lambda: get_forecast_5days(city_entry.get(), result_label))
get_forecast_5days_button.pack()

get_weather_alarm_1day_button = tk.Button(root, text="Pobierz prognozę pogody na jutro", command=lambda: get_weather_alarm_1day(city_entry.get(), result_label))
get_weather_alarm_1day_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
