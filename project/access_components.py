from utils.brick import Motor
from components.gyro_sensor import GyroSensor
from components.colour_sensor import ColourSensor
from components.ultrasonic_sensor import UltrasonicSensor
from config.settings import PORT_MOTOR_LEFT, PORT_MOTOR_RIGHT

# Initialize navigation motors
LEFT_MOTOR = Motor(PORT_MOTOR_LEFT)
RIGHT_MOTOR = Motor(PORT_MOTOR_RIGHT)

# Initialize hardware
GYRO_SENSOR = GyroSensor()
COLOUR_SENSOR = ColourSensor()
ULTRASONIC_SENSOR = UltrasonicSensor()

GYRO_SENSOR.start()
COLOUR_SENSOR.start()
ULTRASONIC_SENSOR.start()

print("Finished initialization.")


def get_left_motor():
    return LEFT_MOTOR


def get_right_motor():
    return RIGHT_MOTOR


def get_gyro_sensor():
    return GYRO_SENSOR


def get_colour_sensor():
    return COLOUR_SENSOR


def get_ultrasonic_sensor():
    return ULTRASONIC_SENSOR
