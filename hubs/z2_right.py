from pybricks.hubs import InventorHub, ThisHub

from pybricks.pupdevices import UltrasonicSensor, Light, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import urandom as random

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 7

LIGHT_INTENSITY = 21

# ==========================================
# HUB
# ==========================================

hub = InventorHub()
hub = ThisHub(broadcast_channel=CHANNEL,observe_channels=[1])

# ==========================================
# FUNCTIONS
# ==========================================

config = {
    "c2c": "n",
    "v2s": "f"
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

# ==========================================
# PORTS
# ==========================================

# CONTROL 1
c2_matrix = ColorLightMatrix(Port.A)
# c2_light = Light(Port.A)
c2_distance_sensor = UltrasonicSensor(Port.C)

# VENT 1
v2_light = Light(Port.B)

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
    c2_distance = c2_distance_sensor.distance()

    # MAKE LOCAL CHANEGS
    if c2_distance < 100:
        hub.ble.broadcast("c2")
        c2_distance_sensor.lights.on(100)

    else:
        hub.ble.broadcast(None)
        c2_distance_sensor.lights.on(LIGHT_INTENSITY)

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Vent One
    if config["v2s"] == "n":
        v2_light.on(100)
    elif config["v2s"] == "m":
        v2_light.on(50)
    elif config["v2s"] == "r":
        v2_light.on(random.randint(0, 100))
    elif config["v2s"] == "f":
        v2_light.off()

    # ==========================================
    # Control One
    if config["c2c"] == "g":
        c2_matrix.on(Color.GREEN)
        # c2_light.on(100)
    elif config["c2c"] == "r":
        c2_matrix.on(Color.RED)
        # c2_light.on(20)
    elif config["c2c"] == "n":
        c2_matrix.off()
        # c2_light.off()

    wait(10)