from utils.brick import reset_brick
from utils.sound import Sound, Song
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
from block_collection import collect_block, drop_off
from move import (
    move_straight,
    turn_without_gyro,
    turn_to_with_gyro,
    set_motor_left_dps,
    set_motor_right_dps,
    stop_motors,
    sweep,
)
from components.speaker import Speaker
from components.touch_sensor import EmergencyStop

import time
import threading
import _thread

# Initialize hardware
COLOUR_SENSOR = get_colour_sensor()
GYRO_SENSOR = get_gyro_sensor()
US_SENSOR = get_ultrasonic_sensor()
SPEAKER = Speaker()
EMERGENCY_STOP = EmergencyStop()


def _watch_emergency_stop():
    while True:
        if EMERGENCY_STOP.stop_pressed():
            print("\nEmergency stop pressed!")
            _thread.interrupt_main()
            return
        time.sleep(0.05)


def start_navigation():
    threading.Thread(target=_watch_emergency_stop, daemon=True).start()
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

        # get into place for second hallway segment
        turn_without_gyro(is_left=False, distance_cm=10.5)
        # time.sleep(1)
        GYRO_SENSOR.reset_angle()
        print("gyro reading: " + str(GYRO_SENSOR.get_angle()))

        # second hallway segment to Room 2
        navigate_hallway(
            distance_wall=55, straight_angle=0, us_weight=10, is_fast=True, timeout=4.8
        )
        turn_without_gyro(is_left=True, distance_cm=11)  # turn into room
        GYRO_SENSOR.reset_angle()
        # time.sleep(1)
        navigate_single_room(sweep_distance_cm_right=2.8)
        move_straight(distance_cm=3, is_forward=False)

        # get into place for third hallway segment
        turn_without_gyro(is_left=False, distance_cm=10.5)
        time.sleep(1)
        GYRO_SENSOR.reset_angle()
        print("gyro reading: " + str(GYRO_SENSOR.get_angle()))

        # third hallway segment to Room 3
        navigate_hallway(
            distance_wall=55, straight_angle=0, is_fast=False, us_weight=5, timeout=6.20
        )
        turn_without_gyro(is_left=False, distance_cm=10.8)  # turn into room
        GYRO_SENSOR.reset_angle()
        # move_straight(distance_cm=2.7, is_forward=False)  # back out

        navigate_double_room()

        # go back to pharmacy
        turn_without_gyro(is_left=False, distance_cm=10.5)
        GYRO_SENSOR.reset_angle()
        # time.sleep(0.5)
        navigate_hallway(
            distance_wall=53,
            straight_angle=0,
            us_weight=10,
            is_fast=True,
            timeout=7.5,
            stop_at_orange=False,
        )
        turn_without_gyro(is_left=False, distance_cm=10.5)
        move_straight(distance_cm=48, is_forward=False)
        turn_without_gyro(is_left=True, distance_cm=10.5)

        GYRO_SENSOR.reset_angle()

        play_victory_sound()

    except KeyboardInterrupt:
        print("\nShutting down...")
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
    turn_without_gyro(is_left=True, distance_cm=2.35)  # was 2.45
    move_straight(distance_cm=8.2, is_forward=True)
    collect_block()
    move_straight(distance_cm=7, is_forward=False)
    turn_without_gyro(is_left=True, distance_cm=9.3)


def navigate_single_room(sweep_distance_cm=2.6, sweep_distance_cm_right=0):
    """
    Navigates the robot through a single-bed room, scanning
    the bed and detecting its position, then dropping off the block if necessary
    - min_distance_wall: distance the robot should be from the left wall to prevent collision
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is swivelling relative to the straight angle
    """
    print("navigating single room")
    # TODO: set max sweeps

    start_angle = GYRO_SENSOR.get_angle()
    move_forward_cm = 10

    green_bed_found, num_forward_increments = sweep(
        max_sweeps=5,
        move_forward_cm=move_forward_cm,
        sweep_distance_cm=sweep_distance_cm,
        sweep_distance_cm_right=sweep_distance_cm_right,
    )
    time.sleep(2)
    if green_bed_found:
        turn_without_gyro(is_left=False, distance_cm=0.9)  # added turn # was 1
        print("NAVIGATION.PY - green bed foudn")
        if num_forward_increments >= 3:
            straight_distance = 8
        else:
            straight_distance = 11

        move_straight(straight_distance, is_forward=True)
        drop_off()  # drop off block
        play_success_sound()
        move_straight(straight_distance, is_forward=False)
    print("num forward increments: " + str(num_forward_increments))

    if num_forward_increments >= 1:  # if num sweeps 3 or greater # was 2
        print("adjusting before moving backwards")
        move_straight(
            num_forward_increments * (1 / 3) * move_forward_cm, is_forward=False
        )  # go backwards to starting position
        print("--------------- go back to starting position ------")
        # time.sleep(0.5)

        turn_to_with_gyro(start_angle)  # reorient back to center
        # time.sleep(0.5)
        move_straight(
            num_forward_increments * (2 / 3) * move_forward_cm, is_forward=False
        )

    else:
        move_straight(
            num_forward_increments * move_forward_cm, is_forward=False
        )  # reorient back to center
        turn_to_with_gyro(start_angle)
        # go backwards to starting position

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
    navigate_single_room(sweep_distance_cm=2, sweep_distance_cm_right=2.8)
    # time.sleep(0.5)
    turn_without_gyro(is_left=False, distance_cm=3.5)
    move_straight(distance_cm=45, is_forward=False)
    turn_without_gyro(is_left=True, distance_cm=2.5)
    GYRO_SENSOR.reset_angle()
    # time.sleep(0.5)
    navigate_hallway(
        distance_wall=6, straight_angle=0, us_weight=15, is_fast=False, timeout=7
    )
    time.sleep(1)
    navigate_single_room(sweep_distance_cm=2, sweep_distance_cm_right=2.7)


def navigate_hallway(
    distance_wall, straight_angle, us_weight, is_fast, timeout=None, stop_at_orange=True
):
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
    print("navigating hallway")
    integral = 0.0
    prev_error = None
    last_valid_distance = distance_wall  # fallback when US reading is unreliable

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
            if stop_at_orange and colour == "ORANGE":
                move_straight(distance_cm=5, is_forward=True)
                stop_motors()
                print("detected orange - stop")
                return

            # Weighted combined error (degrees and cm normalised by their weights)
            gyro_error = ((angle - straight_angle + 180) % 360) - 180
            if distance <= 200:
                last_valid_distance = distance
            else:
                last_valid_distance = 2

            us_error = last_valid_distance - distance_wall
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


def play_victory_sound():
    # Super Mario Bros course clear fanfare
    s = 0.085  # sixteenth note (~176 BPM)
    e = 0.17  # eighth note
    q = 0.34  # quarter note

    notes = [
        ("G4", s),
        ("C5", s),
        ("E5", s),
        ("G5", s),
        ("C5", s),
        ("E5", s),
        ("G5", e),
        ("Ab5", e),
        ("G5", e),
        ("Eb5", s),
        ("Ab5", s),
        ("C6", s),
        ("Eb6", s),
        ("Ab5", s),
        ("C6", s),
        ("Eb6", e),
        ("Bb5", e),
        ("Eb6", e),
        ("G6", e),
        ("Bb5", s),
        ("Eb6", s),
        ("G6", s),
        ("Bb5", s),
        ("Eb6", s),
        ("G6", s),
        ("Bb6", e),
        ("B5", e),
        ("E6", e),
        ("G#6", e),
        ("B5", s),
        ("E6", s),
        ("G#6", s),
        ("B5", s),
        ("E6", s),
        ("G#6", s),
        ("B6", e),
        ("C7", q),
    ]
    song = Song([Sound(duration=d, pitch=n, volume=100) for n, d in notes])
    song.compile()
    song.play()
    song.wait_done()


def play_success_sound():
    # Super Mario Bros course clear fanfare
    s = 0.085  # sixteenth note (~176 BPM)
    e = 0.17  # eighth note
    q = 0.34  # quarter note

    notes = [
        ("B5", s),
        ("E6", s),
        ("G#6", s),
        ("B6", e),
        ("C7", q),
    ]
    song = Song([Sound(duration=d, pitch=n, volume=100) for n, d in notes])
    song.compile()
    song.play()
    song.wait_done()


if __name__ == "__main__":
    start_navigation()
