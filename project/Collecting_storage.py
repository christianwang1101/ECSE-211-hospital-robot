import time

from utils.brick import Motor


def spin_second_motor_once(port="C", turn_degrees=90, dps=120, settle_seconds=0.5):
	"""Rotate a second motor by a fixed amount (default 90 degrees)."""
	second_motor = Motor(port)
	second_motor.reset_encoder()

	try:
		second_motor.set_limits(dps=dps)
		seconds = abs(turn_degrees) / float(dps)
		print(f"Turning second motor on port {port} by {turn_degrees} degrees at {dps} dps...")
		second_motor.set_position_relative(turn_degrees)
		time.sleep(seconds + settle_seconds)
	finally:
		second_motor.set_power(0)


def run_broom_turn_test(
	turn_degrees=260,
	dps_in=250,
	dps_out=100,
	second_motor_port="A",
	second_turn_degrees=110,
	second_motor_dps=180,
	settle_seconds=0.5,
):
	"""Turn broom motor out/back, then rotate a second motor by 90 degrees."""
	motor = Motor("D")

	# Start this test from a known encoder reference.
	motor.reset_encoder()

	try:
		motor.set_limits(dps=dps_in)
		seconds_in = abs(turn_degrees) / float(dps_in)
		print(f"Turning forward by {turn_degrees} degrees at {dps_in} dps...")
		motor.set_position_relative(turn_degrees)
		time.sleep(seconds_in + settle_seconds)

		motor.set_limits(dps=dps_out)
		seconds_out = abs(turn_degrees) / float(dps_out)
		print(f"Turning back by {-turn_degrees} degrees at {dps_out} dps...")
		motor.set_position_relative(-turn_degrees)
		time.sleep(seconds_out + settle_seconds)

		spin_second_motor_once(port=second_motor_port,
			turn_degrees=second_turn_degrees,
			dps=second_motor_dps,
			settle_seconds=settle_seconds,
		)

		print("Broom turn test complete.")
	finally:
		motor.set_power(0)


if __name__ == "__main__":
	run_broom_turn_test()


