import sys, os
import tkinter as tk

class config:
    debug = True

    screen_size = [800,480]
    screen_background = None
    
    button_background = None
    button_foreground = None
    button_background_active = None
    button_foreground_active = None
    button_interval = 80

    noaa_server = "https://api.weather.gov/points/{latitude},{longitude}"
    noaa_user_agent = "(gridlabd.us, gridlabd@gmail.com)"

def debug(msg,context_level=1):
    if config.debug:
        if type(context_level) is int and context_level >= 0:
            import inspect
            caller = inspect.stack()[context_level]
            filename = os.path.basename(caller.filename)
            print(f"DEBUG [{caller.function}()@{filename}#{caller.lineno}]: {msg}",
                    file=sys.stderr,flush=True)
        else:
            print(f"DEBUG [thermostat]: {msg}",
                    file=sys.stderr,flush=True)

# try:
#     sys.path.append("/usr/local/opt/gridlabd/current/share/gridlabd")
#     import noaa_forecast as noaa
#     if location.info:
#         debug(f"requesting weather forecast for IP address {location.info.ip}")
#         forecast = noaa.getforecast(location.info.latlng[0],location.info.latlng[1])
#         debug(f"forecast for {location.info.city}, {location.info.state} ({location.info.country}) ok")
#     else:
#         raise Exception(f"no location for forecast")
# except Exception as err:
#     debug(f"{err} (location.latlon={location.latlon})")
#     forecast = None

import geocoder, requests, json, datetime
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
            self.raw = json.loads(requests.get(location["properties"]["forecast"],headers=headers).content.decode("utf-8"))
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

class data:
    indoor_temperature = 72.0
    system_mode = "Auto"

class settings:
    operating_mode = "Auto"
    heating_setpoint = 70.0
    cooling_setpoint = 78.0

current_button = None
def enable_buttons(disable=[]):
    for name,button in buttons.items():
        if name in disable:
            button["button"]["state"] = "disable"
            current_button = button
            button["command"].hide()
        else:
            button["button"]["state"] = "normal"

class main:

    top = None
    layout_data = {
        "indoor_temperature" : {
            "item" : None,
            "type" : tk.Label,
            "source" : "data.indoor_temperature",
            "format" : "%.0f",
            "font" : ("Arial",144),
            "x" : 50,
            "y" : 50,
        },
        "system_mode" : {
            "item" : None,
            "type" : tk.Button,
            "source" : "data.system_mode",
            "format" : "%s",
            "font" : ("Arial",36),
            "x" : 50,
            "y" : 200,
        },
        "current_datetime" :
        {
            "item" : None,
            "type" : tk.Label,
            "source" : "datetime.datetime.now().strftime('%A, %B %d, %Y %I:%M %PM')",
            "format" : "%s",
            "font" : ("Arial",20),
            "x" : 300,
            "y" : 50,
        },
        "outdoor_temperature" : {
            "item" : None,
            "type" : tk.Label,
            "source" : "noaa().temperature",
            "format" : "%.0f F",
            "font" : ("Arial",36),
            "x" : 300,
            "y" : 100,
        },
        "outdoor_weather" : {
            "item" : None,
            "type" : tk.Label,
            "source" : "noaa().temperature_trend",
            "format" : "(%s)",
            "font" : ("Arial",36),
            "x" : 400,
            "y" : 100,
        },
        "outdoor_forecast" : {
            "item" : None,
            "type" : tk.Label,
            "source" : "noaa().forecast_short",
            "format" : "%s",
            "font" : ("Arial",36),
            "x" : 300,
            "y" : 150,
        },
    }

    def __init__(self,top=None):
        if top:
            debug(f"creating {self.__class__.__name__}",2)
            main.layout()
            self.top = top
        else:
            main.update()
            main.show()

    @classmethod
    def show(self):
        debug("opening main",2)
        enable_buttons(disable="main")
        pass

    @classmethod
    def hide(self):
        debug("closing main",2)
        pass

    @classmethod
    def layout(self):
        debug("laying out main",2)
        for name, layout in self.layout_data.items():
            try:
                layout["item"] = layout["type"]()
                layout["item"]["text"] = layout["format"] % eval(layout["source"])
                layout["item"]["font"] = layout["font"]
                layout["item"].place(x=layout["x"],y=layout["y"])
            except Exception as err:
                debug(f"exception context: {name} = {layout}")
                raise

    @classmethod
    def update(self):
        debug("updating main",2)
        pass

class setup:

    top = None

    def __init__(self,top=None):
        if top:
            debug("creating setup",2)
            self.top = top
        else:
            setup.show()

    @classmethod
    def show(self):
        debug("opening setup",2)
        enable_buttons(disable="setup")
        pass

    @classmethod
    def hide(self):
        debug("closing setup",2)
        pass

def thermostat():
    for button, specs in buttons.items():
        specs["command"](wnd)
    main()

    debug("starting mainloop")
    wnd.mainloop()
    debug("mainloop terminated")

buttons = {
    "main" : {
        "text" : "Main",
        "command" : main,
        "button" : None,
    },
    "setup" : {
        "text" : "Setup",
        "command" : setup,
        "button" : None,
    },
}

if __name__ == "__main__":
    wnd = tk.Tk(className="pipy Thermostat")

    wnd.geometry("x".join(list(map(lambda x:str(x),config.screen_size))))
    wnd["background"] = config.screen_background

    x_pos = 10
    y_pos = 10
    for name, specs in buttons.items():

        button = tk.Button(wnd,highlightbackground=config.button_background,font=("Arial",20))
        for spec,value in specs.items():
            button[spec] = value
        button["bg"] = config.button_background
        button["fg"] = config.button_foreground
        button["activebackground"] = config.button_background
        button["activeforeground"] = config.button_foreground
        button.place(x=x_pos, y=y_pos)
        buttons[name]["button"] = button
        x_pos += config.button_interval

    thermostat()
