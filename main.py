#import sensors
#import commands as cmd

import threading
import commands as cmd
import message as msg

def main():

    # Begin listening for and sending requests over socket
    sender = threading.Thread(name='sender', target=msg.sender)
    sender.start()

    receiver = threading.Thread(name='receiver', target=msg.receiver)
    receiver.start()

    msg.command_request()


    while(True):
        # Receive command from host

        user_message = msg.get()
        str(user_message, 'UTF-8')
        a = user_message.find('%')

        if user_message[:a] == 'cmd':

            cmd_string = user_message[a+1:]
            cmd_string = str(cmd_string, 'UTF-8')
            user_command = cmd.parse(cmd_string)       

            # Create new thread and run command
            x = threading.Thread(name='command', target=cmd.exe, args=[user_command])
            x.start()
        elif user_message[:a] == 'rep':
            msg.receive_reply(user_message[a+1:])
            

if __name__ == "__main__":
    main()