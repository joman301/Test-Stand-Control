import random
import serial
import serial.tools.list_ports


class Communication:
    baudrate = ''
    portName = ''
    dummyPlug = False
    testPlug = False
    ports = serial.tools.list_ports.comports()
    ser = serial.Serial()

    def __init__(self):
        self.baudrate = 9600
        print("The available ports are (if none appear, press any letter): ")
        for port in sorted(self.ports):
            # Yoinking the ports available on the computer: https://stackoverflow.com/a/52809180
            print(("{}".format(port)))
        self.portName = input("Write serial port name (ex: /dev/ttyUSB0): ")
        try:
            self.ser = serial.Serial(self.portName, self.baudrate)  # Trying to connect to the port and read data
        except serial.serialutil.SerialException:
            print("Can't open : ", self.portName)  # Runs if it can't connect to the port, turns dummy mode on
            print("Please enter any letter if you want dummy data, or 'test' if you want to test.")
            print("This will default to dummy data if neither selected.")
            desired_data = input('Desired Data:')
            if desired_data == 'test':
                self.testPlug = True
                print("Entering test mode, let's see what stupid data is being pumped in")
            else:
                self.dummyPlug = True
                print("Dummy mode activated")

    def close(self):
        if(self.ser.isOpen()):
            self.ser.close()
        else:
            print(self.portName, " it's already closed")

    def getData(self):
        if not self.dummyMode and not self.testMode:  # Pulls data from serial mode if dummy and test not turned on
            value = self.ser.readline()  # read line (single value) from the serial port
            decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
            # print(decoded_bytes)
            value_chain = decoded_bytes.split(",")
        elif self.testMode:  # This guy is the test data!! Pump in whatever data YA HEARDDDDDDDD
            value_chain = [1] + random.sample(range(0, 300), 3) + \
                [random.getrandbits(1)] + random.sample(range(0, 30), 8)
            print(value_chain)
        else:  # The lovely dummy mode provided standard by the program Jon yoinked
            value_chain = [0] + random.sample(range(0, 300), 1) + \
                [random.getrandbits(1)] + random.sample(range(0, 20), 8)
            print(value_chain)

        return value_chain


    def isOpen(self):
        return self.ser.isOpen()

    def dummyMode(self):
        return self.dummyPlug

    def testMode(self):
        return self.testPlug
