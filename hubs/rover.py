from pybricks.hubs import EssentialHub, ThisHub

from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pybricks.iodevices import XboxController

hub = EssentialHub()
hub = ThisHub(broadcast_channel=1,observe_channels=[2,3,4])

# 1 - rover
# 2 - z1_power_tower
# 3 - z1_bridge_control_vent
# 4 - z1_tower
# 5 - z2_station_vent_tower
# 6 - z2_gate_vent_car
# 7 - z2_control_x2
# 8 - z3_tower_vent
# 9 - z3_home_vent

'''
def g1_check():

    global t1_colour
    t1_colour_previous = t1_colour

    t1_set_colour("")
    wait(500)

    t1_set_colour("r")
    wait(500)

    t1_set_colour(t1_colour_previous)
    wait(500)

    t1_set_colour("")
    wait(500)

    t1_set_colour(t1_colour_previous)
    wait(500)

    if t1_colour_previous == "r":
        sound_success("3")
        return True

    else:
        sound_error("3")
        return False
'''
# ==========================================
# CHANNEL 2
# ==========================================

def t1_set_colour(colour):

    global t1_colour
    t1_colour = colour
    hub.ble.broadcast("2,t1c," + colour)
    wait(250)
    hub.ble.broadcast(None)

def p1_set_motor(action):

    global ps_level, p1_status

    if p1_status != action:
        p1_status = action
        hub.ble.broadcast("2,p1m," + action)
        wait(250)
        hub.ble.broadcast(None)

# ==========================================
# CHANNEL 3
# ==========================================

def c1_set_colour(colour):

    global c1_colour
    c1_colour = colour
    hub.ble.broadcast("3,c1c," + colour)
    wait(250)
    hub.ble.broadcast(None)

def v1_set_lights(status):

    global v1_status
    v1_status = status
    hub.ble.broadcast("3,v1s," + status)
    wait(250)
    hub.ble.broadcast(None)

def g1_set_status(status):

    global g1_status
    g1_status = status
    hub.ble.broadcast("3,g1s," + status)
    wait(250)
    hub.ble.broadcast(None)

# ==========================================
# CHANNEL 4
# ==========================================

def t2_set_colour(colour):

    global t2_colour
    t2_colour = colour
    hub.ble.broadcast("4,t2c," + colour)
    wait(250)
    hub.ble.broadcast(None)

def sound_success(channel):
    hub.ble.broadcast(channel + ",s")
    wait(50)
    hub.ble.broadcast(None)

def sound_error(channel):
    hub.ble.broadcast(channel + ",e")
    wait(50)
    hub.ble.broadcast(None)

# ==========================================
# CHANNEL 5
# ==========================================

def s1_reset():

    hub.ble.broadcast("5,s1r")
    wait(250)
    hub.ble.broadcast(None)

# Motor A is your steering motor
steering_motor = Motor(Port.B)
steering_motor.reset_angle(0)
MAX_ANGLE = 30

# Motor B is your drive motor (back wheels)
drive_motor = Motor(Port.A)

# Connect to the Xbox Controller
hub.light.on(Color.BLUE)

print("Searching for controller...")
xbox = XboxController()
hub.light.on(Color.GREEN)
print("Connected!")

print("Setting Tower One to BLUE")
t1_colour = "g"
t1_set_colour("g")

print("Setting Tower Two to RED")
t2_colour = "r"
t2_set_colour("r")

print("Setting Power One to 0 degrees")
ps_level = 0
ps_angel = 0
p1_status = "s"
# function

print("Setting Control One to RED")
c1_colour = "r"
c1_set_colour("r")

print("Turning off Vent One")
v1_status = "f"
v1_set_lights("f")

print("Closing Gate One")
g1_pass = "w"
g1_status = "c"
g1_set_status("c")

print("Resetting Station One")
ps_angel = 0
ps_level = 0
s1_reset()

'''
print("Closing Gate One")
g1_status = "c"
hub.ble.broadcast("3,g,c")
wait(100)
'''

# Main Control Loop
print("Play code started...")
while True:

    # ==========================================
    # DRIVING
    # ==========================================

    drive_speed = xbox.joystick_left()[1] * (-2.5)
    
    steer_speed = xbox.joystick_right()[0] * (-1)
    steer_speed = (steer_speed / 100) * MAX_ANGLE
    
    # Stop motors if sticks are in the deadzone (near center)
    if abs(drive_speed) < 50:
        drive_speed = 0
        
    if drive_speed < 0:
        hub.light.on(Color.GREEN)
    elif drive_speed > 0:
        hub.light.on(Color.RED)
    else:
        hub.light.on(Color.BLUE)

    if abs(steer_speed) < 5:
        steer_speed = 0
    
    drive_motor.run(drive_speed)
    steering_motor.track_target(steer_speed)
    
    # ==========================================
    # CHANNEL 2 - TOWER 1 AND POWER 1
    # ==========================================

    # Data coming from channel two is [t1_distance,p1_reflection]
    c2_string = hub.ble.observe(2)

    if c2_string != None:
        c2_data = c2_string.split(",")
        t1_distance = int(c2_data[0])
        p1_reflection = int(c2_data[1])
    else: 
        t1_distance = 2000
        p1_reflection = 0

    # TOWER 1
    if t1_distance < 100:
        if Button.A in xbox.buttons.pressed():
            t1_set_colour("g")
        elif Button.B in xbox.buttons.pressed():
            t1_set_colour("r")
        elif Button.X in xbox.buttons.pressed():
            t1_set_colour("b")
        elif Button.Y in xbox.buttons.pressed():
            t1_set_colour("y")

    # POWER 1
    if p1_reflection > 0:
        if Button.RB in xbox.buttons.pressed():
            p1_set_motor("r")
            ps_angel -= 1
        elif Button.LB in xbox.buttons.pressed():
            p1_set_motor("l")
            ps_angel += 1
        elif Button.Y in xbox.buttons.pressed():
            if ps_level < 1000:
                p1_set_motor("f")
                ps_level += 1
            else:
                p1_set_motor("s")
        else:
            p1_set_motor("s")

        if ps_angel < 0: ps_angel = 0
        elif ps_angel > 300: ps_angel = 300

        if ps_level < 0: ps_level = 0
        elif ps_level > 500: ps_level = 500

    else:
        p1_set_motor("s")

    # ==========================================
    # CHANNEL 3 - CONTROL 1
    # ==========================================

    # Data coming from channel three is [c1_distance]
    c3_string = hub.ble.observe(3)

    if c3_string != None:
        c1_distance = int(c3_string)
    else: 
        c1_distance = 2000

    # CONTROL 1
    if t1_colour == "b" and t2_colour == "y" and g1_pass == "w":
        g1_pass = "r"
        c1_set_colour("g")
    elif t1_colour != "b" and t2_colour != "y" and g1_pass == "r":
        g1_pass = "w"
        c1_set_colour("r")

    if c1_distance < 100:
        if t1_colour == "b" and t2_colour == "y":
            if Button.DOWN in xbox.buttons.pressed():
                g1_set_status("o")
            elif Button.UP in xbox.buttons.pressed():
                g1_set_status("c")

    # ==========================================
    # CHANNEL 4 - TOWER 2
    # ==========================================
    
    # Data coming from channel four is [t2_distance]
    c4_string = hub.ble.observe(4)

    if c4_string != None:
        # c4_data = c4_string.split(",")
        # t2_distance = int(c4_data[0])
        # p2_reflection = int(c4_data[1])
        t2_distance = int(c4_string)
    else: 
        t2_distance = 2000

    # TOWER 2
    if t2_distance < 100:
        if Button.A in xbox.buttons.pressed():
            t2_set_colour("g")
        elif Button.B in xbox.buttons.pressed():
            t2_set_colour("r")
        elif Button.X in xbox.buttons.pressed():
            t2_set_colour("b")
        elif Button.Y in xbox.buttons.pressed():
            t2_set_colour("y")

    '''
    g1_string = hub.ble.observe(3)

    if g1_string != None:
        # t1_data = t1_string.split(",")
        # t1_distance = t1_data[0]
        g1_distance = g1_string
    else: 
        g1_distance = 2000

    if g1_distance < 100:

        if Button.UP in xbox.buttons.pressed():

            if g1_check():
                hub.ble.broadcast("3,g,c")
                wait(100)
                hub.ble.broadcast(None)

        elif Button.DOWN in xbox.buttons.pressed():

            if g1_check():
                hub.ble.broadcast("3,g,o")
                wait(100)
                hub.ble.broadcast(None)
    '''


    '''
    t2_string = hub.ble.observe(3)

    if t2_string != None:
        t2_data = {item.split("=")[0]: (item.split("=")[1]) for item in t2_string.split(",")}
        t2 = t2_data.get("t2", "")

    t3_string = hub.ble.observe(4)

    if t3_string != None:
        t3_data = {item.split("=")[0]: (item.split("=")[1]) for item in t3_string.split(",")}
        t3 = t3_data.get("t3", "")
    '''

    '''
    if t1 == "b" and t2 == "b" and t3 == "y":
        g1 = "u"
    else: 
        g1 = "l"

    controller_string += g1

    # print(controller_string + t1 + t2 + t3)
    # hub.ble.broadcast(controller_string)
    '''

    # wait(20)

    print("Observing player data...")

    wait(20)