# Mini-Photobooth
mini photobooth using a Raspberry Pi 3 A+, which takes a picture with a fish hole camera lens, formats the picture and instantly prints it through a thermal printer using python scripts

## Hardware Used
- Raspberry Pi 3 A+\
- Integrated thermal printer 58mm BT USB TTL RS232\
- Old phone (samsung) as disaplay screen\
- Fish hole camera module\
- Arcade style button\
- alligator clip wires\
- Micro USB data transfer cable\

## Run through
1. screen is idle waiting for butten to be pressed
2. when button is pressed countdown begins and is shown on the display screen 3 2 1..
3. the picture is taken 
4. the picture is printed immediatly after 
5. the screen returns to idle waiting for the button to be pressed and process repeats

##Requirements
- picamzero (camera)
- escpos (printer)
- RealVNC viewer app (display from phone)
