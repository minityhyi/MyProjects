from machine import Pin, PWM
from time import sleep

A1 = Pin(3, Pin.OUT)
en12 = Pin(1, Pin.OUT)
en34 = Pin(2, Pin.OUT)
A3 = PWM(Pin(5, Pin.OUT), freq=50, duty_ns=1000000)


en12.value(1)
en34.value(1)
A1.value(1)
x = 0
while True:
    A3.duty_ns(2500000)
    sleep(0.5)
    A3.duty_ns(1500000)
    sleep(0.5)
    A3.duty_ns(500000)
    sleep(0.5)


A3.deinit()