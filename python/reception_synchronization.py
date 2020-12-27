# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

from python.setup import setup_arduino_communication
import pickle
from datetime import datetime

def ca1_receive_fixed_duration(duration, fileToSave=None, verbose=False):
    ser, res, volt = setup_arduino_communication()
    if verbose: print("Arduino communication open successfully")

    ser.write(str(duration).encode())
    arduinoData = ser.readline().decode().split('\r')
    if verbose:
        print("Data collected")

    arduinoData = [float(i)*volt/res for i in arduinoData[:-1]]
    if verbose: print("Data converted")

    if fileToSave is not None:
        try:
            with open('../pickle/ca1 ' + fileToSave + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(arduinoData, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()

        except IOError:
            print ("Error: File path provided does not seem to exist.")

    ser.close()
    if verbose: print("Arduino communication closed")


# Test
ca1_receive_fixed_duration(4, 'exA', verbose=True)