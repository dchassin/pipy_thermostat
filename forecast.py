import geocoder, requests, json, datetime
from config import config
from debug import debug

location_info = geocoder.ip('me')

class noaa:

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

    def __init__(self,refresh=False):
        if not self.raw or refresh:
            url = config.noaa_server.format(latitude=location_info.latlng[0],longitude=location_info.latlng[1])
            headers = {'User-agent' : config.noaa_user_agent}
            location = json.loads(requests.get(url,headers=headers).content.decode("utf-8"))
            self.raw = json.loads(requests.get(location["properties"]["forecastHourly"],headers=headers).content.decode("utf-8"))
            refresh = True
        if refresh:
            data = self.raw["properties"]["periods"][0]
            debug(data)
            self.name = data["name"]
            self.datetime = datetime.datetime.strftime(datetime.datetime.fromisoformat(data["startTime"]),"%m/%d/%Y\n%H:%M")
            self.daytime = data["isDaytime"]
            self.temperature = data["temperature"]
            self.temperature_trend = data["temperatureTrend"]
            self.forecast_short = data["shortForecast"]
            self.image = data["icon"]
            self.wind_speed = data["windSpeed"]
            self.wind_direction = data["windDirection"]
