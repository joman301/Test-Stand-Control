from enum import Enum
import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

LAST_COMMAND = []
LOX_MOTOR_POS_DEG = 0
KER_MOTOR_POS_DEG = 0

motors = MotorKit(i2c=board.I2C())

class Dev(enum):
    LOX_MOTOR = 1
    KER_MOTOR = 2

#dictionary of all commands, and number of args
commands = {
    "lox_is": [lox_is, 1],
    "lox_ds": [lox_ds, 1],
    "ker_is": [ker_is, 1],
    "ker_ds": [ker_ds, 1],

    "lox_inc": [lox_inc, 2],
    "lox_dec": [lox_dec, 2],
    "ker_inc": [ker_inc, 2],
    "ker_dec": [ker_dec, 2],

    "help": [help, 1],
    "quit": [quit, 1],
    "rr": [rr, 1]
}


def exe(user_command):
    global LAST_COMMAND 
    LAST_COMMAND = user_command
    if cmd in commands.keys():
        if len(user_command)==len(commands.get(user_command[0])):
            try:
                commands[user_command](*user_command)
                return 1
            except:
                return 2
    else:
        return 1

def rr():
    if len(LAST_COMMAND) > 0:
        exe(LAST_COMMAND)
    else:
        return 1

def rotate(motor, step_count):
    global LOX_MOTOR_POS_DEG, KER_MOTOR_POS_DEG

    if step_count > 0:
        dir = stepper.FORWARD
    else:
        dir = stepper.BACKWARD
        step_count = step_count * -1
    
    if motor == Dev.LOX_MOTOR:
        for i in range(step_count):
            motors.stepper1.onestep(direction = dir, style=stepper.SINGLE)
            LOX_MOTOR_POS_DEG += 1.8
            time.sleep(0.01)
        motors.stepper1.release()

    elif motor == Dev.KER_MOTOR:
        for i in range(step_count):
            motors.stepper2.onestep(direction = dir, style=stepper.SINGLE)
            KER_MOTOR_POS_DEG
            time.sleep(0.01)
        motors.stepper2.release()

def rotate_deg(stepper, deg):
    steps = deg//1.8
    rotate(stepper, steps)

def lox_motor_pos():
    return LOX_MOTOR_POS_DEG

def ker_motor_pos():
    return KER_MOTOR_POS_DEG

def lox_is():
    rotate(Dev.LOX_MOTOR,10)

def lox_ds():
    rotate(Dev.LOX_MOTOR,-10)

def ker_is():
    rotate(Dev.KER_MOTOR,10)

def ker_ds():
    rotate(Dev.KER_MOTOR,-10)

def lox_inc(n):
    rotate(Dev.LOX_MOTOR,n)

def lox_dec(n):
    rotate(Dev.LOX_MOTOR,-1*n)

def ker_inc(n):
    rotate(Dev.KER_MOTOR,n)

def ker_dec(n):
    rotate(Dev.KER_MOTOR,-1*n)