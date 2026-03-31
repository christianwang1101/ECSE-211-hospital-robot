from utils.brick import EV3GyroSensor
from time import sleep
from config.settings import PORT_GYRO
import threading

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
        self._lock = threading.Lock()
        print("Finished initializing gyro sensor")

    def start(self):
        t = threading.Thread(target=self._poll, daemon=True)
        t.start()

    def _poll(self):
        while True:
            try:
                angle = self.read_angle()
                with self._lock:
                    self._angle = angle
            except Exception as e:
                print(f"Gyro poll error: {e}")
            sleep(POLL_INTERVAL)

    def get_angle(self):
        with self._lock:
            return self._angle

    def read_angle(self):
        """Poll the gyro sensor and return the current angle (degrees) relative
        to the origin set at initialization. Filters out drift using DPS_DEADBAND."""
        while True:
            try:
                reading = self._sensor.get_both_measure()
            except Exception:
                # Sensor mode was reset (e.g. by motor voltage spike); reconfigure and retry
                try:
                    self._sensor.set_mode(EV3GyroSensor.Mode.BOTH)
                    self._sensor.wait_ready()
                except Exception:
                    pass
                sleep(POLL_INTERVAL)
                continue
            if reading is not None:
                current, dps = reading
                if abs(dps) >= DPS_DEADBAND:
                    delta = current - self._origin
                    self._angle = delta % 360 if delta >= 0 else -((-delta) % 360)
                return self._angle
            sleep(POLL_INTERVAL)
