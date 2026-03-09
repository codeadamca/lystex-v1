from pybricks.hubs import InventorHub, ThisHub

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 4

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
    "t2c": "r"
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

# TOWER 2
t2_matrix = ColorLightMatrix(Port.A)
t2_distance_sensor = UltrasonicSensor(Port.C)

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
    t2_distance = t2_distance_sensor.distance()

    # MAKE LOCAL CHANEGS
    if t2_distance < 100:
        hub.ble.broadcast("t2")
        t2_distance_sensor.lights.on(100)

    else:
        hub.ble.broadcast(None)
        t2_distance_sensor.lights.on(LIGHT_INTENSITY)    

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Tower Two
    if config["t2c"] == "r": 
        t2_matrix.on(Color.RED)
    elif config["t2c"] == "y": 
        t2_matrix.on(Color.YELLOW)
    elif config["t2c"] == "b": 
        t2_matrix.on(Color.BLUE)
    elif config["t2c"] == "g": 
        t2_matrix.on(Color.GREEN)
    else:
        t2_matrix.off()

    wait(10)