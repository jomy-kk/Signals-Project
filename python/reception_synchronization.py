# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

from python.setup import setup_arduino_communication
import pickle, numpy as np
from datetime import datetime

def ca1_receive_fixed_duration(duration, fileToSave=None, verbose=False):
    ser, res, volt = setup_arduino_communication()
    if verbose: print("Arduino communication open successfully")

    ser.write(str(duration).encode())
    arduinoData = ser.readline().decode().split('\r')
    if verbose:
        print("Data collected")

    arduinoData = [float(i)*volt/res for i in arduinoData[:-1]]
    if verbose:
        print("Data converted")
        print(arduinoData)
        print(len(arduinoData), "samples")

    if fileToSave is not None:
        try:
            with open('../pickle/' + fileToSave + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(arduinoData, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()
                if verbose: print("Signal saved in 'pickle'.")

        except IOError:
            print ("Error: File path provided does not seem to exist.")

    ser.close()
    if verbose: print("Arduino communication closed")


def cs_simulate_signal(duration, sampling_frequency, fileToSave=None, verbose=False):

    if verbose: print("Simulating signal for", duration, "seconds...")

    duration = duration * 1000 # ms
    intervals = 1/sampling_frequency*1000 # ms

    # cos 800 Hz
    samples = np.linspace(0, duration, int(intervals*duration), endpoint=False)
    signal1 = np.cos(2 * np.pi * 800 * samples)

    # sin 1600 Hz
    samples = np.linspace(0, duration, int(intervals*duration), endpoint=False)
    signal2 = np.sin(2 * np.pi * 1600 * samples)

    # cos 3200 Hz
    samples = np.linspace(0, duration, int(intervals*duration), endpoint=False)
    signal3 = np.cos(2 * np.pi * 3200 * samples)

    signal = 1000 * (signal1 + signal2 + signal3)

    if fileToSave is not None:
        try:
            with open('../pickle/' + fileToSave + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(signal, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()
                if verbose: print("Signal saved in 'pickle'.")

        except IOError:
            print ("Error: File path provided does not seem to exist.")

    '''
    fig = plt.figure()

    plt.subplot(4, 1, 1)
    plt.title("cos(800 Hz)")
    plt.plot(samples, signal1, 'r-', linewidth=0.5)
    plt.xlabel('Time (ms)')
    plt.xlim((0, 1000))
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 2)
    plt.title("sin(1600 Hz)")
    plt.plot(samples, signal2, 'g-', linewidth=0.5)
    plt.xlabel('Time (ms)')
    plt.xlim((0, 1000))
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 3)
    plt.title("cos(3200 Hz)")
    plt.plot(samples, signal3, 'b-', linewidth=0.5)
    plt.xlabel('Time (ms)')
    plt.xlim((0, 1000))
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 4)
    plt.title("1000 mV [cos(800 Hz) + sin(1600 Hz) + cos(3200 Hz)]")
    plt.plot(samples, signal, 'black', linewidth=0.5)
    plt.xlabel('Time (ms)')
    plt.xlim((0, 1000))
    plt.ylabel('Amplitude (mV)')

    plt.show()

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '_decomposed_1s.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

    fig = plt.figure()
    plt.plot(samples, signal1, 'r-', linewidth=0.5, label='cos(800 Hz)')
    plt.plot(samples, signal2, 'g-', linewidth=0.5, label='sin(1600 Hz)')
    plt.plot(samples, signal3, 'b-', linewidth=0.5, label='cos(3200 Hz)')
    plt.plot(samples, signal/1000, 'black', linewidth=1.5, label='Total')
    plt.xlim((0, 90))
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.legend(loc='best')

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '_decomposed_1period.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

    fig = plt.figure(figsize=(16,4))
    plt.plot(samples, signal, 'black', linewidth=0.5)
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude (mV)')

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '_complete.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")
    '''
    return signal


# Test
#ca1_receive_fixed_duration(30, 'AL5 arb', verbose=True)

duration = 6 # seconds
import matplotlib.pyplot as plt
res = cs_simulate_signal(duration, 6400, 'CS', verbose=True)
