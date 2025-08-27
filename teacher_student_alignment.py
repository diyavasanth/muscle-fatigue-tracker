import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dtaidistance import dtw

# ---------- SETTINGS ----------
teacher_file = "teacher.csv"
student_file = "student.csv"

compare_col = "acc_mag"  # or ax, ay, az, gx, gy, gz

# ---------- LOAD DATA ----------
def load_data(filename):
    df = pd.read_csv(filename)

    # Compute magnitude if not already present
    if "acc_mag" not in df.columns:
        df["acc_mag"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)

    # Use "Time(samples)" if available, else fall back to index
    if "Time(samples)" in df.columns:
        df["time_axis"] = df["Time(samples)"]
    elif "Time" in df.columns:
        df["time_axis"] = df["Time"]
    else:
        df["time_axis"] = np.arange(len(df))  # use row index as time

    return df

teacher = load_data(teacher_file)
student = load_data(student_file)

# ---------- ALIGN USING DTW ----------
t_series = teacher[compare_col].values
s_series = student[compare_col].values

# Compute DTW distance
distance = dtw.distance(t_series, s_series)
alignment = dtw.warping_path(t_series, s_series)

print(f"DTW distance between teacher and student: {distance:.2f}")
print("✅ Lower distance = more similar movements")

# ---------- PLOT ----------
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(teacher["time_axis"], t_series, label="Teacher")
plt.plot(student["time_axis"], s_series, label="Student", alpha=0.7)
plt.title("Raw Motion Data")
plt.xlabel("Time")
plt.ylabel(compare_col)
plt.legend()

plt.subplot(2, 1, 2)
dtwvis = np.array(alignment)
plt.plot(dtwvis[:,0], dtwvis[:,1], 'r.')
plt.title("DTW Alignment (red dots show how teacher ↔ student points match)")
plt.xlabel("Teacher timeline")
plt.ylabel("Student timeline")

plt.tight_layout()
plt.show()
