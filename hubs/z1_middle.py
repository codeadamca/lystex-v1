from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, ColorLightMatrix, Light, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import urandom as random

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 3

LIGHT_INTENSITY = 21

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
    "c1c": "n",
    "g1s": "c",
    "v1s": "f",
    "a3": ""
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

def g1_reset_function():

    global config

    config = {
        "c1c": "n",
        "g1s": "c",
        "v1s": "f",
        "a3": ""
    }

    track = g1_motor.run_until_stalled(500, Stop.HOLD, 45)
    g1_motor.reset_angle(0)

    wait(3000)


# ==========================================
# PORTS
# ==========================================

# CONTROL 1
c1_matrix = ColorLightMatrix(Port.A)
c1_distance_sensor = UltrasonicSensor(Port.C)

# VENT 1
v1_light = Light(Port.D)

# GATE 1
g1_motor = Motor(Port.B)

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
    c1_distance = c1_distance_sensor.distance()

    # MAKE LOCAL CHANEGS
    if c1_distance < 100:
        hub.ble.broadcast("c1")
        c1_distance_sensor.lights.on(100)

    else:
        hub.ble.broadcast(None)
        c1_distance_sensor.lights.on(LIGHT_INTENSITY)

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Vent One
    if config["v1s"] == "n":
        v1_light.on(100)
    elif config["v1s"] == "m":
        v1_light.on(50)
    elif config["v1s"] == "r":
        v1_light.on(random.randint(0, 100))
    elif config["v1s"] == "f":
        v1_light.off()

    # ==========================================
    # Control One
    if config["c1c"] == "g":
        c1_matrix.on(Color.GREEN)
    elif config["c1c"] == "r":
        c1_matrix.on(Color.RED)
    elif config["c1c"] == "n":
        c1_matrix.off()

    # ==========================================
    # Gate One
    if config["g1s"] == "o":
        g1_motor.run_target(500, -POWER_MAX_LEVEL, Stop.HOLD, False)
    elif config["g1s"] == "c":
        g1_motor.run_target(500, 0, Stop.HOLD, False)
        
    # ==========================================
    # Actions
    if config["a3"] == "r":
        print("reset")
        g1_reset_function()
        config["a3"] = ""

    wait(10)