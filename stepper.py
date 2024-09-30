from machine import Pin, ADC
from time import sleep

class stepper:

    def __init__(self):
        self.A = Pin(12, Pin.OUT)
        self.B = Pin(13, Pin.OUT)
        self.C = Pin(14, Pin.OUT)
        self.D = Pin(15, Pin.OUT)
        self.sleeptime = 0.02
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
            for x in range(50):
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
            for x in range(50):
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

            
if __name__ == "__main__":
    SS = stepper()
    while True:
        SS.turnR()
        SS.turnL()