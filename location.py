import geocoder
from config import config
from debug import debug

class location:
    name = None
    latlng = None

    def __init__(self):
        if config.location_geo:
            self.latlng = config.location_geo
        else:
            self.latlng = geocoder.ip('me')
        debug(f"location is {self.latlng}")