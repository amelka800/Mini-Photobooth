// test script 
from escpos.printer import Usb

p = Usb(0x1d81, 0x5721)
p.text("Hello from Raspberry Pi!\n")
p.ln(3)
p.cut()
