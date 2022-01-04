import sys, os, datetime
import tkinter as tk

from config import config
from debug import debug
from main import main
from setup import setup

current_button = None

def enable_buttons(disable=[]):
    for name,button in buttons.items():
        if name in disable:
            button["button"]["state"] = "disable"
            current_button = button
            button["command"].hide()
        else:
            button["button"]["state"] = "normal"

def thermostat():
    for button, specs in buttons.items():
        specs["command"](wnd)
    main(wnd)

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
