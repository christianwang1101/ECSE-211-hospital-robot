from components.motor_drum import DrumMotor
from read_colour_sensor import ColourSensor
from utils.brick import EV3GyroSensor, EV3UltrasonicSensor, Motor, wait_ready_sensors, reset_brick
import threading
import time

# Initialize hardware
COLOUR_SENSOR = ColourSensor()
GYRO_SENSOR = EV3GyroSensor(2)
ULTRASONIC_SENSOR = EV3UltrasonicSensor(3)
wait_ready_sensors()

print("Finished initialization.")

def start_navigation():
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
    pass

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
    # Validate input: exit early if no swivels requested
    # if max_swivels <= 0:
    #     return False

    # Initialize drive motors (A and D) for differential turning (in-place rotation)
    left_motor, right_motor = Motor.create_motors("AD")
    # Configuration: rotation distance per swivel, angle tolerance, motor speed, turn timeout
    swivel_angle = 20
    angle_tolerance = 2
    turn_speed_dps = 120
    turn_timeout = 2.0

    # Helper: stop both motors immediately
    def stop_motors():
        left_motor.set_dps(0)
        right_motor.set_dps(0)
        

    # Helper: poll colour sensor and return True if red or green detected
    def bed_detected():
        detected_colour = COLOUR_SENSOR.read_colour()
        return detected_colour in ("RED", "GREEN")

    try:
        # Initialize gyro sensor: reset to 0 degrees and wait for readiness
        GYRO_SENSOR.reset_measure()
        GYRO_SENSOR.wait_ready()

        # Record starting angle as reference point for target rotations
        start_angle = GYRO_SENSOR.get_abs_measure()
        if start_angle is None:
            return False

        # Alternate direction for back-and-forth swiveling: +1 for right, -1 for left
        direction = 1
        # Main loop: perform up to max_swivels back-and-forth rotations
        for _ in range(max_swivels):
            # Check colour before each swivel movement
            if bed_detected():
                return True

            # Calculate target angle: rotate by swivel_angle in current direction
            target_angle = start_angle + direction * swivel_angle
            start_time = time.time()

            # Inner loop: rotate until target angle is reached (with timeout)
            while True:
                # Get current rotation angle from gyro sensor
                current_angle = GYRO_SENSOR.get_abs_measure()
                if current_angle is None:
                    if time.time() - start_time > turn_timeout:
                        break
                    continue

                # Calculate rotation error and check if target reached within tolerance
                error = target_angle - current_angle
                if abs(error) <= angle_tolerance:
                    break

                # Set motor speeds: opposite directions for in-place swivel
                motor_speed = turn_speed_dps if error > 0 else -turn_speed_dps
                left_motor.set_dps(motor_speed)
                right_motor.set_dps(-motor_speed)

                # Poll colour sensor during rotation for early bed detection
                if bed_detected():
                    return True

                # Timeout safety check: abort turn if taking too long
                if time.time() - start_time > turn_timeout:
                    break

            # Stop motors and reverse direction for next swivel
            stop_motors()
            direction *= -1

        return False
    finally:
        stop_motors()

def drop_off_block():
    # some code to drop off the block at this position, will prob
    # be called by 
    pass
    
if __name__ == "__main__":
    start_navigation()