import time

import Adafruit_DHT
from Beacon.beacon import Beacon

if __name__ == "__main__":
    B = Beacon()
    B.start()
    B.unstop()
    sensor = Adafruit_DHT.DHT11
    DHT11_pin = 4
    while 1:

        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT11_pin)
        if humidity is not None and temperature is not None:
            print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            B.set_temp(temperature)
            time.sleep(30)

        else:
            print('Failed to get reading from the sensor. Try again!')
