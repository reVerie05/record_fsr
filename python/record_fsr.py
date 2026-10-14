
import serial
import csv
from datetime import datetime

# Change COM3 to your Arduino's port
PORT = "COM5"
BAUD_RATE = 9600

filename = "fsr_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"

print("Connecting to Arduino...")

with serial.Serial(PORT, BAUD_RATE, timeout=1) as arduino:
    # Opening the serial connection may reset the Arduino
    print("Connected! Waiting for button presses...")
    recording = False
    csv_file = None
    writer = None

    try:
        while True:
            line = arduino.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            if not line:
                continue

            if line == "START":
                csv_file = open(
                    filename, "w", newline="", encoding="utf-8"
                )
                writer = csv.writer(csv_file)
                writer.writerow(["Time_ms", "ADC", "Voltage_V"])
                recording = True
                print(f"Recording started: {filename}")

            elif line == "STOP":
                if recording:
                    csv_file.close()
                    csv_file = None
                    writer = None
                    recording = False
                    print("Recording stopped. Data saved.")

            elif line.startswith("DATA,") and recording:
                values = line.split(",")

                if len(values) == 4:
                    writer.writerow(values[1:])
                    csv_file.flush()

    except KeyboardInterrupt:
        print("\nStopping recorder...")

    finally:
        if csv_file is not None:
            csv_file.close()

print("Finished.")
