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

    location_name = None # "Redwood City, CA"
    location_geo = None # [37.5,-122.3]
