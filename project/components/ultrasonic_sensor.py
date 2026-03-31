from utils.brick import EV3UltrasonicSensor, wait_ready_sensors
from time import sleep
from config.settings import PORT_ULTRASONIC
import threading

POLL_INTERVAL = 0.05  # seconds


class UltrasonicSensor:
    def __init__(self):
        self._sensor = EV3UltrasonicSensor(PORT_ULTRASONIC)
        wait_ready_sensors(True)
        self._distance = None
        self._lock = threading.Lock()
        print("Finished initializing ultrasonic sensor")

    def start(self):
        t = threading.Thread(target=self._poll, daemon=True)
        t.start()

    def _poll(self):
        while True:
            try:
                distance = self.read_distance()
                with self._lock:
                    self._distance = distance
            except Exception as e:
                print(f"US poll error: {e}")
            sleep(POLL_INTERVAL)

    def get_distance(self):
        with self._lock:
            return self._distance

    def read_distance(self):
        """Poll the ultrasonic sensor continuously until a valid reading is
        returned. Returns the distance in cm."""
        while True:
            try:
                distance = self._sensor.get_value()
            except Exception:
                try:
                    self._sensor.set_mode(self._sensor.Mode.CM)
                    self._sensor.wait_ready()
                except Exception:
                    pass
                sleep(POLL_INTERVAL)
                continue
            if distance is not None:
                return distance
            sleep(POLL_INTERVAL)
