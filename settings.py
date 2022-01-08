import os, sys, json
from debug import debug

json_file = "settings.json"

class settings:
    valid_modes = ["Off","Auto","Heat","Cool","Vent","Aux"]
    
    operating_mode = "Auto"
    heating_setpoint = 70.0
    cooling_setpoint = 78.0

    @classmethod
    def load(self):
        if os.path.exists(json_file):
            with open(json_file,"r") as f:
                data = json.load(f)
                try:
                    self.operating_mode = data["mode"]
                    self.heating_setpoint = data["theat"]
                    self.cooling_setpoint = data["tcool"]
                except:
                    pass

    @classmethod
    def save(self):
        with open(json_file,"w") as f:
            json.dump(f,dict(mode=self.operating_mode,theat=self.heating_setpoint,tcool=self.cooling_setpoint),indent=4)

    @classmethod
    def set_mode(self,mode=None,main=None):
        if mode in self.valid_modes:
            self.operating_mode = mode
        else:
            n = self.valid_modes.index(self.operating_mode) + 1
            if n == len(self.valid_modes): n = 0
            self.operating_mode = self.valid_modes[n]
        debug(f"setting.set_mode(mode={mode}): mode = {self.operating_mode}")
        if main: main.update()

    @classmethod
    def temperature_up(self):
        self.heating_setpoint += 1
        pass

    @classmethod
    def temperature_down(self):
        self.heating_setpoint -= 1
        pass
        
