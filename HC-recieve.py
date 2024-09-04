from machine import Pin, UART
from time import sleep

RX = Pin(44)
TX = Pin(43)
baudrate = 9600
uart = UART(1, baudrate, rx=RX, tx=TX)
uart.init(baudrate, bits=8, parity=None, stop=1)

while True:
    if uart.any():
        sleep(0.2)
        data = uart.readline().decode('utf-8').strip()
        
    
        print(data)
        
    
    