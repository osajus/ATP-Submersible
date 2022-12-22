import time
from smbus import SMBus
from ctypes import c_short, c_ushort


class BMP:
    
    
    def __init__(self, ADDRESS = 0x77):
        # Default I2C address
        self.ADDRESS = ADDRESS  
        # RPI2 uses /dev/i2c/1
        self.bus = SMBus(1)  

    def getCalibrationData(self, reg_key):
        # Get the registry value of the key parameter
        reg_val = self.bus.read_i2c_block_data(self.ADDRESS, reg_key, 2)

        if (reg_key >= 0xB0 and reg_key <=0xB7):
            # AC5, AC6 are 'unsigned short' datatypes.
            return c_ushort((reg_val[0] << 8) + reg_val[1]).value
        else:
            # Everything else are 'short' datatypes. 
            return c_short((reg_val[0] << 8) + reg_val[1]).value

    def normalize_temp(self):
        # Read calibration data from BMP180 EEPROM.  Following datasheet
        AC5 = self.getCalibrationData(0xB2)
        AC6 = self.getCalibrationData(0xB4)
        MC = self.getCalibrationData(0xBC)
        MD = self.getCalibrationData(0xBE)
        # Write 02E into reg 0xF4 then wait 4.5ms
        self.bus.write_byte_data(self.ADDRESS, 0xF4, 0x2E)
        time.sleep(0.0045)

        # Read 0xF6 (MSB), 0xF7 (LSB)
        (msb, lsb) = self.bus.read_i2c_block_data(self.ADDRESS, 0xF6, 2)

        # Uncompensated Temp (UT) = MSB << 8 + LSB
        UT = (msb << 8) + lsb
        
        # Calculate True Temp (T)
        X1 = ((UT - AC6) * AC5) >> 15
        X2 = (MC << 11) / (X1 + MD)
        B5 = X1 + X2
        temp = (int(B5 + 8) >> 4) / 10.0
        return temp

    def get_tempC(self):
        tempC = self.normalize_temp()
        return tempC
    
    def get_tempF(self):
        tempC = self.normalize_temp()
        # Convert to degrees Freedom
        tempF = round((tempC * 1.8) + 32, 1)
        return tempF
