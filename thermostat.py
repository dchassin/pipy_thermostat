import sys, os
import tkinter as tk
import urllib.request
import io
from PIL import ImageTk, Image

class config:
    debug = True

    screen_size = [800,480]
    screen_background = None
    
    button_background = None
    button_foreground = None
    button_background_active = None
    button_foreground_active = None
    button_interval = 100

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

class data:
    indoor_temperature = 72.0
    system_mode = "Off"

class settings:
    valid_modes = ["Off","Auto","Heat","Cool","Vent","Aux"]
    operating_mode = "Auto"
    heating_setpoint = 70.0
    cooling_setpoint = 78.0
    @classmethod
    def set_mode(self,mode=None):
        if mode in self.valid_modes:
            self.operating_mode = mode
        else:
            n = self.valid_modes.index(self.operating_mode) + 1
            if n == len(self.valid_modes): n = 0
            self.operating_mode = self.valid_modes[n]
        debug(f"setting.set_mode(mode={mode}): mode = {self.operating_mode}")
        main.update()

class image:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        img = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(img)
        debug(f"image url = '{url}', img = {img}")

    def get(self):
        return self.image

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
            "x" : 25,
            "y" : 60,
        },
        "system_mode" : {
            "item" : None,
            "type" : tk.Label,
            "source" : "data.system_mode",
            "format" : "%s",
            "font" : ("Arial",24),
            "x" : 25,
            "y" : 240,
        },
        "operating_mode" : {
            "item" : None,
            "type" : tk.Button,
            "source" : "settings.operating_mode",
            "format" : "%s",
            "font" : ("Arial",36),
            "x" : 25,
            "y" : 280,
            "command" : "settings.set_mode",
        },
        "current_datetime" :
        {
            "item" : None,
            "type" : tk.Label,
            "source" : "datetime.datetime.now().strftime('%A, %B %d, %Y %I:%M %p')",
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
            "y" : 160,
        },
        "outdoor_image" : {
            "item" : None,
            "type" : tk.Label,
            "image" : "noaa().image",
            "x" : 300,
            "y" : 220,
        }
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
                if "format" in layout.keys() and "source" in layout.keys():
                    layout["item"] = layout["type"](self.top)
                    layout["item"]["text"] = layout["format"] % eval(layout["source"])
                if "image" in layout.keys():
                    url = eval(layout["image"]).replace("small","large")
                    layout["item"] = layout["type"](self.top,image=image(url).get())
                if "font" in layout.keys():
                    layout["item"]["font"] = layout["font"]
                layout["item"].place(x=layout["x"],y=layout["y"])
                if "command" in layout.keys():
                    layout["item"]["command"] = eval(layout["command"])
            except Exception as err:
                debug(f"exception context: {name} = {layout}")
                raise

    @classmethod
    def update(self):
        debug("updating main",2)
        for name, layout in self.layout_data.items():
            try:
                if "format" in layout.keys() and "source" in layout.keys():
                    layout["item"]["text"] = layout["format"] % eval(layout["source"])
                if "image" in layout.keys():
                    url = eval(layout["image"]).replace("small","large")
                    layout["item"].configure(image=image(url).get())
                    layout["item"].image = image(url).get()
            except Exception as err:
                debug(f"exception context: {name} = {layout}")
                raise

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
