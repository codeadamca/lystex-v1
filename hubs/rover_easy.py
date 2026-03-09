from pybricks.hubs import EssentialHub, ThisHub

from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pybricks.iodevices import XboxController

import umath as math

# ==========================================
# CONSTANTS
# ==========================================

CHANNEL = 1

BROADCAST_LENGTH = 250

POWER_MAX_LEVEL_COUNTER = 5000
POWER_MAX_ANGLE_COUNTER = 100

STEER_MAX_ANGLE = 30

# ==========================================
# HUB
# ==========================================

hub = EssentialHub()
hub = ThisHub(broadcast_channel=CHANNEL,observe_channels=[2,3,4,5,6,7,8,9])

# 1 - rover
# 2 - z1_left
# 3 - z1_middle
# 4 - z1_right
# 5 - z2_left
# 6 - z2_middle
# 7 - z2_right
# 8 - z3_left
# 9 - z3_middle

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
# FUNCTIONS
# ==========================================

def broadcast(channel, data, time = False):

    global tracking

    if time == False: time = BROADCAST_LENGTH

    pairs = data.split(",")

    new = False

    for pair in pairs:

        key, value = pair.split("=")

        if key not in tracking or tracking[key] != value:  

            new = True
            tracking[key] = value

    if new == True:

        hub.ble.broadcast(str(channel) + ":" + data)
        wait(time)
        hub.ble.broadcast(None)

def gameover():

    global game

    game = False

    t1_colour = "r"
    t2_colour = "r"
    t3_colour = "r"

    broadcast(2, "t1c=r,p1m=s", 500)
    broadcast(3, "c1c=r,v1s=n", 500)
    broadcast(4, "t2c=r", 500)
    broadcast(5, "t3c=r,s1c=r,v3s=n", 500)
    broadcast(6, "c2c=r,r1s=n", 500)
    broadcast(7, "c2c=r,v2s=n", 500)
    broadcast(8, "p2m=s", 500)
    broadcast(9, "v4s=f,v5s=f,v6s=f", 500)

    print("Game Over!!!")

def gamewin():

    global win

    win = True

    t1_colour = "r"
    t2_colour = "r"
    t3_colour = "r"

    broadcast(2, "t1c=g,p1m=s", 500)
    broadcast(3, "c1c=g,v1s=r", 500)
    broadcast(4, "t2c=g", 500)
    broadcast(5, "t3c=g,s1c=g,v3s=r", 500)
    broadcast(6, "g2c=g,r1s=r", 500)
    broadcast(7, "c2c=g,v2s=r", 500)
    broadcast(8, "p2m=s", 500)
    broadcast(9, "v4s=r,v5s=r,v6s=r", 500)

    print("Game Over!!!")


    
'''
def t1_set_colour(colour):

    global t1_colour
    t1_colour = colour
    hub.ble.broadcast("2,t1c," + colour)
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

def p1_set_motor(action):

    global s1_tracking

    if s1_tracking != action:
        s1_tracking = action
        hub.ble.broadcast("2,p1m," + action)
        wait(BROADCAST_LENGTH)
        hub.ble.broadcast(None)

# ==========================================
# CHANNEL 3

def c1_set_colour(colour):

    global c1_colour
    c1_colour = colour
    hub.ble.broadcast("3,c1c," + colour)
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

def v1_set_lights(status):

    print("Changing V1 Status to " + status)

    global v1_status
    v1_status = status
    hub.ble.broadcast("3,v1s," + status)
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

def g1_set_status(status):

    global g1_status
    g1_status = status
    hub.ble.broadcast("3,g1s," + status)
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

# ==========================================
# CHANNEL 4

def t2_set_colour(colour):

    global t2_colour
    t2_colour = colour
    hub.ble.broadcast("4,t2c," + colour)
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

def sound_success(channel):
    hub.ble.broadcast(channel + ",s")
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

def sound_error(channel):
    hub.ble.broadcast(channel + ",e")
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

# ==========================================
# CHANNEL 5

def s1_reset():

    hub.ble.broadcast("5,s1r")
    wait(BROADCAST_LENGTH)
    hub.ble.broadcast(None)

def s1_set_motor(level):

    global s1_level_tracking

    # print(str(level) + " - " + str(s1_level_tracking))

    if s1_level_tracking != level:
        
        s1_level_tracking = level
        percent = level * 20
        hub.ble.broadcast("5,s1f," + str(percent))
        wait(BROADCAST_LENGTH)
        hub.ble.broadcast(None)

def s1_set_point(angle):

    global s1_angle_tracking

    # print(str(angle) + " - " + str(s1_angle_tracking))

    if s1_angle_tracking != angle:
        
        s1_angle_tracking = angle
        hub.ble.broadcast("5,s1p," + str(angle))
        wait(BROADCAST_LENGTH)
        hub.ble.broadcast(None)

def s1_set_zone(angle):

    global s1_zone

    if 45 <= angle <= 80:
        next_zone = "bridge"
    elif 90 <= angle <= 110:
        next_zone = "car"
    elif 110 <= angle <= 135:
        next_zone = "gate"
    elif 135 <= angle <= 175:
        next_zone = "home"
    else:
        next_zone = "none"

    if next_zone != s1_zone:

        s1_zone = next_zone

        print(s1_zone)

        if s1_zone == "none":

            print("none")
            c1_set_colour("n")
            v1_set_lights("f")

        elif s1_zone == "bridge":

            print("bridge")
            c1_set_colour("r")
            v1_set_lights("n")
'''        

# ==========================================
# PORTS
# ==========================================

# Motor A is your steering motor
steering_motor = Motor(Port.B)
steering_motor.reset_angle(0)

# Motor B is your drive motor (back wheels)
drive_motor = Motor(Port.A)

# ==========================================
# SETUP
# ==========================================

# Create a tracking variable to prevent 
# redundant braodcasting
tracking = {}

# Connect to the Xbox Controller
print("Searching for controller...")
hub.light.on(Color.BLUE)
xbox = XboxController()
hub.light.on(Color.GREEN)
print("Connected!")

print("Setting default spot")
spot = "none"

'''
print("Setting Tower One to BLUE")
t1_colour = "g"
t1_set_colour("g")

print("Setting Tower Two to RED")
t2_colour = "r"
t2_set_colour("r")

print("Resetting Station One")
s1_angle = 0
s1_angle_counter = 0
s1_angle_tracking = 0
s1_level = 0
s1_level_tracking = 0
s1_level_counter = 0
s1_tracking = "s"
s1_zone = "none"
s1_reset()

print("Setting Control One to RED")
c1_colour = "r"
c1_set_colour("n")

print("Turning off Vent One")
v1_status = "f"
v1_set_lights("f")

print("Closing Gate One")
g1_pass = "w"
g1_status = "c"
g1_set_status("c")
'''

print("Resetting problems")
p1 = False
p2 = False
p3 = False
p4 = False
game = True
win = False

print("Setting tower one to yellow")
t1_colour = "y"
broadcast(2, "t1c=y", 500)

print("Setting tower two to red")
t2_colour = "r"
broadcast(4, "t2c=r", 500)

print("Setting tower three to green")
t3_colour = "g"
broadcast(5, "t3c=g", 500)

print("Turning off vents in zone three")
broadcast(9, "v4s=f,v5s=f,v6s=f", 500)

print("Turning off vents in zone two left")
broadcast(5, "v3s=f", 500)
broadcast(7, "v2s=f,c2c=n", 500)

print("Turning off vents and lights in zone one middle")
broadcast(3, "v1s=f,c1c=n", 500)


print("Setting defaults for station one")
power_angle = 0
power_angle_counter = 0
power_level = 0
power_level_counter = 0
power_zone = "none"
broadcast(5, "a5=r", 2500)


print("Setting gate one to closed")
broadcast(3, "a3=r", 2500)

print("Resetting rover one")
broadcast(6, "a6=r", 2500)

print("Resetting gate three to closed")
broadcast(9, "a9=r", 2500)

# ==========================================
# PLAY LOOP
# ==========================================

# Main Control Loop
print("Play code started...")
while True:

    # ==========================================
    # FETCH JOYSTICK DATA ONCE

    try:
        joystick_left = xbox.joystick_left()
        joystick_right = xbox.joystick_right()
        buttons_pressed = xbox.buttons.pressed()

    except OSError:
        joystick_left = [0, 0]
        joystick_right = [0, 0]
        buttons_pressed = []

    # ==========================================
    # DRIVING

    drive_speed = joystick_left[1] * (-2.5)
    
    steer_speed = joystick_right[0] * (-1)
    steer_speed = (steer_speed / 100) * STEER_MAX_ANGLE
    
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
    
    if game == True and win == False:

        drive_motor.run(drive_speed)
        steering_motor.track_target(steer_speed)

        # ==========================================
        # OBSERVE all applicable channels and set 
        # spot accordingly

        c2_string = hub.ble.observe(2)
        c3_string = hub.ble.observe(3)
        c4_string = hub.ble.observe(4)
        c5_string = hub.ble.observe(5)
        # c6_string = hub.ble.observe(6)
        c7_string = hub.ble.observe(7)
        c8_string = hub.ble.observe(8)
        c9_string = hub.ble.observe(9)

        if c2_string != None: spot_next = c2_string
        elif c3_string != None: spot_next = c3_string
        elif c4_string != None: spot_next = c4_string
        elif c5_string != None: spot_next = c5_string
        # elif c6_string != None: spot_next = c6_string
        elif c7_string != None: spot_next = c7_string
        elif c8_string != None: spot_next = c8_string
        elif c9_string != None: spot_next = c9_string
        else: spot_next = "none"

        # Detect spot changes
        if spot_next != spot:

            print("Spot change from: " + spot + " to: " + spot_next)
            spot = spot_next
        
        # ==========================================
        # If current spot is tower one
        if spot == "t1":

            # Set colour based on button press
            if Button.A in buttons_pressed:
                broadcast(2, "t1c=g")
                t1_colour = "g"
            elif Button.B in buttons_pressed:
                broadcast(2, "t1c=r")
                t1_colour = "r"
            elif Button.X in buttons_pressed:
                broadcast(2, "t1c=b")
                t1_colour = "b"
            elif Button.Y in buttons_pressed:
                broadcast(2, "t1c=y")
                t1_colour = "y"

        # ==========================================
        # If current spot is tower two
        elif spot == "t2":

            # Set colour based on button press
            if Button.A in buttons_pressed:
                broadcast(4, "t2c=g")
                t2_colour = "g"
            elif Button.B in buttons_pressed:
                broadcast(4, "t2c=r")
                t2_colour = "r"
            elif Button.X in buttons_pressed:
                broadcast(4, "t2c=b")
                t2_colour = "b"
            elif Button.Y in buttons_pressed:
                broadcast(4, "t2c=y")
                t2_colour = "y"

        # ==========================================
        # If current spot is tower three
        elif spot == "t3":

            # Set colour based on button press
            if Button.A in buttons_pressed:
                broadcast(5, "t3c=g")
                t3_colour = "g"
            elif Button.B in buttons_pressed:
                broadcast(5, "t3c=r")
                t3_colour = "r"
            elif Button.X in buttons_pressed:
                broadcast(5, "t3c=b")
                t3_colour = "b"
            elif Button.Y in buttons_pressed:
                broadcast(5, "t3c=y")
                t3_colour = "y"

        # ==========================================
        # If current spot is power one
        elif spot == "p1":

            # Set motor action based on button press
            if Button.RB in buttons_pressed:
                # Trun motor right and subtract from angle
                broadcast(2, "p1m=r")
                broadcast(8, "p2m=r")
                power_angle_counter -= 2
            elif Button.LB in buttons_pressed:
                # Turn motor left and add to angle
                broadcast(2, "p1m=l")
                broadcast(8, "p2m=l")
                power_angle_counter += 2
            elif Button.Y in buttons_pressed:
                # Turn motor full and add to level
                broadcast(2, "p1m=f")
                broadcast(8, "p2m=f")
                power_level_counter += 10
            else:
                broadcast(2, "p1m=s")
                broadcast(8, "p2m=s")

        # ==========================================
        # If current spot is power one
        elif spot == "p2":

            # Set motor action based on button press
            if Button.RB in buttons_pressed:
                # Trun motor right and subtract from angle
                broadcast(2, "p1m=r")
                broadcast(8, "p2m=r")
                power_angle_counter -= 2
            elif Button.LB in buttons_pressed:
                # Turn motor left and add to angle
                broadcast(2, "p1m=l")
                broadcast(8, "p2m=l")
                power_angle_counter += 2
            elif Button.Y in buttons_pressed:
                # Turn motor full and add to level
                broadcast(2, "p1m=f")
                broadcast(8, "p2m=f")
                power_level_counter += 10
            else:
                broadcast(2, "p1m=s")
                broadcast(8, "p2m=s")

        # ==========================================
        # If current spot is control one
        elif spot == "c1":

            # if power_zone == "bridge":

            if Button.DOWN in buttons_pressed:
                # if t1_colour == "b" and t2_colour == "y":
                broadcast(3, "g1s=o")
                p1 = True

            if Button.UP in buttons_pressed:
                # if t1_colour == "b" and t2_colour == "y":
                broadcast(3, "g1s=c")
                p1 = False

        # ==========================================
        # If current spot is control two
        elif spot == "c2":

            # if power_zone == "gate":

            if Button.LB in buttons_pressed:
                if t1_colour == "g" and t2_colour == "y" and t3_colour == "b":
                    broadcast(6, "g2s=l,g2c=g")
                    p3 = True

            elif Button.RB in buttons_pressed:
                if t1_colour == "g" and t2_colour == "y" and t3_colour == "b":
                    broadcast(6, "g2s=r,g2c=r")
                    p3 = False

        # ==========================================
        # If current spot is c3
        elif spot == "c3":

            # if p1 == False or p2 == False or p3 == False:

            # gameover()

            # print("Game Over")

            # elif power_zone == "home":

            if Button.LEFT in buttons_pressed:
                broadcast(9, "g3m=l")
                p4 = False

            elif Button.RIGHT in buttons_pressed:
                broadcast(9, "g3m=r")
                p4 = True
                gamewin()

            else:
                broadcast(9, "g3m=s")
                p4 = False

        else:

            # If not in a spot stop power rotators
            broadcast(2, "p1m=s")
            broadcast(8, "p2m=s")

        # ==========================================
        # Check Control One light password
        # if power_zone == "bridge":
        if t1_colour == "b" and t2_colour == "y":
            broadcast(3, "c1c=g")
        else:
            broadcast(3, "c1c=r")

        # ==========================================
        # Check Control Two light password
        # if power_zone == "gate":

        if t1_colour == "g" and t2_colour == "y" and t3_colour == "b":
            broadcast(7, "c2c=g")
        else:
            broadcast(7, "c2c=r")

        # ==========================================
        # Check Control Two light password
        # if power_zone == "home":

        broadcast(9, "v4s=n,v5s=n,v6s=n")

        # ==========================================
        # Calculate updated power level and angle
        power_level_counter -= 1
        if power_level_counter < 0: power_level_counter = 0
        elif power_level_counter > POWER_MAX_LEVEL_COUNTER: power_level_counter = POWER_MAX_LEVEL_COUNTER
        power_level = math.ceil(power_level_counter / (POWER_MAX_LEVEL_COUNTER / 5))
        broadcast(5, "s1f=" + str(power_level))

        if power_angle_counter < 0: power_angle_counter = 0
        elif power_angle_counter > POWER_MAX_ANGLE_COUNTER: power_angle_counter = POWER_MAX_ANGLE_COUNTER
        power_angle = round(power_angle_counter / POWER_MAX_ANGLE_COUNTER * 180)
        broadcast(5, "s1p=" + str(power_angle))

        # print(str(power_angle) + " - " + str(power_level))

        # ==========================================
        # Move car if power zone and button pressed
        if power_zone == "car":

            if Button.DOWN in buttons_pressed:
                broadcast(6, "r1m=b")
                p2 = False

            if Button.UP in buttons_pressed:
                broadcast(6, "r1m=f")
                p2 = True

        # ==========================================
        # Calculate power zone
        if 45 <= power_angle <= 80:
            power_zone_next = "bridge"
        elif 90 <= power_angle <= 110:
            power_zone_next = "car"
        elif 110 <= power_angle <= 135:
            power_zone_next = "gate"
        elif 135 <= power_angle <= 175:
            power_zone_next = "home"
        else:
            power_zone_next = "none"
        
        # Detect power zone change
        if power_zone_next != power_zone:

            print("Zone change from: " + power_zone + " to: " + power_zone_next)
            power_zone = power_zone_next

            if power_zone == "bridge":
                broadcast(3, "v1s=m,c1c=r", 500)
                broadcast(7, "v2s=f,c2c=n")
                broadcast(5, "v3s=f")
                broadcast(6, "r1s=f,g2s=s,g2c=n")

            elif power_zone == "car":
                broadcast(3, "v1s=f,c1c=n")
                broadcast(7, "v2s=m,c2c=n")
                broadcast(5, "v3s=f")
                broadcast(6, "r1s=m,g2s=s,g2c=n")

            elif power_zone == "gate":
                broadcast(3, "v1s=f,c1c=n")
                broadcast(7, "v2s=f,c2c=r")
                broadcast(5, "v3s=n")
                broadcast(6, "r1s=f,g2s=r,g2c=r")

            elif power_zone == "home":
                broadcast(3, "v1s=f,c1c=n")
                broadcast(7, "v2s=f,c2c=n")
                broadcast(5, "v3s=f")
                broadcast(6, "r1s=f,g2s=s,g2c=n")

            else:
                broadcast(3, "v1s=f,c1c=n")
                broadcast(7, "v2s=f,c2c=n")
                broadcast(5, "v3s=f")
                broadcast(6, "r1s=f,g2s=s,g2c=n")

    '''
    # ==========================================
    # CHANNEL 3 - CONTROL 1

    # CONTROL 1
    if s1_zone == "bridge":
    
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

    # print("Observing player data...")

    wait(10)