import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your CSV file (replace with actual filename)
df = pd.read_csv("imu_log_20250827_093145.csv")

# Convert values to numeric just in case
df = df.apply(pd.to_numeric, errors="coerce")

# Compute magnitude of acceleration & gyro
df["acc_mag"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)
df["gyro_mag"] = np.sqrt(df["gx"]**2 + df["gy"]**2 + df["gz"]**2)

# --- 1. RMS (root mean square) trend ---
window = 100  # number of samples in each analysis window
df["acc_rms"] = df["acc_mag"].rolling(window).apply(lambda x: np.sqrt(np.mean(x**2)))
df["gyro_rms"] = df["gyro_mag"].rolling(window).apply(lambda x: np.sqrt(np.mean(x**2)))

# --- 2. Variance (movement stability) ---
df["acc_var"] = df["acc_mag"].rolling(window).var()
df["gyro_var"] = df["gyro_mag"].rolling(window).var()

# --- 3. Frequency analysis (FFT) ---
fs = 50  # Hz (adjust to your Arduino sample rate)
N = len(df["acc_mag"].dropna())
freqs = np.fft.rfftfreq(N, 1/fs)
fft_vals = np.abs(np.fft.rfft(df["acc_mag"].dropna()))

# --- Plot ---
plt.figure(figsize=(12,8))

plt.subplot(3,1,1)
plt.plot(df["acc_mag"], label="Acc Magnitude")
plt.plot(df["acc_rms"], label="Acc RMS", color="orange")
plt.legend()
plt.title("Acceleration Magnitude & RMS")

plt.subplot(3,1,2)
plt.plot(df["acc_var"], label="Acc Variance", color="red")
plt.legend()
plt.title("Movement Variability (fatigue ↑ if this rises)")

plt.subplot(3,1,3)
plt.plot(freqs, fft_vals, color="purple")
plt.title("Frequency Spectrum of Acceleration")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()
