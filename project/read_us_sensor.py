from utils.brick import EV3UltrasonicSensor, wait_ready_sensors
from time import sleep
from config.settings import PORT_ULTRASONIC

POLL_INTERVAL = 0.05  # seconds


class UltrasonicSensor:

    def __init__(self):
        self._sensor = EV3UltrasonicSensor(PORT_ULTRASONIC)
        wait_ready_sensors(True)
        print("Finished initializing ultrasonic sensor")

    def read_distance(self):
        """Poll the ultrasonic sensor continuously until a valid reading is
        returned. Returns the distance in cm."""
        while True:
            distance = self._sensor.get_value()
            if distance is not None:
                return distance
            sleep(POLL_INTERVAL)
