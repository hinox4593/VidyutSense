import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from signal_processing.src.waveform_generator import CLASS_GENERATORS

root = tk.Tk()
root.title("VidyutSense")
root.geometry("650x550")
root.configure(bg="#0b1425")

label_title = tk.Label(
    root, text="VIDYUTSENSE",
    font=("Helvetica", 20, "bold"),
    fg="white", bg="#0b1425"
)
label_title.pack(pady=(15, 5))

label_status = tk.Label(
    root, text="Select a scenario",
    font=("Helvetica", 12),
    fg="#f0a030", bg="#0b1425"
)
label_status.pack(pady=(0, 10))

fig = Figure(figsize=(6, 3.5), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("Waveform")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)


def select_scenario(name):
    label_status.config(text=f"Selected: {name}")

    rng = np.random.default_rng()
    t, waveform = CLASS_GENERATORS[name](rng)

    ax.clear()
    ax.set_title(f"Waveform — {name}")
    ax.plot(t * 1000, waveform)
    ax.set_xlabel("time (ms)")
    canvas.draw()


button_frame = tk.Frame(root, bg="#0b1425")
button_frame.pack()

btn_normal = tk.Button(
    button_frame, text="NORMAL",
    command=lambda: select_scenario("NORMAL")
)
btn_normal.pack(side="left", padx=5)

btn_harmonic = tk.Button(
    button_frame, text="HARMONIC DISTORTION",
    command=lambda: select_scenario("HARMONIC_DISTORTION")
)
btn_harmonic.pack(side="left", padx=5)

btn_transient = tk.Button(
    button_frame, text="TRANSIENT EVENT",
    command=lambda: select_scenario("TRANSIENT_EVENT")
)
btn_transient.pack(side="left", padx=5)

root.mainloop()
