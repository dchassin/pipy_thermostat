import os, sys
from config import config
import inspect

def debug(msg,context_level=1):
    if config.debug:
        if type(context_level) is int and context_level >= 0:
            caller = inspect.stack()[context_level]
            filename = os.path.basename(caller.filename)
            print(f"DEBUG [{caller.function}()@{filename}#{caller.lineno}]: {msg}",
                    file=sys.stderr,flush=True)
        else:
            print(f"DEBUG [thermostat]: {msg}",
                    file=sys.stderr,flush=True)

