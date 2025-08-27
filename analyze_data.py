import asyncio
from bleak import BleakClient, BleakScanner
import csv
import datetime

# Replace with the UUIDs from your Arduino sketch
IMU_SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
IMU_CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def main():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    target = None

    for d in devices:
        name = d.name or "Unknown"
        print(f"{name}: {d.address}")
        if "Arduino" in name:
            print("✅ Found Arduino:", name, d.address)
            target = d   # <-- FIXED (now we save the device)

    if not target:
        print("❌ Device not found!")
        return

    print(f"Connecting to {target.name} ({target.address})...")

    async with BleakClient(target) as client:
        print("✅ Connected!")

        filename = f"imu_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ax","ay","az","gx","gy","gz","mx","my","mz"])

            def notification_handler(sender, data):
                try:
                    line = data.decode("utf-8").strip()
                    values = line.split(",")
                    if len(values) == 9:
                        writer.writerow(values)
                        print(values)
                except Exception as e:
                    print("Parse error:", e)

            await client.start_notify(IMU_CHAR_UUID, notification_handler)

            print("Logging IMU data... press Ctrl+C to stop")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("Stopped logging.")

            await client.stop_notify(IMU_CHAR_UUID)

asyncio.run(main())
