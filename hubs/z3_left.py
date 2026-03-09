from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 8
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
    "p2m": "s"
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

# ==========================================
# PORTS
# ==========================================

# POWER 1
p2_motor = Motor(Port.A)
p2_colour_sensor = ColorSensor(Port.C)

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
    p2_reflection = p2_colour_sensor.reflection()

    # MAKE LOCAL CHANEGS
    if p2_reflection != 0:
        hub.ble.broadcast("p2")
        p2_colour_sensor.lights.on(100)
    
    else:
        hub.ble.broadcast(None)
        p2_colour_sensor.lights.on(LIGHT_INTENSITY)

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Power Two
    if config["p2m"] == "l": 
        p2_motor.dc(25)
    elif config["p2m"] == "r": 
        p2_motor.dc(-25)
    elif config["p2m"] == "f": 
        p2_motor.dc(100)
    elif config["p2m"] == "s":
        p2_motor.dc(0)

    wait(10)