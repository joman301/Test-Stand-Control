#import sensors
#import commands as cmd
import zmq
import time
import threading

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def wait():
    time.sleep(5)
    print('yee')

def main():

    for i in range(10):
        x = threading.Thread(name='wait', target = wait)
        x.start()
    
    while(True):
        for thread in threading.enumerate():
            print(thread.name)
        time.sleep(1)


    '''


    while(True):
        cmd_string = socket.recv()

        print("received command: ", cmd_string)

        socket.send(b"running command")
        '''
    

if __name__ == "__main__":
    main()