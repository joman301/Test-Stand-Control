#import sensors
#import commands as cmd
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def main():
    while(True):
        cmd_string = socket.recv()

        print("received command: ", cmd_string)

        socket.send(b"running command")
    

if __name__ == "__main__":
    main()