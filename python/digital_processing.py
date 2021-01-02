import matplotlib.pyplot as plt
import numpy as np
from numpy import arange
from scipy.io import wavfile
from scipy.signal import freqz, lfilter, ellip, ellipord, cheb1ord, cheby1

def DI_BD_IIRchebyI(wav_file_path, plot_interval, verbose=False):
    def mfreqz(b,a=1):

        w,h = signal.freqz(b,a)
        h_dB = 20 * np.log10 (np.abs(h))

        subplot(2,1,1)
        plot(w/max(w),h_dB)
        ylim(-150, 5)
        ylabel('Magnitude (db)')
        xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
        title(r'Frequency response')
        subplot(212)
        h_Phase = np.unwrap(np.arctan2(np.imag(h), np.real(h)))
        plot(w/np.max(w),h_Phase)
        ylabel('Phase (radians)')
        xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
        title(r'Phase response')
        subplots_adjust(hspace=0.5)
        plt.show()
    # ------------------------------------------------
    # Create a signal.
    # ------------------------------------------------

    samplerate, x = wavfile.read(wav_file_path)
    nsamples = x.size
    t = arange(nsamples) / samplerate

    # ------------------------------------------------
    # Create a IIR filter and apply it to x.
    # ------------------------------------------------

    N, Wn = cheb1ord(ws=[0.55, 0.65], wp= [0.5, 0.7], gstop=60, gpass=1)
    b, a = cheby1(N, 1, Wn, btype='bandstop')
    w, h = freqz(b, a, fs=200000)

    # passband from 0.05 to 0.3 times the Nyquist frequency with 60 dbstop band and 1 dbpassband attenuation
    b,a= signal.iirdesign(wp = [0.5, 0.7], ws= [0.55, 0.65], gstop= 60, gpass=1, ftype='ellip')
    # %% bandpass frequency responsem
    freqz(b, a)
    # %% Impulse
    responseimpz(b, a)


    fig = plt.figure()
    h_dB = 20 * np.log10(np.abs(h))
    plt.plot(w, h_dB, 'b-')
    #plt.ylim(-150, 5)
    plt.ylabel('Magnitude (dB)')
    plt.xlabel('Frequency (Hz)')
    plt.grid(True)
    fig.savefig('DI.png', bbox_inches='tight')


    # Apply filtfilt to signal
    filtered_x = lfilter(b, a, x)

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
    fig.savefig('DI.png', bbox_inches='tight')

    if verbose:
        plt.show()
