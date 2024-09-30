import math
from machine import Pin, PWM
from time import sleep

class Baad:
    def __init__(self):
        self.en12 = Pin(1, Pin.OUT)
        self.en34 = Pin(2, Pin.OUT)
        self.A1 = PWM(Pin(4, Pin.OUT), freq=200, duty_u16=40000)
        self.A3 = PWM(Pin(5, Pin.OUT), freq=50, duty_ns=1000000)

        self.en12.value(1)
        self.en34.value(1)
        
    def servo(self):
        x = 0
        while x != 10:
            A3.duty_ns(2500000)
            sleep(1)
            A3.duty_ns(1500000)
            sleep(1)
            A3.duty_ns(500000)
            sleep(1)
            x += 1
            
        A3.deinit()
        
    def DCStart(self):
        self.A1.duty_u16(65000)
        sleep(4)
        self.A1.duty_u16(0)
        sleep(1)
        

        
if __name__=="__main__":
    
    SSHolmeaa = Baad()
    #SSHolmeaa.servo()
    SSHolmeaa.DCStart()
        

        