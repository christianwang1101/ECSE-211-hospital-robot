from utils.brick import Motor
from config.settings import PORT_MOTOR
import time

"""
DrumMotor Component
Controls the pace of the motor moving the rod
"""

class DrumMotor:
    def __init__(self, default_tempo=120):
        self.tempo = default_tempo
                
        self.MOTOR = Motor(PORT_MOTOR)
        self.__initialize_motor()

        self.drum_running = False # keep track of whether or not motor is running
        print("Initialized motor")

    def __initialize_motor(self):
        # Reset encoder to set current position as 0 degrees
        self.MOTOR.reset_encoder()
        self.MOTOR.set_limits(dps=360)
        
    def start_drumming_loop(self):
        # calculate tempo
        rest_amount = 60 / self.tempo
        self.drum_running = True
        print("Starting drumming")

        try:
            while self.drum_running:
                # Move forward 90 degrees
                self.MOTOR.set_position_relative(90)
                time.sleep(rest_amount)  # Wait for movement to complete
                
                # Move backward 90 degrees
                self.MOTOR.set_position_relative(-90)
                time.sleep(rest_amount)
        except KeyboardInterrupt:
            print("\nCode interrupted")
            self.__stop_drumming()
    
    def __stop_drumming(self):
        self.drum_running = False
        self.MOTOR.set_position_relative(0)
        print("Stopping drumming")
    
    def cleanup(self):
        self.__stop_drumming()