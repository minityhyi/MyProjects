from machine import Pin, UART
from time import sleep
from stepper import stepper
from ESC import ESC

RX = Pin(44)
TX = Pin(43)
baudrate = 9600
uart = UART(1, baudrate, rx=RX, tx=TX)
uart.init(baudrate, bits=8, parity=None, stop=1)
print("listens for signal on 9600")
step= stepper()
thruster = ESC()
propelPos = 0
thruster.arm_esc()

while True:
    
    if uart.any():
        sleep(0.2)
        data = uart.readline().decode('utf-8').strip()
        print(data)
        
        li = data.split(",")
        
        if li[0] == "1":
            propelPos += 1
            if propelPos <= 5:
                step.turnL()
            elif propelPos >= 5:
                propelPos = 5
            
            
        elif li[1] == "1":
            propelPos -= 1
            if propelPos >= -5:
                step.turnR()
            elif propelPos <= -5:
                propelPos = -5
        
        elif li[2] == "1":
            thruster.speed_up()
        
        elif li[3] == "1":
            thruster.speed_down()
            
        elif li[4] == "1":
            thruster.stop()
        print(propelPos)
            
    
    
        
    
        
    
    