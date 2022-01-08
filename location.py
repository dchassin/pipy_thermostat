import geocoder
from config import config
from debug import debug

class location:
    name = None
    geoinfo = None

    def __init__(self):
        if config.location_geo:
            self.latlng = config.location_geo
        else:
            self.geoinfo = geocoder.ip('me')
        debug(f"location is {self.geoinfo}")

    def latitude(self):
        return self.geoinfo.latlng[0]

    def longitude(self):
        return self.geoinfo.latlng[1]

    def str(self):
        return str(self.geoinfo)
