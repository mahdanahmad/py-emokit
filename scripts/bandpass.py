import os, sys
import scipy.signal as signal
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import *

b, a = createButterPass(5, 20, 128, 10, 'band')

# plt.plot(b, a)
# plt.figure()

w, h = signal.freqz(b, a)
# plt.plot(w, 20 * np.log10(abs(h)))
# plt.plot(w, abs(h))

# plt.plot((128 * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
# plt.xscale('log')
# plt.title('Butterworth filter frequency response')
# plt.xlabel('Frequency')
# plt.ylabel('Amplitude [dB]')
# plt.margins(0, 0.1)
# plt.grid(which='both', axis='both')
# plt.axvline(100, color='green') # cutoff frequency
# plt.xlim([0, 100])
# plt.plot()

plt.plot((128 * 0.5 / np.pi) * w, abs(h))
# plt.plot([0, 0.5 * 128], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid(True)
plt.xlim([0,30])

plt.show()
