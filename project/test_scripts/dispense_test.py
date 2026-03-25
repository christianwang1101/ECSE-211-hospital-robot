import time

from utils.brick import Motor


def spin_second_motor_twice(port="C", turn_degrees=110, dps=180, settle_seconds=3):
	"""Rotate a second motor by a fixed amount (default 90 degrees)."""
	second_motor = Motor(port)
	second_motor.reset_encoder()

	try:
		for _ in range(2):
			second_motor.set_limits(dps=dps)
			seconds = abs(turn_degrees) / float(dps)
			print(f"Turning second motor on port {port} by {turn_degrees} degrees at {dps} dps...")
			second_motor.set_position_relative(turn_degrees)
			time.sleep(seconds + settle_seconds)
	finally:
		second_motor.set_power(0)

if __name__ == "__main__":
	spin_second_motor_twice()
