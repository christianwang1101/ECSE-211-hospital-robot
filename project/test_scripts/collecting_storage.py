import time

from config.settings import PORT_MOTOR
from utils.brick import Motor


def run_grip_turn_test(turn_degrees=250, dps_in=180, dps_out=80, settle_seconds=0.5):
    """Turn grip once: faster in, slower out."""
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

        print("Grip turn test complete.")
    finally:
        motor.set_power(0)


if __name__ == "__main__":
    run_grip_turn_test()
