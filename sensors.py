'''List of methods which can read data from
various sensors on the assembly'''
from datetime import datetime
from enum import Enum
from ADCDifferentialPi import ADCDifferentialPi

# A/D Differential Sensor
ADC_ADDR_ONE = 0x68
ADC_ADDR_TWO = 0x6b
ADC_BITRATE = 18

adc = ADCDifferentialPi(ADC_ADDR_ONE, ADC_ADDR_TWO, ADC_BITRATE)

class Data(Enum):
    LOX_PSI = 1
    KER_PSI = 2
    PRES_PSI = 3

#Calibration for a + bx voltage/data translation
#First value is y-int, second is slope
conv_linear = {
    Data.LOX_PSI: [0, 100000],
    Data.KER_PSI: [0, 100000],
    Data.PRES_PSI: [0, 100000]
}

def read(data):
    '''Returns the specified data from the sensor'''
    voltage = read_voltage(data)
    convert = conv_linear.get(data)
    return convert[0] + voltage*convert[1]

def read_all():
    '''Collects data from all sensors and stores it as one
    line of a .csv file'''
    csv_string = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    csv_string = csv_string + ','
    for item in Data:
        data_point = read(item)
        csv_string = csv_string + str(data_point) + ','
    csv_string = csv_string[:-1] + "\n"
    return csv_string


def read_voltage(data):
    '''Returns the raw voltage value from the sensor'''
    match data:    
        case Data.LOX_PSI:
            return adc.read_voltage(2)
        case Data.KER_PSI:
            return adc.read_voltage(3)
        case Data.PRES_PSI:
            return adc.read_voltage(4)

def calibrate(data):
    '''sets current value from sensor as 0'''
    global conv_linear
    current_value = read(data)
    convert = conv_linear.get(data)
    conv_linear[data] = [convert[0] - current_value, convert[1]]           

