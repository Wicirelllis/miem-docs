import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import sys


class hw_1:
    def __init__(self) -> None:
        self.freqs = {
            "1": [697, 1209],
            "2": [697, 1336],
            "3": [697, 1477],
            "4": [770, 1209],
            "5": [770, 1336],
            "6": [770, 1477],
            "7": [852, 1209],
            "8": [852, 1336],
            "9": [852, 1477],
            "0": [941, 1336],
            "a": [697, 1633],
            "b": [770, 1633],
            "c": [852, 1633],
            "d": [941, 1633],
            "*": [941, 1209],
            "#": [941, 1477],
        }
        self.p = pyaudio.PyAudio()
        self.fs = 10_000
        self.duration = 0.5
        self.stream = None
        self._start_stream()

    def _start_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.fs, output=True)

    def do_work(self) -> None:
        print("Welcome, type 'help' for help and 'exit' to exit.")
        while True:
            s = input().lower()
            if s == "exit":
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
                sys.exit(0)
            elif s == "help":
                print(
                    "\nType single key (from '1234567890*#ABCDabcd', either lower or uppercase are acceptable) to play corresponding beep and show plot."
                    "\nType sequence of key symbols (e.g. *1801#) to play beeps in sequence. No plot is shown in this mode."
                    "\nAlso the following options are available:"
                    "\n    get"
                    "\n        Get the value of parameter. Available parameters are:"
                    "\n            fs - sampling frequency, Hz. Must be integer. Default is 10000Hz"
                    "\n            dur - duration of the beep, seconds. Default is 0.5s"
                    "\n        Example: get fs"
                    "\n    set"
                    "\n        Set the value of parameter. Same options as get."
                    "\n        Example: set fs 2000"
                    "\n    help"
                    "\n        Print this help page."
                    "\n    exit"
                    "\n        Close the program."
                )
                continue
            elif s.startswith("get"):
                if "fs" in s:
                    print(self.fs)
                elif "dur" in s:
                    print(self.duration)
                continue
            elif s.startswith("set"):
                if "fs" in s:
                    self.fs = int(s.split(" ")[-1])
                    self._start_stream()
                elif "dur" in s:
                    self.duration = float(s.split(" ")[-1])
                continue
            elif not set(s) <= set("1234567890*#abcd"):
                print("Unkonwn symbols in the input. Try again.")
                continue
            self.play_seq(s)

    def play_seq(self, s: str) -> None:
        if len(s) == 1:
            self.play_tone(s)
            self.draw_plot(s)
        else:
            for k in s:
                self.play_tone(k)

    def play_tone(self, k: str) -> None:
        freqs = self.freqs[k]
        samples = np.mean(
            np.sin(np.outer(freqs, 2 * np.pi * np.arange(self.fs * self.duration) / self.fs)),
            axis=0).astype(np.float32).tobytes()
        self.stream.write(samples)

    def draw_plot(self, k: str) -> None:
        freqs = self.freqs[k]
        x = np.linspace(0, 0.005, 100_000)
        y = np.mean(np.sin(np.outer(freqs, 2 * np.pi * x)), axis=0)

        fig, ax = plt.subplots()
        ax.set_xlim(0, 0.005)
        ax.set_ylim(-1, 1)
        ax.set_xlabel("Time, s")
        ax.set_ylabel("Amplitudes")
        ax.set_title(f"{k} - {freqs} Hz")
        ax.plot(x, y)
        fig.show()


hw = hw_1()
hw.do_work()
