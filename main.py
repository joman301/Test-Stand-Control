import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

'''known issues:
errno13: permission denied /dev/i2c-1'''

# object for controlling motors
motors = MotorKit(i2c=board.I2C())

# stepper1 --> M1, M2 terminals
# stepper2 --> M3, M4 terminals

# 200 steps --> 360 deg; 1.8 deg per step

# stepper.FORWARD = clockwise, increase presssure
# stepper.BACKWARD = counterclockwise, decrease pressure

running = False

def rotate(motornum, steps):

    if motornum==1 and steps>0:
        for i in range(steps):
            motors.stepper1.onestep(direction = stepper.FORWARD, style=stepper.DOUBLE)
            time.sleep(0.01)
        motors.stepper1.release()

    elif motornum==1 and steps<=0:
        steps = steps*-1
        for i in range(steps):
            motors.stepper1.onestep(direction = stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(0.01)
        motors.stepper1.release()

    elif motornum==2 and steps>0:
        for i in range(steps):
            motors.stepper2.onestep(direction = stepper.FORWARD, style=stepper.DOUBLE)
            time.sleep(0.01)
        motors.stepper2.release()
    
    elif motornum==2 and steps<=0:
        steps = steps*-1
        for i in range(steps):
            motors.stepper2.onestep(direction = stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(0.01)
        motors.stepper2.release()
    
    else:
        print("rotate: err: incorrect parameters")

def rotate_deg(stepper, deg):

    steps = deg//1.8
    rotate(stepper, steps)


def lox_is():
    rotate(1,10)

def lox_ds():
    rotate(1,-10)

def ker_is():
    rotate(2,10)

def ker_ds():
    rotate(2,-10)

def lox_inc(n):
    rotate(1,n)

def lox_dec(n):
    rotate(1,-1*n)

def ker_inc(n):
    rotate(2,n)

def ker_dec(n):
    rotate(2,-1*n)

def help():
    s = '''
    lox_is: runs 10 steps forward on lox
    lox_ds: runs 10 steps backward on lox
    ker_is: runs 10 steps forward on kerosene
    ker_ds: runs 10 steps backward on kerosene

    lox_inc [n]: runs n steps forward on lox
    lox_dec [n]: runs n steps backward on lox
    ker_inc [n]: runs n steps forward on kerosene
    ker_dec [n]: runs n steps backward on kerosene

    help: print help menu
    quit: leave program
    rr: repeat last command
    '''
    print(s)

def quit():
    global running
    running = False

commands = {
    "lox_is": lox_is,
    "lox_ds": lox_ds,
    "ker_is": ker_is,
    "ker_ds": ker_ds,

    "lox_inc": lox_inc,
    "lox_dec": lox_dec,
    "ker_inc": ker_inc,
    "ker_dec": ker_dec,

    "help": help,
    "quit": quit 
}

def main():
    print('Welcome')
    print('If you need help, type \"help\" into the cmd line')

    global running 
    running = True
    cmd = ''
    cmd_param = 0
    param_used = False
    while(running):
        
        # remove spaces and capitalization from input
        user_command = str.lower(input('$'))
        user_command = user_command.replace(' ','')
        
        # parse command for numerical condition appended to end
        if user_command != 'rr':
            try:
                for i, character in enumerate(user_command):
                    if character.isdigit():
                        cmd = user_command[:i]
                        cmd_param = int(user_command[i:])
                        param_used = True
                        break
                    else:
                        param_used = False
            except:
                print('err: command not found')
                continue

        if param_used==False and user_command != 'rr':
            cmd = user_command

        # safety to keep steps below 50
        if cmd_param > 50 and param_used == True:
            cont = input(f"Are you sure you want to use step size {cmd_param}? [yes/no]")
            if str.lower(cont) != 'yes':
                print('Ignoring command')
                print()
                continue

        # execute command if located in commands list
        if cmd in commands.keys() or cmd=='rr':
            if param_used==False:
                print(f'running {cmd}')
                try:
                    commands[cmd]()
                    print('done')
                except:
                    print('err: missing parameter')
            else:
                print(f'running {cmd} with step {cmd_param}')
                try:
                    commands[cmd](cmd_param)
                    print('done')
                except:
                    print('err: extra parameter')
        else:
            print('err: command not found')

        
        print()

if __name__ == "__main__":
    main()