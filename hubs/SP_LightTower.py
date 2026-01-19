from pybricks.hubs import PrimeHub, ThisHub

from pybricks.pupdevices import Motor, ColorSensor, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pybricks.pupdevices import ColorLightMatrix
from pybricks.pupdevices import UltrasonicSensor

hub = PrimeHub()
hub = ThisHub(broadcast_channel=2,observe_channels=[1])

matrix = ColorLightMatrix(Port.A)
distance_sensor = UltrasonicSensor(Port.C)

while True:

    controller_string = hub.ble.observe(1)

    distance = distance_sensor.distance()

    if distance < 100:

        distance_sensor.lights.on(100)

        if controller_string != None:

            controller_data = {item.split('=')[0]: int(item.split('=')[1]) for item in controller_string.split(',')}

            if controller_data["y"] == 1:
                matrix.on(Color.YELLOW)

            elif controller_data["x"] == 1:
                matrix.on(Color.BLUE)

            elif controller_data["a"] == 1:
                matrix.on(Color.GREEN)

            elif controller_data["b"] == 1:
                matrix.on(Color.RED)
    
    else:

        distance_sensor.lights.off()

        
    wait(200)