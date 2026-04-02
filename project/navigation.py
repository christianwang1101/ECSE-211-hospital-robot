from utils.brick import reset_brick
from config.settings import (
    HALLWAY_BASE_SPEED,
    HALLWAY_MIN_SPEED,
    HALLWAY_MAX_SPEED,
    FAST_HALLWAY_BASE_SPEED,
    FAST_HALLWAY_MIN_SPEED,
    FAST_HALLWAY_MAX_SPEED,
    HALLWAY_LOOP_SLEEP,
    HALLWAY_GYRO_WEIGHT,
    HALLWAY_KP,
    HALLWAY_KI,
    HALLWAY_KD,
    HALLWAY_INTEGRAL_CLAMP,
)
from access_components import get_gyro_sensor, get_colour_sensor, get_ultrasonic_sensor
from block_collection import collect_block, spin_dispeser_motor_once, drop_off
from move import (
    move_straight,
    turn_without_gyro,
    turn_to_with_gyro,
    set_motor_left_dps,
    set_motor_right_dps,
    stop_motors,
    sweep,
)

import time

# Initialize hardware
COLOUR_SENSOR = get_colour_sensor()
GYRO_SENSOR = get_gyro_sensor()
US_SENSOR = get_ultrasonic_sensor()


def start_navigation():
    try:
        # pharmacy
        navigate_pharmacy()
        time.sleep(1)
        GYRO_SENSOR.reset_angle()

        # first hallway segment to Room 1
        navigate_hallway(
            distance_wall=5, straight_angle=0, us_weight=15, is_fast=False, timeout=9
        )
        move_straight(distance_cm=5, is_forward=True)  # go forward a bit
        navigate_single_room()
        move_straight(distance_cm=3, is_forward=False)  # go back a bit

        # get into place for second hallway segment
        turn_without_gyro(is_left=False, distance_cm=10.5)
        time.sleep(1)
        GYRO_SENSOR.reset_angle()
        print("gyro reading: " + str(GYRO_SENSOR.get_angle()))

        # second hallway segment to Room 2
        navigate_hallway(
            distance_wall=55, straight_angle=0, us_weight=10, is_fast=True, timeout=4.8
        )
        turn_without_gyro(is_left=True, distance_cm=10.5)  # turn into room
        GYRO_SENSOR.reset_angle()
        time.sleep(1)
        navigate_single_room()

        # get into place for third hallway segment
        turn_without_gyro(is_left=False, distance_cm=10.5)
        time.sleep(1)
        GYRO_SENSOR.reset_angle()
        print("gyro reading: " + str(GYRO_SENSOR.get_angle()))

        # third hallway segment to Room 3
        navigate_hallway(
            distance_wall=53, straight_angle=0, is_fast=True, us_weight=8, timeout=6
        )
        turn_without_gyro(is_left=False, distance_cm=10.5)  # turn into room
        GYRO_SENSOR.reset_angle()
        move_straight(distance_cm=2.7, is_forward=False)  # back out
        navigate_double_room()  # TODO

    except KeyboardInterrupt:
        print("\nShutting down...")
        # TODO: emergency stop, reset motors
    finally:
        reset_brick()
        exit()


def navigate_pharmacy():
    """
    Navigate the pharmacy area with dimensions approximately 48.9 x 20 units.
    The robot starts in this area and needs to move around.
    """
    collect_block()
    move_straight(distance_cm=7.5, is_forward=False)
    turn_without_gyro(is_left=True, distance_cm=2.4)
    move_straight(distance_cm=8.2, is_forward=True)
    collect_block()
    move_straight(distance_cm=7, is_forward=False)
    turn_without_gyro(is_left=True, distance_cm=9.3)


def navigate_single_room():
    """
    Navigates the robot through a single-bed room, scanning
    the bed and detecting its position, then dropping off the block if necessary
    - min_distance_wall: distance the robot should be from the left wall to prevent collision
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is swivelling relative to the straight angle
    """
    print("navigating single room")

    start_angle = GYRO_SENSOR.get_angle()
    move_forward_cm = 10
    sweep_distance_cm = 2.6

    green_bed_found, num_forward_increments = sweep(
        max_sweeps=5,
        move_forward_cm=move_forward_cm,
        sweep_distance_cm=sweep_distance_cm,
    )
    time.sleep(2)
    if green_bed_found:
        print("NAVIGATION.PY - green bed foudn")
        move_straight(9, is_forward=True)
        drop_off()  # drop off block

    move_straight(
        num_forward_increments * move_forward_cm, is_forward=False
    )  # go backwards to starting position

    turn_to_with_gyro(start_angle)  # reorient back to center

    print("finished navigating single room")


def navigate_double_room():
    """
    Navigates the robot through a double-bed room, scanning
    the bed and detecting its position, then dropping off the block if necessary
    Parameters:
    - min_distance_wall: distance the robot should be from the left wall to prevent collision
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is swivelling relative to the straight angle
    """
    print("TODO: navigate double room")
    pass


def navigate_hallway(distance_wall, straight_angle, us_weight, is_fast, timeout=None):
    """
    Navigates the robot through the hallways of the obstacle course using a PID
    controller that fuses gyro heading and left-wall US distance into a single
    steering correction applied while the robot stays in motion throughout.

    Sign convention (positive correction → steer left, toward wall):
      gyro_error = angle - straight_angle   (positive = turned right)
      us_error   = distance - distance_wall (positive = drifted away from wall)
    Both are positive when the robot has drifted right, so they add constructively.

    Parameters:
    - distance_wall (cm): target distance from the left wall
    - num_black_lines: number of black lines to count as position milestones
    - straight_angle: target gyro heading for straight travel
    """
    integral = 0.0
    prev_error = None

    start_time = time.time()

    # Wait for all sensors to produce valid first readings
    while True:
        if (
            COLOUR_SENSOR.get_colour() is not None
            and GYRO_SENSOR.get_angle() is not None
            and US_SENSOR.get_distance() is not None
        ):
            break
        time.sleep(0.05)

    while True:
        try:
            if timeout is not None and time.time() - start_time >= timeout:
                stop_motors()
                print("timer ended. stopping motors.")
                return

            colour = COLOUR_SENSOR.get_colour()
            angle = GYRO_SENSOR.get_angle()
            distance = US_SENSOR.get_distance()

            if angle is None or distance is None:
                time.sleep(HALLWAY_LOOP_SLEEP)
                continue

            # Enter room on orange line
            if colour == "ORANGE":
                stop_motors()
                print("detected orange - stop")
                return

            # Weighted combined error (degrees and cm normalised by their weights)
            gyro_error = ((angle - straight_angle + 180) % 360) - 180
            us_error = distance - distance_wall
            combined_error = HALLWAY_GYRO_WEIGHT * gyro_error + us_weight * us_error
            print("-------------------------------------")
            print("colour_reading: " + str(colour))
            print("gyro_reading: " + str(angle))
            print("us_reading: " + str(distance))
            print("gyro_error: " + str(gyro_error))
            print("us_error: " + str(us_error))
            print("combined_error: " + str(combined_error))

            # PID terms
            integral += combined_error * HALLWAY_LOOP_SLEEP
            integral = max(
                -HALLWAY_INTEGRAL_CLAMP, min(HALLWAY_INTEGRAL_CLAMP, integral)
            )
            derivative = (
                (combined_error - prev_error) / HALLWAY_LOOP_SLEEP
                if prev_error is not None
                else 0.0
            )
            prev_error = combined_error
            print("integral: " + str(integral))
            print("derivative: " + str(derivative))
            print("prev_error: " + str(prev_error))

            correction = (
                HALLWAY_KP * combined_error
                + HALLWAY_KI * integral
                + HALLWAY_KD * derivative
            )
            print("correction: " + str(correction))

            # Positive correction steers left: left slower, right faster
            if is_fast:
                left_speed = max(
                    FAST_HALLWAY_MIN_SPEED,
                    min(
                        FAST_HALLWAY_MAX_SPEED,
                        int(FAST_HALLWAY_BASE_SPEED - correction),
                    ),
                )
                right_speed = max(
                    FAST_HALLWAY_MIN_SPEED,
                    min(
                        FAST_HALLWAY_MAX_SPEED,
                        int(FAST_HALLWAY_BASE_SPEED + correction),
                    ),
                )
            else:
                left_speed = max(
                    HALLWAY_MIN_SPEED,
                    min(HALLWAY_MAX_SPEED, int(HALLWAY_BASE_SPEED - correction)),
                )
                right_speed = max(
                    HALLWAY_MIN_SPEED,
                    min(HALLWAY_MAX_SPEED, int(HALLWAY_BASE_SPEED + correction)),
                )

            print("left_speed: " + str(left_speed))
            print("right_speed: " + str(right_speed))

            set_motor_left_dps(left_speed)
            set_motor_right_dps(right_speed)

            time.sleep(HALLWAY_LOOP_SLEEP)
        except Exception as e:
            print("navigate_hallway error: " + str(e))


if __name__ == "__main__":
    start_navigation()
