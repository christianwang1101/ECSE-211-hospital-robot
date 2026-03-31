from utils.brick import reset_brick
from config.settings import (
    HALLWAY_BASE_SPEED,
    HALLWAY_MIN_SPEED,
    HALLWAY_MAX_SPEED,
    HALLWAY_LOOP_SLEEP,
    HALLWAY_GYRO_WEIGHT,
    HALLWAY_US_WEIGHT,
    HALLWAY_KP,
    HALLWAY_KI,
    HALLWAY_KD,
    HALLWAY_INTEGRAL_CLAMP,
)
from access_components import get_gyro_sensor, get_colour_sensor, get_ultrasonic_sensor
from block_collection import collect_block
from move import (
    move_straight,
    turn_without_gyro,
    turn_to_with_gyro,
    set_motor_left_dps,
    set_motor_right_dps,
    stop_motors,
)

import time

# Initialize hardware
COLOUR_SENSOR = get_colour_sensor()
GYRO_SENSOR = get_gyro_sensor()
US_SENSOR = get_ultrasonic_sensor()


def start_navigation():
    try:
        navigate_hallway(
            distance_wall=10, num_black_lines=3, straight_angle=0
        )  # TODO: tune distance_wall

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
    move_straight(distance_cm=2, is_forward=False)
    turn_to_with_gyro(21)
    collect_block()
    move_straight(distance_cm=2.8, is_forward=True)
    collect_block()
    move_straight(distance_cm=2, is_forward=False)
    turn_to_with_gyro(0)


def navigate_hallway(distance_wall, num_black_lines, straight_angle):
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
    black_line_count = 0
    on_black_line = False

    integral = 0.0
    prev_error = None

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
                navigate_single_room(distance_wall, straight_angle)
                return

            # Count black lines as position milestones (edge-detect to avoid double-counting)
            if colour == "BLACK":
                if not on_black_line:
                    black_line_count += 1
                    on_black_line = True
                    print("scanned black line")
            else:
                on_black_line = False

            # Weighted combined error (degrees and cm normalised by their weights)
            gyro_error = ((angle - straight_angle + 180) % 360) - 180
            us_error = distance - distance_wall
            combined_error = HALLWAY_GYRO_WEIGHT * gyro_error + HALLWAY_US_WEIGHT * us_error

            # PID terms
            integral += combined_error * HALLWAY_LOOP_SLEEP
            integral = max(-HALLWAY_INTEGRAL_CLAMP, min(HALLWAY_INTEGRAL_CLAMP, integral))
            derivative = (combined_error - prev_error) / HALLWAY_LOOP_SLEEP if prev_error is not None else 0.0
            prev_error = combined_error

            correction = HALLWAY_KP * combined_error + HALLWAY_KI * integral + HALLWAY_KD * derivative

            # Positive correction steers left: left slower, right faster
            left_speed = max(HALLWAY_MIN_SPEED, min(HALLWAY_MAX_SPEED, int(HALLWAY_BASE_SPEED - correction)))
            right_speed = max(HALLWAY_MIN_SPEED, min(HALLWAY_MAX_SPEED, int(HALLWAY_BASE_SPEED + correction)))

            set_motor_left_dps(left_speed)
            set_motor_right_dps(right_speed)

            time.sleep(HALLWAY_LOOP_SLEEP)
        except Exception as e:
            print("navigate_hallway error: " + str(e))


def navigate_single_room(min_distance_wall, straight_angle):
    """
    Navigates the robot through a single-bed room, scanning
    the bed and detecting its position, then dropping off the block if necessary
    - min_distance_wall: distance the robot should be from the left wall to prevent collision
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is swivelling relative to the straight angle
    """
    print("navigating single room")


def navigate_double_room(min_distance_wall, straight_angle):
    """
    Navigates the robot through a double-bed room, scanning
    the bed and detecting its position, then dropping off the block if necessary
    Parameters:
    - min_distance_wall: distance the robot should be from the left wall to prevent collision
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is swivelling relative to the straight angle
    """
    pass


if __name__ == "__main__":
    start_navigation()
