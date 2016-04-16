from preprocess import *
import scipy.signal as signal
import matplotlib.pyplot as plt

b, a = createButterBandpass(5, 15, 129, 10)

# plt.plot(b, a)
# plt.figure()

w, h = signal.freqz(b, a)
# plt.plot(w, 20 * np.log10(abs(h)))
# plt.plot(w, abs(h))

plt.plot((128 * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
# plt.xscale('log')
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(100, color='green') # cutoff frequency
# plt.xlim([0, 100])
# plt.plot()

plt.show()
