# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""
import configparser
import serial, time

def setup_arduino_communication():
    config = configparser.ConfigParser()
    config.read('../setup.ini')

    ser = serial.Serial(config['serialCom']['serialPort'], int(config['serialCom']['baudRate']))
    time.sleep(int(config['serialCom']['waitingSecondsToOpen']))

    resolution = int(config['arduino']['resolution'])
    voltage = float(config['arduino']['voltage'])

    return ser, resolution, voltage