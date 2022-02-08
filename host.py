'''Host computer, which receives/sends
commands to the server'''
import zmq

context = zmq.Context()

receive_socket = context.socket(zmq.PAIR)
receive_socket.connect("tcp://10.0.0.1:5555")
send_socket = context.socket(zmq.PAIR)
send_socket.connect("tcp://10.0.0.1:5556")



while(True):
        message = receive_socket.recv()
        message = str(message, 'UTF-8')

        '''Message types:
        cmr - Request for a command from server
        req - Request for string input from server
        cmd - Command with arguments, which can be executed on server
        rep - Reply to a request for string input'''

        a = message.find('%')
        if message[:a] == "cmr":
                reply = input(message[a+1:])
                reply = "cmd%" + reply
                send_socket.send_string(reply)
        elif message[:a] == "req":
                reply = input(message[a+1:])
                reply = "rep%" + reply
                send_socket.send_string(reply)

