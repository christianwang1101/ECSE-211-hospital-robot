from utils.brick import TouchSensor
from config.settings import PORT_TOUCH_SENSOR_STOP

"""
TouchSensors Component
Controls the start and emergency stop
"""


class EmergencyStop:
    def __init__(self):
        self.STOP_SENSOR = TouchSensor(PORT_TOUCH_SENSOR_STOP)

        print("TOUCH: Initialized start and stop touch sensors")

    def stop_pressed(self):
        if self.STOP_SENSOR.is_pressed():
            print("TOUCH: Stop pressed")
            return True
        return False
