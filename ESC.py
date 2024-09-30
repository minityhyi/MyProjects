from machine import Pin, PWM, ADC
from time import sleep

class ESC:
    
    def __init__(self):
        # Configure the GPIO pin connected to the ESC signal wire
        esc_pin = Pin(7, Pin.OUT)  # Change to the GPIO pin you're using
        self.esc_pwm = PWM(esc_pin)
        self.esc_pwm.freq(50)  # ESCs usually expect a 50 Hz PWM signal
        self.x = 0.45


    def set_throttle(self,throttle):
        # The pulse width for ESCs is usually between 1000 and 2000 microseconds
        # 0.0 -> 1000 µs, 1.0 -> 2000 µs
        pulse_width = 1000 + int(throttle * 1000)
        self.esc_pwm.duty_u16(int(pulse_width * 65535 / 20000))

    def arm_esc(self):
        """
        Send a calibration signal to arm the ESC.
        """
        print("Arming ESC...")
        for throttle in range(1, 100):
            self.set_throttle(throttle/100)
            sleep(0.1)
        self.set_throttle(0.5)
    
    def speed_up(self):
        
        self.x += 0.02
        if self.x >= 0.65:
            self.x = 0.65
        self.set_throttle(self.x)
            
    def speed_down(self):
        
        self.x -= 0.02
        if self.x <= 0.35:
            self.x = 0.35
        self.set_throttle(self.x)
    
    def stop(self):
        self.x = 0.5
        self.set_throttle(self.x)


    def main():
        x = 0.5
        set_throttle(0.4)
        sleep(15)
        # Test different throttle levels
        for throttle in range(1, 100):
            set_throttle(throttle/100)
            sleep(0.1)
        while True:
            n = butUp.value()
            t = butDown.value()
            sleep(0.01)
            if n == 1:
                x += 0.001
            if t == 1:
                x += -0.001
            if x >= 0.65:
                x= 0.65
            if x <= 0.35:
                x= 0.35
        
            

if __name__ == '__main__':
    tho = ESC()
    tho.arm_esc()