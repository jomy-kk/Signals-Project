# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

from python.setup import setup_arduino_communication
import pickle, numpy as np
from datetime import datetime
import tkinter as tk

def ca1_receive_fixed_duration(duration, sampling_frequency, fileToSave=None, verbose=False):
    '''
    Acquires #(duration*sampling_frequency) samples from 2 channels the Arduino sends,
    and returns them as numpy arrays.

    :param duration: The duration of the signal you want to simulate (in seconds).
    :param sampling_frequency: The frequency at which the signal would be sampled (in Hertz).

    :param fileToSave: If given, it stores both signals individually as pickle objects in that path inside 'pickle'.
    :param verbose: If given, the function log is printed on the terminal.

    :return: data_a, data_b
             The signals from each channel that where sent though the serial port.

    Notes:
        - The messages should be sent in a "chanelLabel:value;channelLabel:value" format, where "value"s are the
          analog amplitude values.

        - The analog amplitude values are converted to voltage values according to the resolution and
          operating voltage set in setup.ini

        - The serial line port and baud rate should be set in setup.ini
    '''

    # Open serial port
    ser, res, volt = setup_arduino_communication()
    if verbose: print("Arduino communication open successfully")

    # Prepares samples variables
    n_samples = duration*sampling_frequency
    data_a = np.array([])
    data_b = np.array([])

    # Retrieves the channel labels
    ser.reset_input_buffer()
    received = ser.readline().decode().split('\r\n')[0] # use one message (Arduino should be continuously sending)
    a, b = received.split(';')
    label_a, label_b = a.split(':')[0], b.split(':')[0]

    # Collecting the defined number of samples
    if verbose: print("Started sampling...")
    while n_samples > 0:
        values = ser.readline().decode().split('\r\n')
        a, b = values[0].split(';')
        data_a = np.append(data_a, a.split(':')[1])
        data_b = np.append(data_b, b.split(':')[1])
        n_samples -= 1
    if verbose: print("Data collected: ", duration, "seconds.")

    # Convert data to voltage values
    data_a = [float(i)*volt/res for i in data_a]
    data_b = [float(i)*volt/res for i in data_b]
    if verbose:
        print("Data converted")
        print('From pin', label_a + ':', len(data_a), "samples")
        print('From pin', label_b + ':', len(data_b), "samples")

    # Save both signals if 'fileToSave' was given
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

    # Close serial port
    ser.close()
    if verbose: print("Arduino communication closed")

    return data_a, data_b



def ca2_receive_free_duration(fileToSave=None, verbose=False):
    '''
    Creates a GUI window where the user can acquire 1 channel signal for as long as wanted.
    The user can do as many acquisitions as wanted.

    :param fileToSave: If given, it stores both signals individually as pickle objects in that path inside 'pickle'.
    :param verbose: If given, the function log is printed on the terminal.

    :return: time, data
             The time points and the voltage points that where sent though the serial port.

    Notes:
        - The messages should be sent in a "time:value" format, where "time"s are the time points in milliseconds,
          and value"s are the analog amplitude values.

        - The analog amplitude values are converted to voltage values according to the resolution and
          operating voltage set in setup.ini

        - The serial line port and baud rate should be set in setup.ini
    '''

    # Global variables to be accessed by other functions
    global cond, data, time, fs, vb, file
    cond = False # controls the exit of 'get_data' procedure
    data = np.array([])
    time = np.array([])
    vb, file = verbose, fileToSave

    # Open serial port
    ser, res, volt = setup_arduino_communication()
    ser.reset_input_buffer()
    if verbose: print("Arduino communication open successfully")


    def acquire_stop():
        global cond, data, time, fs, vb, file
        cond = False # Allows flow to exit 'get_data' procedure
        ser.write('0'.encode()) # Sends an instruction trough serial port for the Arduino to stop sending messages
        if verbose: print("Data collected")

        # Convert data to voltage values
        data = [float(i) * volt / res for i in data] # volts

        # Shift time points to start at t=0s
        initial_time = float(time[0])
        time = [(float(t) - initial_time)/1000 for t in time] # seconds
        if vb:
            print("Data converted")
            print(len(data), "samples")

        # Save [time, data] if 'fileToSave' was given in a pickle object
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
        cond = True # Blocks flow in 'get_data' procedure
        ser.write('1'.encode()) # Instructs Arduino to start sampling and sending messages
        root.after(1000, get_data) # waits 1s before it starts receiving messages


    def get_data():
        global cond, data, time, fs, vb, nsamples
        if cond == True: # while true, read messages from Arduino
            if vb: print("Sampling...")
            received = ser.readline().decode().split('\r\n')[0]
            received = received.split(':')
            t = received[0]
            val = received[1]
            time = np.append(time, t)
            data = np.append(data, val)
            root.after(1, get_data) # do-while -like block

    def quit():
        ser.close() # Close serial port
        if verbose: print("Arduino communication closed")
        root.quit() # Close program

    # Creates GUI window
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
    '''
    Simulates a signal of the form 1000(cos(800Hz) + sin(1600Hz) + cos(3200Hz)) and
    returns a sample of it sampled at sampling_frequency for the specified duration.

    :param duration: The duration of the signal you want to simulate (in seconds).
    :param sampling_frequency: The frequency at which the signal would be sampled (in Hertz).

    :param fileToSave: If given, it stores the signal as pickle object in that path inside 'pickle'.
    :param verbose: If given, the function log is printed on the terminal.

    :return: signal
             The signal samples that where simulated.

    Notes:
        - It also shows the plots of the function decomposed as saves them as png images if 'fileToSave'
          is given, inside 'plots'. The same for a preview of the simulated signal.
    '''

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
