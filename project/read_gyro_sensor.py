from utils.brick import EV3GyroSensor
from time import sleep
from config.settings import PORT_GYRO

DPS_DEADBAND = 2
POLL_INTERVAL = 0.05  # seconds

class GyroSensor:

    def __init__(self):
        self._sensor = EV3GyroSensor(PORT_GYRO, mode=EV3GyroSensor.Mode.BOTH)
        self._sensor.wait_ready()
        self._sensor.reset_measure()
        self._sensor.wait_ready()

        origin_reading = self._sensor.get_both_measure()
        if origin_reading is None:
            raise RuntimeError("Could not read gyro origin value.")
        self._origin, _ = origin_reading
        self._angle = 0
        print("Finished initializing gyro sensor")

    def read_angle(self):
        """Poll the gyro sensor and return the current angle (degrees) relative
        to the origin set at initialization. Filters out drift using DPS_DEADBAND."""
        while True:
            reading = self._sensor.get_both_measure()
            if reading is not None:
                current, dps = reading
                if abs(dps) >= DPS_DEADBAND:
                    delta = current - self._origin
                    self._angle = delta % 360 if delta >= 0 else -((-delta) % 360)
                return self._angle
            sleep(POLL_INTERVAL)
