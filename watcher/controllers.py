import time
from enum import Enum


class Conversions(Enum):
    SEC=1
    HOUR=60*60
    DAY=24*60*60
           
def timer(restart_time:float,units:str ="HOUR"):
    """
    Returns the results of a function when a given time have passed from the last call,
    otherwise returns True ('False' as a result is not accepted from pynput, stops the Listeners)
    """
    def wrap_(func):
        last_time=0
        def wrapped(*args,**kwds):
            nonlocal last_time
            dt=time.time()-last_time
            if not last_time or dt>restart_time*Conversions[units].value :
                last_time=time.time()
                return func(*args,**kwds)
            return True
        return wrapped
    return wrap_

def calls(n_calls:int):
    """
    Controlls the times you can call a function,
    if exceed the n_calls returns True ('False' as a result is not accepted from pynput, stops the Listeners)
    """
    def wrap_(func):
        curr_calls=0
        def wrapped(*args,**kwds):
            nonlocal curr_calls
            if curr_calls<n_calls:
                curr_calls+=1
                return func(*args,**kwds)
            return True
        return wrapped
    return wrap_
    
