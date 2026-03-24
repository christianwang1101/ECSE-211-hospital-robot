from utils.brick import EV3ColorSensor, wait_ready_sensors
from time import sleep
from config.settings import PORT_COLOR_SENSOR, COLOUR_READINGS_MAP, COLOUR_LUMINOSITY_MAP
from collections import Counter
import math
import threading

class ColourSensor:
    SAMPLE_SIZE = 5
    MIN_CONSENSUS = 3
    POLL_INTERVAL = 0.1  # seconds between readings

    def __init__(self):
        self._sensor = EV3ColorSensor(PORT_COLOR_SENSOR)
        wait_ready_sensors(True)
        self._colour = None
        self._lock = threading.Lock()
        print("Finished initializing colour sensor")

    def start(self):
        t = threading.Thread(target=self._poll, daemon=True)
        t.start()

    def _poll(self):
        while True:
            colour = self.read_colour()
            with self._lock:
                self._colour = colour

    def get_colour(self):
        with self._lock:
            return self._colour

    def _normalize(self, color_data):
        r, g, b = color_data[:3]
        denominator = float(r) + float(g) + float(b)
        if denominator != 0:
            return float(r) / denominator, float(g) / denominator, float(b) / denominator, denominator
        return 0, 0, 0, 0

    def _classify(self, normalized):
        best_match = "BLACK"
        min_distance = 0.05

        luminosity = normalized[3]

        for (min_lum, max_lum), color_name in COLOUR_LUMINOSITY_MAP.items():
            if min_lum <= luminosity <= max_lum:
                best_match = color_name

        for reference_point, color_name in COLOUR_READINGS_MAP.items():
            distance = math.dist(normalized[:3], reference_point)
            if distance < min_distance:
                min_distance = distance
                best_match = color_name

        return best_match

    def read_colour(self):
        """Poll the colour sensor continuously until a confident classification
        is made (at least MIN_CONSENSUS matching readings in SAMPLE_SIZE samples).
        Returns the classified colour string."""
        while True:
            readings = []
            for _ in range(self.SAMPLE_SIZE):
                data = self._sensor.get_value()
                if data is not None:
                    readings.append(self._classify(self._normalize(data)))
                sleep(self.POLL_INTERVAL)

            counts = Counter(readings)
            top_colour, top_count = counts.most_common(1)[0]
            if top_count >= self.MIN_CONSENSUS:
                return top_colour
