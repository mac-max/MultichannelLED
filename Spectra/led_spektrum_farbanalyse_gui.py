
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_cie_1931_color_matching():
    wl = np.arange(360, 831)
    x_bar = np.exp(-0.5 * ((wl - 595) / 33)**2)
    y_bar = np.exp(-0.5 * ((wl - 565) / 30)**2)
    z_bar = np.exp(-0.5 * ((wl - 445) / 20)**2)
    return wl, x_bar, y_bar, z_bar

def spectrum_to_xy(wavelengths, intensities):
    wl_cie, x_bar, y_bar, z_bar = get_cie_1931_color_matching()
    x_interp = np.interp(wavelengths, wl_cie, x_bar)
    y_interp = np.interp(wavelengths, wl_cie, y_bar)
    z_interp = np.interp(wavelengths, wl_cie, z_bar)
    X = np.sum(intensities * x_interp)
    Y = np.sum(intensities * y_interp)
    Z = np.sum(intensities * z_interp)
    total = X + Y + Z
    if total == 0:
        return 0, 0
    return X / total, Y / total

def estimate_cct(x, y):
    n = (x - 0.3320) / (y - 0.1858)
    CCT = 437 * n**3 + 3601 * n**2 + 6861 * n + 5517
    return CCT

class ColorAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spektralanalyse – Farbort & CCT")
        self.geometry("700x500")
        self.xy_label = ttk.Label(self, text="Farbort (x, y): ---")
        self.xy_label.pack(pady=10)
        self.cct_label = ttk.Label(self, text="Farbtemperatur (CCT): --- K")
        self.cct_label.pack(pady=5)
        ttk.Button(self, text="CSV-Datei laden", command=self.load_csv).pack(pady=10)
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("xy-Farbort in CIE 1931 Diagramm")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_xlim(0, 0.8)
        self.ax.set_ylim(0, 0.9)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV-Dateien", "*.csv")])
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path)
            if 'Wavelength' not in df.columns or 'Intensity' not in df.columns:
                raise ValueError("CSV muss Spalten 'Wavelength' und 'Intensity' enthalten.")
            wl = df['Wavelength'].values
            inten = df['Intensity'].values
            inten = inten / np.max(inten)
            x, y = spectrum_to_xy(wl, inten)
            cct = estimate_cct(x, y)
            self.xy_label.config(text=f"Farbort (x, y): ({x:.4f}, {y:.4f})")
            self.cct_label.config(text=f"Farbtemperatur (CCT): {cct:.0f} K")
            self.plot_xy(x, y)
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def plot_xy(self, x, y):
        self.ax.clear()
        self.ax.set_title("xy-Farbort in CIE 1931 Diagramm")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_xlim(0, 0.8)
        self.ax.set_ylim(0, 0.9)
        self.ax.grid(True)
        self.ax.plot(x, y, 'ro', label="Messwert")
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = ColorAnalyzerApp()
    app.mainloop()
