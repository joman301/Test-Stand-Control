'''Responsible for managing all incoming and outgoing
data between host and server, and ensures multiple
threads have access to such functionality'''
import queue
import threading
import zmq
import sensors
from enum import IntEnum

# ZMQ setup
context = zmq.Context()
send_socket = context.socket(zmq.PUSH)
send_socket.bind("tcp://*:5555")
receive_socket = context.socket(zmq.PULL)
receive_socket.bind("tcp://*:5556")

# Queue of all data that will later be sent to the host
SEND_INFO = queue.Queue()

# Queue of all demands from the host
RECEIVED_DEMANDS = queue.Queue(1)

# Queue of all responses to demands from the server
DEMAND_REPLIES = queue.Queue(1)

# Queue of all commands from the host
RECEIVED_COMMANDS = queue.Queue(1)

class Status(IntEnum):
    WAITING = 1
    CMD_READY = 2
    DMR_READY = 3

# Current status of server (used by host to test 
# connection and determine when to send messages)
SERVER_STATUS = Status.WAITING

# Global entity which determines whether
# to send .csv logging data
LOGGING = threading.Event()
LOGGING.clear()

# Global entity which determines whether
# requests can be made by the server
CAN_GET_USER_INPUT = threading.Event()
CAN_GET_USER_INPUT.set()

def sender():
    '''Immediately sends any info in the
    SEND_INFO queue over the socket'''
    global SEND_INFO
    while(True):
        send_socket.send_string(SEND_INFO.get())

def receiver():
    '''Puts any received info from the socket
    in its respective queue'''
    global RECEIVED_COMMANDS, DEMAND_REPLIES
    while(True):
        message = receive_socket.recv()
        message = str(message, 'UTF-8')
        a = message.find('%')
        if message[:a] == "cmd":
            RECEIVED_COMMANDS.put(message[a+1:], block=False)
        elif message[:a] == "dmr":
            DEMAND_REPLIES.put(message[a+1:], block=False)
        elif message[:a] == "sta":
            set_status(SERVER_STATUS)

def tell(message = ""):
    '''Sends a string message to the host'''
    global SEND_INFO
    message = "msg%" + message
    SEND_INFO.put(message)

def send_logs():
    '''thread that reads sensor data and sends it to the
    host over the socket'''
    global SEND_INFO
    global LOGGING
    LOGGING.wait()

    threading.Timer(0.1, send_logs).start()
    message = 'log%' + sensors.read_all()
    SEND_INFO.put(message)

def get_cmd():
    '''waits until user input is allowed, then sets server status
    to enable commands, then returns received command'''
    global RECEIVED_COMMANDS, CAN_GET_USER_INPUT, SERVER_STATUS

    CAN_GET_USER_INPUT.wait()
    set_status(Status.CMD_READY)

    a = RECEIVED_COMMANDS.get()
    set_status(Status.WAITING)

    return a

def get_dmd():
    '''Received demands from the host, and replies with a string'''
    global RECEIVED_DEMANDS
    demand = RECEIVED_DEMANDS.get()
    message = "dmr%"
    if demand == "status":
        message = str(SERVER_STATUS)
    SEND_INFO.put(message)
        

def demand(message):
    '''Waits until user input is allowed, then sets server status
    to enable demand replies, then returns received demand reply'''
    global CAN_GET_USER_INPUT
    global SERVER_STATUS

    CAN_GET_USER_INPUT.wait()
    CAN_GET_USER_INPUT.clear()

    tell(message)

    set_status(Status.DMR_READY)
    a = DEMAND_REPLIES.get()
    set_status(Status.WAITING)
    CAN_GET_USER_INPUT.set()
    return a

def logging(currently_logging = True):
    '''determines whether send_logs should send
    log data'''
    global LOGGING
    if currently_logging:
        LOGGING.set()
    else:
        LOGGING.clear()

def set_status(status):
    global SEND_INFO, SERVER_STATUS
    SERVER_STATUS = status
    message = "sta%" + str(int(status))
    SEND_INFO.put(message)

def cmd_ready():
    set_status(Status.CMD_READY)
    CAN_GET_USER_INPUT.set()