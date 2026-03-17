from utils.brick import EV3ColorSensor, wait_ready_sensors
from time import sleep
from config.settings import COLOUR_READINGS_MAP, COLOUR_LUMINOSITY_MAP
import math

COLOUR_SENSOR = EV3ColorSensor(3)

def normalize_reading(color_data):
    r, g, b = color_data[:3]

    # normalization
    denominator = float(r) + float(g) + float(b)
    if denominator != 0:
        r_norm = float(r) / denominator
        g_norm = float(g) / denominator
        b_norm = float(b) / denominator
    else:
        r_norm = g_norm = b_norm = 0
        
    return r_norm, g_norm, b_norm, denominator   

def classify_color(color_data):
    best_match = ""
    min_distance = float('inf')
    
    luminosity = color_data[3]
    color_data = color_data[:3]
    
    # check if B or W (only look at luminosity)
    for (min_luminosity, max_luminosity), colour in COLOUR_LUMINOSITY_MAP:
        if min_luminosity <= luminosity <= max_luminosity:
            return colour
        
    # check other colours (look at euclidean distance)
    for (reference_point, color_name) in COLOUR_READINGS_MAP:
        distance = math.dist(color_data, reference_point)
        if distance < min_distance:
            min_distance = distance
            best_match = color_name
    
    print("Shortest Distance: " + min_distance)
    return best_match
        
# continual loop -> collect 100 readings, then try to classify colour 
# maybe add some delay

wait_ready_sensors(True)
print("Finished initialization. Sensor is ready.")

try:
    while True:
        color_data = COLOUR_SENSOR.get_value()
        if color_data is not None: 
            normalized_color_data = normalize_reading(color_data)
            classified_color = classify_color(normalized_color_data)
            print("COLOUR: " + classified_color)
        
        sleep(0.25) # polling rate is every 0.25 sec
    
except KeyboardInterrupt:
    print("Finished program")