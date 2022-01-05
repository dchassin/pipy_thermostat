from debug import debug

class setup:

    top = None

    def __init__(self,top=None):
        if top:
            debug("creating setup",2)
            self.top = top
        else:
            self.show()

    @classmethod
    def show(self):
        debug("opening setup",2)
        enable_buttons(disable="setup")
        pass

    @classmethod
    def hide(self):
        debug("closing setup",2)
        pass

