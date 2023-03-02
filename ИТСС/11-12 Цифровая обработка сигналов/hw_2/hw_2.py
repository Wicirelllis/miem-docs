import copy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class hw_2:
    def __init__(self) -> None:
        self.N = 5 # Your variant number
        self.threshold = 0.7 # You may have to adjust it for better results

        if self.N % 2 == 0:
            self.A = 15 * self.N
            self.B = self.N
            self.fc = 3_000 * self.N
            self.fm = 100 * self.N
        else:
            self.A = 10 * self.N
            self.B = 2 * self.N
            self.fc = 2_000 * self.N
            self.fm = 150 * self.N

        self.fs = 5 * self.fc # Sampling frequency
        self.IMG_DIR = "img/"
        Path(self.IMG_DIR).mkdir(parents=True, exist_ok=True)

    def am_signal(self, t: list[float], noise: bool = True, noise_scale: float = 0.3) -> list[float]:
        """Evaluate am-signal at specific values."""
        carrier = self.A * np.sin(2 * np.pi * self.fc * t)
        message = self.B * np.sin(2 * np.pi * self.fm * t)
        signal = (1 + message / self.A) * carrier
        if noise:
            signal += np.random.normal(0, noise_scale * self.B, signal.shape)
        return signal

    def fm_signal(self, t: list[float], noise: bool = True, noise_scale: float = 0.3) -> list[float]:
        """Evaluate fm-signal at specific values."""
        message = self.B * np.sin(2 * np.pi * self.fm * t)
        signal = self.A * np.sin(2 * np.pi * self.fc * t + message)
        if noise:
            signal += np.random.normal(0, noise_scale * self.B, signal.shape)
        return signal

    def draw_plot(self, x_: list[float], y_: list[float], xlabel: str, ylabel: str,
                  title: str, filename: str, ylog: bool = False) -> None:
        _, ax = plt.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if ylog:
            ax.set_yscale("log")
            ax.set_ylim(0.001, 1900)
        else:
            ax.set_ylim(0, self.A + 2 * self.B)
        ax.set_title(title)
        x, y = zip(*sorted(zip(x_, y_)))
        ax.plot(x, y)
        plt.savefig(f"{self.IMG_DIR}/{filename}")

    def plot_wave(self, wave_: callable, pre: str) -> None:
        """Plot every needed plot (signal, 1/2-sided spectrum, w and w/o noise, filtered)."""
        t = np.arange(15 * self.fc / self.fm) / self.fs
        wave = wave_(t, False)
        wave_with_noise = wave_(t, True)

        # DFT
        freqs = np.fft.fftfreq(len(wave), 1 / self.fs)
        ffts = np.abs(np.fft.fft(wave)) / len(wave)
        ffts_with_noise = np.abs(np.fft.fft(wave_with_noise) / len(wave_with_noise))

        # Filter noise by setting small values in spectrum to zero
        ffts_filtered_raw = np.fft.fft(wave_with_noise) / len(wave)
        mask = np.abs(ffts_filtered_raw) < self.threshold
        ffts_filtered_raw[mask] = 0
        ffts_filtered = np.abs(ffts_filtered_raw)

        # Inverse DFT
        wave_filtered = np.abs(np.fft.ifft(ffts_filtered_raw)) * len(wave)


        # Signal itself
        self.draw_plot(t, wave, "Time, s", "Amplitude", f"{pre} signal, without noise", f"{pre}_signal.png")
        self.draw_plot(t, wave_with_noise, "Time, s", "Amplitude", f"{pre} signal, with noise", f"{pre}_signal_with_noise.png")

        # Double-sided spectrum
        self.draw_plot(freqs, ffts, "Frequency, Hz", "Amplitude", f"Double-sided spectrum of {pre} signal, without noise", f"{pre}_spectrum_double_sided.png", True)
        self.draw_plot(freqs, ffts_with_noise, "Frequency, Hz", "Amplitude", f"Double-sided spectrum of {pre} signal, with noise", f"{pre}_spectrum_double_sided_with_noise.png", True)
        self.draw_plot(freqs, ffts_filtered, "Frequency, Hz", "Amplitude", f"Double-sided spectrum of {pre} signal, after noise filtering", f"{pre}_spectrum_double_sided_filtered.png", True)

        # Single-sided spectrum
        l = len(wave) // 2
        freqs = np.fft.fftfreq(len(wave), 1 / self.fs)[:l]
        ffts = (np.abs(np.fft.fft(wave)) / len(wave))[:l]
        ffts_with_noise = (np.abs(np.fft.fft(wave_with_noise)) / len(wave_with_noise))[:l]

        ffts_filtered_raw = np.fft.fft(wave_with_noise) / len(wave)
        mask = np.abs(ffts_filtered_raw) < self.threshold
        ffts_filtered_raw[mask] = 0
        ffts_filtered = np.abs(ffts_filtered_raw)

        self.draw_plot(freqs, ffts, "Frequency, Hz", "Amplitude", f"Single-sided spectrum of {pre} signal, without noise", f"{pre}_spectrum_single_sided.png", True)
        self.draw_plot(freqs, ffts_with_noise, "Frequency, Hz", "Amplitude", f"Single-sided spectrum of {pre} signal, with noise", f"{pre}_spectrum_single_sided_with_noise.png", True)
        self.draw_plot(freqs, ffts_filtered, "Frequency, Hz", "Amplitude", f"Single-sided spectrum of {pre} signal, after noise filtering", f"{pre}_spectrum_single_sided_filtered.png", True)

        # Filtered signal (after inverse DFT)
        self.draw_plot(t, wave_filtered, "Time, s", "Amplitude", f"{pre} signal, after noise filtering", f"{pre}_signal_filtered.png")

    def do_work(self):
        self.plot_wave(self.am_signal, "AM")
        self.plot_wave(self.fm_signal, "FM")

hw = hw_2()
hw.do_work()
