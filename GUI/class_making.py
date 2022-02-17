import time
import pandas as pd
import numpy as np
import csv
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
import pyqtgraph as pg

from GUI import press_graph1, press_graph2, press_graph3, temp_graph, sec_total


# This class will be used to define all sensors and sensor operations, including graphing
class Sensor:
    def __init__(self, input_name, input_type, input_ar_num, input_pos, input_file, read_csv):
        self.name = input_name      # The given name of the sensor
        self.type = input_type      # The type of sensor (pressure, temp, etc)
        self.arr = input_ar_num     # Specifies which sensor array the sensor is part of
        self.pos = input_pos        # If in sensor array configuration, specifies order of sensors (should be 0-2)
        # self.pin0 = input_pin0      # The first sensor associated pin on the BBB
        # self.pin1 = input_pin1      # The second sensor associated pin on the BBB
        self.file = input_file      # The file name associated with the sensor
        self.read_csv = read_csv    # If true, this will read from the csv instead of generating data
        self.avg_data = []          # A list that will average the given data
        self.time = sec_total - 20

        if self.type == 'Pressure':
            if self.arr == 1:
                self.plot = press_graph1.plot(pen=(102, 252, 241))
            elif self.arr == 2:
                self.plot = press_graph2.plot(pen=(100, 100, 100))
            elif self.arr == 3:
                self.plot = press_graph3.plot(pen=(200, 200, 200))
            else:
                print('Error with {}: check that it has an array value of 1-3'.format(self.name))
        elif self.type == 'Temperature':
            self.plot = temp_graph.plot(pen=(102, 252, 241))

        self.data = np.zeros(20, dtype=float)  # An initially empty list used to contain data for plotting

    # This function is used to process csv files from PTs - returns the value corresponding to the psi of this sensor
    def csv_tail(self):
        with open(self.file, "r") as f:
            for line in f:  # Skips to the end of the file, returns the last line as a string
                pass
            line = line.strip()  # Stripping the \n character
            line = line.split(',')  # Splitting the string into parts based off of comma
            # float_line = [float(x) for x in line[1:]]  # Converts the data values into floats (REMOVES TIME STAMP)
            float_value = float(line[self.pos + 1])  # Yoinks the associated psi data value from the csv
        return float_value

    # This function will read the sensor based off of its type - whether a temperature or a pressure sensor
    def read_sensor(self):
        if self.type == 'Pressure':
            # print("I'm reading pressure")
            sensor_data = self.csv_tail()
            # Analog conversion data script
        elif self.type == 'Temperature':
            # print("I'm reading temperature")
            sensor_data = self.csv_tail()
            # Analog or digital conversion data script
        else:
            print('I think that you have entered something incorrectly')
        return sensor_data

    # This function will update the graph with data read for this sensor
    def graph_update(self, time):
        self.data[:-1] = self.data[1:]
        self.data[-1] = self.read_sensor()
        time_shifted = time - 20
        self.plot.setData(self.data)
        self.plot.setPos(time_shifted, 0)

    def average(self):
        print("I will be used to create the average of the data")

    def volt_to_psi(self):
        print("I will convert voltages to PSI for us to understand")

    def save_data(self):
        data_df = pd.DataFrame(self.data, columns=['Time', 'P0'])


# This class will be used to control and define valves in the system
class Valve:
    def __init__(self, input_name, input_type, input_pin):
        self.name = input_name
        self.type = input_type
        self.pin = input_pin
        self.state = 'AHHHHHH AHHHHHHHHH'
        self.df = pd.DataFrame(columns={'time', 'position'})

    def open(self):
        t = time.process_time()
        print("I will open the valve")
        self.state = 'open'

    def close(self):
        print("I will close the valve")
        self.state = 'closed'

    def get_state(self):
        print(self.name, 'is', self.state)


if __name__ == '__main__':
    print('This will print when this file is run directly, but this will not print if this file is being imported.')
    test_valve = Valve('Valve 1','Shutoff', 1)
    test_valve2 = Valve('Valve 2', 'Shutoff', 2)
