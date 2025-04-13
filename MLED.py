import os
import tkinter as tk
from tkinter import ttk

# --- Für Blinka I2C-Probleme auf älteren Pis ---
os.environ["BLINKA_FORCECHIP"] = "BCM2XXX"

# --- PCA9685 / I2C Setup ---
import board
import busio
from adafruit_pca9685 import PCA9685

# I2C-Verbindung aufbauen
i2c = busio.I2C(board.SCL, board.SDA)

# PCA9685 mit Adresse 0x41 initialisieren
pca = PCA9685(i2c, address=0x41)
pca.frequency = 1000  # 1 kHz für LEDs / Konstantstromquelle

# --- GUI Setup ---
root = tk.Tk()
root.title("LED PWM Steuerung – PCA9685 @ 0x41")

sliders = []

def set_pwm(channel, percent):
    percent = max(0, min(100, percent))  # Begrenzung 0–100%
    value = int((percent / 100) * 0xFFFF)
    pca.channels[channel].duty_cycle = value

def on_slider_move(channel, var):
    value = var.get()
    set_pwm(channel, value)

def all_off():
    for ch in range(8):
        sliders[ch].set(0)
        pca.channels[ch].duty_cycle = 0

# --- GUI Elemente erstellen ---
for ch in range(8):
    frame = ttk.Frame(root)
    frame.pack(fill='x', padx=10, pady=4)

    label = ttk.Label(frame, text=f"Kanal {ch}")
    label.pack(side='left')

    var = tk.IntVar()
    slider = ttk.Scale(
        frame, from_=0, to=100, orient='horizontal',
        variable=var,
        command=lambda val, ch=ch, v=var: on_slider_move(ch, v)
    )
    slider.pack(side='left', expand=True, fill='x')
    sliders.append(var)

# --- Alles aus Button ---
btn = ttk.Button(root, text="Alle Kanäle AUS", command=all_off)
btn.pack(pady=12)

root.mainloop()
