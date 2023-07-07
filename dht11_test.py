import machine
import dht
import time

# Configure DHT11 sensor
dht_pin = machine.Pin(16)
sensor = dht.DHT11(dht_pin)

while True:
    try:
        # Read temperature and humidity from DHT11 sensor
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Print the temperature and humidity readings
        print("Temperature: {:.1f} °C".format(temperature))
        print("Humidity: {:.1f}%".format(humidity))

    except Exception as e:
        print("Error reading DHT11 sensor:", str(e))

    # Delay before taking the next reading
    time.sleep(2)
