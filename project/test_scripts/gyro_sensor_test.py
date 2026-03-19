#!/usr/bin/env python3

import time

from utils.brick import EV3GyroSensor, reset_brick


DPS_DEADBAND = 2


def main():
    gyro = EV3GyroSensor(1, mode=EV3GyroSensor.Mode.BOTH)
    print("Gyro initialized on port 1.")

    try:
        gyro.wait_ready()
        gyro.reset_measure()
        gyro.wait_ready()

        start = gyro.get_both_measure()
        if start is None:
            print("Could not read gyro origin value.")
            return
        origin, _ = start
        turned = 0

        print(f"Origin angle: {origin}")
        print("Rotate the sensor/robot. Press Ctrl+C to stop.\n")

        while True:
            reading = gyro.get_both_measure()
            if reading is None:
                print("No gyro data")
            else:
                current, dps = reading
                if abs(dps) >= DPS_DEADBAND:
                    delta = current - origin
                    turned = delta % 360 if delta >= 0 else -((-delta) % 360)
                print(f"Turned from origin: {turned:.1f} degrees")
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        reset_brick()


if __name__ == "__main__":
    main()
