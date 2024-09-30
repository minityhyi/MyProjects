from machine import Pin, UART
from time import sleep


uart = UART(1, baudrate=9600, tx=Pin(5), rx=Pin(4))


moveLeft = Pin(8, Pin.IN, Pin.PULL_DOWN)
moveRight = Pin(18, Pin.IN, Pin.PULL_DOWN)
speedUp = Pin(38,Pin.IN, Pin.PULL_DOWN)
speedDown= Pin(37,Pin.IN, Pin.PULL_DOWN)
stop= Pin(36,Pin.IN, Pin.PULL_DOWN)


while True : 
    leftVal = moveLeft.value()
    rightVal = moveRight.value()
    speedUpVal = speedUp.value()
    speedDownVal = speedDown.value()
    stopVal = stop.value()
    message = ','.join([str(leftVal), str(rightVal), str(speedUpVal), str(speedDownVal), str(stopVal)])
    #message = "hej"
    #print("hej")
    print(f"leftVal: {leftVal}, rightVal: {rightVal}, speedUpVal: {speedUpVal} speedDownVal: {speedDownVal} stopval: {stopVal}")
    uart.write(message)
    sleep(0.5)

