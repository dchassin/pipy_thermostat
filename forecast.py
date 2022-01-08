import requests, json, datetime
from config import config
from debug import debug
from location import location

location_info = location()

class noaa:

    error = None
    raw = None
    name = None
    datetime = None
    daytime = None
    temperature = None
    temperature_unit = None
    temperature_trend = None
    wind_speed = None
    wind_direction = None
    forecast_short = None
    forecast_long = None
    image = None
    wind_speed = None
    wind_direction = None
    endtime = None

    def __init__(self,refresh=False):
        if not self.raw or self.endtime < datetime.datetime.now() or refresh:
            url = config.noaa_server.format(latitude=location_info.latitude(),longitude=location_info.longitude())
            headers = {'User-agent' : config.noaa_user_agent}
            location = json.loads(requests.get(url,headers=headers).content.decode("utf-8"))
            self.raw = json.loads(requests.get(location["properties"]["forecastHourly"],headers=headers).content.decode("utf-8"))
            debug(f"forecast for {location_info.str()} from URL '{url}' is {self.raw}")
            try:
                data = self.raw["properties"]["periods"][0]
                self.name = data["name"]
                self.datetime = datetime.datetime.strftime(datetime.datetime.fromisoformat(data["startTime"]),"%m/%d/%Y\n%H:%M")
                self.daytime = data["isDaytime"]
                self.temperature = data["temperature"]
                self.temperature_trend = data["temperatureTrend"]
                self.forecast_short = data["shortForecast"]
                self.image = data["icon"]
                self.wind_speed = data["windSpeed"]
                self.wind_direction = data["windDirection"]
                self.endtime = datetime.datetime.fromisoformat(data["endTime"])
                self.error = False
            except:
                self.error = True
