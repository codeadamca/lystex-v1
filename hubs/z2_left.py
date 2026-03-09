from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, UltrasonicSensor, ColorLightMatrix, Light
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import urandom as random

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 5

LIGHT_INTENSITY = 21

POWER_MAX_ANGLE = 180
POWER_MAX_LEVEL = 16 * 360

# ==========================================
# HUB
# ==========================================

hub = PrimeHub()
hub = ThisHub(broadcast_channel=CHANNEL,observe_channels=[1])

# ==========================================
# FUNCTIONS
# ==========================================

config = {
    "t3c": "g",
    "s1c": "r",
    "s1f": "0",
    "s1p": "0",
    "v3s": "f",
    "a5": ""
}

def update(data):

    global config

    channel, data = data.split(":")

    if int(channel) == CHANNEL:

        print("Data: " + data)

        pairs = data.split(",")

        for pair in pairs:

            key, value = pair.split("=")

            try:
                config[key] = int(value)
            except ValueError:
                config[key] = value

def s1_reset_function():

    global config

    config = {
        "t3c": "g",
        "s1c": "r",
        "s1f": "0",
        "s1p": "0",
        "v3s": "f",
        "a5": ""
    }

    track = s1_motor_pointer.run_until_stalled(250, Stop.HOLD, 45)
    s1_motor_pointer.reset_angle(0)

    # s1_motor_fill.run_angle(500, -2880, Stop.HOLD, True)
    # print("Lowering")

    track = s1_motor_fill.run_until_stalled(1000, Stop.HOLD, 35)
    s1_motor_fill.reset_angle(0)

    # print("Activating")
    # s1_motor_pointer.run_angle(100, -MAX_POINT_ROTATION, Stop.HOLD, True)
    # s1_motor_fill.run_angle(100, -MAX_FILL_ROTATION, Stop.HOLD, True)

    s1_matrix.on(Color.RED)

    wait(3000)

# ==========================================
# PORTS
# ==========================================

# TOWER 1
s1_motor_pointer = Motor(Port.E)
s1_motor_fill = Motor(Port.A)
s1_matrix = ColorLightMatrix(Port.C)

# TOWER 3
t3_matrix = ColorLightMatrix(Port.F)
t3_distance_sensor = UltrasonicSensor(Port.D)

# LIGHT 2
v3_light = Light(Port.B)

# ==========================================
# SETUP
# ==========================================

# ==========================================
# PLAY LOOP
# ==========================================

while True:

    # ==========================================
    # LOCAL

    # GET LOCAL DATA
    t3_distance = t3_distance_sensor.distance()

    # MAKE LOCAL CHANEGS
    if t3_distance < 100:
        hub.ble.broadcast("t3")
        t3_distance_sensor.lights.on(100)

    else:
        hub.ble.broadcast(None)
        t3_distance_sensor.lights.on(LIGHT_INTENSITY)

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Tower Three
    if config["t3c"] == "r": 
        t3_matrix.on(Color.RED)
    elif config["t3c"] == "y": 
        t3_matrix.on(Color.YELLOW)
    elif config["t3c"] == "b": 
        t3_matrix.on(Color.BLUE)
    elif config["t3c"] == "g": 
        t3_matrix.on(Color.GREEN)
    else:
        t3_matrix.off()

    # ==========================================
    # Station One 
    s1_motor_pointer.run_target(500, -int(config["s1p"]), Stop.HOLD, False)

    target_angle = int(-POWER_MAX_LEVEL * (int(config["s1f"]) * 20 / 100))
    s1_motor_fill.run_target(1000, target_angle, Stop.HOLD, False)

    # print(str(config["s1f"]) + " - " + str(target_angle))

    if config["s1f"] in [5,4]: s1_matrix.on(Color.GREEN)
    elif config["s1f"] in [3,2,1]: s1_matrix.on(Color.ORANGE)
    else: s1_matrix.on(Color.RED)

    # ==========================================
    # Vent Two
    if config["v3s"] == "n":
        v3_light.on(100)
    elif config["v3s"] == "m":
        v3_light.on(50)
    elif config["v3s"] == "r":
        v3_light.on(random.randint(0, 100))
    elif config["v3s"] == "f":
        v3_light.off()

    # ==========================================
    # Actions
    if config["a5"] == "r":
        s1_reset_function()
        config["a5"] = ""

    wait(10)