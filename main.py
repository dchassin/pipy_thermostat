import sys, os, datetime
import tkinter as tk

from debug import debug
from data import data
from forecast import noaa
from settings import settings
from image import image

class main:

    top = None
    layout_data = {
        "indoor_temperature" : {
            "item" : None,
            "type" : tk.Label,
            "source" : "data.indoor_temperature",
            "format" : "%.0f",
            "font" : ("Arial",128),
            "x" : 25,
            "y" : 60,
        },
        "temperature_up" : {
            "item" : None,
            "type" : tk.Button,
            "source" : "'\u25B2'",
            "format" : "%s",
            "font" : ("Arial",36),
            "x" : 225,
            "y" : 75,
            "command" : "settings.temperature_up",
        },
        "temperature_down" : {
            "item" : None,
            "type" : tk.Button,
            "source" : "'\u25BC'",
            "format" : "%s",
            "font" : ("Arial",36),
            "x" : 225,
            "y" : 150,
            "command" : "settings.temperature_down",
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
            "source" : "datetime.datetime.now().strftime('%A, %B %d, %Y %I:%M %p').replace(' 0',' ')",
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
                sec = datetime.datetime.now().second
                self.top.after((60-sec+1)*1000,self.update)
            except Exception as err:
                debug(f"exception context: {name} = {layout}")
                raise

