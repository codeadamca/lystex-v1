from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import ColorLightMatrix, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
hub = ThisHub(broadcast_channel=4,observe_channels=[1])

# TOWER 2
t2_matrix = ColorLightMatrix(Port.A)
t2_distance_sensor = UltrasonicSensor(Port.C)

def t2_colour_function(colour):

    if colour == "r": 
        t2_matrix.on(Color.RED)
    elif colour == "y": 
        t2_matrix.on(Color.YELLOW)
    elif colour == "b": 
        t2_matrix.on(Color.BLUE)
    elif colour == "g": 
        t2_matrix.on(Color.GREEN)
    else:
        t2_matrix.off()

while True:

    # TOWER 2
    # Get distance and broadcast over hub
    t2_distance = t2_distance_sensor.distance()

    if t2_distance < 100:
        t2_distance_sensor.lights.on(100)
    else:
        t2_distance_sensor.lights.on(10)

    # BROADCAST
    hub.ble.broadcast(str(t2_distance))

    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None:

        ble_data = ble_string.split(",")

        if ble_data[0] == "4":
            if ble_data[1] == "t2c":
                t2_colour_function(ble_data[2])

    print("Observing player data...")

    wait(20)