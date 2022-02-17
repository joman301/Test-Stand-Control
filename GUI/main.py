import math
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from communication import Communication
from data_handler import data_handler
from GUI import *
from class_making import *
import numpy
import pandas as pd
import numpy as np
import sys
from time import sleep
import csv

sec_total = 0


def update_graphs(sensors):  # This accepts a dictionary of sensors (created in the initialization area)
    for sensor in sensors.values():
        sensor.graph_update(sec_total)
    # return data_combined


# A function used to update the GUI - choose what data you want updated
def update():
    global sec_total
    try:
        sec_total += (time_increment / 1000)
        update_time(sec_total, time_increment)
        update_graphs(p_sensors1)
        update_graphs(p_sensors2)
        update_graphs(p_sensors3)
        #update_graphs(t_sensors)

        # data_base.save(value_chain) # Part of the saving function

    except IndexError:
        print('Something is not indexing in the update function in main.py, please fix')


'''
    Initialization code -------------------------------------------------------------
'''
# press_csv = 'data_example.csv'  # The csv file to read things in from
press_csv = 'test.csv'
read_csv = False  # If reading in live data from csv, set this to true
time_increment = 250  # Amount of time it will take to update the GUI and data collection, measured in ms


# Example pressure sensor objects and characteristics
p_sensors1 = {
    'p_sensor1': Sensor('Pressure Sensor 1', 'Pressure', 1, 0, press_csv, read_csv),
    # 'p_sensor2': Sensor('Pressure Sensor 2', 'Pressure', 1, 1, press_csv, read_csv),
    # 'p_sensor3': Sensor('Pressure Sensor 3', 'Pressure', 1, 2, press_csv, read_csv)
}
# Creating a second pressure sensor array
p_sensors2 = {
    'p_sensor4': Sensor('Pressure Sensor 4', 'Pressure', 2, 3, press_csv, read_csv),
    #'p_sensor5': Sensor('Pressure Sensor 5', 'Pressure', 2, 4, press_csv, read_csv),
    #'p_sensor6': Sensor('Pressure Sensor 6', 'Pressure', 2, 5, press_csv, read_csv)
}
# Creating a third pressure sensor array
p_sensors3 = {
    'p_sensor7': Sensor('Pressure Sensor 7', 'Pressure', 3, 6, press_csv, read_csv),
    #'p_sensor8': Sensor('Pressure Sensor 8', 'Pressure', 3, 7, press_csv, read_csv),
    #'p_sensor9': Sensor('Pressure Sensor 9', 'Pressure', 3, 8, press_csv, read_csv)
}
# Example temperature sensor objects and characteristics
'''
t_sensors = {
    't_sensor1': Sensor('Temperature Sensor 1', 'Temperature', 4, 0, press_csv, read_csv),
    't_sensor2': Sensor('Temperature Sensor 2', 'Temperature', 4, 1, press_csv, read_csv),
    't_sensor3': Sensor('Temperature Sensor 3', 'Temperature', 4, 2, press_csv, read_csv)
}
'''

'''
    GUI Set-up and Updating Scripts ========================================================================
'''

# Begins the loop/ update for the GUI script
if ser.isOpen() or ser.dummyMode() or ser.testMode():
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(time_increment)  # Set this to the desired update speed of the GUI [milliseconds]
else:
    print("Something is wrong with the update call for the GUI, investigate!")

# This is the command that keeps the GUI file running
if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()  # This command (.exec) runs the program and opens everything above


'''
    Stuff that is going to run if/when you click the 'x' to exit the GUI ======================================
'''


'''# Infinite loop will not run until GUI is closed - decide if anything needs to happen after GUI closes
while True:
    print('Test test test')
    sleep(1)'''
