import asyncio
from bleak import BleakClient, BleakScanner
import numpy as np
from collections import deque

# UUIDs from your Arduino sketch
IMU_SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
IMU_CHAR_UUID    = "12345678-1234-5678-1234-56789abcdef1"

# Buffer to hold recent samples
window_size = 100   # number of samples in rolling window (~2s if 50 Hz)
acc_buffer = deque(maxlen=window_size)
gyro_buffer = deque(maxlen=window_size)

def detect_fatigue():
    if len(acc_buffer) < window_size:
        return None  # not enough data yet

    acc_arr = np.array(acc_buffer)
    gyro_arr = np.array(gyro_buffer)

    # RMS
    acc_rms = np.sqrt(np.mean(acc_arr**2))
    gyro_rms = np.sqrt(np.mean(gyro_arr**2))

    # Variance
    acc_var = np.var(acc_arr)
    gyro_var = np.var(gyro_arr)

    # Heuristic fatigue rules
    fatigue_flag = False
    reasons = []

    if acc_rms < 0.2:   # weak movements
        fatigue_flag = True
        reasons.append("Low RMS (weaker movements)")

    if acc_var > 1.0:   # unstable motion
        fatigue_flag = True
        reasons.append("High variance (shaky)")

    return fatigue_flag, acc_rms, acc_var, reasons

def notification_handler(sender, data):
    try:
        line = data.decode("utf-8").strip()
        values = line.split(",")
        if len(values) == 9:
            ax, ay, az, gx, gy, gz, mx, my, mz = map(float, values)
            acc_mag = np.sqrt(ax**2 + ay**2 + az**2)
            gyro_mag = np.sqrt(gx**2 + gy**2 + gz**2)

            acc_buffer.append(acc_mag)
            gyro_buffer.append(gyro_mag)

            result = detect_fatigue()
            if result:
                fatigue, acc_rms, acc_var, reasons = result
                if fatigue:
                    print(f"⚠️ Fatigue detected! RMS={acc_rms:.2f}, Var={acc_var:.2f} | {'; '.join(reasons)}")
                else:
                    print(f"OK: RMS={acc_rms:.2f}, Var={acc_var:.2f}")

    except Exception as e:
        print("Parse error:", e)

async def main():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    target = None

    for d in devices:
        if "Arduino" in (d.name or ""):  # adjust if your Arduino advertises differently
            target = d
            break

    if not target:
        print("❌ Arduino not found!")
        return

    print(f"Connecting to {target.name} ({target.address})...")
    async with BleakClient(target) as client:
        print("✅ Connected! Streaming IMU data...")
        await client.start_notify(IMU_CHAR_UUID, notification_handler)

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Stopped.")
            await client.stop_notify(IMU_CHAR_UUID)

asyncio.run(main())
