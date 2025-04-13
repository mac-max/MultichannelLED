#!/bin/bash

echo "Starte Einrichtung für PCA9685 + AS7341 auf Raspberry Pi..."

# 1. System aktualisieren
echo "Aktualisiere Systempakete..."
sudo apt update
sudo apt upgrade -y

# 2. Python-Pakete installieren
echo "Installiere Python-Grundpakete..."
sudo apt install -y python3-pip python3-dev i2c-tools git

# 3. I2C aktivieren, falls nicht schon geschehen
echo "Aktiviere I2C-Schnittstelle..."
sudo raspi-config nonint do_i2c 0

# 4. Adafruit Blinka (Hardware-API)
echo "Installiere Adafruit Blinka..."
pip3 install --upgrade adafruit-blinka

# 5. Bibliothek für PCA9685 (LED-Treiber)
echo "Installiere PCA9685-Treiber..."
pip3 install adafruit-circuitpython-pca9685

# 6. Bibliothek für AS7341 (Farbsensor)
echo "Installiere AS7341-Treiber..."
pip3 install adafruit-circuitpython-as7341

# 7. Test: I2C-Geräte anzeigen
echo "Aktuell angeschlossene I2C-Geräte:"
i2cdetect -y 1

# 8. Empfehlung zur Umgebungsvariable
if ! grep -q "BLINKA_FORCECHIP=BCM2XXX" ~/.bashrc; then
  echo "Exportiere BLINKA_FORCECHIP=BCM2XXX in ~/.bashrc"
  echo 'export BLINKA_FORCECHIP=BCM2XXX' >> ~/.bashrc
  source ~/.bashrc
fi

echo "Einrichtung abgeschlossen!"
echo "Starte dein Python-Skript mit: python3 dein_script.py"
