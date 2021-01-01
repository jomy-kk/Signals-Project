# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

from python.setup import setup_arduino_communication
import pickle, numpy as np
from datetime import datetime
import tkinter as tk

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

def ca2_receive_free_duration(sampling_frequency, fileToSave=None, verbose=False):
    global cond, data, fs, vb
    cond = False
    data = np.array([])
    fs, vb = int(sampling_frequency), verbose


    ser, res, volt = setup_arduino_communication()
    ser.reset_input_buffer()
    if verbose: print("Arduino communication open successfully")

    def acquire_stop():
        global cond, data
        cond = False
        ser.write('0'.encode())
        if verbose: print("Data collected")

        data = [float(i) * volt / res for i in data]
        if verbose:
            print("Data converted")
            print(len(data), "samples")

        if fileToSave is not None:
            try:
                with open('../pickle/' + fileToSave + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                    pickle.dump(data, output, protocol=pickle.HIGHEST_PROTOCOL)
                    output.close()
                    data.clear()
                    if verbose: print("Signal saved in 'pickle'.")

            except IOError:
                print("Error: File path provided does not seem to exist.")

    def acquire_start():
        global cond
        cond = True
        root.after(1, get_data)

    def get_data():
        global cond, data, fs, vb
        if cond == True:
            if vb: print("Sampling...")
            ser.write('1'.encode())
            val = ser.readline().decode().split('\r\n')
            data = np.append(data, val[0])
            root.after(int(1/fs*1000), get_data)

    def quit():
        ser.close()
        if verbose: print("Arduino communication closed")
        root.quit()

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    root.title("PSSI - Group B3 - Acquire analog signal")

    start_button = tk.Button(frame, text="Start Acquisition", command=lambda: acquire_start())
    start_button.pack(side=tk.LEFT)

    stop_button = tk.Button(frame, text="Stop Acquisition", command=lambda: acquire_stop())
    stop_button.pack(side=tk.LEFT)

    quit_button = tk.Button(frame, text="Quit", fg="red", command=lambda: quit())
    quit_button.pack(side=tk.RIGHT)

    root.mainloop()
    root.after(1, acquire_start)

    return data


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

#duration = 6 # seconds
#res = cs_simulate_signal(duration, 6400, 'CS', verbose=True)

ca2_receive_free_duration(400, 'test', verbose=True)