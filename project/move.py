from access_components import (
    get_left_motor,
    get_right_motor,
    get_gyro_sensor,
    get_colour_sensor,
)
from config.settings import (
    SPEED_DPS_TURN,
    SPEED_DPS_STRAIGHT,
    DISTANCE_CM_TURN,
    RADIUS_WHEEL,
)

import math
import time

# Initialize navigation motors
LEFT_MOTOR = get_left_motor()
RIGHT_MOTOR = get_right_motor()

# Initialize hardware
GYRO_SENSOR = get_gyro_sensor()
COLOUR_SENSOR = get_colour_sensor()


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


def turn_without_gyro(
    is_left, speed_dps=SPEED_DPS_TURN, distance_cm=DISTANCE_CM_TURN, stop_condition=None
):
    """
    Parameters:
    - stop_condition: optional callable; if it returns a non-None value mid-turn, motors
      stop and the function returns that value (early exit). Returns None on normal completion.
    """
    linear_speed = RADIUS_WHEEL * math.radians(speed_dps)  # cm/s
    duration = distance_cm / linear_speed
    poll_interval = 0.01

    if is_left:
        LEFT_MOTOR.set_dps(-speed_dps)
        RIGHT_MOTOR.set_dps(speed_dps)
    else:
        LEFT_MOTOR.set_dps(speed_dps)
        RIGHT_MOTOR.set_dps(-speed_dps)

    elapsed = 0.0
    while elapsed < duration:
        time.sleep(poll_interval)
        elapsed += poll_interval
        if stop_condition is not None:
            result = stop_condition()
            if result is not None:
                print("STOPPED CONDITION MET")
                stop_motors()
                return result

    stop_motors()
    return None


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
        elif target_angle - 3 < current_angle < target_angle + 3:
            break

        error = ((target_angle - current_angle + 180) % 360) - 180
        if abs(error) <= 2:
            break

        print("Current angle: " + str(current_angle))
        print("Error: " + str(error))

        if error < 0:
            # left
            LEFT_MOTOR.set_dps(-speed_dps)
            RIGHT_MOTOR.set_dps(speed_dps)
        else:
            # right
            LEFT_MOTOR.set_dps(speed_dps)
            RIGHT_MOTOR.set_dps(-speed_dps)

        time.sleep(0.02)

    stop_motors()

    if wait_time > 0:
        time.sleep(wait_time)


def sweep(max_sweeps, move_forward_cm, sweep_distance_cm, sweep_distance_cm_right=0):
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
    if (sweep_distance_cm_right == 0): sweep_distance_cm_right = sweep_distance_cm

    def stop_on_colour():
        # GREEN => success (True), RED => failure (False), anything else => keep scanning (None).
        colour = COLOUR_SENSOR.get_colour_instant()
        print("COLOUR: " + str(colour))
        if colour == "GREEN":
            return True
        if colour == "RED":
            return False
        return None

    dps = 60

    for num_forward_increments in range(max_sweeps):
        state = turn_without_gyro(
            is_left=True,
            speed_dps=dps,
            distance_cm=sweep_distance_cm,
            stop_condition=stop_on_colour,
        )  # go left
        if state is not None:
            return state, num_forward_increments

        state = turn_without_gyro(
            is_left=False,
            speed_dps=dps,
            distance_cm=sweep_distance_cm_right,
            stop_condition=stop_on_colour,
        )  # go back to center
        if state is not None:
            return state, num_forward_increments

        state = turn_without_gyro(
            is_left=False,
            speed_dps=dps,
            distance_cm=sweep_distance_cm,
            stop_condition=stop_on_colour,
        )  # go right
        if state is not None:
            return state, num_forward_increments

        state = turn_without_gyro(
            is_left=True,
            speed_dps=dps,
            distance_cm=sweep_distance_cm_right,
            stop_condition=stop_on_colour,
        )  # go back to center
        if state is not None:
            return state, num_forward_increments

        move_straight(distance_cm=move_forward_cm, is_forward=True, speed_dps=500)

    return False, max_sweeps - 1


def set_motor_left_dps(dps):
    LEFT_MOTOR.set_dps(dps)


def set_motor_right_dps(dps):
    RIGHT_MOTOR.set_dps(dps)
