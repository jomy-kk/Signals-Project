# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

from python.setup import setup_arduino_communication
import pickle, numpy as np
import matplotlib.pyplot as plt

def e2_multi_channel_subplots(signalA, signalB, labelA, labelB, sampling_frequencyA, sampling_frequencyB, sampling_time, fileToSave=None, verbose=False):
    if verbose:
        print("Plotting both signals...")

    fig = plt.figure()

    plt.subplot(2,1,1)
    t = np.linspace(0, sampling_time*1000, len(signalA), endpoint=False)
    plt.plot(t, [(i/5*1024)*3.5/1024 for i in signalA], 'b-', linewidth=0.5)
    plt.title(labelA)
    plt.xlabel('Time (ms)')
    plt.xlim((100, 500))
    plt.ylabel('Amplitude (V)')
    #plt.ylim(2.5, 3.5)

    plt.subplot(2, 1, 2)
    t = np.linspace(0, sampling_time*1000, len(signalB), endpoint=False)
    plt.plot(t, signalB, 'b-', linewidth=0.5)
    plt.title(labelB)
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude (V)')
    plt.ylim((np.min(signalB) * 1.1, np.max(signalB) * 1.1))

    if fileToSave is not None:
        fig.savefig('../plots/' + fileToSave + '.png', bbox_inches='tight')
        if verbose:
            print("Image saved in 'plots'.")

    plt.show()




# Test
with open("../pickle/AL2 2020-12-28 15:29:51.129775.pickle", 'rb') as AL1:
    signalA = pickle.load(AL1)
    AL1.close()

'''
with open ("../pickle/AL5 noise 2020-12-28 15:36:36.051989.pickle", 'r') as AL4:
    signalB = pickle.load(AL4)
    AL4.close()
'''
print(signalA)
e2_multi_channel_subplots(signalA, signalA, 'AL2', 'AL1', 40, 40, 30, verbose=True)