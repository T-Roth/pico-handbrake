import time
import board
import digitalio
import analogio
import usb_hid
import os
from adafruit_hid.gamepad import Gamepad

# ----------------------------
# Pin Configuration
# ----------------------------

# Potentiometer analog input (GP26 = A0)
pot = analogio.AnalogIn(board.A0)

# Calibration button (e.g. GP17)
cal_button = digitalio.DigitalInOut(board.GP17)
cal_button.switch_to_input(pull=digitalio.Pull.UP)

# Debugging LED (GP14)
led = digitalio.DigitalInOut(board.GP14)
led.direction = digitalio.Direction.OUTPUT
led.value = False  # Start off

# Calibration file path
CALIBRATION_FILE = "/calibration.txt"

# Default fallback values (used if no file found)
MIN_POT = 20000
MAX_POT = 30000

# Initialize Gamepad HID device
gp = Gamepad(usb_hid.devices)


# ----------------------------
# Helper Functions
# ----------------------------

def save_calibration(min_val, max_val):
    with open(CALIBRATION_FILE, "w") as f:
        f.write(f"{min_val}\n{max_val}\n")
    print(f"✅ Calibration saved: {min_val} - {max_val}")

def load_calibration():
    global MIN_POT, MAX_POT
    try:
        with open(CALIBRATION_FILE, "r") as f:
            lines = f.readlines()
            MIN_POT = int(lines[0].strip())
            MAX_POT = int(lines[1].strip())
        print(f"✅ Loaded calibration: {MIN_POT} - {MAX_POT}")
        return True
    except Exception as e:
        print("⚠️ No calibration file found. Using defaults.", e)
        return False

def scaled_pot_value(raw):
    raw = max(MIN_POT, min(MAX_POT, raw))
    if MAX_POT == MIN_POT:
        return 0  # avoid divide by zero
    return int((raw - MIN_POT) / (MAX_POT - MIN_POT) * 255)

def calibrate():
    print("🛠 Entering calibration mode...")
    led.value = True  # Turn on LED to indicate calibration

    min_reading = 65535
    max_reading = 0

    while True:
        val = pot.value
        min_reading = min(min_reading, val)
        max_reading = max(max_reading, val)

        print(f"Current: {val} | Min: {min_reading} | Max: {max_reading}")

        # Wait for button press to save and exit
        if not cal_button.value:
            time.sleep(0.5)  # debounce
            print("💾 Saving calibration...")
            save_calibration(min_reading, max_reading)
            break

        time.sleep(0.05)

    led.value = False  # Turn off LED when done

# ----------------------------
# Startup Logic
# ----------------------------

# If button held at startup → enter calibration
if not cal_button.value:
    time.sleep(0.5)  # debounce
    calibrate()

# Load saved or default calibration values
load_calibration()

# ----------------------------
# Main Loop
# ----------------------------

while True:
    # Read potentiometer and scale to Z-axis
    z_value = scaled_pot_value(pot.value)
    gp.move_joysticks(z=z_value)

    # Reuse the button as joystick Button 1
    if not cal_button.value:
        gp.press_buttons(1)
    else:
        gp.release_buttons(1)

    time.sleep(0.01)
