import os
import tkinter as tk
from tkinter import ttk

# --- Für Blinka auf Raspberry Pi ---
os.environ["BLINKA_FORCECHIP"] = "BCM2XXX"

import board
import busio
from adafruit_pca9685 import PCA9685

# I2C initialisieren
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 1000

# Kanalnamen definieren
channel_names = [
    "rot", "weiß", "blau", "grün", "orange", "gelb", "UV", "pink"
]

# GUI Fenster
root = tk.Tk()
root.title("LED PWM Steuerung – PCA9685 @ 0x41")

sliders = []
entries = []

def set_pwm(channel, percent):
    percent = max(0, min(100, percent))  # Begrenzen
    value = int((percent / 100) * 0xFFFF)
    pca.channels[channel].duty_cycle = value

def on_slider_move(channel, var, entry_var):
    value = var.get()
    set_pwm(channel, value)
    entry_var.set(f"{int(value)}")

def on_entry_change(channel, slider_var, entry_var):
    try:
        value = int(entry_var.get())
        value = max(0, min(100, value))
        slider_var.set(value)
        set_pwm(channel, value)
    except ValueError:
        pass  # Ungültige Eingabe ignorieren

def all_off():
    for ch in range(8):
        sliders[ch].set(0)
        entries[ch].set("0")
        pca.channels[ch].duty_cycle = 0

# GUI-Elemente
for ch in range(8):
    frame = ttk.Frame(root)
    frame.pack(fill='x', padx=10, pady=4)

    label = ttk.Label(frame, text=f"Kanal {ch} ({channel_names[ch]})", width=18)
    label.pack(side='left')

    slider_var = tk.IntVar()
    entry_var = tk.StringVar(value="0")

    slider = ttk.Scale(
        frame, from_=0, to=100, orient='horizontal',
        variable=slider_var,
        command=lambda val, ch=ch, sv=slider_var, ev=entry_var: on_slider_move(ch, sv, ev)
    )
    slider.pack(side='left', expand=True, fill='x', padx=(5, 5))

    entry = ttk.Entry(frame, textvariable=entry_var, width=5)
    entry.pack(side='right')
    entry.bind("<Return>", lambda event, ch=ch, sv=slider_var, ev=entry_var: on_entry_change(ch, sv, ev))

    sliders.append(slider_var)
    entries.append(entry_var)

# Alles-aus-Button
btn = ttk.Button(root, text="Alle Kanäle AUS", command=all_off)
btn.pack(pady=12)

root.mainloop()
