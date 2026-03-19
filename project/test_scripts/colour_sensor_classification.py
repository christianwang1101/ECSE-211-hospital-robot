from utils.brick import EV3ColorSensor, wait_ready_sensors
from time import sleep
from config.settings import COLOUR_READINGS_MAP, COLOUR_LUMINOSITY_MAP
from collections import Counter
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
    best_match = "BLACK"
    min_distance = 0.05
    
    luminosity = color_data[3]
    color_data = color_data[:3]
    
    print("Luminosity: " + str(luminosity))
    # check if B or W (only look at luminosity)
    for (min_luminosity, max_luminosity), color_name in COLOUR_LUMINOSITY_MAP.items():
        if min_luminosity <= luminosity <= max_luminosity:
            best_match = color_name
                
    # check other colours (look at euclidean distance)
    for reference_point, color_name in COLOUR_READINGS_MAP.items():
        distance = math.dist(color_data, reference_point)
        if distance < min_distance:
            min_distance = distance
            best_match = color_name
    
    # print("Shortest Distance: " + str(min_distance))
    return best_match
        
# continual loop -> collect 100 readings, then try to classify colour 
# maybe add some delay

wait_ready_sensors(True)
print("Finished initialization. Sensor is ready.")

counter = 1
classified_colors = []
try:
    while True:
        
        color_data = COLOUR_SENSOR.get_value()
        if color_data is not None: 
            normalized = normalize_reading(color_data)
            classified_color = classify_color(normalized)
            classified_colors.append(classified_color)
        
        if (counter % 5 == 0):
            counts = Counter(classified_colors)
            for color, count in counts.items():
                if count >= 3:
                    print("COLOUR: " + color)
            
            classified_colors = []
            
        counter += 1
        sleep(0.1) # polling rate is every 0.05 sec, print every 0.25 secs
    
except KeyboardInterrupt:
    print("Finished program")