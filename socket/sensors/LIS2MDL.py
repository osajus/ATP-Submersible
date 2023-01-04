#####
## 
## For the Adafruit LIS2MDL - 488 friple-axis magnetometer
## 
## https://learn.adafruit.com/adafruit-lis2mdl-triple-axis-magnetometer/overview
## https://www.mouser.com/datasheet/2/389/lis2mdl-1849648.pdf
##
#####

import time
from smbus2 import SMBus
import struct
import math

#region Register Map
OFFSET_X_REG_L = 0x45
OFFSET_X_REG_H = 0x46
OFFSET_Y_REG_L = 0x47
OFFSET_Y_REG_H = 0x48
OFFSET_Z_REG_L = 0x49
OFFSET_Z_REG_H = 0x4A
CFG_REG_A = 0x60
CFG_REG_B = 0x61
CFG_REG_C = 0x62
STATUS_REG = 0x67
OUTX_L_REG = 0x68
OUTX_H_REG = 0x69
OUTY_L_REG = 0x6A
OUTY_H_REG = 0x6B
OUTZ_L_REG = 0x6C
OUTZ_H_REG = 0x6D
TEMP_OUT_L_REG = 0x6E
TEMP_OUT_H_REG = 0x6F
INT_CRTL_REG = 0x63
INT_SOURCE_REG = 0x64
INT_THS_L_REG = 0x65
#endregion


class LIS2MDL:
    _I2C_ADDRESS = 0x1E
    _MAG_SCALE = 0.15
    hardiron_calibration = [-7.334999999999999, 4.68], [-3.87, 3.1725], [-22.229999999999997, -14.355]
    bus = SMBus(1) 
    
    def __init__(self):
        self.reset()

    def reset(self):
        # Set the sensor to default state. Soft reset
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_A, 0b00100000)
        time.sleep(0.1)
        # Reboot
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_A, 0b01000000)
        time.sleep(0.1)
        # Set mode to continuous
        # Also enable temp compensation
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_A, 0b10000000)
        # Set BDU to avoid reading incorrect data when reading asynchronously
        # Also set interrupt signal to be driven on INT/DRDY pin
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_C, 0b01010000)
        # Set interrupt bit to latched
        # Also set polarity of interrupt bit (1 = interrupt)
        self.bus.write_byte_data(self._I2C_ADDRESS, INT_CRTL_REG, 0b00000110)
        # Set interrupt block recognition checks after hard-iron correction
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_B, 0b00001000)
        # Let measurements stabilize
        time.sleep(0.1)
    
    def their_reset(self):
        # This can probably be deleted soon
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_A, 0b00100000)
        time.sleep(0.1)
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_A, 0b01000000)
        time.sleep(0.1)
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_A, 0xF1)
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_B, 0x08)
        self.bus.write_byte_data(self._I2C_ADDRESS, CFG_REG_C, 0x50)
        self.bus.write_byte_data(self._I2C_ADDRESS, INT_CRTL_REG, 0xE7)

    def calibrate(self):
        self.hardiron_calibration = [[1000, -1000], [1000, -1000], [1000, -1000]]
        print("Calibrating in 3..")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)
        start_time = time.monotonic()
        while time.monotonic() - start_time < 10.0:
            magval = self.magnetic()
            print("Calibrating - X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(*magval))
            for i, axis in enumerate(magval):
                self.hardiron_calibration[i][0] = min(self.hardiron_calibration[i][0], axis)
                self.hardiron_calibration[i][1] = max(self.hardiron_calibration[i][1], axis)
            print("Calibration complete:")
            print("hardiron_calibration =", self.hardiron_calibration)

    def magnetic(self):
        _raw_x = self.get_data(OUTX_L_REG)
        _raw_y = self.get_data(OUTY_L_REG)
        _raw_z = self.get_data(OUTZ_L_REG)

        return (
            _raw_x * self._MAG_SCALE,
            _raw_y * self._MAG_SCALE,
            _raw_z * self._MAG_SCALE,
        )
    
    def get_data(self, coordinate):
        buf = bytearray(struct.calcsize('<h'))
        buf[0],  buf[1] = self.bus.read_i2c_block_data(self._I2C_ADDRESS, coordinate, 2)
        return struct.unpack_from('<h', buf, 0)[0] * 0.15
    
    def normalize(self,magvals):
        ret = [0, 0, 0]
        for i, axis in enumerate(magvals):
            minv, maxv = self.hardiron_calibration[1]
            axis = min(max(minv, axis), maxv)
            ret[i] = (axis - minv) * 200 / (maxv - minv) + -100
        return ret

    def get_heading(self):
        magvals = self.magnetic()
        normvals = self.normalize(magvals)
        compass_heading = int(math.atan2(normvals[1], normvals[0]) * 180.0 / math.pi)
        compass_heading += 180
        return compass_heading


def main():
    LIS = LIS2MDL()
    #LIS.calibrate()
    

    print("Getting ready to run")
    time.sleep(3)

    i = 0
    while i < 60:
        time.sleep(.5)
        i += 1
        compass_heading = LIS.get_heading()
        print("Heading:", compass_heading)

if __name__ == "__main__":
    main()
