# -----------------------------------------------------
# SENSOR PORTS
PORT_TOUCH_SENSOR_STOP = 2
PORT_COLOR_SENSOR = 4
PORT_GYRO = 1
PORT_ULTRASONIC = 3

# MOTOR PORTS - PORT B IS FAULTY.
PORT_MOTOR_SCOOPER = "B"
PORT_MOTOR_DISPENSER = "C"
PORT_MOTOR_RIGHT = "D"
PORT_MOTOR_LEFT = "A"
RADIUS_WHEEL = 2  # in cm

# -----------------------------------------------------
# Block collection motor config
MOTOR_SETTLE_SECONDS = 0.5
DISPENSER_MOTOR_TURN_DEGREES = 110
DISPENSER_MOTOR_DPS = 250
DISPENSER_MOTOR_DROPOFF_DPS = 200

SCOOPER_MOTOR_TURN_DEGREES = 260
DISPENSER_MOTOR_DPS_IN = 280
DISPENSER_MOTOR_DPS_OUT = 150

# -----------------------------------------------------
# Navigation config
SPEED_DPS_STRAIGHT = 400

SPEED_DPS_TURN = 100
DISTANCE_CM_TURN = 10.5  # for 90 deg turn

# Hallway navigation PID constants

FAST_HALLWAY_BASE_SPEED = 260  # dps, nominal forward speed
FAST_HALLWAY_MIN_SPEED = 230  # dps floor (keep robot moving)
FAST_HALLWAY_MAX_SPEED = 300  # dps ceiling (prevent wheel slip)
HALLWAY_BASE_SPEED = 120  # dps, nominal forward speed
HALLWAY_MIN_SPEED = 90  # dps floor (keep robot moving)
HALLWAY_MAX_SPEED = 160  # dps ceiling (prevent wheel slip)

FAST_HALLWAY_BASE_SPEED = 260  # dps, nominal forward speed
FAST_HALLWAY_MIN_SPEED = 230  # dps floor (keep robot moving)
FAST_HALLWAY_MAX_SPEED = 300  # dps ceiling (prevent wheel slip)
HALLWAY_LOOP_SLEEP = 0.02  # seconds between control loop iterations

# Combined error: weighted_error = GYRO_WEIGHT * gyro_error + US_WEIGHT * us_error
# gyro_error: degrees (angle - straight_angle)
# us_error:   cm     (current_distance - target_distance)
HALLWAY_GYRO_WEIGHT = 1.0  # weight on gyro error term

HALLWAY_KP = 10.0  # proportional gain
HALLWAY_KI = 0.1  # integral gain
HALLWAY_KD = 2.0  # derivative gain
HALLWAY_INTEGRAL_CLAMP = 50.0  # anti-windup: clamp integral accumulator

# -----------------------------------------------------
# Colour sensor config
COLOUR_READINGS_MAP = {
    (0.8270283597, 0.09330910053, 0.07966253976): "RED",
    (0.4119988175, 0.4934499177, 0.09455126476): "GREEN",
    (0.306345733, 0.3369803063, 0.3566739606): "BLUE",
    (0.5969191562, 0.3411060927, 0.06197475105): "YELLOW",
    (0.7399380805, 0.213622291, 0.04643962848): "ORANGE",
}

COLOUR_LUMINOSITY_MAP = {(400, 1000): "WHITE"}
