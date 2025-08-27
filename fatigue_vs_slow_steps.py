import pandas as pd
import numpy as np

# Load your CSV (from Arduino BLE logger)
df = pd.read_csv("imu_log_20250827_112552.csv")

# 1. Compute magnitude of acceleration
df["acc_mag"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)

# 2. Sliding window size (e.g., 2 sec if sampling ~50Hz → 100 samples)
window = 100  

# 3. Compute rolling RMS and Variance
df["rms_acc"] = df["acc_mag"].rolling(window).apply(lambda x: np.sqrt(np.mean(x**2)))
df["acc_var"] = df["acc_mag"].rolling(window).var()

# 4. Baseline calibration (first 10 sec, adjust if needed)
baseline_rms = df["rms_acc"][:500].mean()
baseline_var = df["acc_var"][:500].mean()

print(f"📊 Baseline RMS: {baseline_rms:.4f}")
print(f"📊 Baseline Variance: {baseline_var:.4f}")

# 5. Define thresholds (tweak as needed!)
RMS_DROP_THRESHOLD = 0.7        # 30% drop
VAR_INCREASE_THRESHOLD = 1.5    # 2x increase

# 6. Classify each window
def classify(rms, var):
    if pd.isna(rms) or pd.isna(var):
        return "Unknown"
    if rms < baseline_rms * RMS_DROP_THRESHOLD and var > baseline_var * VAR_INCREASE_THRESHOLD:
        return "Fatigue"
    elif rms < baseline_rms * RMS_DROP_THRESHOLD and var <= baseline_var * VAR_INCREASE_THRESHOLD:
        return "Intentional Slow"
    else:
        return "Normal"

df["classification"] = df.apply(lambda row: classify(row["rms_acc"], row["acc_var"]), axis=1)

# Save results
df.to_csv("imu_fatigue_analysis.csv", index=False)

# Show the entire dataset
pd.set_option("display.max_rows", None)   # show all rows
pd.set_option("display.max_columns", None) # show all columns
print(df[["acc_mag", "rms_acc", "acc_var", "classification"]])
