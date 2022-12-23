#####
## 
## For the Honeywell SSCDANT030PG2A3 liquid media pressure sensor
## https://media.digikey.com/pdf/Data%20Sheets/Honeywell%20PDFs/ssc_series_DS.pdf
## https://prod-edam.honeywell.com/content/dam/honeywell-edam/sps/siot/en-us/products/sensors/pressure-sensors/board-mount-pressure-sensors/common/documents/sps-siot-i2c-comms-digital-output-pressure-sensors-tn-008201-3-en-ciid-45841.pdf?download=false 
##
#####


import time
from smbus import SMBus

class SSC30:

    def __init__(self, ADDRESS = 0x28):
        # Default i2c address of device
        self.ADDRESS = 0x28
        # Instantiate SMBus object (Rpi uses /dev/i2c/1)
        self.bus = SMBus(1)
    
    def get_tempC(self):
        # Get 3 bytes - last is Temp
        data = self.bus.read_i2c_block_data(self.ADDRESS, 0, 3)
        tempR = data[2]
        # Conversion (see datasheet)
        tempR <<= 3
        tempC = round(((tempR / 2047) * 200) - 50, 1)
        return tempC

    def get_tempF(self):
        tempC = self.get_tempC()
        tempF = round((tempC * 1.8) + 32, 1)
        return tempF

    def get_pressPSI(self):
        # Get first two bytes of pressure data
        data = self.bus.read_i2c_block_data(self.ADDRESS, 0, 2)
        # Combine two bytes
        # Get Most Sig byte
        presOut = data[0]
        # Mask out status bits (if present)
        presOut &= 0b00111111
        # Left shift it 8 bits
        presOut <<= 8 
        # OR mask in the Least Sig byte
        presOut |= data[1]
        #print(presOut)
        # Conversion variables
        OUTmax = 16383 # 100% of 2^14 counts
        OUTmin = 1638  # 10%
        PRESmax = 30   # in psi
        PRESmin = 0    # in psi
        # Conversion Calculations (see datasheet)
        presPSI = (presOut - OUTmin) * (PRESmax - PRESmin) 
        presPSI = (presPSI / (OUTmax - OUTmin)) + PRESmin
        return round(presPSI,4)
    
    def get_pressFT(self):
        psi = self.get_pressPSI()
        ft = psi * 2.30666
        return round(ft, 4)
