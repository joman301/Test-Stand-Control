import os
import time
from ADCDifferentialPi import ADCDifferentialPi

# I2C Addresses for hat
# Channels 1-4: Address One
# Channels 5-8: Address Two
I2C_ADDR_ONE = 0x68
I2C_ADDR_TWO = 0x6b

# Bitrate can be 12, 14, 16, or 18
BITRATE = 16

def main():
    adc = ADCDifferentialPi(I2C_ADDR_ONE, I2C_ADDR_TWO, BITRATE)

    while True:
        os.system('clear')
        print("Channel 1: %02f" % adc.read_voltage(1))
        print("Channel 2: %02f" % adc.read_voltage(2))
        print("Channel 3: %02f" % adc.read_voltage(3))
        print("Channel 4: %02f" % adc.read_voltage(4))
        print("Channel 5: %02f" % adc.read_voltage(5))
        print("Channel 6: %02f" % adc.read_voltage(6))
        print("Channel 7: %02f" % adc.read_voltage(7))
        print("Channel 8: %02f" % adc.read_voltage(8))
        time.sleep(2)

if __name__ == '__main__':
    main()