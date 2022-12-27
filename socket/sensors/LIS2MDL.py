#####
## 
## For the Adafruit LIS2MDL - 488 friple-axis magnetometer
## 
## https://learn.adafruit.com/adafruit-lis2mdl-triple-axis-magnetometer/overview
## https://www.mouser.com/datasheet/2/389/lis2mdl-1849648.pdf
##
#####
#print(bin(a[1])[2:].zfill(8))

import time
from smbus2 import SMBus
import struct


# Register address map
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

ADDRESS = 0x1E
bus = SMBus(1)  

def get_config():
    print(f"Current CFG-A {bin(bus.read_i2c_block_data(ADDRESS, CFG_REG_A, 1)[0])[2:].zfill(8)}")
    #print(f"Current CFG-B {bin(bus.read_i2c_block_data(ADDRESS, CFG_REG_B, 1)[0])[2:].zfill(8)}")
    #print(f"Current CFG-C {bin(bus.read_i2c_block_data(ADDRESS, CFG_REG_C, 1)[0])[2:].zfill(8)}")
    #print(f"Current STATUS {bin(bus.read_i2c_block_data(ADDRESS, STATUS_REG, 1)[0])[2:].zfill(8)}")
    

def change_config():
    #bus.write_block_data(ADDRESS, CFG_REG_A, [0b00000000])
    bus.write_byte_data(ADDRESS, CFG_REG_A, 0b00000010)
    time.sleep(0.2)
    print(f"New CFG-A {bin(bus.read_i2c_block_data(ADDRESS, CFG_REG_A, 1)[0])[2:].zfill(8)}")
    print(f"Current STATUS {bin(bus.read_i2c_block_data(ADDRESS, STATUS_REG, 1)[0])[2:].zfill(8)}")

def set_mode(state):
    #  Get current state
    reg_val = bus.read_byte_data(ADDRESS, CFG_REG_A, 1)
    
    if state == 'idle':
        # Set bits 0 and 1 to 11
        reg_val |= (1 << 0)
        reg_val |= (1 << 1)
    elif state == 'single':
        # Set bits 0 and 1 to 01
        reg_val |= (1 << 0)
        reg_val &= ~ (1 << 1) & 255        
    elif state == 'continuous':
        # Set bits 0 and 1 to 00
        reg_val &= ~ (1 << 0) & 255 
        reg_val &= ~ (1 << 1) & 255 
    else:
        print("I don't understand that")
    bus.write_byte_data(ADDRESS, CFG_REG_A, reg_val)
    print(f"**Set CFG-A to {bin(bus.read_i2c_block_data(ADDRESS, CFG_REG_A, 1)[0])[2:].zfill(8)}")

def set_temp_comp(state: bool):
    #  Get current state
    reg_val = bus.read_byte_data(ADDRESS, CFG_REG_A, 1)
    if state == True:
        # Set bit 7 to 1
        reg_val |= (1 << 7)
    else:
        # Set bit 7 to 0
        reg_val &= ~ (1 << 7) & 255 
    bus.write_byte_data(ADDRESS, CFG_REG_A, reg_val)
    print(f"**Set CFG-A to {bin(bus.read_i2c_block_data(ADDRESS, CFG_REG_A, 1)[0])[2:].zfill(8)}")

def reset_reg_a():
    bus.write_byte_data(ADDRESS, CFG_REG_A, 0x3)
    print(f"**New CFG-A {bin(bus.read_i2c_block_data(ADDRESS, CFG_REG_A, 1)[0])[2:].zfill(8)}")       


def get_data():    
    buf = bytearray(struct.calcsize('<h'))
    buf[0],  buf[1] = bus.read_i2c_block_data(ADDRESS, OUTX_L_REG, 2)
    print(list(buf))
    print(struct.unpack_from('<h', buf, 0)[0])
    print(struct.unpack_from('<h', buf, 0)[0] * 0.15)
    
    

#get_config()
#change_config()
#reset_reg_a()
#set_mode('single')
#set_temp_comp(True)
#

set_mode('continuous')

i = 0
while i < 1:
    get_data()
    time.sleep(1)
    i +=1