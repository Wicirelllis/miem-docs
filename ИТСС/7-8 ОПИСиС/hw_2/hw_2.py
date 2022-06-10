from typing import Callable, List
import matplotlib.pyplot as plt
import numpy as np

SAMPLING_RATE = 20 # samples per second
BIT_DEPTH = 8
RESOLUTION = 2 ** BIT_DEPTH
TIME_FRAME = 1 # in seconds
# MAX_AMPLITUDE = 1
# DELTA_Q = 0
A_MAX = 0
A_MIN = 0

def f(t: float) -> float:
    """Return signal amplitude at t seconds."""
    freq = 1
    return np.sin(2 * np.pi * freq * t) + np.sin(4 * np.pi * freq * t)

def discretization(
    signal: Callable,
    discretization_frequency: int = SAMPLING_RATE,
    resolution: int = RESOLUTION,
    time_frame: int = TIME_FRAME) -> List[int]:
    """Perform discretization of signal. Return list of samples."""
    times = []
    amplitudeds = []
    n = discretization_frequency * time_frame
    delta_t = 1. / discretization_frequency
    for i in range(n):
        times.append(delta_t * i)
        amplitudeds.append(signal(delta_t * i))
    return (times, amplitudeds)

def quantization(
    samples: List[float],
    resolution: int = RESOLUTION) -> List[int]:
    """Perform quantization of discretized signal. Return list of samples."""
    a_min = min(samples)
    a_max = max(samples)
    global A_MIN, A_MAX
    A_MIN = a_min
    A_MAX = a_max
    delta_q = (a_max - a_min) / (resolution - 1)
    quants = []
    for a in samples:
        quants.append(round((a - a_min) / delta_q))
    return quants

def encoding(samples: List[int], bit_depth: int = BIT_DEPTH) -> List[int]:
    """Transform sequence of quantized values into one-and-zero sequence. Use natural binary code."""
    res = []
    for sample in samples:
        res.extend([int(d) for d in bin(sample)[2:].zfill(bit_depth)])
    return res

def bipolar_encoding(samples: List[int]) -> List[int]:
    """Perform bipolar encoding for physical level."""
    res = []
    last = -1
    for sample in samples:
        if sample == 0:
            res.append(0)
        else:
            last *= -1
            res.append(last)
    return res

def bipolar_decoding(samples: List[int]) -> List[int]:
    """Perform bipolar decoding."""
    return [abs(sample) for sample in samples]

def decoding(samples: List[int], bit_depth: int = BIT_DEPTH) -> List[int]:
    """Perform decoding from natural binary code."""
    # print(samples)
    res = []
    for i in range(len(samples) // bit_depth):
        # get bit_depth bits from dequence of bits
        s = samples[i * bit_depth:(i + 1) * bit_depth]
        # convert bits to decimal number
        d = int("".join(map(str, s)), 2)
        res.append(d)
    return res

def digital2analog(
    samples: List[int],
    a_min: float = A_MIN,
    a_max: float = A_MAX,
    resolution: int = RESOLUTION) -> List[float]:
    return [sample * (A_MAX - A_MIN) / RESOLUTION + A_MIN for sample in samples]


# make signal discrete over time, but keep continuous over amplitude
times, discretized_signal = discretization(f)
# make signal discrete over amplitude
digital_signal = quantization(discretized_signal)
# now signal is digital (descrete over both time and amplitude)
# encode digital signal using natural binary encoing
encoded_signal = encoding(digital_signal)
# encode signal for physical-level using bipolar encoding
phys_level_signal = bipolar_encoding(encoded_signal)
#
# transfer over transmission line happens here
#
# decode signal from physical-level
decoded_phys_level_signal = bipolar_decoding(phys_level_signal)
# decode signal to sequence of descrete levels
decoded_signal = decoding(decoded_phys_level_signal)
# restore image of original digital signal after transmission
image_signal = digital2analog(decoded_signal)


# plots
# analog signal
fig, ax = plt.subplots(dpi=150)
ax.set_title("Исходный аналоговый сигнал")
ax.set_xlabel("$t$, мс")
ax.set_ylabel("$V_{0}$, В")
x = np.linspace(0, TIME_FRAME, 100_000)
y = [f(x_) for x_ in x]
ax.plot(x, y, label="Исходный сигнал", color="b")
ax.plot(times, discretized_signal, "-o", label="Дискретный по времени", color="orange")
fig.legend(loc="right")
fig.tight_layout()
plt.savefig("1.png")

# digital signal
fig, ax = plt.subplots(dpi=150)
ax.set_title("Цифровой сигнал")
ax.set_xlabel("$t$, мс")
ax.set_ylabel("Уровни квантования")
ax.plot(times, digital_signal, "-o", label="Цифровой сигнал", color="r")
fig.tight_layout()
plt.savefig("2.png")

# encoded signal
fig, ax = plt.subplots(dpi=150)
ax.set_title("Кодированный сигнал")
ax.set_xlabel("$t$, мс")
t = np.linspace(0, TIME_FRAME, len(encoded_signal))
ax.plot(t, encoded_signal, drawstyle="steps-pre")
fig.tight_layout()
plt.savefig("3.png")

# phys-level signal
fig, ax = plt.subplots(dpi=150)
ax.set_title("Физический уровень")
ax.set_xlabel("$t$, мс")
t = np.linspace(0, TIME_FRAME, len(encoded_signal))
ax.plot(t, phys_level_signal, drawstyle="steps-pre", color="r")
fig.tight_layout()
plt.savefig("4.png")

# encoded and phys-level signal
fig, ax = plt.subplots(dpi=150)
ax.set_title("Кодированный сигнал")
ax.set_xlabel("$t$, мс")
t = np.linspace(0, TIME_FRAME, len(encoded_signal))
ax.plot(t, encoded_signal, drawstyle="steps-pre", lw=3, label="Кодированный сигнал")
ax.plot(t, phys_level_signal, drawstyle="steps-pre", color="r", lw=1, label="Физический уровень")
fig.legend(loc="right")
fig.tight_layout()
plt.savefig("5.png")

# original analog signal and analog signal after transmission
fig, ax = plt.subplots(dpi=150)
ax.set_title("Исходный аналоговый сигнал")
ax.set_xlabel("$t$, мс")
ax.set_ylabel("$V_{0}$, В")
x = np.linspace(0, TIME_FRAME, 100_000)
y = [f(x_) for x_ in x]
ax.plot(x, y, label="Исходный сигнал", color="b")
ax.plot(times, image_signal, "-o", label="Образ", color="orange")
fig.legend(loc="right")
fig.tight_layout()
plt.savefig("6.png")
# plt.show()
