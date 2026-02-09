from components.motor_drum import DrumMotor
from components.speaker import Speaker
from components.touch_sensors import TouchSensors
from components.ultrasonic_notes import UltrasonicNoteReader
from utils.brick import wait_ready_sensors, reset_brick

"""
Controller for hardware components of digital flute
"""

# Initialize hardware
drum = DrumMotor()
speaker = Speaker()
touch = TouchSensors()
note_reader = UltrasonicNoteReader()
wait_ready_sensors()

print("Finished initialization.")

def start_program():
    try: 
        if (touch.start_pressed()): run_digital_flute()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        reset_brick()
        exit()
    
def run_digital_flute():
    try:
        drum.start_drumming_loop()
        
        while True:
            if touch.stop_pressed():
                break
            
            # play note based on ultrasonic reading
            note = note_reader.get_note()
            if note: speaker.play_note(note)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # stop drum and speaker immediately
        drum.cleanup()
        speaker.cleanup()
        reset_brick()
        exit()
    
if __name__ == "__main__":
    start_program()