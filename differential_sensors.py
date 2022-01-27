import os
import time
import pandas as pd
from datetime import datetime
from ADCDifferentialPi import ADCDifferentialPi

# I2C Addresses for hat
# Channels 1-4: Address One
# Channels 5-8: Address Two
I2C_ADDR_ONE = 0x68
I2C_ADDR_TWO = 0x6b

# Bitrate can be 12, 14, 16, or 18
BITRATE = 18

def main():
    adc = ADCDifferentialPi(I2C_ADDR_ONE, I2C_ADDR_TWO, BITRATE)

    #Create file for data
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    file_name = "data/Differential_Data_" + current_date + ".csv"

    df = pd.DataFrame(columns = ["Channel 1 Voltage", "Channel 1 Pressure"])
    df.to_csv(file_name, mode = 'w')

    while True:
        os.system('clear')

        #Read data from i2c lanes
        CH1_VOLTAGE = adc.read_voltage(1)
        print("Channel 1: %02f V" % CH1_VOLTAGE)

        CH1_PRESSURE = 100000*CH1_VOLTAGE
        print("Pressure: %02f psi" % CH1_PRESSURE)

        #Save data to the csv file
        current_time = datetime.now().strftime("%H:%M:%S")
        df = pd.DataFrame(
            {"Channel 1 Voltage" : [CH1_VOLTAGE],
                "Channel 1 Pressure" : [CH1_PRESSURE]},
                index = [current_time])            
        
        df.to_csv(file_name, mode='a', header=False)
        time.sleep(0.5)

if __name__ == '__main__':
    main()