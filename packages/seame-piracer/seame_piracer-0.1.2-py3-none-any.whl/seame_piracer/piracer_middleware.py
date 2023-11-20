import os
import time
from seame_piracer.vehicles import PiRacerStandard
from seame_piracer.gamepads import ShanWanGamepad
from threading import Thread

class PiRacer_Middleware(object):
    def __init__(self):
        self.piracer = PiRacerStandard()
        self.battery_voltage = 0
        self.battery = 0
        self.mode = 0.5
        self.gear = 0

    def get_mode(self):
        return self.mode * 10

    def get_gear(self):
        return self.gear

    def get_battery(self):
        self.battery_voltage = self.piracer.get_battery_voltage()
        self.battery = round((self.battery_voltage - 9) / 3.2 * 100)
        if self.battery < 0:
            self.battery = 0
        return self.battery

    def mode_select(self, smode:int):
        self.mode = smode / 10
        print("set mode: ", self.mode)

    def gear_select(self, sgear:int):
        self.gear = sgear
        print("set gear: ", self.gear)
        
    def set_throttle(self, throttle:float):
        self.piracer.set_throttle_percent(throttle)
        
    def set_steering(self, steering:float):
        self.piracer.set_steering_percent(steering)
