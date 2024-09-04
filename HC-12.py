from machine import Pin, UART
from time import sleep


uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))


moveLeft = Pin(15, Pin.IN, Pin.PULL_DOWN)
moveRight = Pin(16, Pin.IN, Pin.PULL_DOWN)
speedUp = Pin(17,Pin.IN, Pin.PULL_DOWN)
speedDown= Pin(18,Pin.IN, Pin.PULL_DOWN)
stop= Pin(8,Pin.IN)


while True : 
    leftVal = moveLeft.value()
    rightVal = moveRight.value()
    speedUpVal = speedUp.value()
    speedDownVal = speedDown.value()
    stopVal = stop.value()
    message = [str(leftVal), str(rightVal), str(speedUpVal), str(speedDownVal), str(stopVal)]
    sleep(0.5)
    uart.write(message.encode('uft-8'))

