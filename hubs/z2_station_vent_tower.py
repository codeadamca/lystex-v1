from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, UltrasonicSensor, ColorLightMatrix, Light
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
hub = ThisHub(broadcast_channel=5,observe_channels=[1])

# TOWER 1
s1_motor_pointer = Motor(Port.A)
s1_matrix = ColorLightMatrix(Port.C)
s1_motor_fill = Motor(Port.E)

MAX_POINT_ROTATION = 180
MAX_FILL_ROTATION = 18 * 360

# POWER 1
# p1_motor = Motor(Port.B)
# p1_colour_sensor = ColorSensor(Port.D)

def s1_reset_function():

    s1_motor_pointer.run_until_stalled(250, Stop.COAST, 45)
    s1_motor_pointer.reset_angle(0)

    # s1_motor_fill.run_angle(500, -2880, Stop.HOLD, True);
    # print("Lowering")

    s1_motor_fill.run_until_stalled(1000, Stop.COAST, 45)
    s1_motor_fill.reset_angle(0)

    print("Activating")

    s1_motor_pointer.run_angle(100, -MAX_POINT_ROTATION, Stop.HOLD, True);
    s1_motor_fill.run_angle(100, -MAX_FILL_ROTATION, Stop.HOLD, True);


s1_reset_function()

def s1_fill_function(colour):

    print("fill")

def s1_point_function(colour):

    print("point")

    '''
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
    '''

'''
def p1_motor_function(action):

    if action == "l": 
        p1_motor.dc(25)
    elif action == "r": 
        p1_motor.dc(-25)
    elif action == "f": 
        p1_motor.dc(100)
    elif action == "s": 
        p1_motor.dc(0)
'''

while True:

    # STATION 1
    # No broadcast data

    # VENT 1

    # TOWER 3

    # BROADCAST
    # hub.ble.broadcast(str(t1_distance) + "," + str(p1_reflection))

    # OBSERVE DATA
    ble_string = hub.ble.observe(1)

    if ble_string != None:

        ble_data = ble_string.split(",")

        if ble_data[0] == "5":
            if ble_data[1] == "s1p":
                s1_point_function(ble_data[2])
            elif ble_data[1] == "s1f":
                s1_fill_function(ble_data[2])
            elif ble_data[1] == "s1r":
                s1_reset_function()

    # print("Observing player data...")

    wait(20)