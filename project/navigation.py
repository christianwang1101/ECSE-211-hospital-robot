from components.motor_drum import DrumMotor
from utils.brick import EV3ColorSensor, EV3GyroSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
import threading
import time

# Initialize hardware
COLOUR_SENSOR = EV3ColorSensor(1)
GYRO_SENSOR = EV3GyroSensor(2)
ULTRASONIC_SENSOR = EV3UltrasonicSensor(3)
wait_ready_sensors()

print("Finished initialization.")

def start_navigation():
    try:
        #TODO: add scooper function to pick up blocks initiailly
        navigate_hallway()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        reset_brick()
        exit()



def navigate_hallway(distance_wall, num_black_lines, straight_angle):
    """
   Navigates the robot through the hallways of the obstacle course
    Parameters:
    - distance_wall: distance the robot should be from the left wall to enter the room
    correctly
    - num_black_lines: number of black lines the robot should travel over before
    entering the room
    - straight_angle: the angle the robot should be (relative to the original start position)
    for it to be travelling in a straight line. Adjustments to the motor and rotation of the robot
    would be based of this paramter to make sure the robot is travelling straight
    """

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
    
if __name__ == "__main__":
    start_navigation()