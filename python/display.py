# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

import pickle, numpy as np
import matplotlib.pyplot as plt

def e2_multi_channel_subplots(signalA, signalB, labelA, labelB, duration, fileToSave=None, verbose=False):
    if verbose:
        print("Plotting both signals...")

    fig = plt.figure(figsize=(16,8))

    plt.subplot(2,1,1)
    t = np.linspace(0, duration, len(signalA), endpoint=False)
    plt.plot(t, signalA, 'b-', linewidth=0.5)
    plt.title(labelA)
    plt.xlabel('Time (s)')
    plt.xlim((1, 1.02))
    plt.ylabel('Amplitude (V)')

    plt.subplot(2, 1, 2)
    t = np.linspace(0, duration, len(signalB), endpoint=False)
    plt.plot(t, signalB, 'b-', linewidth=0.5)
    plt.title(labelB)
    plt.xlabel('Time (s)')
    plt.xlim((1, 1.02))
    plt.ylabel('Amplitude (V)')
    plt.subplots_adjust(hspace=0.4)

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '_partial.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

    plt.show()

    fig = plt.figure(figsize=(16,8))

    plt.subplot(2, 1, 1)
    t = np.linspace(0, duration, len(signalA), endpoint=False)
    plt.plot(t, signalA, 'b-', linewidth=0.5)
    plt.title(labelA)
    plt.xlabel('Time (s)')
    plt.xlim((0, duration))
    plt.ylabel('Amplitude (V)')

    plt.subplot(2, 1, 2)
    t = np.linspace(0, duration, len(signalB), endpoint=False)
    plt.plot(t, signalB, 'b-', linewidth=0.5)
    plt.title(labelB)
    plt.xlabel('Time (s)')
    plt.xlim((0, duration))
    plt.ylabel('Amplitude (V)')
    plt.subplots_adjust(hspace=0.5)

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '_complete.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

    plt.show()

def ef_save_to_csv(signal, times, fileToSave, verbose=False):
    time_points     = np.array(times) # one column for time points
    sample_points   = np.array(signal) # one column for sample points
    array = np.column_stack((time_points, sample_points))
    print(array)
    np.savetxt(fileToSave + '.csv', array, delimiter=",")
    if verbose: print("Saved signal in csv file to", fileToSave)

# Test
'''
with open("../pickle/AL1_mock.pickle", 'rb') as AL1:
    signal_al1 = pickle.load(AL1)
    AL1.close()

with open("../pickle/AL4_mock.pickle", 'rb') as AL4:
    signal_al4 = pickle.load(AL4)
    AL4.close()

e2_multi_channel_subplots(signal_al1, signal_al4, 'A0', 'A5', 12, 'ExB - E2(A0, A5)', verbose=True)
'''
#ef_save_to_csv(signal_al1, 'teste', True)
