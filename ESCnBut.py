from machine import Pin, PWM, ADC
from time import sleep

# Configure the GPIO pin connected to the ESC signal wire
esc_pin = Pin(7, Pin.OUT)  # Change to the GPIO pin you're using
esc_pwm = PWM(esc_pin)
esc_pwm.freq(50)  # ESCs usually expect a 50 Hz PWM signal
butUp = Pin(12, Pin.IN, Pin.PULL_DOWN)
butDown = Pin(13, Pin.IN, Pin.PULL_DOWN)


def set_throttle(throttle):
    """
    Set the throttle level of the ESC.
    
    :param throttle: Throttle level (0.0 to 1.0)
    """
    # The pulse width for ESCs is usually between 1000 and 2000 microseconds
    # 0.0 -> 1000 µs, 1.0 -> 2000 µs
    pulse_width = 1000 + int(throttle * 1000)
    esc_pwm.duty_u16(int(pulse_width * 65535 / 20000))

def arm_esc():
    """
    Send a calibration signal to arm the ESC.
    """
    print("Arming ESC...")
    for _ in range(3):
        set_throttle(0.1)  # Minimum throttle
        sleep(1)
        set_throttle(0.9)  # Maximum throttle
        sleep(1)
    set_throttle(0.1)  # Minimum throttle
    
def potentiometerReading():
    potVal = pot.read_u16()
    newVal = potVal/65534
    print(newVal)
    sleep(0.6)
    return newVal 

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
    main()