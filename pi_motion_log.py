#!/usr/bin/python3

from gpiozero import MotionSensor
import time
import datetime
from core.influx_logger import Influx_logger

class Motion_Logger(Influx_logger):

    number_of_buffer = 1
    motion_dict = {}
    buffer_time_interval = datetime.timedelta(minutes=1)
    
    def __init__(self):
        super().__init__()
        self.log_file = self.log_folder.joinpath(
            f'log_motion_{datetime.datetime.now().date()}')
        self.pir = MotionSensor(21)
    
    def run(self):
        while 1:
            if self.pir.motion_detected:
                print(f'Motion detected!')
                ts_string_now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
                self.motion_dict[ts_string_now] = self.motion_dict.get(ts_string_now, 0) + 1
                print(self.motion_dict)

            key_to_delete = []
            for ts_string, motion_times in self.motion_dict.items():
                ts_object = datetime.datetime.strptime(ts_string, '%Y-%m-%d %H:%M')
                ts_object_now = datetime.datetime.utcnow()
                if ts_object_now - self.buffer_time_interval > ts_object:
                    print(f'==> got a past ts_key : {ts_string}, value: {motion_times}')
                    data = {
                        'measurement': 'motion_log',
                        'time': ts_string,
                        'fields': {'times': motion_times}
                    }
                    self.logging_with_buffer(data)
                    key_to_delete.append(ts_string)
            
            for key in key_to_delete:
                del self.motion_dict[key]

            time.sleep(2)

if __name__ == '__main__':
    logger = Motion_Logger()
    logger.run()
