from machine import Pin, ADC
from time import sleep

class stepper:

    def __init__(self):
        self.A = Pin(1, Pin.OUT)
        self.B = Pin(2, Pin.OUT)
        self.C = Pin(3, Pin.OUT)
        self.D = Pin(4, Pin.OUT)
        self.xAxis = ADC(Pin(5, Pin.IN), atten=ADC.ATTN_11DB)
        self.yAxis = ADC(Pin(16, Pin.IN), atten=ADC.ATTN_11DB)
        self.sleeptime = 0.005
        self.signals = [self.A, self.B, self.C, self.D]

        self.Rsequence = [[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]]
        self.Lsequence = [[0,0,0,1],
                        [0,0,1,0],
                        [0,1,0,0],
                        [1,0,0,0]]

        self.position = 0
        
    def turnR(self):
        try:
            for i in range(4):
                self.signals[i].value(self.Rsequence[self.position][i])
            self.position += 1
            self.position = self.position % 4
            sleep(self.sleeptime)
        finally:
            self.A.off()
            self.B.off()
            self.C.off()
            self.D.off()
            
            
    def turnL(self):    
        try:
            for i in range(4):
                self.signals[i].value(self.Lsequence[self.position][i])
            self.position += 1
            self.position = self.position % 4
            sleep(self.sleeptime)
        finally:
            self.A.off()
            self.B.off()
            self.C.off()
            self.D.off()
    def joystick(self):
        
        xValue = self.xAxis.read_u16()
        sleep(0.1)
        return xValue
            
if __name__ == "__main__":
    SS = stepper()
    while True:
    #SS.turnR()
        turnValue = SS.joystick()
        
        if turnValue <= 600:
            SS.turnL()
            SS.turnL()
            SS.turnL()
            SS.turnL()
            SS.turnL()
            SS.turnL()
            
        if turnValue >= 60000:
            SS.turnR()
            SS.turnR()
            SS.turnR()
            SS.turnR()
            SS.turnR()
            SS.turnR()
    
