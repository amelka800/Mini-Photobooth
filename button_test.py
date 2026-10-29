// buttom test py file nano 
from gpiozero import Button
from signal import pause

button = Button(21)
button.when_pressed = lambda: print("Button pressed!")
pause()
