# -*- coding: utf-8 -*-
"""
PSSI - Project Group B3
@authors: João Saraiva, Tiago Mimoso
"""

from matplotlib import ticker
import matplotlib.pyplot as plt
import pickle, numpy as np
from datetime import datetime
from scipy.signal import iirdesign, filtfilt, resample, freqz, impulse, medfilt

def DI_IIRfilter_BR(signal, f1, f2, sampling_frequency, gstop, fileToSave=None, verbose=False):
    '''
    Designs an IIR band-reject Cauer/elliptic filter, with a stop-bandwidth of [f1, f2].
    Plots the frequency response and impulse response.
    Applies the filter to the given signal and plots the filtered output.

    :param signal: The signal to be filtered
    :param f1: The lower cutoff frequency (in Hertz).
    :param f2: The higher cutoff frequency (in Hertz).
    :param sampling_frequency: The sampling frequency at which the signal was acquired (in Hertz).
    :param gstop: The minimum attenuation in the stop-band (in dB).

    :param fileToSave: If given, it stores the filtered signal as pickle object in that path inside 'pickle',
                       and the images as png in that path inside 'plots'.
    :param verbose: If given, the function log is printed on the terminal.

    :return: filtered_signal
             The filtered signal after the filter was applied to the original.
    '''

    # Computes Nyquist frequency
    nyquist_frequency = sampling_frequency/2

    # Computes cutoff frequencies coefficients, normalized from 0 to 1, where 1 is the Nyquist frequency.
    f1_coeff, f2_coeff = f1/nyquist_frequency, f2/nyquist_frequency

    # Design bandreject from f1_coeff to f2_coeff times the Nyquist frequency with gstop dB stop band and 1 dB passband attenuation
    b, a = iirdesign(wp=[f1_coeff-0.05, f2_coeff+0.05], ws=[f1_coeff, f2_coeff], gstop=gstop, gpass=1, ftype='ellip')
    if verbose: print("Filter designed")

    # Frequency response
    if fileToSave is not None:
        w, h = freqz(b, a)

        fig, ax1 = plt.subplots()
        ax1.set_title('Digital filter frequency response')
        ax1.plot(w, 20 * np.log10(abs(h)), 'b')
        ax1.set_ylabel('Amplitude [dB]', color='b')
        ax1.set_xlabel('Frequency [rad/sample]')
        ax1.grid()
        ax2 = ax1.twinx()
        angles = np.unwrap(np.angle(h))
        ax2.plot(w, angles, 'g')
        ax2.set_ylabel('Angle (radians)', color='g')
        ax2.grid()
        ax2.axis('tight')
        nticks = 8
        ax1.yaxis.set_major_locator(ticker.LinearLocator(nticks))
        ax2.yaxis.set_major_locator(ticker.LinearLocator(nticks))

        plt.show()
        fig.savefig('../plots/' + fileToSave + '_frequency_response.png', bbox_inches='tight')
        if verbose:
            print("Frequency Response saved in 'plots'.")

    # Impulse response
    if fileToSave is not None:
        t, yout = impulse((b, a))
        fig = plt.figure()
        plt.stem(t, yout)
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.show()
        fig.savefig('../plots/' + fileToSave + '_impulse_response.png', bbox_inches='tight')
        if verbose:
            print("Impulse Response saved in 'plots'.")

    # Apply filter
    filtered_signal = filtfilt(b, a, signal)
    if verbose: print("Filter applied forward and backward to the signal.")

    # Save filtered signal if 'fileToSave' was given
    if fileToSave is not None:
        try:
            with open('../pickle/' + fileToSave + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(filtered_signal, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()
                if verbose: print("Filtered signal saved in 'pickle'.")

        except IOError:
            print("Error: File path provided does not seem to exist.")

    return filtered_signal



def DR_uniform_resample(signal, sampling_times, resampling_duration, resampling_frequency, fileToSave=None, verbose=False):
    '''
    Performs a uniform resample on the given simple.
    It also plots a preview of the resampled result against the original signal.

    :param signal: The original signal to be resampled.
    :param sampling_times:  The original time points at which the signal was sampled.
    :param resampling_duration: The duration the resampled signal should have (in seconds).
    :param resampling_frequency: The sampling frequency the resampled signal should have (in Hertz).

    :param fileToSave: If given, it stores the resampled signal as pickle object in that path inside 'pickle'.
    :param verbose: If given, the function log is printed on the terminal.

    :return: resampled_times, resampled_signal
             The resampled time points and the resampled signal on those time points.
    '''

    # Prepare number of samples and time points
    resampling_num_samples = int(resampling_duration*resampling_frequency)
    uniform_times = np.linspace(0, resampling_duration, resampling_num_samples, endpoint=False)

    # Do resampling
    resampled_signal, resampled_times = resample(signal, num=resampling_num_samples, t=uniform_times)

    # Plot result
    fig = plt.figure(figsize=(16,8))
    plt.plot(sampling_times, signal, 'b.-')
    plt.plot(uniform_times, resampled_signal, 'go-', mfc='none')
    plt.xlim((0,0.3))
    plt.legend(['original', 'resampled'], loc='best')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (V)')
    plt.show()
    fig.savefig('../plots/ExA - DR.png', bbox_inches='tight')

    # Save resampled signal if 'fileToSave' was given
    if fileToSave is not None:
        try:
            with open('../pickle/' + fileToSave + ' ' + str(datetime.now()) + '.pickle', 'wb') as output:
                pickle.dump(resampled_signal, output, protocol=pickle.HIGHEST_PROTOCOL)
                output.close()
                if verbose: print("Filtered signal saved in 'pickle'.")

        except IOError:
            print("Error: File path provided does not seem to exist.")

    return resampled_times, resampled_signal


# Test Topic A

'''
with open("../pickle/AL6_with_sampling_times 2021-01-04 14:24:32.487008.pickle", "rb") as file:
    obj = pickle.load(file)
    times = obj[0]
    signal = obj[1]
    file.close()

resampled_times, resampled_signal = DR_uniform_resample(signal, times, 12, 400, fileToSave='ExA - DR', verbose=True)

from python.display import ef_save_to_csv
ef_save_to_csv(resampled_signal, resampled_times, fileToSave='ExA - EF', verbose=True)
'''


# Test Topic C

with open("../pickle/CS 2021-01-03 12:21:04.113930.pickle", "rb") as file:
    signal = pickle.load(file)
    file.close()
filtered_signal = DI_IIRfilter_BR(signal, f1=1593, f2=1608, sampling_frequency=6400, gstop=60, fileToSave='ExC - DI', verbose=True)

from python.display import e2_multi_channel_subplots
e2_multi_channel_subplots(signal, filtered_signal, 'Original', 'Filtered', 6, fileToSave='ExC - E2', verbose=True)
