from machine import Pin
import time

led_pins = [16,17,18]
leds = [Pin(led_pins[0],Pin.OUT),Pin(led_pins[1],Pin.OUT),
        Pin(led_pins[2],Pin.OUT)]
delay_t = 0.1
while True:
    for led in leds:
        led.high()
        time.sleep(delay_t)
        led.low()
        time.sleep(delay_t)