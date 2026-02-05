from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
hub = ThisHub(broadcast_channel=2,observe_channels=[1])

# TOWER 1
t1_matrix = ColorLightMatrix(Port.A)
t1_distance_sensor = UltrasonicSensor(Port.C)

# POWER 1
p1_motor = Motor(Port.B)
p1_colour_sensor = ColorSensor(Port.D)

def t1_colour_function(colour):

    if colour == "r": 
        t1_matrix.on(Color.RED)
    elif colour == "y": 
        t1_matrix.on(Color.YELLOW)
    elif colour == "b": 
        t1_matrix.on(Color.BLUE)
    elif colour == "g": 
        t1_matrix.on(Color.GREEN)
    else:
        t1_matrix.off()

def p1_motor_function(action):

    if action == "l": 
        p1_motor.dc(25)
    elif action == "r": 
        p1_motor.dc(-25)
    elif action == "f": 
        p1_motor.dc(100)
    elif action == "s": 
        p1_motor.dc(0)

while True:

    # TOWER 1
    # Get distance and broadcast over hub
    t1_distance = t1_distance_sensor.distance()

    if t1_distance < 100:
        t1_distance_sensor.lights.on(100)
    else:
        t1_distance_sensor.lights.on(10)

    # POWER 1
    p1_reflection = p1_colour_sensor.reflection()

    # if p1_colour == 0:
    # p1_colour_sensor.lights.on(10)
    # else:
    if p1_reflection != 0:
        p1_colour_sensor.lights.on(100)

    # BROADCAST
    hub.ble.broadcast(str(t1_distance) + "," + str(p1_reflection))

    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None:

        ble_data = ble_string.split(",")

        if ble_data[0] == "2":
            if ble_data[1] == "t1c":
                t1_colour_function(ble_data[2])
            elif ble_data[1] == "p1m":
                p1_motor_function(ble_data[2])

    print("Observing player data...")

    wait(20)