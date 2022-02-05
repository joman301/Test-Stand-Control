#import sensors
#import commands as cmd
import zmq
import time
import threading
import commands as cmd

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def wait(text):
    time.sleep(5)
    print(text)

def main():

    while(True):
        # Receive command from host
        cmd_string = socket.recv()
        cmd_string = str(cmd_string, 'UTF-8')
        user_command = cmd.parse(cmd_string)       

        # Create new thread and run command
        x = threading.Thread(name='command', target=cmd.exe, args=[user_command])
        #x = threading.Thread(name='test', target=wait, args=['yee'])
        x.start()

        socket.send(b"running command")

if __name__ == "__main__":
    main()