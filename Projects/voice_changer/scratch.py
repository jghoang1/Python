from scipy.signal import butter, lfilter, freqs, hilbert
import matplotlib.pyplot as plt
import numpy as np


# SR = 44100
# class Test():
#     def __init__(self) -> None:
#         self.n_channels = 4
#         self.max_freq = 20_000
#         self.min_freq = 50
#         self.q = 3
#         self.filter_order = 5

#         base_freq = (self.max_freq/self.min_freq)**(1/(self.n_channels-1))
#         base_channel = np.log(self.min_freq) / np.log(base_freq)
#         self.boost = 3 * np.sqrt(self.n_channels)

#         self.filters = []
#         for k in range(self.n_channels):
#             fc = base_freq ** (base_channel + k)
            
#             if k == 0:
#                 # First channel is low pass
#                 b, a = butter(self.filter_order, fc * self.q, "lowpass", SR)
#                 self.filters.append((b,a))
#             elif k == self.n_channels - 1:
#                 # Last channel is high pass
#                 b, a = butter(self.filter_order, fc / self.q, "highpass", SR)
#                 self.filters.append((b,a))

#             else:
#                 # Middle channels are band pass
#                 b, a = butter(self.filter_order, (fc / self.q, fc * self.q), "bandpass", SR)
#                 self.filters.append((b,a))
    
#     def _get_channel_amplitudes(self, modulator):
#         out = []
#         for b,a in self.filters:
#             filtered = lfilter(b, a, modulator)
#             filtered *= self.boost
#             out.append(hilbert(filtered))
#         return out

#     def _get_channel_carriers(self, carrier):
#         out = []
#         for b,a in self.filters:
#             filtered = lfilter(b, a, carrier)
#             filtered *= self.boost
#             out.append(filtered)
#         return out


# test = Test()
# print(test.fcs)
# for i in range(len(test.filters)):
#     b, a = test.filters[i]
#     fc = test.fcs[i]
#     w, h = freqs(b, a)
#     plt.semilogx(w, 20 * np.log10(abs(h)))
#     plt.title('Butterworth filter frequency response')
#     plt.xlabel('Frequency [radians / second]')
#     plt.ylabel('Amplitude [dB]')
#     plt.margins(0, 0.1)
#     plt.grid(which='both', axis='both')
#     plt.axvline(fc, color='green') # cutoff frequency
#     plt.axvline(fc * test.q, color='green', linestyle="--") # cutoff frequency
#     plt.axvline(fc / test.q, color='green', linestyle="--") # cutoff frequency
# plt.show()


import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low')

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 5
fs = 44100     # sample rate, Hz
cutoff = 150  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)
print(b,a)
# Plot the frequency response.
w, h = freqz(b, a, fs=fs, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(w, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = 0.1        # seconds
n = int(T * fs) # total number of samples
n = 576
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
# data = np.sin(50*2*np.pi*t) + 1.5*np.cos(150*2*np.pi*t) + 0.5*np.sin(1500*2*np.pi*t)
data = np.array([  348,   449,   527,   586,   600,   539,   404,   257,   191,
         172,   188,   267,   394,   490,   575,   694,   748,   754,
         784,   852,   949,  1016,  1053,  1065,  1106,  1242,  1317,
        1296,  1188,   994,   820,   758,   755,   756,   764,   834,
         915,   951,   909,   768,   683,   662,   725,   843,   895,
         868,   809,   755,   768,   824,   891,   992,  1112,  1249,
        1353,  1413,  1463,  1522,  1537,  1508,  1493,  1411,  1244,
        1114,  1015,   918,   854,   832,   853,   847,   826,   858,
         882,   871,   897,   992,  1153,  1300,  1354,  1302,  1224,
        1135,  1066,  1100,  1179,  1280,  1377,  1445,  1482,  1536,
        1635,  1673,  1568,  1334,  1083,   878,   746,   669,   628,
         606,   542,   435,   303,   287,   409,   623,   839,   970,
        1013,   972,   913,   822,   725,   609,   454,   322,   267,
         239,   193,   225,   333,   464,   590,   682,   770,   822,
         819,   732,   574,   451,   373,   338,   264,   144,    24,
         -51,   -93,   -47,    81,   274,   548,   762,   830,   759,
         665,   627,   585,   515,   449,   368,   233,   119,    52,
          80,   190,   329,   435,   457,   515,   591,   706,   853,
         978,  1010,   929,   791,   664,   596,   557,   569,   579,
         526,   444,   387,   379,   414,   451,   441,   493,   614,
         685,   735,   802,   896,  1013,  1125,  1206,  1230,  1265,
        1275,  1282,  1282,  1184,  1062,   982,   960,   881,   757,
         619,   478,   368,   281,   250,   308,   411,   505,   539,
         537,   480,   365,   284,   275,   284,   239,   170,   143,
         199,   253,   283,   333,   383,   394,   372,   346,   317,
         286,   259,   231,   194,   143,    39,   -54,  -108,  -103,
           3,   144,   283,   380,   386,   369,   329,   326,   416,
         496,   556,   559,   593,   633,   635,   640,   664,   677,
         656,   534,   374,   345,   460,   698,   899,   898,   788,
         724,   728,   798,   842,   867,   875,   745,   500,   289,
         149,    87,    48,    12,   -18,   -65,  -169,  -345,  -378,
        -289,  -207,  -191,  -215,  -243,  -266,  -210,  -110,    39,
         144,   215,   321,   394,   406,   312,   193,   134,   109,
         117,   115,   127,   132,   173,   235,   182,    13,  -153,
        -304,  -486,  -646,  -769,  -903, -1030, -1055,  -969,  -800,
        -593,  -375,  -217,  -108,   -14,    70,   127,   226,   356,
         406,   406,   384,   341,   256,   167,    96,    60,    37,
          26,    75,   245,   538,   805,   979,  1069,  1093,  1038,
         914,   792,   685,   555,   443,   332,   242,   189,   119,
          74,   103,   185,   350,   578,   778,   909,   950,   958,
         944,   913,   901,   885,   858,   871,   884,   885,   906,
         924,   889,   851,   856,   905,   957,  1006,  1074,  1129,
        1191,  1207,  1175,  1176,  1253,  1305,  1284,  1266,  1299,
        1352,  1434,  1500,  1496,  1480,  1439,  1375,  1294,  1207,
        1191,  1261,  1293,  1317,  1339,  1296,  1263,  1240,  1221,
        1199,  1188,  1183,  1122,  1065,  1057,  1168,  1273,  1309,
        1371,  1431,  1496,  1555,  1618,  1664,  1644,  1538,  1377,
        1173,  1013,   970,   963,   936,   922,   894,   835,   762,
         699,   672,   596,   484,   366,   271,   231,   235,   241,
         203,   116,   -27,  -248,  -389,  -405,  -389,  -374,  -359,
        -336,  -357,  -342,  -285,  -242,  -241,  -268,  -241,  -199,
        -172,  -136,  -189,  -360,  -553,  -702,  -802,  -860,  -838,
        -828,  -816,  -744,  -576,  -441,  -306,  -177,  -153,  -127,
         -71,    -3,    -8,  -100,  -257,  -353,  -318,  -239,  -154,
        -122,  -185,  -325,  -507,  -632,  -602,  -500,  -459,  -486,
        -501,  -448,  -407,  -374,  -407,  -485,  -525,  -509,  -473,
        -440,  -329,  -213,  -107,   -28,    62,   123,    82,    90,
         160,   177,    85,   -17,  -100,  -162,  -173,  -172,  -231,
        -348,  -495,  -659,  -737,  -779,  -875,  -964,  -998, -1021,
       -1021, -1056, -1150, -1202, -1175, -1122, -1149, -1242, -1282,
       -1239, -1167, -1117, -1131, -1100,  -957,  -802,  -694,  -601,
        -546,  -545,  -593,  -665,  -738,  -788,  -836,  -945, -1019,
        -959,  -868,  -822,  -768,  -703,  -645,  -649,  -738,  -807,
        -806,  -730,  -634,  -531,  -464,  -485,  -532,  -573,  -525],
      dtype=np.int16)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
