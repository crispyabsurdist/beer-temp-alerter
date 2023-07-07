import machine
import dht
import time

# Define the GPIO pins connected to the DHT11 sensor and the RGB LED
dht_data_pin = machine.Pin(0)
led_red_pin = machine.Pin(2, machine.Pin.OUT)
led_green_pin = machine.Pin(3, machine.Pin.OUT)
led_blue_pin = machine.Pin(4, machine.Pin.OUT)

# Create a DHT11 sensor object
dht_sensor = dht.DHT11(dht_data_pin)

# Define the temperature thresholds for color changes
cold_threshold = 18
hot_threshold = 21

# Function to control LED color based on temperature
def set_led_color(temperature):
    if temperature < cold_threshold:
        # Cold temperature: Set LED to blue
        led_red_pin.off()
        led_green_pin.off()
        led_blue_pin.on()
    elif temperature > hot_threshold:
        # Hot temperature: Set LED to red
        led_red_pin.on()
        led_green_pin.off()
        led_blue_pin.off()
    else:
        # Moderate temperature: Set LED to green
        led_red_pin.off()
        led_green_pin.on()
        led_blue_pin.off()

# Main loop
while True:
    # Measure the temperature and humidity
    dht_sensor.measure()
    
    # Read the temperature from the sensor
    temperature = dht_sensor.temperature()
    print("Temperature:", temperature)

    # Update the LED color based on the temperature
    set_led_color(temperature)

    # Wait for a certain interval before measuring temperature again
    time.sleep(1)
