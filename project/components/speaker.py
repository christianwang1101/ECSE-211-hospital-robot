from utils import sound
from utils.sound import NOTES
import time
import threading

"""
Speaker Component
Handles audio output for the digital flute
"""

class Speaker:
    def __init__(self, default_pitch="A4", default_duration=1):
        self.SPEAKER = sound.Sound(duration=default_duration, pitch=default_pitch, volume=200)
        self.current_note = None  # Track currently playing note
        print("SPEAKER: Initialized speaker")
        
    def play_note(self, note: str):
        print(f"SPEAKER: Playing note: {note}")
        self.current_note = note

        try:
            self.SPEAKER.set_pitch(NOTES[note])
            self.SPEAKER.update_audio()
            self.SPEAKER.play()
            self.SPEAKER.wait_done()

        except KeyboardInterrupt:
            print("\nSPEAKER: Code interrupted")
            self.__stop_note()

    def __stop_note(self):
        self.SPEAKER.stop()
        self.current_note = None  # Reset tracked note
        print("SPEAKER: Stopping speaker")

    def cleanup(self):
        self.__stop_note()