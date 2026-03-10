from pybricks.hubs import EssentialHub
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pybricks.iodevices import XboxController

hub = EssentialHub()

drive_motor = DCMotor(Port.A)

ROVER_MAX_POWER = 30

print("Searching for controller...")
hub.light.on(Color.BLUE)
xbox = XboxController()
hub.light.on(Color.GREEN)
print("Connected!")

while True:

    try:
        joystick_left = xbox.joystick_left()

    except OSError:
        joystick_left = [0, 0]

    drive_speed = joystick_left[1] * (-1) / 100

    if abs(drive_speed) < 0.2:
        drive_speed = 0
        
    if drive_speed < 0:
        hub.light.on(Color.GREEN)
    elif drive_speed > 0:
        hub.light.on(Color.RED)
    else:
        hub.light.on(Color.BLUE)

    drive_motor.dc(drive_speed * ROVER_MAX_POWER)

