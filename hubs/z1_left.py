from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 2
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
    "t1c": "y",
    "p1m": "s"
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

# TOWER 1
t1_matrix = ColorLightMatrix(Port.A)
t1_distance_sensor = UltrasonicSensor(Port.C)

# POWER 1
p1_motor = Motor(Port.B)
p1_colour_sensor = ColorSensor(Port.D)

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
    t1_distance = t1_distance_sensor.distance()
    p1_reflection = p1_colour_sensor.reflection()

    # MAKE LOCAL CHANEGS
    if t1_distance < 100:
        hub.ble.broadcast("t1")
        t1_distance_sensor.lights.on(100)
        p1_colour_sensor.lights.on(LIGHT_INTENSITY)

    elif p1_reflection != 0:
        hub.ble.broadcast("p1")
        t1_distance_sensor.lights.on(LIGHT_INTENSITY)
        p1_colour_sensor.lights.on(100)
    
    else:
        hub.ble.broadcast(None)
        t1_distance_sensor.lights.on(LIGHT_INTENSITY)
        p1_colour_sensor.lights.on(LIGHT_INTENSITY)

    # ==========================================
    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None: update(ble_string)

    # ==========================================
    # Tower One
    if config["t1c"] == "r": 
        t1_matrix.on(Color.RED)
    elif config["t1c"] == "y": 
        t1_matrix.on(Color.YELLOW)
    elif config["t1c"] == "b": 
        t1_matrix.on(Color.BLUE)
    elif config["t1c"] == "g": 
        t1_matrix.on(Color.GREEN)
    else:
        t1_matrix.off()

    # ==========================================
    # Power One
    if config["p1m"] == "l": 
        p1_motor.dc(25)
    elif config["p1m"] == "r": 
        p1_motor.dc(-25)
    elif config["p1m"] == "f": 
        p1_motor.dc(100)
    elif config["p1m"] == "s":
        p1_motor.dc(0)

    wait(10)