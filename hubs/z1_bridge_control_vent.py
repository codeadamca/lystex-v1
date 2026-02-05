from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, ColorLightMatrix, Light, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
hub = ThisHub(broadcast_channel=3,observe_channels=[1])

# CONTROL 1
c1_matrix = ColorLightMatrix(Port.A)
c1_distance_sensor = UltrasonicSensor(Port.C)

# VENT 1
v1_light = Light(Port.E)

# BRIDGE 1
b1_motor = Motor(Port.B)

def c1_colour_function(colour):

    if colour == "r": 
        c1_matrix.on(Color.RED)
    elif colour == "g": 
        c1_matrix.on(Color.GREEN)
    else:
        c1_matrix.off()

def v1_light_function(status):

    if status == "n": 
        v1_light.on(100)
    elif status == "f": 
        v1_light.off()

def b1_motor_function(action):

    if action == "o": 
        b1_motor.run_until_stalled(-500, Stop.COAST, 45)
    elif action == "c": 
        b1_motor.run_until_stalled(500, Stop.COAST, 45)

while True:

    # TOWER 1
    # Get distance and broadcast over hub
    c1_distance = c1_distance_sensor.distance()

    if c1_distance < 100:
        c1_distance_sensor.lights.on(100)
    else:
        c1_distance_sensor.lights.on(10)

    # VENT 1
    
    # GATE 1

    # BROADCAST
    hub.ble.broadcast(str(c1_distance))

    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None:

        ble_data = ble_string.split(",")

        if ble_data[0] == "3":
            if ble_data[1] == "c1c":
                c1_colour_function(ble_data[2])
            elif ble_data[1] == "v1s":
                v1_light_function(ble_data[2])
            elif ble_data[1] == "g1s":
                b1_motor_function(ble_data[2])

    print("Observing player data...")

    wait(20)