from machine import Pin
from time import sleep

A, B, C, D = Pin(1, Pin.OUT), Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT)
sleeptime = 0.002

signals = [A, B, C, D]

sequence = [[1,0,0,0],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]]

position = 0

try:
	while True:
		for i in range(4):
			signals[i].value(sequence[position][i])
		
		position += 1
		position = position % 4
		sleep(sleeptime)
finally:
	print("stepper stopped")