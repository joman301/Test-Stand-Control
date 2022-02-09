'''Host computer, which receives/sends
commands to the server'''
import zmq
import pandas as pd
from datetime import datetime
import queue
import threading

context = zmq.Context()

receive_socket = context.socket(zmq.PAIR)
receive_socket.connect("tcp://10.0.0.1:5555")
send_socket = context.socket(zmq.PAIR)
send_socket.connect("tcp://10.0.0.1:5556")

current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
file_name = "data/Differential_Data_" + current_date + ".csv"

df = pd.DataFrame(columns = ["LOX psi", "KER psi", "PRES psi"])
df.to_csv(file_name, mode = 'w')

SEND_INFO = queue.Queue()
RECEIVED_INFO = queue.Queue()

RECEIVED_REQUESTS = queue.Queue()

def sender():
    '''Immediately sends any info in the
    SEND_INFO queue over the socket'''
    global SEND_INFO
    while(True):
        send_socket.send_string(SEND_INFO.get())

def receiver():
    '''Puts any received info from the socket
    in the RECEIVED_INFO queue'''
    global RECEIVED_INFO
    while(True):
        RECEIVED_INFO.put(receive_socket.recv())

def get():
        '''gets the earliest info from the
        RECEIVED_INFO queue'''
        global RECEIVED_INFO
        return RECEIVED_INFO.get()

def send(message):
        '''adds a string to the SEND_INFO queue'''
        global SEND_INFO
        SEND_INFO.put(message)

def send_command(message):
        reply = input(message)
        reply = "cmd%" + reply
        send(reply)

def receive_request(message):
        global RECEIVED_REQUESTS
        RECEIVED_REQUESTS.put(message)

def get_requests():
        while(True):
                message = RECEIVED_REQUESTS.get()
                a = message.find('%')
                if message[:a] == "cmr":
                        reply = input(message[a+1:])
                        reply = "cmd%" + reply
                        send(reply)
                elif message[:a] == "req":
                        reply = input(message[a+1:])
                        reply = "rep%" + reply
                        send(reply)
        

requester = threading.Thread(name='requester', target = get_requests)
requester.start()

sender = threading.Thread(name='sender', target=sender)
sender.start()

receiver = threading.Thread(name='receiver', target=receiver)
receiver.start()
        

while(True):

        '''Message types:
        cmr - Request for a command from server
        req - Request for string input from server
        cmd - Command with arguments, which can be executed on server
        rep - Reply to a request for string input
        dat - CSV data from the server'''

        message = get()
        message = str(message, 'UTF-8')
        a = message.find('%')
        if message[:a] == "cmr" or message[:a] == "req":
                receive_request(message)
        elif message[:a] == "dat":
                with open(file_name, 'a') as file:
                        print(message[a+1:])
                        file.write(message[a+1:])
                file.close()


