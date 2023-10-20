#
# Dosing functions
#
import numpy as np

def constant(X):
    # Constant dosing of strength X
    return lambda t: X + t*0

def pulse(X, t0, dt):
    # Dosing at constant intervals dt apart 
    # for t0 seconds of strength X
    return lambda t: X * (t0<=t%dt)

def sawtooth(X, dt):
    # Dosing at constant intervals dt apart 
    # of strength 0 - X
    return lambda t: X * (t%dt)/dt

def sine(X, dt):
    # Dosing as a sine curve with period dt
    return lambda t: X * np.sin(t * 2*np.pi/dt) + X