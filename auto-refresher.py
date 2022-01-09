import sys
import time

from pynput.keyboard import Key, Controller, Listener, KeyCode

running = True
refreshing = False

if len(sys.argv) > 1:
    interval = float(sys.argv[1])
else:
    interval = 2

def on_press(key):

    global running
    global refreshing
    
    if key == Key.print_screen:
        if refreshing:
            refreshing = False
            print("Pausing auto-refresh")
        else:
            refreshing = True
            print("Starting auto-refresh")
    elif key == Key.scroll_lock:
        listener.stop()
        running = False
        refreshing = False
        print("Exiting program (this may take", interval, "seconds)")
        
        # The exit() function is used as a place holder to halt the program immediately when Scroll Lock is pressed.
        exit()

keyboard = Controller()

listener = Listener(on_press=on_press)
listener.start()

while running:
    if refreshing:
        keyboard.press(Key.f5)
        keyboard.release(Key.f5)
    time.sleep(interval)