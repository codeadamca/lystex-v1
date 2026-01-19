from pybricks.hubs import EssentialHub, ThisHub
from pybricks.pupdevices import Motor, ColorSensor, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pybricks.iodevices import XboxController

hub = EssentialHub()
hub = ThisHub(broadcast_channel=1,observe_channels=[2])

# Motor A is your steering motor
steering_motor = Motor(Port.B)
# Motor B is your drive motor (back wheels)
drive_motor = Motor(Port.A)

# 2. Connect to the Xbox Controller
hub.light.on(Color.BLUE)

print("Searching for controller...")
xbox = XboxController()
hub.light.on(Color.GREEN)
print("Connected!")

steering_motor.reset_angle(0)

MAX_ANGLE = 30

# 3. Main Control Loop
while True:
    
    drive_speed = xbox.joystick_left()[1] * (-5)
    
    steer_speed = xbox.joystick_right()[0] * (-1)
    steer_speed = (steer_speed / 100) * MAX_ANGLE
    
    # Stop motors if sticks are in the deadzone (near center)
    if abs(drive_speed) < 50:
        drive_speed = 0
    if abs(steer_speed) < 20:
        steer_speed = 0
    
    drive_motor.run(drive_speed)
    steering_motor.track_target(steer_speed)

    controller_data = {}

    if Button.Y in xbox.buttons.pressed():
        controller_data["y"] = 1
    else:
        controller_data["y"] = 0

    if Button.X in xbox.buttons.pressed():
        controller_data["x"] = 1
    else:
        controller_data["x"] = 0

    if Button.A in xbox.buttons.pressed():
        controller_data["a"] = 1
    else:
        controller_data["a"] = 0
    
    if Button.B in xbox.buttons.pressed():
        controller_data["b"] = 1
    else:
        controller_data["b"] = 0

    controller_string = ",".join([f"{k}={v}" for k, v in controller_data.items()])
    
    hub.ble.broadcast(controller_string)
        
    wait(20)