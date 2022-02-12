'''Host computer, which receives/sends
commands to the server'''
import zmq
import pandas as pd
from datetime import datetime
import queue
import threading
from enum import IntEnum

# ZMQ setup
context = zmq.Context()
receive_socket = context.socket(zmq.PAIR)
receive_socket.connect("tcp://10.0.0.1:5555")
send_socket = context.socket(zmq.PAIR)
send_socket.connect("tcp://10.0.0.1:5556")

current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
file_name = "data/Differential_Data_" + current_date + ".csv"

df = pd.DataFrame(columns = ["LOX psi", "KER psi", "PRES psi"])
df.to_csv(file_name, mode = 'w')

# Queue of all data that will later be sent to the server
SEND_INFO = queue.Queue()

# Queue of all demands from the server
RECEIVED_LOGS = queue.Queue()
RECEIVED_MESSAGES = queue.Queue()

# Enums for status of server
class Status(IntEnum):
    WAITING = 1
    CMD_READY = 2
    DMR_READY = 3

# Current status of the server (used by host to test
# connection and determine when to send messages)
SERVER_STATUS = 0

# Set if the server status changed
STATUS_CHANGE = threading.Event()
STATUS_CHANGE.clear()

def sender():
    '''Immediately sends any info in the
    SEND_INFO queue over the socket'''
    global SEND_INFO
    while(True):
        send_socket.send_string(SEND_INFO.get())

def receiver():
    '''Puts any received info from the socket
    in the RECEIVED_INFO queue'''
    global RECEIVED_LOGS, RECEIVED_MESSAGES, SERVER_STATUS
    while(True):
        message = receive_socket.recv()
        message = str(message, 'UTF-8')
        a = message.find('%')
        if message[:a] == "log":
            RECEIVED_LOGS.put(message[a+1:])
        elif message[:a] == "msg":
            RECEIVED_MESSAGES.put(message[a+1:])
        elif message[:a] == "sta":
            a = int(message[a+1:])
            if SERVER_STATUS != a:
                SERVER_STATUS = a
                STATUS_CHANGE.set()

def logger():
    '''Thread which stores all data in the RECEIVED_LOGS
    queue as a csv file'''
    while(True):
        data = RECEIVED_LOGS.get()
        with open(file_name, 'a') as file:
            file.write(data)
            file.close()

def req_status():
    '''Manually get the current status of the server'''
    global SEND_INFO
    message = "sta%"
    SEND_INFO.put(message)

def user_io():
    '''Thread which controls user io, by getting input
    and printing output'''
    global SEND_INFO, STATUS_CHANGE, SERVER_STATUS
    while(True):
        STATUS_CHANGE.wait()
        STATUS_CHANGE.clear()

        if SERVER_STATUS == Status.WAITING:
            print(". . .")
        elif SERVER_STATUS == Status.CMD_READY:
            cmd = input("> > > ")
            cmd = "cmd%" + cmd
            SEND_INFO.put(cmd)
        elif SERVER_STATUS == Status.DMR_READY:
            dmr = input("---> ")
            dmr = "dmr%" + dmr
            SEND_INFO.put(dmr)

def user_messages():
    '''Thread which prints all received messages to the console'''
    global RECEIVED_MESSAGES
    while(True):
        message = RECEIVED_MESSAGES.get()
        print(message)


send = threading.Thread(name='sender', target=sender)
send.start()

receive = threading.Thread(name='receiver', target=receiver)
receive.start()

log = threading.Thread(name='logger', target=logger)
log.start()

req_status()

STATUS_CHANGE.wait()
print("Sucessfully Connected")

user_inout = threading.Thread(name='userio', target=user_io)
user_inout.start()

user_message = threading.Thread(name='user_messages', target=user_messages)
user_message.start()

'''Message types:
    Sent:
        cmd - Command with arguments, which can be executed on server
        dmr - Replies to demands from the server
        sta - Requests the server status
    Received:
        log - CSV data from the server
        sta - The current server status'''
