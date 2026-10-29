import time, threading, subprocess, queue
import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageEnhance
from gpiozero import Button
from escpos.printer import Usb, Serial

# ---------- settings ----------
BUTTON_PIN  = 21
PHOTO       = "/home/amelka800/photo.jpg"
PRINT_WIDTH = 384          # 58mm printer = 384, 80mm printer = 576
COUNTDOWN   = 3

def get_printer():
    return Usb(0x0416, 0x5011)                              # change to your IDs
    # return Serial(devfile="/dev/serial0", baudrate=9600)  # or use this for serial
# ------------------------------

events = queue.Queue()
busy = False

root = tk.Tk()
root.configure(bg="black")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())
root.bind("<space>", lambda e: events.put("press"))   # keyboard backup for testing

label = tk.Label(root, text="Press the button!", font=("Helvetica", 48),
                 fg="white", bg="black")
label.pack(expand=True, fill="both")

def say(text):
    label.config(image="", text=text)
    label.image = None

def show_photo():
    img = Image.open(PHOTO)
    w, h = root.winfo_width(), root.winfo_height()
    img = ImageOps.contain(img, (w, h))
    tkimg = ImageTk.PhotoImage(img)
    label.config(image=tkimg, text="")
    label.image = tkimg          # keep a reference or it disappears

def print_photo():
    img = Image.open(PHOTO).convert("L")
    img = ImageOps.fit(img, (PRINT_WIDTH, int(PRINT_WIDTH * 0.8)))
    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = img.convert("1")                       # dithered black & white
    p = get_printer()
    p.image(img)
    p.text("\n\n\n")
    try:
        p.cut()
    except Exception:
        pass
    p.close()

def worker():
    """Runs in a background thread so the window doesn't freeze."""
    global busy
    try:
        subprocess.run(["rpicam-still", "--nopreview", "-t", "1",
                        "--width", "1280", "--height", "960", "-o", PHOTO], check=True)
        root.after(0, show_photo)
        print_photo()
    except Exception as e:
        print("Error:", e)
        root.after(0, lambda: say("Oops, try again"))
    time.sleep(4)                                # leave the photo on screen
    root.after(0, lambda: say("Press the button!"))
    busy = False

def countdown(n):
    if n > 0:
        say(str(n))
        root.after(1000, countdown, n - 1)
    else:
        say("Smile!")
        threading.Thread(target=worker, daemon=True).start()

def poll():
    global busy
    while not events.empty():
        events.get()
        if not busy:
            busy = True
            countdown(COUNTDOWN)
    root.after(100, poll)

button = Button(BUTTON_PIN, bounce_time=0.1)
button.when_pressed = lambda: events.put("press")   # thread-safe hand-off

poll()
root.mainloop()
