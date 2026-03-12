from utils.brick import EV3ColorSensor, wait_ready_sensors
from time import sleep
import keyboard

COLOUR_SENSOR_DATA_FILE = "../data_analysis/colour_sensor_data.csv"
COLOUR_SENSOR = EV3ColorSensor(3)
COLOUR_MAP = {}

# loop -> for each colour (red, green, blue, yellow, orange)
# prompt user: hold the block in front of the sensor for 3 seconds
# program should normalize the values, average them, and write to a csv file with the format: colour, r, g, b, intensity

wait_ready_sensors(True)
print("Finished initialization. Sensor is ready.")

# run for each of the colours
for color in ["red", "green", "blue", "yellow", "orange"]:
    print("Hold the {} block in front of the sensor for 3 seconds. When you're done, press Enter...".format(color))
    sleep(3) 
    print("Starting data collection...")

    # get the color data
    while True:
        # detect if enter is pressed then exit
        if keyboard.is_pressed('enter'):
            print("Data collection stopped.")
            break

        # collect colour until enter is pressed
        color_data = COLOUR_SENSOR.get_value()

        total_red = []
        total_green = []
        total_blue = []
        total_intensity = []

        if color_data is not None:
            r, g, b = color_data[:3]

            # normalization
            denominator = float(r) + float(g) + float(b)
            if denominator != 0:
                r_norm = float(r) / denominator
                g_norm = float(g) / denominator
                b_norm = float(b) / denominator
            else:
                r_norm = g_norm = b_norm = 0

            total_red.append(r_norm)
            total_green.append(g_norm)
            total_blue.append(b_norm)
            total_intensity.append(denominator)

        # calculate the average of the collected data
        avg_red = sum(total_red) / len(total_red) if total_red else 0
        avg_green = sum(total_green) / len(total_green) if total_green else 0
        avg_blue = sum(total_blue) / len(total_blue) if total_blue else 0
        avg_intensity = sum(total_intensity) / len(total_intensity) if total_intensity else 0

        COLOUR_MAP.update({color: (avg_red, avg_green, avg_blue, avg_intensity)})

# write the data to a csv file
with open(COLOUR_SENSOR_DATA_FILE, "w") as f:
    f.write("colour,red,green,blue,intensity\n")
    for color, values in COLOUR_MAP.items():
        f.write("{},{},{},{},{}\n".format(color, *values))
