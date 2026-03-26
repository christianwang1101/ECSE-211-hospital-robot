from utils.brick import Motor
from components.gyro_sensor import GyroSensor
from components.colour_sensor import ColourSensor
from config.settings import (
    PORT_MOTOR_LEFT,
    PORT_MOTOR_RIGHT,
    SPEED_DPS_TURN,
    SPEED_DPS_STRAIGHT,
    DISTANCE_CM_TURN,
    RADIUS_WHEEL,
)

import math
import time

# Initialize navigation motors
LEFT_MOTOR = Motor(PORT_MOTOR_LEFT)
RIGHT_MOTOR = Motor(PORT_MOTOR_RIGHT)

# Initialize hardware
GYRO_SENSOR = GyroSensor()
COLOUR_SENSOR = ColourSensor()

GYRO_SENSOR.start()
COLOUR_SENSOR.start()

print("Finished initialization.")


def stop_motors():
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)


def move_straight(distance_cm, is_forward=True, speed_dps=SPEED_DPS_STRAIGHT):
    """
    Move the robot straight for a given distance at a given speed.

    Parameters:
    - distance_cm: distance to travel in centimeters
    - speed_dps: speed in degrees per second for the motors
    """
    linear_speed = RADIUS_WHEEL * math.radians(speed_dps)  # cm/s
    if is_forward:
        LEFT_MOTOR.set_dps(speed_dps)
        RIGHT_MOTOR.set_dps(speed_dps)
    else:
        LEFT_MOTOR.set_dps(-speed_dps)
        RIGHT_MOTOR.set_dps(-speed_dps)
    time.sleep(distance_cm / linear_speed)
    stop_motors()


def turn_without_gyro(is_left, speed_dps=SPEED_DPS_TURN, distance_cm=DISTANCE_CM_TURN):
    linear_speed = RADIUS_WHEEL * math.radians(speed_dps)  # cm/s

    if is_left:
        LEFT_MOTOR.set_dps(speed_dps)
        RIGHT_MOTOR.set_dps(-speed_dps)
    else:
        LEFT_MOTOR.set_dps(-speed_dps)
        RIGHT_MOTOR.set_dps(speed_dps)
    time.sleep(distance_cm / linear_speed)
    stop_motors()


def turn_to_with_gyro(target_angle, speed_dps=SPEED_DPS_TURN, timeout=1.5, wait_time=0):
    """
    Turn the robot in place to a target heading using gyro feedback.

    Parameters:
    - target_angle: desired heading in degrees (relative to starting position)
    - speed_dps: rotation speed in degrees per second
    - timeout: max seconds to spend turning before giving up
    - wait_time: time to wait in seconds after reaching the target angle
    """
    turn_start = time.time()
    while time.time() - turn_start < timeout:
        current_angle = GYRO_SENSOR.get_angle()
        if current_angle is None:
            time.sleep(0.02)
            continue

        error = ((target_angle - current_angle + 540) % 360) - 180
        if abs(error) <= 2:
            break

        if error > 0:
            LEFT_MOTOR.set_dps(-speed_dps)
            RIGHT_MOTOR.set_dps(speed_dps)
        else:
            LEFT_MOTOR.set_dps(speed_dps)
            RIGHT_MOTOR.set_dps(-speed_dps)

        time.sleep(0.02)

    stop_motors()

    if wait_time > 0:
        time.sleep(wait_time)


def swivel(max_swivels):
    """
    Swivels the robot back and forth a max set number of times
    Terminates early when colour sensor detects red or green
    Parameters:
    - max_swivels: max number of times the robot will rotate back & forth before
    termination
    Returns:
    - true -> GREEN detected (target found)
    - false -> RED detected OR no target found after all sweeps
    """

    def target_state():
        # GREEN => success (True), RED => failure (False), anything else => keep scanning (None).
        colour = COLOUR_SENSOR.get_colour()
        if colour == "GREEN":
            return True
        if colour == "RED":
            return False
        return None

    # Wait briefly until gyro has a valid baseline angle.
    center_angle = GYRO_SENSOR.get_angle()
    if center_angle is None:
        for _ in range(20):
            time.sleep(0.05)
            center_angle = GYRO_SENSOR.get_angle()
            if center_angle is not None:
                break
    if center_angle is None:
        return False

    LEFT_MOTOR.set_limits(dps=180)
    RIGHT_MOTOR.set_limits(dps=180)

    left_target = center_angle + 20
    right_target = center_angle - 20

    for _ in range(max_swivels):
        turn_to_with_gyro(left_target)
        state = target_state()
        if state is not None:
            return state
        move_straight(distance_cm=2.5, speed_dps=140)
        state = target_state()
        if state is not None:
            return state

        turn_to_with_gyro(right_target)
        state = target_state()
        if state is not None:
            return state
        move_straight(distance_cm=2.5, speed_dps=140)
        state = target_state()
        if state is not None:
            return state

    return False


def set_motor_left_dps(dps):
    LEFT_MOTOR.set_dps(dps)


def set_motor_right_dps(dps):
    RIGHT_MOTOR.set_dps(dps)
