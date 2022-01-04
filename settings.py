from debug import debug

class settings:
    valid_modes = ["Off","Auto","Heat","Cool","Vent","Aux"]
    operating_mode = "Auto"
    heating_setpoint = 70.0
    cooling_setpoint = 78.0
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

