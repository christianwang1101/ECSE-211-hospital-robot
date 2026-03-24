from components.motor_drum import DrumMotor
from read_colour_sensor import ColourSensor
from read_gyro_sensor import GyroSensor
from read_us_sensor import UltrasonicSensor
from utils.brick import Motor

import threading
import time
RADIUS_WHEEL = 2 #in cm

# Initialize hardware
COLOUR_SENSOR = ColourSensor
GYRO_SENSOR = GyroSensor
US_SENSOR = UltrasonicSensor

# Initialize navigation motors (assuming differential drive)
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

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
          # test comment
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

def move_straight(distance_cm, speed_dps):
    """
    Move the robot straight for a given distance at a given speed.
    
    Parameters:
    - distance_cm: distance to travel in centimeters
    - speed_dps: speed in degrees per second for the motors
    """
    # Calculate time needed: time = distance / speed
    # But we need to convert speed from dps to cm/s
    # This is a simplification - in reality you'd need wheel diameter and gear ratio
    # For now, assume speed_dps is roughly proportional to cm/s
    linear_speed= RADIUS_WHEEL * (speed_dps * (3.14 / 180))  # convert dps to cm/s
    time_seconds = distance_cm / linear_speed  # rough approximation
    
    # Set both motors to move forward at the same speed
    LEFT_MOTOR.set_dps(speed_dps)
    RIGHT_MOTOR.set_dps(speed_dps)
    
    # Wait for the calculated time
    time.sleep(time_seconds)
    
    # Stop the motors
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)

def rotate_to_angle(target_angle, speed_dps=100, wait_time=0):
    """
    Rotate the robot in place to reach a target angle using the gyro sensor.
    
    Parameters:
    - target_angle: the desired angle in degrees (relative to starting position)
    - speed_dps: rotation speed in degrees per second
    - wait_time: time to wait in seconds after reaching the target angle
    """
    current_angle = GYRO_SENSOR.get_angle()
    if current_angle is None:
        print("Gyro sensor not ready")
        return
    
    angle_difference = target_angle - current_angle
    
    # Determine direction: positive difference = turn right, negative = turn left
    if angle_difference > 0:
        # Turn right: left motor forward, right motor backward
        LEFT_MOTOR.set_dps(speed_dps)
        RIGHT_MOTOR.set_dps(-speed_dps)
    else:
        # Turn left: left motor backward, right motor forward
        LEFT_MOTOR.set_dps(-speed_dps)
        RIGHT_MOTOR.set_dps(speed_dps)
    
    # Wait until we reach the target angle (with some tolerance) # if angle is not between +- 2 degrees of target angle, motor will keep turning
    tolerance = 2  # degrees
    while abs(GYRO_SENSOR.get_angle() - target_angle) > tolerance:
        time.sleep(0.05)
    
    # Stop motors
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)
    
    # Wait the specified time
    if wait_time > 0:
        time.sleep(wait_time)

def pharmacy_navigation():
    """
    Navigate the pharmacy area with dimensions approximately 48.9 x 20 units.
    The robot starts in this area and needs to move around.
    """
    # Move straight for 20 cm at 200 dps
    move_straight(distance_cm=20, speed_dps=200)
    
    # Parameters
    x_degrees = 90
    wait_time = 2  # seconds
    
    # Rotate right to X degrees, wait
    rotate_to_angle(x_degrees, wait_time=wait_time)
    
    # Go back to 0 degrees
    rotate_to_angle(0)
    
    # Rotate left to -X degrees, wait
    rotate_to_angle(-x_degrees, wait_time=wait_time)
    
    # Go back to 0 degrees
    rotate_to_angle(0)
    
    # Rotate 180 degrees to face the opposite direction
    rotate_to_angle(180)
    
    # Move back the way we started (same distance, opposite direction)
    move_straight(distance_cm=20, speed_dps=200)
    
    # Final right rotation
    rotate_to_angle(90)
    
    # TODO: Add more navigation logic for the pharmacy area\



def drop_off_block():
    # some code to drop off the block at this position, will prob
    # be called by 
    
if __name__ == "__main__":
    start_navigation()