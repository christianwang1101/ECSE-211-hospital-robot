import time

from utils.brick import Motor
from config.settings import (
    PORT_MOTOR_DISPENSER,
    PORT_MOTOR_SCOOPER,
    MOTOR_SETTLE_SECONDS,
    DISPENSER_MOTOR_TURN_DEGREES,
    DISPENSER_MOTOR_DPS,
    SCOOPER_MOTOR_TURN_DEGREES,
    DISPENSER_MOTOR_DPS_IN,
    DISPENSER_MOTOR_DPS_OUT,
)


def spin_scooper_motor():
    """Turn broom motor out/back, then rotate a second motor by 90 degrees."""
    # Scooper motor initialization
    scooper_motor = Motor(PORT_MOTOR_SCOOPER)
    scooper_motor.reset_encoder()

    try:
        scooper_motor.set_limits(dps=SCOOPER_MOTOR_TURN_DEGREES)
        seconds_in = abs(SCOOPER_MOTOR_TURN_DEGREES) / float(DISPENSER_MOTOR_DPS_IN)
        print(
            f"Turning forward by {SCOOPER_MOTOR_TURN_DEGREES} degrees at {DISPENSER_MOTOR_DPS_IN} dps..."
        )
        scooper_motor.set_position_relative(SCOOPER_MOTOR_TURN_DEGREES)
        time.sleep(seconds_in + MOTOR_SETTLE_SECONDS)

        scooper_motor.set_limits(dps=DISPENSER_MOTOR_DPS_OUT)
        seconds_out = abs(SCOOPER_MOTOR_TURN_DEGREES) / float(DISPENSER_MOTOR_DPS_OUT)
        print(
            f"Turning back by {-SCOOPER_MOTOR_TURN_DEGREES} degrees at {DISPENSER_MOTOR_DPS_OUT} dps..."
        )
        scooper_motor.set_position_relative(-SCOOPER_MOTOR_TURN_DEGREES)
        time.sleep(seconds_out + MOTOR_SETTLE_SECONDS)

        print("Scooped block.")
    finally:
        scooper_motor.set_power(0)


def spin_dispeser_motor_once():
    """Rotate a second motor by a fixed amount (default 90 degrees)."""
    dispenser_motor = Motor(PORT_MOTOR_DISPENSER)
    dispenser_motor.reset_encoder()

    try:
        dispenser_motor.set_limits(dps=DISPENSER_MOTOR_DPS)
        seconds = abs(DISPENSER_MOTOR_TURN_DEGREES) / float(DISPENSER_MOTOR_DPS)
        print(
            f"Turning second motor on port {PORT_MOTOR_DISPENSER} by {DISPENSER_MOTOR_TURN_DEGREES} degrees at {DISPENSER_MOTOR_DPS} dps..."
        )
        dispenser_motor.set_position_relative(DISPENSER_MOTOR_TURN_DEGREES)
        time.sleep(seconds + MOTOR_SETTLE_SECONDS)

        print("Stored block.")
    finally:
        dispenser_motor.set_power(0)


def collect_block():
    """Turn broom motor out/back, then rotate a second motor by 90 degrees."""
    spin_scooper_motor()
    spin_dispeser_motor_once()
    print("Collected block.")


if __name__ == "__main__":
    collect_block()
