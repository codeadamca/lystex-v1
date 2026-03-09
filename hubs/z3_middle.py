from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, Light, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import urandom as random

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 9

LIGHT_INTENSITY = 21

# ==========================================
# HUB
# ==========================================

hub = PrimeHub()
hub = ThisHub(broadcast_channel=CHANNEL,observe_channels=[1])

# ==========================================
# FUNCTIONS
# ==========================================

config = {
    "v4s": "f",
    "v5s": "f",
    "v6s": "f",
    "g3m": "s",
    "a9": ""
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

def g3_reset_function():

    global config

    config = {
        "v4s": "f",
        "v5s": "f",
        "v6s": "f",
        "g3m": "s",
        "a9": ""
    }

    g3_motor.run_until_stalled(-250, Stop.HOLD, 45)
    g3_motor.reset_angle(0)

    wait(2500)


# ==========================================
# PORTS
# ==========================================

# Gate 2
# c3_colour_sensor = ColorSensor(Port.E)
c3_distance_sensor = UltrasonicSensor(Port.B)

# VENT 1
v4a_light = Light(Port.A)
v4b_light = Light(Port.C)
v5_light = Light(Port.D)
v6_light = Light(Port.E)

# GATE 3
g3_motor = Motor(Port.F)

# ==========================================
# SETUP
# ==========================================
g3_reset_function()

# ==========================================
# PLAY LOOP
# ==========================================

while True:

    # ==========================================
    # LOCAL 

    # GET LOCAL DATA
    # c3_reflection = c3_colour_sensor.reflection()
    c3_distance = c3_distance_sensor.distance()
    
    if c3_distance < 100:
        hub.ble.broadcast("c3")
        c3_distance_sensor.lights.on(100)

    else:
        hub.ble.broadcast(None)
        c3_distance_sensor.lights.on(LIGHT_INTENSITY)

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Vent Four
    if config["v4s"] == "n":
        v4a_light.on(100)
        v4b_light.on(100)
    elif config["v4s"] == "m":
        v4a_light.on(50)
        v4b_light.on(5)
    elif config["v4s"] == "r":
        v4a_light.on(random.randint(0, 100))
        v4b_light.on(random.randint(0, 100))
    elif config["v4s"] == "f":
        v4a_light.off()
        v4b_light.off()

    # ==========================================
    # Vent Five
    if config["v5s"] == "n":
        v5_light.on(100)
    elif config["v5s"] == "m":
        v5_light.on(50)
    elif config["v5s"] == "r":
        v5_light.on(random.randint(0, 100))
    elif config["v5s"] == "f":
        v5_light.off()

    # ==========================================
    # Vent Six
    if config["v6s"] == "n":
        v6_light.on(100)
    elif config["v6s"] == "m":
        v6_light.on(50)
    elif config["v6s"] == "r":
        v6_light.on(random.randint(0, 100))
    elif config["v6s"] == "f":
        v6_light.off()

    # ==========================================
    # Home One
    if config["g3m"] == "l": 
        # g3_motor.run_target(250, 0, Stop.HOLD, False)
        g3_motor.run_until_stalled(250, Stop.HOLD, 45)
    elif config["g3m"] == "r": 
        # g3_motor.run_target(250, 1440, Stop.HOLD, False)
        g3_motor.run_until_stalled(250, Stop.HOLD, 45)
    elif config["g3m"] == "s":
        g3_motor.dc(0)

    # ==========================================
    # Actions
    if config["a9"] == "r":
        print("reset")
        g3_reset_function()
        config["a9"] = ""

    wait(10)