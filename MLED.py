import tkinter as tk
from tkinter import ttk
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# I2C initialisieren
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 1000  # 1 kHz für Konstantstromquellen ideal

# GUI Fenster
root = tk.Tk()
root.title("LED PWM Steuerung (PCA9685)")

# Referenzen auf Slider
sliders = []

def set_pwm(channel, value_percent):
    """Setzt die PWM für einen Kanal basierend auf Prozentwert (0–100%)"""
    value_percent = max(0, min(100, value_percent))  # begrenzen
    duty_cycle = int((value_percent / 100.0) * 0xFFFF)
    pca.channels[channel].duty_cycle = duty_cycle

def slider_callback(channel, var):
    """Wird aufgerufen, wenn ein Slider bewegt wird"""
    value = var.get()
    set_pwm(channel, value)

def all_off():
    """Alle Kanäle ausschalten"""
    for i in range(8):
        sliders[i].set(0)
        pca.channels[i].duty_cycle = 0

# UI erstellen
for i in range(8):
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=5, fill='x')

    label = ttk.Label(frame, text=f"Kanal {i}")
    label.pack(side='left')

    var = tk.IntVar()
    slider = ttk.Scale(
        frame, from_=0, to=100, orient='horizontal',
        variable=var,
        command=lambda val, ch=i, v=var: slider_callback(ch, v)
    )
    slider.pack(side='left', expand=True, fill='x')
    sliders.append(var)

# Schaltfläche: Alles aus
off_button = ttk.Button(root, text="Alles aus", command=all_off)
off_button.pack(pady=10)

# GUI starten
root.mainloop()
