#!/usr/bin/python3

import datetime
import time
from core.influx_logger import Influx_logger
import Adafruit_DHT


class Temp_Humid_Logger(Influx_logger):

    number_of_buffer = 1

    def __init__(self):
        super().__init__()
        self.log_file = self.log_folder.joinpath(
            f'log_temp_humid_{datetime.datetime.now().date()}')

    def run(self):
        # Sensor should be set to Adafruit_DHT.DHT11,
        # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
        # sensor = Adafruit_DHT.DHT22
        sensor = Adafruit_DHT.DHT11

        # Example using a Raspberry Pi with DHT sensor
        # connected to GPIO23.
        pin = 20

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        if humidity is not None and temperature is not None:
            print(f'Temp={temperature:0.1f} C  Humidity={humidity:0.1f} %')
            data = {
                'measurement': 'temp_humid',
                'time': ts,
                'fields': {'temp': float(temperature), 'humid': float(humidity)}
            }
            self.logging_with_buffer(data)
        else:
            print('Failed to get reading. Try again!')


if __name__ == '__main__':
    logger = Temp_Humid_Logger()
    logger.run()
