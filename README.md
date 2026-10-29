# Raspberry Pi Thermal Printer Photobooth
 
A DIY photobooth built on a Raspberry Pi. Press an arcade button, get a 3-2-1 countdown on an old phone screen, and the Pi takes your photo and prints it on a thermal receipt printer.
 
## How it works
 
1. Press the arcade button.
2. A countdown appears on the display (an old phone running RealVNC Viewer).
3. The camera module takes a photo.
4. The photo is shown on screen, converted to dithered black and white, and printed.

 ## Hardware 
 
| Part | Notes |
|---|---|
| Raspberry Pi 3 A+ | Runs everything |
| Camera module | Connected with a wide ribbon cable |
| Thermal printer (58mm, "Printer 58A") | Connected over USB |
| Arcade-style button | Wired to the GPIO pins |
| Display screen | An old phone, using RealVNC Viewer |
| Shoebox | Used as the frame/enclosure |
| Alligator clip wires | Used for all connectors |

## 1. Camera
 
1. Physically connect the camera to the Pi with the wide ribbon cable (power the Pi off first).
2. Install the camera library:
```bash
   sudo apt update
   sudo apt install python3-picamzero
```
3. Take a test picture:
```bash
   rpicam-still -o ~/Desktop/testimage.jpg
```
4. The picture is saved on the Pi. To view it on your computer, open a **new terminal on your computer** (not the one connected to the Pi) and copy it across with `scp`:
```bash
   scp amelka800@raspberrypi.local:~/Desktop/testimage.jpg .
```
   The `.` at the end means "download into the current folder".
 
### 2. Thermal printer
 
1. Install the Python package:
```bash
   sudo apt install python3-escpos
```
   (For the virtual environment used in this project, `escpos-env`, install `python-escpos` with pip inside it.)
2. Find the printer's USB IDs:
```bash
   lsusb
```
   Output:
```
   Bus 001 Device 002: ID 1d81:5721 Printer 58A
```
   So the vendor ID is `0x1d81` and the product ID is `0x5721`.
3. Test script (`test_print.py`) which will print Hello from Raspberry Pi!:
```python
   from escpos.printer import Usb
 
   p = Usb(0x1d81, 0x5721)
   p.text("Hello from Raspberry Pi!\n")
   p.ln(3)
   p.cut()
```
4. Run it using the virtual environment's Python:
```bash
   ~/escpos-env/bin/python ~/test_print.py
```
 
**Shortcut:** typing that whole command every time is annoying. Add a shebang as the very first line of the script so it knows which interpreter to use:
 
```python
#!/home/amelka800/escpos-env/bin/python
```
 
Then make the file executable:
 
```bash
chmod +x ~/test_print.py
```
 
Now you can run it with just `~/test_print.py`.
 
### 3. Arcade button
 
Wire the two button tabs to **physical pin 40 (GPIO 21)** and **physical pin 39 (GND)**. It doesn't matter which tab goes to which pin. No resistor is needed because the Pi's internal pull-up is used. Beware the button may hve appitional LED tabs. 
 
Check the wiring without any Python:
 
```bash
pinctrl get 21
```
 
- Not pressed: `21: ip    -- | hi`
- Pressed: `21: ip    -- | lo`
  
Then test with a script (`button_test.py`):
 
```python
from gpiozero import Button
from signal import pause
 
button = Button(21)
button.when_pressed = lambda: print("Button pressed!")
pause()
```

If youre having issues you can directly run a spare wire through pin 39 to 40, to isolate if th eproblem is with the physical connection or the script
 
### 4. Display
 
An old phone is used as the display through the RealVNC Viewer app.
 
1. Enable VNC on the Pi: `sudo raspi-config` → **Interface Options** → **VNC** → **Yes**.
2. Find the Pi's IP address with `hostname -I`.
3. On the phone, install **RealVNC Viewer**, add the Pi's IP and log in with the Pi username and password. The phone must be on the same Wi-Fi network as the Pi.
## The photobooth script
 
Create the script:
 
```bash
nano photobooth.py
```
 
It ties the parts together: button press → countdown on the VNC screen → camera capture → display the photo → print it.
 
The window has to open on the Pi's desktop, so run it from a terminal on the phone:

Press **Esc** to quit.
 
## Troubleshooting
 
| Problem | What to try |
|---|---|
| Camera not found | Power off and reseat the ribbon cable at both ends, then check with `rpicam-hello --list-cameras`|
| Printer doesn't print | Re-check the USB IDs with `lsusb` |
| Button does nothing | Check `pinctrl get 21` changes when pressed, and that both clips are firmly on the tabs, not the LED tabs |
| Note when changing components make sure to power off Pi |
 
