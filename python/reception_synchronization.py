# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

from python.setup import setup_arduino_communication
import pickle, numpy as np
from datetime import datetime
import tkinter as tk
import time as T

def ca1_receive_fixed_duration(duration, sampling_frequency, fileToSave=None, verbose=False):
    ser, res, volt = setup_arduino_communication()
    if verbose: print("Arduino communication open successfully")

    n_samples = duration*sampling_frequency
    data_a = np.array([])
    data_b = np.array([])

    ser.reset_input_buffer()
    received = ser.readline().decode().split('\r\n')[0]
    a, b = received.split(';')
    label_a, label_b = a.split(':')[0], b.split(':')[0]
    if verbose: print("Started sampling...")

    while n_samples > 0:
        values = ser.readline().decode().split('\r\n')
        a, b = values[0].split(';')
        data_a = np.append(data_a, a.split(':')[1])
        data_b = np.append(data_b, b.split(':')[1])
        n_samples -= 1

    if verbose: print("Data collected: ", duration, "seconds.")

    data_a = [float(i)*volt/res for i in data_a]
    data_b = [float(i)*volt/res for i in data_b]
    if verbose:
        print("Data converted")
        #print(data_a)
        print('From pin', label_a + ':', len(data_a), "samples")
        #print(data_b)
        print('From pin', label_b + ':', len(data_b), "samples")

    if fileToSave is not None:
        try:
            with open('../pickle/' + fileToSave + ' pin' + label_a + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(data_a, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()
            with open('../pickle/' + fileToSave + ' pin' + label_b + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(data_b, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()

            if verbose: print("Signals saved in 'pickle'.")

        except IOError:
            print ("Error: File path provided does not seem to exist.")

    ser.close()
    if verbose: print("Arduino communication closed")

def ca2_receive_free_duration(fileToSave=None, verbose=False):
    global cond, data, time, fs, vb, file
    cond = False
    data = np.array([])
    time = np.array([])
    vb, file = verbose, fileToSave


    ser, res, volt = setup_arduino_communication()
    ser.reset_input_buffer()
    if verbose: print("Arduino communication open successfully")

    def acquire_stop():
        global cond, data, time, fs, vb, file
        cond = False
        ser.write('0'.encode())
        if verbose: print("Data collected")

        data = [float(i) * volt / res for i in data] # volts
        initial_time = float(time[0])
        time = [(float(t) - initial_time)/1000 for t in time] # seconds
        if vb:
            print("Data converted")
            print(len(data), "samples")

        if file is not None:
            try:
                with open('../pickle/' + file + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                    pickle.dump([time, data], output, protocol=pickle.HIGHEST_PROTOCOL)
                    output.close()
                    data.clear()
                    if vb: print("Signal saved in 'pickle'.")

            except IOError:
                print("Error: File path provided does not seem to exist.")

        '''
        from matplotlib import pyplot as plt
        fig = plt.figure()
        plt.plot(time, data, 'b-', linewidth=0.5)
        plt.xlabel('Time (s)')
        plt.xlim((1, 2))
        plt.ylabel('Amplitude (V)')

        fig.savefig('../plots/AL6.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

        plt.show()
        '''


    def acquire_start():
        global cond
        cond = True
        ser.write('1'.encode())
        root.after(1000, get_data)

    global nsamples
    nsamples = 0

    def get_data():
        global cond, data, time, fs, vb, nsamples
        if cond == True:
            if vb: print("Sampling...")
            received = ser.readline().decode().split('\r\n')[0]
            received = received.split(':')
            t = received[0]
            val = received[1]
            time = np.append(time, t)
            data = np.append(data, val)
            nsamples = nsamples + 1
            if nsamples == 4800:
                cond = False
                acquire_stop()
            root.after(1, get_data)

    def quit():
        ser.close()
        if verbose: print("Arduino communication closed")
        root.quit()

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    root.title("PSSI - Group B3 - Acquire signal")

    start_button = tk.Button(frame, text="Start Acquisition", command=lambda: acquire_start())
    start_button.pack(side=tk.LEFT)

    stop_button = tk.Button(frame, text="Stop Acquisition", command=lambda: acquire_stop())
    stop_button.pack(side=tk.LEFT)

    quit_button = tk.Button(frame, text="Quit", fg="red", command=lambda: quit())
    quit_button.pack(side=tk.RIGHT)

    root.mainloop()
    root.after(1, acquire_start)

    return time, data


def cs_simulate_signal(duration, sampling_frequency, fileToSave=None, verbose=False):

    if verbose: print("Simulating signal for", duration, "seconds...")

    samples = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False)

    # cos 800 Hz
    signal1 = np.cos(2 * np.pi * 800 * samples)

    # sin 1600 Hz
    signal2 = np.sin(2 * np.pi * 1600 * samples)

    # cos 3200 Hz
    signal3 = np.cos(2 * np.pi * 3200 * samples)

    # summed signal
    signal = 1000 * (signal1 + signal2 + signal3)

    if fileToSave is not None:
        try:
            with open('../pickle/' + fileToSave + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(signal, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()
                if verbose: print("Signal saved in 'pickle'.")

        except IOError:
            print ("Error: File path provided does not seem to exist.")


    from matplotlib import pyplot as plt

    fig = plt.figure(figsize=(16,8))

    plt.subplot(4, 1, 1)
    plt.title("cos(800 Hz)")
    plt.plot(samples, signal1, 'r-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim((0, 0.1))
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 2)
    plt.title("sin(1600 Hz)")
    plt.plot(samples, signal2, 'g-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim((0, 0.1))
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 3)
    plt.title("cos(3200 Hz)")
    plt.plot(samples, signal3, 'b-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim((0, 0.1))
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 4)
    plt.title("1000 mV [cos(800 Hz) + sin(1600 Hz) + cos(3200 Hz)]")
    plt.plot(samples, signal, 'black', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim((0, 0.1))
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
    plt.xlim((0, 0.00125))
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend(loc='best')
    plt.show()

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '_decomposed_1period.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

    fig = plt.figure(figsize=(16,4))
    plt.plot(samples, signal, 'black', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim((0, 0.05))
    plt.ylabel('Amplitude (mV)')
    plt.show()

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '_complete.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

    return signal



# Test
#ca1_receive_fixed_duration(1, 400, verbose=True)

#duration = 6 # seconds
#res = cs_simulate_signal(duration, 6400, 'CS', verbose=True)

ca2_receive_free_duration(400, 'AL6', verbose=True)
