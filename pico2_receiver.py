import network
import time
import socket
import machine
import connect
from machine import Pin, PWM

# Configure Wi-Fi credentials
SSID = connect.SSID
PASSWORD = connect.PASSWORD

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

# IP addresses of the two Pico W boards
pico1_ip = connect.PICO1_SENDER
pico2_ip = connect.PICO2_RECEIVER

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to Pico W #2 IP address
server_address = (pico2_ip, 6969)
sock.bind(server_address)
sock.listen(1)

# Wait for a connection from Pico W #1
conn, addr = sock.accept()
print("Connected with Pico W #1")

# Onboard led
connected_led = machine.Pin("LED", machine.Pin.OUT)
connected_led.on()

# Configure RGB LED pins
led_pins = [16, 17, 18]  # Pins where RGB LED is wired
leds = [Pin(pin, Pin.OUT) for pin in led_pins]  # Pin control array

# Function to set the RGB LED color
def set_led_color(r, g, b):
    leds[0].value(not r)  # Invert the value since LOW turns on the LED
    leds[1].value(not g)
    leds[2].value(not b)

# Function to map temperature to RGB values
def map_temperature_to_color(temperature):
    if temperature < 16:
        return (1, 0, 0)  # Red
    elif temperature < 5:
        return (0, 1, 0)  # Green
    else:
        return (0, 0, 1)  # Blue

while True:
    # Receive temperature data from Pico W #1
    data = conn.recv(1024)
    temperature = float(data.decode().split(":")[1][:-3])
    print(temperature)

    # Map temperature to RGB color values
    color = map_temperature_to_color(temperature)

    # Set the RGB LED color
    set_led_color(*color)

    # Send response back to Pico W #1
    response = "LED color set"
    conn.send(response.encode())

conn.close()
connected_led.off()
