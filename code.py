#region VEXcode Generated Robot Configuration
from vex import *
from cte import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
EntryConveyor1 = Motor(Ports.PORT1, False)
TransportConveyor2 = Motor(Ports.PORT2, True)
ExitConveyor4 = Motor(Ports.PORT4, True)
Arm10 = Arm(Ports.PORT10)
SignalTower6 = SignalTower(Ports.PORT6)
ObjectSensorA = ObjectDetector(brain.three_wire_port.a)
Pneumatic3 = Pneumatic(Ports.PORT3)
DistanceSensor5 = Distance(Ports.PORT5)
OpticalSensor7 = Optical(Ports.PORT7)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()


# Color to String Helper
def convert_color_to_string(col):
    if col == Color.RED:
        return "red"
    if col == Color.GREEN:
        return "green"
    if col == Color.BLUE:
        return "blue"
    if col == Color.WHITE:
        return "white"
    if col == Color.YELLOW:
        return "yellow"
    if col == Color.ORANGE:
        return "orange"
    if col == Color.PURPLE:
        return "purple"
    if col == Color.CYAN:
        return "cyan"
    if col == Color.BLACK:
        return "black"
    if col == Color.TRANSPARENT:
        return "transparent"
    return ""
# Initialize the 6-Axis Arm
Arm10.initialize_arm()

# Reset the Signal Tower lights
SignalTower6.set_color(SignalTower.ALL, SignalTower.OFF)
SignalTower6.set_color(SignalTower.GREEN, SignalTower.ON)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Pseudocode
pseudo = """    
1. Send all four disks on the pallet out destination A
2. Send three cubes out destination A
3. Send two more cubes to the other workcell
4. Reorganize the four remaining cubes on the pallet so they are in a stack of two and three
5. Begin dispensing disks
    a. For each available disk, if that disk is still needed for destination A or B, send it out A or to the other workcell
    b. Place uneeded disks on single color stacks on the pallet
    Repeat until both A and B are fulfilled.
6. Press the button
7. If there are available disks on the pallet to fulfill C, send those to the other workcell.
8. After those are exhausted, send two cubes over to the other workcell.
9. Begin dispensing disks
    a. For each available disk, if that disk is still needed for destination C, send it out to the other workcell
    b. Place uneeded disks on single color stacks on the pallet
    Repeat until C is fulfilled.
10. Press the button
11. Send all remaining disks from either the pallet or dispenser over to the other workcell
12. Send all remaining cubes over to the other workcell
END
"""

# CONSTANTS
CUBE_STACK_1 = (-50, 155)
CUBE_STACK_2 = (-20, 130)

# Variables
aRemaining = {
    "Red Disks": 2,
    "Green Disks": 3,
    "Cubes": 3
}
bRemaining = {
    "Red Disks": 2,
    "Green Disks": 1,
    "Cubes": 2
}
cRemaining = {
    "Red Disks": 1,
    "Green Disks": 1,
    "Cubes": 2
}
dRemaining = {
    "Red Disks": 1,
    "Green Disks": 1,
    "Cubes": 2
}

cubeStack1Count = 0
cubeStack2Count = 0
redDiskStackCount = 0
greenDiskStackCount = 0

# Begin project code
Arm10.set_end_effector_type(Arm.MAGNET)
Pneumatic3.pump_on()
OpticalSensor7.set_light(LedStateType.ON)

def eStop():
    Arm10.set_control_stop(True)
    EntryConveyor1.stop()
    TransportConveyor2.stop()
    ExitConveyor4.stop()
    SignalTower6.set_color(SignalTower.GREEN, SignalTower.OFF)
    SignalTower6.set_color(SignalTower.RED, SignalTower.BLINK)

SignalTower6.pressed(eStop)
def moveFromPalletToConveyor(x,y,z):
    Arm10.move_to(x,y,z)
    Arm10.set_end_effector_magnet(True)
    Arm10.move_inc(0,0,50)
    Arm10.move_to(100,150,60)
    Arm10.set_end_effector_magnet(False)
    Arm10.move_inc(0,0,50)

def moveInitialDisksCubesOffPallet():
    global aRemaining, bRemaining

    TransportConveyor2.set_velocity(100, PERCENT)
    TransportConveyor2.spin(FORWARD)
    Pneumatic3.extend(CYLINDER4)
    Pneumatic3.retract(CYLINDER2)

    # Send disks out A
    moveFromPalletToConveyor(-35,135,50)
    moveFromPalletToConveyor(0,135,50)
    moveFromPalletToConveyor(0,175,50)
    moveFromPalletToConveyor(-35,175,50)

    # Send cubes out A
    moveFromPalletToConveyor(5,130,40)
    moveFromPalletToConveyor(5,160,40)
    moveFromPalletToConveyor(5,190,40)

    #Setup 2
    Pneumatic3.retract(CYLINDER4)
    Pneumatic3.retract(CYLINDER2)
    ExitConveyor4.set_velocity(100, PERCENT)
    ExitConveyor4.spin(FORWARD)

    # Send cubes out B
    moveFromPalletToConveyor(-20,190,40)
    moveFromPalletToConveyor(-20,160,40)

    aRemaining["Red Disks"] -= 2
    aRemaining["Green Disks"] -= 2
    aRemaining["Cubes"] -= 3
    bRemaining["Cubes"] -= 2

def pressButton():
    Arm10.move_to(50, 185, 100)
    Arm10.move_to(50, 185, 15)
    wait(3, SECONDS)
    Arm10.move_inc(0, 0, 85)


def rearrangeCubes():
    global cubeStack1Count, cubeStack2Count

    # First stack is located at (-50, 185)
    Arm10.move_to(CUBE_STACK_1[0], CUBE_STACK_1[1], 150)
    Arm10.set_end_effector_magnet(True)
    Arm10.move_inc(0, 0, -110)
    wait(500, MSEC)
    Arm10.move_inc(0, 0, 110)
    Arm10.move_inc(0, 30, 0)
    Arm10.move_inc(0, 0, -85)
    Arm10.set_end_effector_magnet(False)

    # Second stack is located at (-50, 130)
    Arm10.move_to(CUBE_STACK_2[0], CUBE_STACK_2[1], 150)
    Arm10.set_end_effector_magnet(True)
    Arm10.move_inc(0, 0, -110)
    wait(500, MSEC)
    Arm10.move_inc(0, 0, 110)
    Arm10.move_inc(-30, 0, 0)
    Arm10.move_inc(0, 0, -85)
    Arm10.set_end_effector_magnet(False)
    Arm10.move_inc(0, 0, 85)
    Arm10.move_to(120, 0, 150)

    cubeStack1Count = 2
    cubeStack2Count = 2

def transportObjectOutA():
    # Set up the pneumatics to let objects out a
    Pneumatic3.extend(CYLINDER4)
    Pneumatic3.retract(CYLINDER2)

    # Spin the right stuff
    EntryConveyor1.set_velocity(100, PERCENT)
    TransportConveyor2.set_velocity(100, PERCENT)
    ExitConveyor4.set_velocity(100, PERCENT)
    EntryConveyor1.spin(FORWARD)
    TransportConveyor2.spin(FORWARD)
    ExitConveyor4.stop()

    # Wait till it's definitely gone
    while DistanceSensor5.object_distance(MM) < 230:
        pass
    wait(5, SECONDS)
    EntryConveyor1.stop()
    TransportConveyor2.stop()

def transportObjectToOtherWorkcell():
    # Set up the pneumatics to let objects out b
    Pneumatic3.retract(CYLINDER4)

    # Spin the right stuff
    EntryConveyor1.set_velocity(100, PERCENT)
    TransportConveyor2.set_velocity(100, PERCENT)
    ExitConveyor4.set_velocity(100, PERCENT)
    EntryConveyor1.spin(FORWARD)
    TransportConveyor2.spin(FORWARD)
    ExitConveyor4.spin(FORWARD)

    # Wait till it's definitely gone
    wait(5, SECONDS)
    EntryConveyor1.stop()
    TransportConveyor2.stop()
    ExitConveyor4.stop()

def stackRedDisk():
    global redDiskStackCount
    EntryConveyor1.set_velocity(100, PERCENT)
    EntryConveyor1.spin(FORWARD)
    TransportConveyor2.set_velocity(70, PERCENT)
    TransportConveyor2.spin(FORWARD)
    
    # Spin until the distance sensor can see it
    while DistanceSensor5.object_distance(MM) > 230:
        pass
    TransportConveyor2.set_velocity(10, PERCENT)
    while DistanceSensor5.object_distance(MM) < 95:
        pass
    TransportConveyor2.stop()
    EntryConveyor1.stop()
    Arm10.move_to(95, 160, 100)
    Arm10.move_inc(0, 0, -65)
    Arm10.set_end_effector_magnet(True)
    Arm10.move_inc(0, 0, 30)
    Arm10.move_to(0, 135, 50 + redDiskStackCount*9)
    Arm10.move_inc(0, 0, -25)
    Arm10.set_end_effector_magnet(False)
    Arm10.move_inc(0, 0, 25)
    redDiskStackCount += 1

def stackGreenDisk():
    global greenDiskStackCount
    EntryConveyor1.set_velocity(100, PERCENT)
    EntryConveyor1.spin(FORWARD)
    TransportConveyor2.set_velocity(70, PERCENT)
    TransportConveyor2.spin(FORWARD)
    
    # Spin until the distance sensor can see it
    while DistanceSensor5.object_distance(MM) > 230:
        pass
    TransportConveyor2.set_velocity(10, PERCENT)
    while DistanceSensor5.object_distance(MM) < 95:
        pass
    TransportConveyor2.stop()
    EntryConveyor1.stop()
    Arm10.move_to(95, 160, 100)
    Arm10.move_inc(0, 0, -65)
    Arm10.set_end_effector_magnet(True)
    Arm10.move_inc(0, 0, 30)
    Arm10.move_to(0, 175, 50 + greenDiskStackCount*9)
    Arm10.move_inc(0, 0, -25)
    Arm10.set_end_effector_magnet(False)
    Arm10.move_inc(0, 0, 25)
    greenDiskStackCount += 1
    
def fulfillRemainingABDisks(): 
    global aRemaining, bRemaining
    while aRemaining["Red Disks"] > 0 or aRemaining["Green Disks"] > 0 or bRemaining["Red Disks"] > 0 or bRemaining["Green Disks"] > 0:
        Pneumatic3.extend(CYLINDER1)
        wait(1, SECONDS)
        Pneumatic3.retract(CYLINDER1)
        wait(1, SECONDS)

        diskColor = OpticalSensor7.hue()
        brain.screen.clear_screen()
        if (diskColor < 30):
            brain.screen.print("Red")
            if aRemaining["Red Disks"] > 0:
                transportObjectOutA()
                aRemaining["Red Disks"] -= 1
            elif bRemaining["Red Disks"] > 0:
                transportObjectToOtherWorkcell()
                bRemaining["Red Disks"] -= 1
            else:
                stackRedDisk()
        elif (diskColor > 60):
            brain.screen.print("Green")
            if aRemaining["Green Disks"] > 0:
                transportObjectOutA()
                aRemaining["Green Disks"] -= 1
            elif bRemaining["Green Disks"] > 0:
                transportObjectToOtherWorkcell()
                bRemaining["Green Disks"] -= 1
            else:
                stackGreenDisk()

def moveTwoCubesOutC():
    TransportConveyor2.set_velocity(100, PERCENT)
    ExitConveyor4.set_velocity(100, PERCENT)
    TransportConveyor2.spin(FORWARD)
    ExitConveyor4.spin(FORWARD)
    moveFromPalletToConveyor(-45,130,65)
    moveFromPalletToConveyor(-45,190,65)

def fulfillC():
    global cRemaining, redDiskStackCount, greenDiskStackCount
    moveTwoCubesOutC()
    cRemaining["Cubes"] -= 2
    while cRemaining["Red Disks"] > 0 and redDiskStackCount > 0:
        Arm10.move_to(0, 135, 50 + redDiskStackCount*9)
        moveFromPalletToConveyor(0, 135, 25 + redDiskStackCount*9)
        redDiskStackCount -= 1
        cRemaining["Red Disks"] -= 1
        transportObjectToOtherWorkcell()
    while cRemaining["Green Disks"] > 0 and greenDiskStackCount > 0:
        Arm10.move_to(0, 135, 50 + redDiskStackCount*9)
        moveFromPalletToConveyor(0, 135, 25 + redDiskStackCount*9)
        greenDiskStackCount -= 1
        cRemaining["Green Disks"] -= 1
        transportObjectToOtherWorkcell()
    while cRemaining["Red Disks"] > 0 or cRemaining["Green Disks"] > 0:
        Pneumatic3.extend(CYLINDER1)
        wait(1, SECONDS)
        Pneumatic3.retract(CYLINDER1)
        wait(1, SECONDS)

        diskColor = OpticalSensor7.hue()
        brain.screen.clear_screen()
        if (diskColor < 30):
            brain.screen.print("Red")
            if cRemaining["Red Disks"] > 0:
                transportObjectToOtherWorkcell()
                cRemaining["Red Disks"] -= 1
            else:
                stackRedDisk()
        elif (diskColor > 60):
            brain.screen.print("Green")
            if cRemaining["Green Disks"] > 0:
                transportObjectToOtherWorkcell()
                cRemaining["Green Disks"] -= 1
            else:
                stackGreenDisk()


def moveTwoCubesToD():
    moveFromPalletToConveyor(-45,130,40)
    moveFromPalletToConveyor(-45,190,40)
    wait(2, SECONDS)

def fulfillD():
    global dRemaining, redDiskStackCount, greenDiskStackCount

    EntryConveyor1.set_velocity(100, PERCENT)
    TransportConveyor2.set_velocity(30, PERCENT)
    ExitConveyor4.set_velocity(100, PERCENT)
    TransportConveyor2.spin(FORWARD)
    ExitConveyor4.spin(REVERSE)

    while dRemaining["Red Disks"] > 0 and redDiskStackCount > 0:
        Arm10.move_to(0, 135, 50 + redDiskStackCount*9)
        moveFromPalletToConveyor(0, 135, 25 + redDiskStackCount*9)
        redDiskStackCount -= 1
        dRemaining["Red Disks"] -= 1
    while dRemaining["Green Disks"] > 0 and greenDiskStackCount > 0:
        Arm10.move_to(0, 135, 50 + redDiskStackCount*9)
        moveFromPalletToConveyor(0, 135, 25 + redDiskStackCount*9)
        greenDiskStackCount -= 1
        dRemaining["Green Disks"] -= 1
    while dRemaining["Red Disks"] > 0 or dRemaining["Green Disks"] > 0:
        Pneumatic3.extend(CYLINDER1)
        wait(1, SECONDS)
        Pneumatic3.retract(CYLINDER1)
        wait(1, SECONDS)

        diskColor = OpticalSensor7.hue()
        brain.screen.clear_screen()
        if (diskColor < 30):
            brain.screen.print("Red")
            dRemaining["Red Disks"] -= 1
            EntryConveyor1.spin(FORWARD)
            wait(3, SECONDS)
            EntryConveyor1.stop()
        elif (diskColor > 60):
            brain.screen.print("Green")
            dRemaining["Green Disks"] -= 1
            EntryConveyor1.spin(FORWARD)
            wait(3, SECONDS)
            EntryConveyor1.stop()

    moveTwoCubesToD()
    dRemaining["Cubes"] -= 2
    
    TransportConveyor2.set_velocity(100, PERCENT)
    ExitConveyor4.spin(FORWARD)
    wait(5, SECONDS)

def end():
    Arm10.move_to(120, 0, 100)
    EntryConveyor1.stop()
    TransportConveyor2.stop()
    ExitConveyor4.stop()


# Run the program!
moveInitialDisksCubesOffPallet()
rearrangeCubes()
fulfillRemainingABDisks()
pressButton()
fulfillC()
pressButton()
fulfillD()
end()
