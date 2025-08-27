import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load teacher and student data
teacher = pd.read_csv("teacher.csv")
student = pd.read_csv("student.csv")

# Compute magnitude of acceleration
teacher["acc_mag"] = np.sqrt(teacher["ax"]**2 + teacher["ay"]**2 + teacher["az"]**2)
student["acc_mag"] = np.sqrt(student["ax"]**2 + student["ay"]**2 + student["az"]**2)

# Make sure both have the same length (trim the longer one)
min_len = min(len(teacher), len(student))
teacher = teacher.iloc[:min_len]
student = student.iloc[:min_len]

# Sliding window for RMS
window = 100
teacher["rms_acc"] = teacher["acc_mag"].rolling(window).apply(lambda x: np.sqrt(np.mean(x**2)))
student["rms_acc"] = student["acc_mag"].rolling(window).apply(lambda x: np.sqrt(np.mean(x**2)))

# Compare difference
teacher["student_rms"] = student["rms_acc"].values
teacher["diff"] = abs(teacher["rms_acc"] - teacher["student_rms"])

# Threshold for significant deviation (adjust as needed)
DIFF_THRESHOLD = teacher["diff"].mean() + teacher["diff"].std()
teacher["deviation"] = teacher["diff"] > DIFF_THRESHOLD

# 📊 Plot
plt.figure(figsize=(12,6))
plt.plot(teacher["rms_acc"], label="Teacher (RMS Acc)", color="blue")
plt.plot(student["rms_acc"], label="Student (RMS Acc)", color="red", alpha=0.7)

# Highlight deviations
plt.scatter(teacher.index[teacher["deviation"]],
            student["rms_acc"][teacher["deviation"]],
            color="orange", label="Deviation", zorder=5)

plt.title("Dance Movement Comparison (Teacher vs Student)")
plt.xlabel("Time (samples)")
plt.ylabel("RMS Acceleration")
plt.legend()
plt.show()
