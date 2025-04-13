import os
os.environ["BLINKA_FORCECHIP"] = "BCM2XXX"

import tkinter as tk
from tkinter import ttk
import board
import busio
from adafruit_as7341 import AS7341

import threading
import time

# I2C & Sensor-Setup
i2c = busio.I2C(board.SCL, board.SDA)
sensor = AS7341(i2c)

# GUI
root = tk.Tk()
root.title("AS7341 Live-Spektrum")

# Kanäle laut Datenblatt (korrigiert)
channels = [
    ("415 nm", lambda: sensor.channel_405nm),
    ("435 nm", lambda: sensor.channel_435nm),
    ("470 nm", lambda: sensor.channel_470nm),
    ("505 nm", lambda: sensor.channel_505nm),
    ("555 nm", lambda: sensor.channel_535nm),
    ("585 nm", lambda: sensor.channel_570nm),
    ("620 nm", lambda: sensor.channel_600nm),
    ("670 nm", lambda: sensor.channel_645nm),
    ("710 nm", lambda: sensor.channel_680nm),
    ("860 nm", lambda: sensor.channel_710nm),
]

bars = {}

frame = ttk.Frame(root)
frame.pack(padx=20, pady=10)

# Balkenanzeigen für spektrale Kanäle
for label_text, _ in channels:
    row = ttk.Frame(frame)
    row.pack(fill='x', pady=2)

    label = ttk.Label(row, text=label_text, width=8)
    label.pack(side='left')

    progress = ttk.Progressbar(row, orient='horizontal', length=300, mode='determinate', maximum=60000)
    progress.pack(side='left', padx=5)

    value_label = ttk.Label(row, text="0")
    value_label.pack(side='right')

    bars[label_text] = (progress, value_label)

# Zusatz: Clear-Kanal
clear_row = ttk.Frame(root)
clear_row.pack(fill='x', pady=5, padx=20)

ttk.Label(clear_row, text="Clear", width=8).pack(side='left')
clear_bar = ttk.Progressbar(clear_row, orient='horizontal', length=300, mode='determinate', maximum=60000)
clear_bar.pack(side='left', padx=5)
clear_label = ttk.Label(clear_row, text="0")
clear_label.pack(side='right')

# Zusatz: Flicker-Anzeige
flicker_row = ttk.Frame(root)
flicker_row.pack(pady=(10, 5))
flicker_label = ttk.Label(flicker_row, text="Flicker: wird erkannt ...", font=("Arial", 10, "bold"))
flicker_label.pack()

# Lichtquelle schalten
light_on = False
def toggle_light():
    global light_on
    light_on = not light_on
    sensor.led_current = 20
    sensor.led = light_on
    btn.config(text="Licht AUS" if light_on else "Licht EIN")

btn = ttk.Button(root, text="Licht EIN", command=toggle_light)
btn.pack(pady=10)

# Hilfsfunktion für Flicker-Anzeige
def flicker_text(code):
    return {
        0: "Kein Flimmern erkannt",
        1: "50 Hz erkannt",
        2: "60 Hz erkannt",
        3: "100 Hz erkannt",
        4: "120 Hz erkannt",
        255: "Fehler oder keine Messung"
    }.get(code, f"Unbekannt ({code})")

# Live-Update in Hintergrundthread
def update_loop():
    while True:
        try:
            # Spektralkanäle
            for label_text, getter in channels:
                value = getter()
                bars[label_text][0]['value'] = value
                bars[label_text][1]['text'] = str(value)

            # Clear-Kanal
            c = sensor.clear_channel
            clear_bar['value'] = c
            clear_label['text'] = str(c)

            # Flicker
            f = sensor.flicker_detected
            flicker_label['text'] = "Flicker: " + flicker_text(f)

        except Exception as e:
            print("Fehler beim Sensor:", e)

        time.sleep(0.5)

# Hintergrundthread starten
threading.Thread(target=update_loop, daemon=True).start()

root.mainloop()
