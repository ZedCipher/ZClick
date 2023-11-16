import threading
import pyautogui
import keyboard
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw

# Global variables
running = False
click_thread_running = True
click_interval = 50  # Interval in seconds
icon = None  # Global icon object

def create_image(color):
    if isinstance(color, tuple):
        fill_color = color
    else:
        fill_color = color

    image = Image.new('RGB', (64, 64), fill_color)
    d = ImageDraw.Draw(image)
    d.ellipse([0, 0, 64, 64], fill=fill_color)
    return image

def on_clicked(icon, item=None):
    global running
    running = not running

    if running:
        icon.icon = create_image((50, 205, 50))  # Lime green
    else:
        icon.icon = create_image('red')

def click_loop():
    global click_thread_running, click_interval
    counter = 0

    while click_thread_running:
        if running and counter >= click_interval:
            pyautogui.click()
            counter = 0
        else:
            counter += 1
            pyautogui.sleep(1)

def quit_program(icon, item):
    global click_thread_running
    click_thread_running = False
    icon.stop()

def setup(icon):
    icon.visible = True

def run_icon():
    global icon
    menu = pystray.Menu(item('Start/Stop', on_clicked),
                        item('Quit', quit_program))
    icon = pystray.Icon("test_icon", create_image('red'), "Clicker", menu=menu)
    icon.run(setup)

if __name__ == "__main__":
    click_thread = threading.Thread(target=click_loop)
    click_thread.start()

    icon_thread = threading.Thread(target=run_icon)
    icon_thread.start()

    def hotkey_action():
        global icon
        keyboard.add_hotkey('F6', lambda: on_clicked(icon))

    keyboard_thread = threading.Thread(target=hotkey_action)
    keyboard_thread.start()

    try:
        while True:
            pyautogui.sleep(10)
    except KeyboardInterrupt:
        click_thread_running = False
        if icon:
            icon.stop()
