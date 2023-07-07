import network
import time
import socket
import machine
from dht import DHT11
import connect

connected_led = machine.Pin("LED", machine.Pin.OUT)

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
pico2_ip = connect.PICO2_RECIEVER

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to Pico W #2
server_address = (pico2_ip, 6969)
sock.connect(server_address)

connected_led.on()

# Configure DHT11 sensor
dht_pin = machine.Pin(16, machine.Pin.OUT)
sensor = DHT11(dht_pin)

while True:
    # Read temperature from DHT11 sensor
    sensor.measure()
    temperature = sensor.temperature()

    # Send temperature data to Pico W #2
    message = "Temperature: {:.1f} °C".format(temperature)
    sock.sendall(message.encode())
    print(message)

    # Receive response from Pico W #2
    response = sock.recv(1024)
    print("Received:", response.decode())

    # Toggle the onboard LED based on response
    connected_led.value(not connected_led.value())

    # Add a delay of ten seconds between messages
    time.sleep(10)

sock.close()
connected_led.off()
