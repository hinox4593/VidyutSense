import sys
import os
import json
import random
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
from anomalygate import check_anomaly
from grid_simulator import run_grid_investigation
from device_simulator import DEVICES, DEFAULT_HIGH_ACTIVITY_NODES, run_device_investigation
from assessment import build_assessment

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "models", "classifier.joblib")
model = joblib.load(MODEL_PATH)

STAGE_DELAY_MS = 1100

# Fixed deterministic scenario for the demo narrative: an isolated
# anomaly with low grid correlation (1 out of 10 neighboring houses
# anomalous), so the investigation flow is reproducible live.
DEMO_ANOMALOUS_HOUSES = 1

# Fixed decorative "normal" activity nodes, for visual context only.
# These play no role in the actual spatial-association calculation —
# only the real high-activity node(s) from device_simulator do.
DECORATIVE_DIM_NODES = [
    {"x": 2.5, "y": 2.0}, {"x": 4.0, "y": 4.0}, {"x": 0.7, "y": 2.8},
    {"x": 3.5, "y": 1.5}, {"x": 4.5, "y": 3.2}, {"x": 2.0, "y": 4.8},
]

# State captured from the main pipeline, used by the investigation windows.
last_classification = {}

root = tk.Tk()
root.title("VidyutSense")
root.geometry("800x780")
root.configure(bg="#0b1425")

main_canvas = tk.Canvas(root, bg="#0b1425", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas, bg="#0b1425")

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

label_title = tk.Label(
    scrollable_frame, text="VIDYUTSENSE",
    font=("Helvetica", 18, "bold"),
    fg="white", bg="#0b1425"
)
label_title.pack(pady=(10, 2))

label_status = tk.Label(
    scrollable_frame, text="Select a scenario",
    font=("Helvetica", 11),
    fg="#f0a030", bg="#0b1425"
)
label_status.pack(pady=(0, 8))

button_frame = tk.Frame(scrollable_frame, bg="#0b1425")
button_frame.pack(pady=(0, 8))


def select_scenario(name):
    label_status.config(text=f"Selected: {name}")
    class_var.set("—")
    conf_var.set("Confidence: —")
    status_var.set("—")
    status_reasons_var.set("")
    grid_button.pack_forget()
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

stage_frame = tk.Frame(scrollable_frame, bg="#0b1425")
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

canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
canvas.get_tk_widget().pack(pady=6)

sig_frame = tk.Frame(scrollable_frame, bg="#111c33")
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

cls_frame = tk.Frame(scrollable_frame, bg="#111c33")
cls_frame.pack(pady=(0, 8), padx=20, fill="x")

tk.Label(cls_frame, text="CLASSIFICATION", fg="#8a93a6", bg="#111c33",
         font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(8, 2))

class_var = tk.StringVar(value="—")
tk.Label(cls_frame, textvariable=class_var, fg="#f0a030", bg="#111c33",
         font=("Helvetica", 15, "bold")).pack(anchor="w", padx=14)

conf_var = tk.StringVar(value="Confidence: —")
tk.Label(cls_frame, textvariable=conf_var, fg="white", bg="#111c33",
         font=("Helvetica", 10)).pack(anchor="w", padx=14, pady=(0, 8))

event_frame = tk.Frame(scrollable_frame, bg="#111c33")
event_frame.pack(pady=(0, 8), padx=20, fill="both")

tk.Label(event_frame, text="COMPACT EVENT (what leaves the device)", fg="#8a93a6",
         bg="#111c33", font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(8, 4))

mono_font = tkfont.Font(family="Courier", size=9)
event_text = tk.Text(event_frame, height=5, bg="#0d1729", fg="#9fd6a3",
                      font=mono_font, relief="flat", padx=8, pady=8)
event_text.pack(fill="both", padx=14, pady=(0, 10))
event_text.insert("1.0", "Select a scenario to generate an event...")
event_text.config(state="disabled")

status_frame = tk.Frame(scrollable_frame, bg="#111c33")
status_frame.pack(pady=(0, 20), padx=20, fill="x")

tk.Label(status_frame, text="SIGNAL STATUS", fg="#8a93a6", bg="#111c33",
         font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(8, 2))

status_var = tk.StringVar(value="—")
tk.Label(status_frame, textvariable=status_var, fg="white", bg="#111c33",
         font=("Helvetica", 13, "bold")).pack(anchor="w", padx=14)

status_reasons_var = tk.StringVar(value="")
tk.Label(status_frame, textvariable=status_reasons_var, fg="#8a93a6", bg="#111c33",
         font=("Helvetica", 9), justify="left", wraplength=650).pack(anchor="w", padx=14, pady=(2, 8))


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
    last_classification["behavior_class"] = predicted
    last_classification["confidence"] = confidence

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

    grid_button.pack_forget()

    anomaly_result = check_anomaly(features)
    if anomaly_result["is_anomaly"]:
        status_var.set("ANOMALOUS")
        reasons_text = "\n".join(f"• {r}" for r in anomaly_result["reasons"])
        status_reasons_var.set(reasons_text)
        grid_button.pack(anchor="w", padx=14, pady=(0, 8))
    else:
        status_var.set("NORMAL")
        status_reasons_var.set("No further investigation required.")


# ---------------------------------------------------------------------
# Coordinate mapping: device_simulator uses a 0-6 conceptual grid
# (device x/y values range roughly 1.0-5.0). We map that onto a
# square canvas for the device investigation window.
# ---------------------------------------------------------------------
SCENE_DATA_RANGE = 6.0
CANVAS_SIZE = 480
CANVAS_MARGIN = 50


def data_to_canvas(x, y):
    plot_size = CANVAS_SIZE - 2 * CANVAS_MARGIN
    cx = CANVAS_MARGIN + (x / SCENE_DATA_RANGE) * plot_size
    cy = CANVAS_MARGIN + ((SCENE_DATA_RANGE - y) / SCENE_DATA_RANGE) * plot_size
    return cx, cy


def open_device_window(grid_result, on_assessment_update):
    """Opens a separate popup window containing a visual device scene:
    a square canvas with device positions, dim decorative activity
    nodes (blinking), and the real high-activity node highlighted in
    bright red. Analyzing calls the real device_simulator math."""
    win = tk.Toplevel(root)
    win.title("VidyutSense — Device Investigation")
    win.geometry("560x700")
    win.configure(bg="#0b1425")

    tk.Label(win, text="DEVICE / USAGE INVESTIGATION", fg="white", bg="#0b1425",
             font=("Helvetica", 14, "bold")).pack(pady=(15, 4))
    tk.Label(win, text="Bright red = high electrical activity node",
             fg="#8a93a6", bg="#0b1425", font=("Helvetica", 9)).pack(pady=(0, 10))

    scene = tk.Canvas(win, width=CANVAS_SIZE, height=CANVAS_SIZE,
                       bg="#0d1729", highlightthickness=1, highlightbackground="#1c2947")
    scene.pack(pady=(0, 10))

    # Draw devices as labeled squares
    device_canvas_pos = {}
    for name, dev in DEVICES.items():
        cx, cy = data_to_canvas(dev["x"], dev["y"])
        device_canvas_pos[name] = (cx, cy)
        scene.create_rectangle(cx - 10, cy - 10, cx + 10, cy + 10,
                                fill="#2b3a5c", outline="#5a6b8c")
        scene.create_text(cx, cy + 20, text=name, fill="white",
                           font=("Helvetica", 8, "bold"))

    # Draw decorative dim nodes (blinking, visual only)
    dim_node_ids = []
    for node in DECORATIVE_DIM_NODES:
        cx, cy = data_to_canvas(node["x"], node["y"])
        node_id = scene.create_oval(cx - 4, cy - 4, cx + 4, cy + 4,
                                     fill="#4a1010", outline="")
        dim_node_ids.append(node_id)

    blink_job = {"id": None}

    def blink():
        for node_id in dim_node_ids:
            color = random.choice(["#4a1010", "#6b1a1a", "#3a0c0c"])
            scene.itemconfig(node_id, fill=color)
        blink_job["id"] = win.after(500, blink)

    blink()

    def on_close():
        if blink_job["id"] is not None:
            win.after_cancel(blink_job["id"])
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    # Draw the real high-activity node(s) in bright red
    high_node_canvas_pos = []
    for node in DEFAULT_HIGH_ACTIVITY_NODES:
        cx, cy = data_to_canvas(node["x"], node["y"])
        high_node_canvas_pos.append((cx, cy))
        scene.create_oval(cx - 9, cy - 9, cx + 9, cy + 9,
                           fill="#ff3b3b", outline="#ffb3b3", width=2)
        scene.create_text(cx, cy - 18, text="HIGH ACTIVITY", fill="#ff6b6b",
                           font=("Helvetica", 8, "bold"))

    result_frame = tk.Frame(win, bg="#111c33")
    result_frame.pack(padx=20, pady=(0, 10), fill="x")

    tk.Label(result_frame, text="ANALYSIS RESULT", fg="#8a93a6", bg="#111c33",
             font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(10, 4))

    result_var = tk.StringVar(value="Click ANALYZE to study the high-activity node.")
    tk.Label(result_frame, textvariable=result_var, fg="white", bg="#111c33",
             font=("Helvetica", 10), justify="left", wraplength=500).pack(
        anchor="w", padx=14, pady=(0, 12))

    def analyze():
        device_results = run_device_investigation()
        result = device_results[0]
        best_device = result["most_likely_device"]

        # Draw a line from the high-activity node to the identified device
        hx, hy = high_node_canvas_pos[0]
        dx, dy = device_canvas_pos[best_device]
        scene.create_line(hx, hy, dx, dy, fill="#f0a030", width=2, dash=(4, 2))

        summary = (
            f"Nearest associated device: {best_device}\n"
            f"Association confidence: {result['association_confidence']:.1f}%\n"
            f"Estimated load increase: +{result['load_increase_kw']:.1f} kW\n"
            f"Estimated additional usage: +{result['additional_energy_kwh']:.2f} kWh\n\n"
            f"Context: elevated local usage may explain observed anomaly."
        )
        result_var.set(summary)

        conclusion = build_assessment(
            {"is_anomaly": True, "reasons": []},
            classification=last_classification,
            grid_result=grid_result,
            device_result=result,
        )
        on_assessment_update(conclusion["conclusion"])

    analyze_btn = tk.Button(win, text="ANALYZE HIGH-ACTIVITY NODE", command=analyze)
    analyze_btn.pack(pady=(0, 15))


def open_investigation_window():
    """Opens a separate popup window for the grid investigation. If
    correlation is LOW/MODERATE, offers a button to open the device
    investigation window (its own separate popup)."""
    win = tk.Toplevel(root)
    win.title("VidyutSense — Grid Investigation")
    win.geometry("640x480")
    win.configure(bg="#0b1425")

    tk.Label(win, text="GRID INVESTIGATION", fg="white", bg="#0b1425",
             font=("Helvetica", 16, "bold")).pack(pady=(15, 10))

    grid_frame = tk.Frame(win, bg="#111c33")
    grid_frame.pack(padx=20, pady=(0, 10), fill="x")

    grid_houses_var = tk.StringVar(value="")
    tk.Label(grid_frame, textvariable=grid_houses_var, fg="white", bg="#111c33",
             font=("Courier", 10), justify="left").pack(anchor="w", padx=14, pady=(14, 0))

    grid_summary_var = tk.StringVar(value="")
    tk.Label(grid_frame, textvariable=grid_summary_var, fg="#f0a030", bg="#111c33",
             font=("Helvetica", 11, "bold"), justify="left", wraplength=580).pack(
        anchor="w", padx=14, pady=(10, 14))

    assessment_frame = tk.Frame(win, bg="#111c33")
    assessment_frame.pack(padx=20, pady=(0, 15), fill="x")

    tk.Label(assessment_frame, text="FINAL ASSESSMENT", fg="#8a93a6", bg="#111c33",
             font=("Helvetica", 9, "bold")).pack(anchor="w", padx=14, pady=(10, 4))

    assessment_var = tk.StringVar(value="")
    tk.Label(assessment_frame, textvariable=assessment_var, fg="#f0a030", bg="#111c33",
             font=("Helvetica", 14, "bold"), justify="left", wraplength=580).pack(
        anchor="w", padx=14, pady=(0, 12))

    def update_assessment(text):
        assessment_var.set(text)

    device_button = tk.Button(win, text="CHECK DEVICE USAGE")

    investigation = run_grid_investigation(DEMO_ANOMALOUS_HOUSES)
    houses = investigation["houses"]
    result = investigation["result"]

    lines = []
    for row_start in range(0, 10, 5):
        row_houses = houses[row_start:row_start + 5]
        row_text = "   ".join(f"H{h['house_id']}:{h['status']}" for h in row_houses)
        lines.append(row_text)
    grid_houses_var.set("\n".join(lines))

    summary = (
        f"Anomalous houses: {result['anomalous_houses']}/{result['total_houses']}   "
        f"Grid Correlation Score: {result['grid_correlation_score']}   "
        f"({result['correlation_level']})\n"
        f"{result['interpretation']}"
    )
    grid_summary_var.set(summary)

    if result["correlation_level"] == "HIGH":
        conclusion = build_assessment(
            {"is_anomaly": True, "reasons": []},
            classification=last_classification,
            grid_result=result,
        )
        assessment_var.set(conclusion["conclusion"])
    else:
        device_button.config(command=lambda: open_device_window(result, update_assessment))
        device_button.pack(pady=(0, 10))


grid_button = tk.Button(
    status_frame, text="CHECK SURROUNDING GRID",
    command=open_investigation_window
)

root.mainloop()