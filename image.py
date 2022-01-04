import urllib.request, io
from PIL import ImageTk, Image
from debug import debug

class image:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        img = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(img)
        debug(f"image url = '{url}', img = {img}")

    def get(self):
        return self.image

