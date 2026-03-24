from components.motor_drum import DrumMotor
from read_colour_sensor import ColourSensor
from read_gyro_sensor import GyroSensor
from read_us_sensor import UltrasonicSensor
from utils.brick import Motor, reset_brick
from config.settings import PORT_MOTOR

import threading
import time

# Initialize hardware
COLOUR_SENSOR = ColourSensor()
GYRO_SENSOR = GyroSensor()
US_SENSOR = UltrasonicSensor()
SWIVEL_MOTOR = Motor(PORT_MOTOR)

print("Finished initialization.")

def start_navigation():
    # start sensors
    COLOUR_SENSOR.start()
    GYRO_SENSOR.start()
    US_SENSOR.start()
    
    try:
        #TODO: add scooper function to pick up blocks initiailly
        navigate_hallway(distance_wall=10, num_black_lines=3, straight_angle=-90)
        
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        reset_brick()
        exit()


def navigate_hallway(distance_wall, num_black_lines, straight_angle):
    """
   Navigates the robot through the hallways of the obstacle course
    Parameters:
    - distance_wall (cm): distance the robot should be from the left wall to enter the room
    correctly
    - num_black_lines: number of black lines the robot should travel over before
    entering the room
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is travelling straight
    """
    while True:
      colour   = COLOUR_SENSOR.get_colour()
      angle    = GYRO_SENSOR.get_angle()
      distance = US_SENSOR.get_distance()

      if colour is None or angle is None or distance is None:
          time.sleep(0.05)
          continue  # wait for first readings to come in

      # act on values
      if distance < 15:
          # TODO: stop_motors()
          
      elif colour == "RED":
          # TODO: turn_to_target()
          
      else:
          # TODO: move_forward()
    

def navigate_single_room(min_distance_wall, straight_angle):
    """
    Navigates the robot through a single-bed room, scanning
    the bed and detecting its position, then dropping off the block if necessary
    - min_distance_wall: distance the robot should be from the left wall to prevent collision
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is swivelling relative to the straight angle
    """

    
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

    
def swivel(max_swivels):
    """
    Swivels the robot back and forth a max set number of times
    Terminates early when colour sensor detects red or green
    Parameters:
    - max_swivels: max number of times the robot will rotate back & forth before
    termination
    Returns:
    - true -> bed found, terminated early
    - false -> bed not found
    """
    # Keep argument for compatibility with existing callers; this routine runs fixed 10 turns.
    _ = max_swivels

    # Motor ports
    left_motor = Motor("A")
    right_motor = Motor("B")

    target_colours = {"RED", "GREEN"}

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

    # Set safe speed caps for smoother turning and forward nudges.
    left_motor.set_limits(dps=180)
    right_motor.set_limits(dps=180)

    def stop_drive():
        # Hard stop both motors so each step starts from a known state.
        left_motor.set_dps(0)
        right_motor.set_dps(0)

    def scan_for_target():
        # Early terminate if colour sensor sees a target colour.
        return COLOUR_SENSOR.get_colour() in target_colours

    def angle_error(target, current):
        # Compute shortest signed error in degrees in range [-180, 180].
        return ((target - current + 540) % 360) - 180

    def turn_to(target_angle, timeout=1.5):
        # Turn in place using gyro feedback until robot is near desired heading.
        turn_start = time.time()
        while time.time() - turn_start < timeout:
            if scan_for_target():
                stop_drive()
                return True

            current_angle = GYRO_SENSOR.get_angle()
            if current_angle is None:
                time.sleep(0.02)
                continue

            error = angle_error(target_angle, current_angle)

            # Stop turning once heading error is small enough.
            if abs(error) <= 2:
                break

            # Positive error: need more left turn. Negative error: need more right turn.
            if error > 0:
                left_motor.set_dps(-110)
                right_motor.set_dps(110)
            else:
                left_motor.set_dps(110)
                right_motor.set_dps(-110)

            time.sleep(0.02)

        stop_drive()
        return scan_for_target()

    def move_forward_briefly():
        # Move forward a little after each turn (0.5s as requested).
        left_motor.set_dps(140)
        right_motor.set_dps(140)
        time.sleep(0.5)
        stop_drive()

    # Define left/right look angles approximately 20 degrees around center heading.
    left_target = center_angle + 20
    right_target = center_angle - 20

    # Run exactly 10 turns total: 5 left turns and 5 right turns.
    for _ in range(5):
        if turn_to(left_target):
            return True
        move_forward_briefly()
        if scan_for_target():
            return True

        if turn_to(right_target):
            return True
        move_forward_briefly()
        if scan_for_target():
            return True

    # Completed all turns without finding target colours.
    return False

def drop_off_block():
    # some code to drop off the block at this position, will prob
    # be called by 
    
if __name__ == "__main__":
    start_navigation()