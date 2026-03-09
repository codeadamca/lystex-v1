from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, Light, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import urandom as random

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 6

LIGHT_INTENSITY = 21

ROVER_MAX_DISTANCE = 720

# ==========================================
# HUB
# ==========================================

hub = PrimeHub()
hub = ThisHub(broadcast_channel=CHANNEL,observe_channels=[1])

# ==========================================
# FUNCTIONS
# ==========================================

config = {
    "r1s": "f",
    "r1m": "s",
    "g2s": "s",
    "g2c": "n",
    "a6": ""
}

def update(data):

    global config

    channel, data = data.split(":")

    if int(channel) == CHANNEL:

        print(data)

        pairs = data.split(",")

        for pair in pairs:

            key, value = pair.split("=")

            try:
                config[key] = int(value)
            except ValueError:
                config[key] = value

def r1_reset_function():

    global config

    config = {
        "r1s": "f",
        "r1m": "s",
        "g2s": "s",
        "g2c": "n",
        "a6": ""
    }

    r1_motor.run_until_stalled(250, Stop.HOLD, 65)
    r1_motor.reset_angle(0)

    r1_light.off()
    r1_spotlight.off()

    wait(3000)

# ==========================================
# PORTS
# ==========================================

# ROVER 1
r1_motor = Motor(Port.C)
r1_light = Light(Port.A)
r1_spotlight = Light(Port.E)

# GATE 2
g2_motor_left = Motor(Port.B)
g2_motor_right = Motor(Port.F)
g2_matrix = ColorLightMatrix(Port.D)

# ==========================================
# SETUP
# ==========================================

# ==========================================
# PLAY LOOP
# ==========================================

while True:

    # ==========================================
    # LOCAL 

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Vent One
    if config["r1s"] == "n":
        r1_light.on(100)
        r1_spotlight.on(100)
    elif config["r1s"] == "m":
        r1_light.on(50)
        r1_spotlight.on(50)
    elif config["r1s"] == "r":
        r1_light.on(random.randint(0, 100))
        r1_spotlight.on(random.randint(0, 100))
    elif config["r1s"] == "f":
        r1_light.off()
        r1_spotlight.off()

    # ==========================================
    # Rover One
    if config["r1m"] == "b":
        r1_motor.run_target(150, 0, Stop.HOLD, False)
    elif config["r1m"] == "f":
        r1_motor.run_target(150, -ROVER_MAX_DISTANCE, Stop.HOLD, False)

    # ==========================================
    # Gate Two
    if config["g2s"] == "l": 
        g2_motor_left.run(250)
        g2_motor_right.run(250)
    elif config["g2s"] == "r": 
        g2_motor_left.run(-250)
        g2_motor_right.run(-250)
    elif config["g2s"] == "s":
        g2_motor_left.stop()
        g2_motor_right.stop()

    # ==========================================
    # Gate Two Light
    if config["g2c"] == "g":
        g2_matrix.on(Color.GREEN)
    elif config["g2c"] == "r":
        g2_matrix.on(Color.RED)
    elif config["g2c"] == "n":
        g2_matrix.off()

    # ==========================================
    # Actions
    if config["a6"] == "r":
        r1_reset_function()
        config["a6"] = ""

    wait(10)
