import time

from config.settings import PORT_MOTOR
from utils.brick import Motor


def run_motor(power=50):
	motor = Motor(PORT_MOTOR)

	try:
		motor.set_power(power)
		while True:
			time.sleep(0.2)
	finally:
		motor.set_power(0)

if __name__ == "__main__":
	run_motor()


