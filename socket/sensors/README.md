# ATP ROV Sensor Library
> This folder contains libraries for the various sensors operation onbard the ROV.
> See <a href="https://github.com/osajus/ATP-Submersible/blob/main/requirements.txt">requirements.txt</a> in root for includes used.

---

## Sensor Suite
> Currently, sensors include:
- BMP180
    - <a href="http://shorturl.at/dfwOZ" target="_new">Datasheet</a>
    - A BOSCH sensor that provides both pressure and temperature data.
    - Currently being used only for chamber temperature.
    - BMP180.py is written only to retrieve temp data
        - **Class Name:** BMP
        - **Get temp in degrees F:** get_tempF()
        - **Get temp in degrees C:** get_tempC()

- SSCDANT030PG2A3 
    - <a href="http://shorturl.at/dCPU0" target="_new">Datasheet</a> and <a href="http://shorturl.at/dvzFZ" target="_new">I2C Communications</a>
    - A Honeywell liquid media pressure and temperature sensor
    - This model uses i2c and is rated up to 30 psi, ~70ft
    - Datasheet is not great at explaining things so this library could be improved upon.
        - **Class Name:** SSC30
        - **Get temp in degrees F:** get_tempF()
        - **Get temp in degrees C:** get_tempC()
        - **Get pressure in PSI:** get_pressPSI()
        - **Get pressure in Feet:** get_pressFT()

- LIS2MDL
    - <a href="http://shorturl.at/ryRS8" target="_new">Datasheet</a> and <a href="http://shorturl.at/CLNQX" target="_new">Magnetometer</a>
    - An Adafruit LIS2MDL breakout magnetometer.
    - Uses i2c.  Library based on circuitpython version with significant revision.
    - LIS2MDL.py is written to return compass heading and has calibration mode.
        - **Class Name:** LIS2MDL
        - **Get Compass Heading:** get_heading()
        - **Calibrate:** calibrate()
        - **View Raw data** get_data()
