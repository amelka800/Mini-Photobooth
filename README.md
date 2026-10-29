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
