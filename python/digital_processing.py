import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
from scipy.io import wavfile
from scipy.signal import freqz, lfilter, ellip, ellipord, cheb1ord, cheby1,iirdesign,lfilter, resample
import csv

def DI_BR_IIRchebyI(file_name, plot_interval, verbose=False):
    # --------------------------------------------------
    # Opening the pickle file
    # --------------------------------------------------
    with open("../"+ file_name + ".pickle", "rb") as input_file:
         signal = cPickle.load(input_file)
         input_file.close()

    # --------------------------------------------------
    # Calculating parameters to use in the filter
    # --------------------------------------------------
    nsamples = len(signal)
    time =   #time of the signal aquisition to then use to calculate the sample rate
    samplerate = len(signal)/time
    t = arange(nsamples) / samplerate

    # Values and constants for the purpose of the C part of the project
    cut_off_frequency=1600 # Hz
    atenuation=60


    # ------------------------------------------------
    # Create a IIR filter to apply it to x.
    # ------------------------------------------------
    N, Wn = cheb1ord(ws=[], wp= [0.5, 0.7], gstop=atenuation, gpass=1)
    b, a = cheby1(N, 1, Wn, btype='bandstop')
    w, h = freqz(b, a)

    h_dB = 20 * np.log10(np.abs(h)) # Log scale to use in the frequency response
    # -----------------------------------------------
    #  Apply the filter to the signal from the input file
    #-----------------------------------------------

    filtered_signal = lfilter(b, a, signal)

    return [w,h_dB,filtered_signal]


def DR_uniformresample(file_name, plot_interval, verbose=False):

    with open("../"+ file_name + ".pickle", "rb") as uniform:
         signal = cPickle.load(uniform)
         uniform.close()

    filtered_signal=resample(cvs_file_path, 3)


    return (filtered_signal)
