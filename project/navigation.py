from components.motor_drum import DrumMotor
from utils.brick import reset_brick
from read_colour_sensor import ColourSensor
from read_gyro_sensor import GyroSensor
from read_us_sensor import UltrasonicSensor

import time

# Initialize hardware
COLOUR_SENSOR = ColourSensor
GYRO_SENSOR = GyroSensor
US_SENSOR = UltrasonicSensor

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


def navigate_hallway(distance_wall, distance_error_margin, num_black_lines, straight_angle):
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
      if colour == "ORANGE":
          navigate_single_room()
      
      elif distance < (distance_wall - distance_error_margin):
          move_right()
          
      elif distance > (distance_wall + distance_error_margin):
          move_left()
          
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

def drop_off_block():
    # some code to drop off the block at this position, will prob
    # be called by 
    print("MOTOR: drop off block")
    
def move_right():
    print("MOTOR: move right")

def move_left():
    print("MOTOR: move left")

def move_forward():
    print("MOTOR: move left")
    
if __name__ == "__main__":
    start_navigation()