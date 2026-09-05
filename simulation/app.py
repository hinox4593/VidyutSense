import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import font as tkfont
import numpy as np
import joblib
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from signal_processing.src.waveform_generator import CLASS_GENERATORS, SAMPLE_RATE_HZ
from signal_processing.src.preprocessing import preprocess
from signal_processing.src.fft_analysis import compute_fft
from signal_processing.src.feature_extraction import extract_features, features_to_vector

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "classifier.joblib")
model = joblib.load(MODEL_PATH)

STAGE_DELAY_MS = 1100

root = tk.Tk()
root.title("VidyutSense")
root.geometry("780x800")
root.configure(bg="#0b1425")

label_title = tk.Label(
    root, text="VIDYUTSENSE",
    font=("Helvetica", 18, "bold"),
    fg="white", bg="#0b1425"
)
label_title.pack(pady=(10, 2))

label_status = tk.Label(
    root, text="Select a scenario",
    font=("Helvetica", 11),
    fg="#f0a030", bg="#0b1425"
)
label_status.pack(pady=(0, 8))

# --- Scenario buttons: placed near the top so they're always visible ---
button_frame = tk.Frame(root, bg="#0b1425")
button_frame.pack(pady=(0, 8))


def select_scenario(name):
    label_status.config(text=f"Selected: {name}")
    class_var.set("—")
    conf_var.set("Confidence: —")
    event_text.config(state="normal")
    event_text.delete("1.0", "end")
    event_text.insert("1.0", "Processing...")
    event_text.config(state="disabled")

    highlight_stage("SENSOR")
    rng = np.random.default_rng()
    t, waveform = CLASS_GENERATORS[name](rng)

    ax_wave.clear()
    ax_wave.set_title(f"Waveform - {name}")
    ax_wave.plot(t * 1000, waveform)
    ax_wave.set_xlabel("time (ms)")
    canvas.draw()
    root.after(STAGE_DELAY_MS, lambda: run_dsp_stage(name, t, waveform))


btn_normal = tk.Button(button_frame, text="NORMAL", command=lambda: select_scenario("NORMAL"))
btn_normal.pack(side="left", padx=5)

btn_harmonic = tk.Button(button_frame, text="HARMONIC DISTORTION",
                          command=lambda: select_scenario("HARMONIC_DISTORTION"))
btn_harmonic.pack(side="left", padx=5)

btn_transient = tk.Button(button_frame, text="TRANSIENT EVENT",
                           command=lambda: select_scenario("TRANSIENT_EVENT"))
btn_transient.pack(side="left", padx=5)

# --- Pipeline stage indicator ---
stage_frame = tk.Frame(root, bg="#0b1425")
stage_frame.pack(pady=(0, 8))

stage_labels = {}
for stage in ["SENSOR", "DSP", "SIGNATURE", "ML", "EVENT"]:
    lbl = tk.Label(
        stage_frame, text=stage, font=("Helvetica", 9, "bold"),
        bg="#1c2947", fg="white", padx=10, pady=5
    )
    lbl.pack(side="left", padx=3)
    stage_labels[stage] = lbl


def highlight_stage(stage_name):
    for name, lbl in stage_labels.items():
        lbl.config(bg="#f0a030" if name == stage_name else "#1c2947",
                   fg="#1a1a1a" if name == stage_name else "white")
    root.update()


fig = Figure(figsize=(7, 2.3), dpi=100)
ax_wave = fig.add_subplot(121)
ax_fft = fig.add_subplot(122)
ax_wave.set_title("Waveform")
ax_fft.set_title("FFT Spectrum")
fig.tight_layout(pad=2.0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=6)

sig_frame = tk.Frame(root, bg="#111c33")
sig_frame.pack(pady=(0, 8), padx=20, fill="x")

tk.Label(sig_frame, text="ELECTRICAL SIGNATURE", fg="#8a93a6", bg="#111c33",
         font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(8, 4))

feature_vars = {}
feature_row = tk.Frame(sig_frame, bg="#111c33")
feature_row.pack(fill="x", padx=14, pady=(0, 8))

for feat_name in ["RMS", "Crest Factor", "THD", "Transient Score"]:
    col = tk.Frame(feature_row, bg="#111c33")
    col.pack(side="left", expand=True, fill="x")
    tk.Label(col, text=feat_name, fg="#8a93a6", bg="#111c33",
             font=("Helvetica", 8)).pack()
    var = tk.StringVar(value="—")
    tk.Label(col, textvariable=var, fg="white", bg="#111c33",
             font=("Helvetica", 12, "bold")).pack()
    feature_vars[feat_name] = var

cls_frame = tk.Frame(root, bg="#111c33")
cls_frame.pack(pady=(0, 8), padx=20, fill="x")

tk.Label(cls_frame, text="CLASSIFICATION", fg="#8a93a6", bg="#111c33",
         font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(8, 2))

class_var = tk.StringVar(value="—")
tk.Label(cls_frame, textvariable=class_var, fg="#f0a030", bg="#111c33",
         font=("Helvetica", 15, "bold")).pack(anchor="w", padx=14)

conf_var = tk.StringVar(value="Confidence: —")
tk.Label(cls_frame, textvariable=conf_var, fg="white", bg="#111c33",
         font=("Helvetica", 10)).pack(anchor="w", padx=14, pady=(0, 8))

event_frame = tk.Frame(root, bg="#111c33")
event_frame.pack(pady=(0, 10), padx=20, fill="both")

tk.Label(event_frame, text="COMPACT EVENT (what leaves the device)", fg="#8a93a6",
         bg="#111c33", font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(8, 4))

mono_font = tkfont.Font(family="Courier", size=9)
event_text = tk.Text(event_frame, height=5, bg="#0d1729", fg="#9fd6a3",
                      font=mono_font, relief="flat", padx=8, pady=8)
event_text.pack(fill="both", padx=14, pady=(0, 10))
event_text.insert("1.0", "Select a scenario to generate an event...")
event_text.config(state="disabled")


def run_dsp_stage(name, t, waveform):
    highlight_stage("DSP")
    sig = preprocess(waveform)
    freqs, magnitude = compute_fft(sig, SAMPLE_RATE_HZ)

    ax_fft.clear()
    ax_fft.set_title("FFT Spectrum")
    mask = freqs <= 500
    ax_fft.stem(freqs[mask], magnitude[mask])
    ax_fft.set_xlabel("frequency (Hz)")
    fig.tight_layout(pad=2.0)
    canvas.draw()
    root.after(STAGE_DELAY_MS, lambda: run_signature_stage(name, waveform))


def run_signature_stage(name, waveform):
    highlight_stage("SIGNATURE")
    features = extract_features(waveform, SAMPLE_RATE_HZ)

    feature_vars["RMS"].set(f"{features['rms']:.3f}")
    feature_vars["Crest Factor"].set(f"{features['crest_factor']:.3f}")
    feature_vars["THD"].set(f"{features['thd']:.3f}")
    feature_vars["Transient Score"].set(f"{features['transient_score']:.3f}")

    root.after(STAGE_DELAY_MS, lambda: run_ml_stage(name, features))


def run_ml_stage(name, features):
    highlight_stage("ML")
    vector = features_to_vector(features).reshape(1, -1)
    predicted = model.predict(vector)[0]
    proba = model.predict_proba(vector)[0]
    confidence = float(np.max(proba))

    class_var.set(predicted)
    conf_var.set(f"Confidence: {confidence:.1%}")

    root.after(STAGE_DELAY_MS, lambda: run_event_stage(name, predicted, confidence, features))


def run_event_stage(name, predicted, confidence, features):
    highlight_stage("EVENT")
    event = {
        "type": predicted,
        "confidence": round(confidence, 3),
        "rms": round(features["rms"], 3),
        "thd": round(features["thd"], 3),
        "transient_score": round(features["transient_score"], 3),
        "source": "edge_device",
        "note": "Decision-support classification on controlled synthetic data."
    }
    event_text.config(state="normal")
    event_text.delete("1.0", "end")
    event_text.insert("1.0", json.dumps(event, indent=2))
    event_text.config(state="disabled")


root.mainloop()