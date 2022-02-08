import queue
import threading
import zmq

context = zmq.Context()
send_socket = context.socket(zmq.PAIR)
send_socket.bind("tcp://*:5555")
receive_socket = context.socket(zmq.PAIR)
receive_socket.bind("tcp://*:5556")

# Queue of all data either received or to be sent
SEND_INFO = queue.Queue()
RECEIVED_INFO = queue.Queue()

# Queue of all data which is a reply to a request
RECEIVED_REPLIES = queue.Queue(1)

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

def receive_reply(message):
    '''adds a reply to the RECEIVED_REPLIES queue'''
    global RECEIVED_REPLIES
    RECEIVED_REPLIES.put(message)

def get():
    '''gets the earliest info from the
    RECEIVED_INFO queue'''
    return RECEIVED_INFO.get()

def get_reply():
    '''gets the earliest reply from
    the RECEIVED_REPLIES queue'''
    return RECEIVED_REPLIES.get()

def send(message):
    '''adds a string to the SEND_INFO
    queue'''
    SEND_INFO.put(message)
    

CAN_REQUEST = threading.Event()
CAN_REQUEST.set()

def string_request(message):
    '''request input from the host, and blocks other threads from 
    getting input from the user. Receieved string is returned value'''
    global CAN_REQUEST
    CAN_REQUEST.wait()
    CAN_REQUEST.clear()
    
    message = 'req%' + message
    SEND_INFO.put(message)

    a = get_reply()
    CAN_REQUEST.set()
    return a

def command_request(message = ""):
    '''request a command from the host, and blocks other threads from getting
    input from the user. Received command is immediately executed in main loop'''
    global CAN_REQUEST
    CAN_REQUEST.wait()
    CAN_REQUEST.clear()
    
    message = 'cmr%' + message + "\n> > > "
    SEND_INFO.put(message)
    CAN_REQUEST.set()

