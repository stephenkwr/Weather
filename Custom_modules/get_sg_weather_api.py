import httpx
import datetime

url = "https://api-open.data.gov.sg/v2/real-time/api"
weather_2h = "two-hr-forecast"
weather_24h = "twenty-four-hr-forecast"
weather_96h = "four-day-outlook"
relative_humidity = "relative-humidity"
air_temperature = "air-temperature"
weather_area = "Bukit Merah"
station_name = "Scotts Road"

# Functions to get weather data from Singapore's weather API

def get_2hr_forecast():
    response = httpx.get(f"{url}/{weather_2h}")
    response.raise_for_status()
    return response.json()

def get_24hr_forecast():
    response = httpx.get(f"{url}/{weather_24h}")
    response.raise_for_status()
    return response.json()

def get_4day_outlook():
    response = httpx.get(f"{url}/{weather_96h}")
    response.raise_for_status()
    return response.json()

def get_air_temperature():
    response = httpx.get(f"{url}/{air_temperature}")
    response.raise_for_status()
    return response.json()

def get_relative_humidity():
    response = httpx.get(f"{url}/{relative_humidity}")
    response.raise_for_status()
    return response.json()


def extract_station_id(station_json : dict, station_name : str):
    stations = station_json["data"]["stations"]
    id = None
    for station in stations:
        if station["name"] == station_name:
            id = station["id"]
            break
        
    if id is None:
        return "Station not found"
    return id

def extract_air_temperature_for_station(air_temp_json : dict, station_name : str):
    id = extract_station_id(air_temp_json, station_name)
    if id is None:
        return "Station not found"
    readings = air_temp_json["data"]["readings"][0]["data"]
    
    if readings is None:
        return "No air temperature readings found"
    temperature = None
    for reading in readings:
        if reading["stationId"] == id:
            temperature = reading["value"]
            break
        
    if temperature is None:
        return "Temperature reading not found"
    return (f"  {station_name} air temperature: {temperature}°C")

def extract_humidity_for_station(humidity_json : dict, station_name : str):
    id = extract_station_id(humidity_json, station_name)
    if id is None:
        return "Station not found"
    readings = humidity_json["data"]["readings"][0]["data"]
    
    if readings is None:
        return "No readings found"
    humidity = None
    for reading in readings:
        if reading["stationId"] == id:
            humidity = reading["value"]
            break
        
    if humidity is None:
        return "Humidity reading not found"
    return (f"  {station_name} relative humidity: {humidity}%")


def extract_forecast_2h(data, weather_area, station_name):
    output = []
    output.append(f"2-Hour Weather Forecast {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    forecasts = data["data"]["items"][0]["forecasts"]
    if forecasts is None:
        return "No forecasts found"
    for forecast in forecasts:
        if forecast["area"] == weather_area:
            output.append(f"    {weather_area} forcast: {forecast['forecast']}")
            
    relative_humidity_json = get_relative_humidity()
    output.append(extract_humidity_for_station(relative_humidity_json, station_name))
    air_temperature_json = get_air_temperature()
    output.append(extract_air_temperature_for_station(air_temperature_json, station_name))
    return output
    
    
def extract_forecast_24h(data):
    output = []
    records = data["data"]["records"][0]
    general = records["general"]
    temperature = general["temperature"]
    output.append(f"Temperature - Low: {temperature['low']}°C, High: {temperature['high']}°C")
    output.append(f"Relative Humidity - Low: {general['relativeHumidity']['low']}%, High: {general['relativeHumidity']['high']}%")
    output.append(f"Forecast: {general['forecast']["text"]} ")
    output.append(  f"Wind - Direction: {general['wind']['direction']}, "
                    f"Lowest speed: {general['wind']['speed']['low']}km/h, " 
                    f"Highest speed: {general['wind']['speed']['high']}km/h\n")
                    
    
    periods = records["periods"]
    for period in periods:
        output.append(f"************Valid from {period['timePeriod']['text']}************")
        regions = period["regions"]
        for area, info in regions.items():
            output.append(f"{area}: {info["text"]}")
            
    return output

def extract_forecast_4day(data):
    output = []
    forecasts = data["data"]["records"][0]["forecasts"]
    for forecast in forecasts:
        output.append(f"************************************************")
        output.append(f"Day: {forecast['day']}")
        output.append(f"Time stamp: {forecast['timestamp']} (YYYY-MM-DD HH:MM:SS)")
        output.append(f"Forecast: {forecast['forecast']['summary']}")
        output.append(f"Temperature - Low: {forecast['temperature']['low']}°C, High: {forecast['temperature']['high']}°C")
        output.append(f"Relative Humidity - Low: {forecast['relativeHumidity']['low']}%, High: {forecast['relativeHumidity']['high']}%")
        output.append(  f"Wind - Direction: {forecast['wind']['direction']}, "
                        f"Lowest speed: {forecast['wind']['speed']['low']}km/h, "
                        f"Highest speed: {forecast['wind']['speed']['high']}km/h")
        output.append("")
    return output
    
def main():
    data = get_2hr_forecast()
    extract_forecast_2h(data, weather_area, station_name)
    
    data = get_24hr_forecast()
    output = extract_forecast_24h(data)
    
    data = get_4day_outlook()
    output = extract_forecast_4day(data)
      
if __name__ == "__main__":
    main()