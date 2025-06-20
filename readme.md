# Raspberry Pi Pico Analog USB Handbrake with Auto Calibration (CircuitPython)

This project turns a Raspberry Pi Pico into an analog USB handbrake (or joystick axis) for sim racing games like Assetto Corsa, BeamNG.drive, etc. It uses a potentiometer connected to the Pico's analog input and sends HID joystick signals to your PC. A calibration button lets you easily store and reuse custom motion ranges.

---

## 🧰 Hardware Requirements

- Raspberry Pi Pico or Pico W
- 10kΩ linear potentiometer (B10K)
- Momentary pushbutton (for calibration mode)
- Wires, breadboard, or soldered connections
- USB micro cable
- Optional: switches for additional buttons

---

## 🧠 Features

- USB HID joystick emulation (Z-axis)
- Real-time analog handbrake input using potentiometer
- Press-and-hold button on boot to enter calibration mode
- Saves custom potentiometer range to `calibration.txt`
- Calibration survives reboot and power loss

---

## 🖥️ Setup Instructions

### 1. Flash CircuitPython to Your Pico

1. Hold the **BOOTSEL** button while plugging the Pico into your computer.
2. The Pico will mount as a USB drive called `RPI-RP2`.
3. Go to [https://circuitpython.org/board/raspberry_pi_pico/](https://circuitpython.org/board/raspberry_pi_pico/)
4. Download the latest CircuitPython `.uf2` firmware.
5. Drag and drop the `.uf2` file onto the `RPI-RP2` drive.
6. It will reboot and appear as `CIRCUITPY`.

---

### 2. Install Required Libraries

1. Download the [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries)
2. Unzip it and navigate to the `lib/` folder.
3. Copy the following folder to the Pico’s `CIRCUITPY/lib/` folder:


> You need the `gamepad.py` file inside this folder.

---

### 3. Wire Your Components

#### 🔧 Potentiometer:
| Pot Pin       | Connect to Pico |
|---------------|------------------|
| Left (VCC)    | 3.3V (Pin 36)    |
| Middle (SIG)  | GP26 / A0 (Pin 31) |
| Right (GND)   | GND (Pin 38 or 33) |

#### 🔘 Calibration Button:
| Button Pin    | Connect to Pico |
|---------------|------------------|
| One side      | GND              |
| Other side    | GP15 (Pin 21)    |

---

### 4. Add the Code

1. Copy handbrake/code.py to the `CIRCUITPY` drive (see below).
2. On boot, the script will:
   - Load existing calibration values (if available)
   - Or enter calibration mode if the button is held at boot

---

## 🕹️ How to Calibrate

1. **Press and hold the calibration button** while plugging in the Pico.
2. Move the potentiometer through its entire usable range.
3. **Press the button again** to save min/max values.
4. The values are saved to a file named `calibration.txt` and used on future boots.

---

## 🧪 Joystick Behavior

- The analog input is scaled to 0–255 and sent as the joystick’s **Z-axis**
- You can view the result in:
  - Windows: `joy.cpl`
  - Steam: Controller settings
  - In-game input mapping menus

---

## 🛠️ Example `code.py`

See the full code in this repository or copy from the [main script section](#).

---

## 🛠️ Optional Add-ons

- Add buttons via GPIOs using `gp.press_buttons()` and `gp.release_buttons()`
- Add more analog axes (e.g. clutch, throttle via GP27, GP28)
- Add status LED for calibration mode
- 3D print or laser-cut a compact housing

---

## 🧩 Troubleshooting

| Issue | Fix |
|-------|-----|
| Handbrake not responsive | Check wiring and run calibration |
| Not detected by PC | Ensure CircuitPython is running and HID library is present |
| Values too small | Recalibrate using full range of motion |
| `calibration.txt` missing | It will be created after your first calibration |

---

## 📜 License

MIT License – free to use, modify, and distribute.

---

## 🙌 Credits

Created by [Your Name]  
Inspired by the sim racing DIY community  
Based on [Adafruit HID library](https://github.com/adafruit/Adafruit_CircuitPython_HID)

