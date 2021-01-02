import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
from scipy.io import wavfile
from scipy.signal import freqz, lfilter, ellip, ellipord, cheb1ord, cheby1,iirdesign,lfilter, resample
import csv

def DI_BR_IIRchebyI(cs_file, plot_interval, verbose=False):
    # ------------------------------------------------
    # Create a signal.
    # ------------------------------------------------

    #Opening the pickle file
    with open("caminho para CS......", "rb") as input_file:
         signal = cPickle.load(input_file)
    nsamples = x.size
    t = arange(nsamples) / samplerate

    # Values and constants for the purpose of the C part of the project
    cut_off_frequency=1600 # Hz
    Atenuation=60


    # ------------------------------------------------
    # Create a IIR filter and apply it to x.
    # ------------------------------------------------
    N, Wn = cheb1ord(ws=[], wp= [0.5, 0.7], gstop=atenuation, gpass=1)
    b, a = cheby1(N, 1, Wn, btype='bandstop')
    w, h = freqz(b, a, fs=200000)

    fig = plt.figure()
    h_dB = 20 * np.log10(np.abs(h))
    plt.plot(w, h_dB, 'b-')
    #plt.ylim(-150, 5)
    plt.ylabel('Magnitude (dB)')
    plt.xlabel('Frequency (Hz)')
    plt.grid(True)
    fig.savefig('results_a6/chebyI_frequency_response.png', bbox_inches='tight')


    # Apply filtfilt to signal
    filtered_x = lfilter(b, a, x)
    wavfile.write('looneytunes_IIR_BR_55-65K.filtered_wav', samplerate, filtered_x)

    fig = plt.figure()
    # Plot the original signal.
    plt.subplot(2, 1, 1)
    plt.title('Original')
    plt.plot(t, x, 'b-', linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.xlim(plot_interval)
    plt.ylim(-20500, 20500)
    plt.grid(True)
    # Plot the filtered signal, shifted to compensate for the phase delay.
    plt.subplot(2, 1, 2)
    plt.title('Filtered')
    plt.plot(t, filtered_x, 'g', linewidth=0.5)
    plt.xlim(plot_interval)
    plt.ylim(-20500, 20500)
    plt.xlabel('Time (s)')
    plt.grid(True)
    plt.subplots_adjust(hspace=0.7)
    fig.savefig('results_a6/chebyI_filtered_output.png', bbox_inches='tight')

    if verbose:
        plt.show()

DI_BR_IIRchebyI(signal1, (0,4), verbose=False)


def DR_uniformresample(pickle_file_path, plot_interval, verbose=False):
    resample(cvs_file_path, 6, t=None, axis=0, window=None, domain='time')
