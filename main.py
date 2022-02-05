#import sensors
#import commands as cmd
import zmq
import time
import threading
import commands as cmd

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def wait():
    time.sleep(5)
    print('yee')

def main():

    while(True):
        cmd_string = socket.recv()
        print("received command: ", cmd_string)
        user_command = cmd.parse(cmd_string)       

        x = threading.Thread(name='command', target=cmd.exe, args=[user_command])
        x.start()

        socket.send(b"running command")
        
    

if __name__ == "__main__":
    main()