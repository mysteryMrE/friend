import pyautogui
import random
import tkinter as tk

msg = "Hello Cat!"
print(msg)

# Global variables for cat's position
# These will now be the single source of truth for the cat's coordinates.
x = 1400  # Initial X position
y = 150  # Initial Y position

cycle = 0
check = 1
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
event_number = random.randrange(1, 3, 1)
impath = "D:\\Dokumentumok\\SCHOOL\\pets\\"

# Variables to store mouse click position for dragging
start_drag_x = 0
start_drag_y = 0


# transfer random no. to event
# Now, `event` does not need to pass `x` or `y` because `update` will use global `x` and `y`.
def event(cycle, check, event_number):
    if event_number in idle_num:
        check = 0
        print("idle")
        window.after(400, update, cycle, check, event_number)
    elif event_number == 5:
        check = 1
        print("from idle to sleep")
        window.after(100, update, cycle, check, event_number)
    elif event_number in walk_left:
        check = 4
        print("walking towards left")
        window.after(100, update, cycle, check, event_number)
    elif event_number in walk_right:
        check = 5
        print("walking towards right")
        window.after(100, update, cycle, check, event_number)
    elif event_number in sleep_num:
        check = 2
        print("sleep")
        window.after(1000, update, cycle, check, event_number)
    elif event_number == 14:
        check = 3
        print("from sleep to idle")
        window.after(100, update, cycle, check, event_number)


# making gif work
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number


# `update` now uses global `x` and `y` for position
def update(cycle, check, event_number):
    global x, y  # Declare x and y as global so we can modify them directly

    # Get the current animation frame
    frame = None
    if check == 0:  # idle
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)
    elif check == 1:  # idle to sleep
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, 10, 10)
    elif check == 2:  # sleep
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
    elif check == 3:  # sleep to idle
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, 1, 1)
    elif check == 4:  # walk toward left
        frame = walk_positive[cycle]
        cycle, event_number = gif_work(cycle, walk_positive, event_number, 1, 9)
        x -= 3  # Modify global x for walking
    elif check == 5:  # walk towards right
        frame = walk_negative[cycle]
        cycle, event_number = gif_work(cycle, walk_negative, event_number, 1, 9)
        x += 3  # Modify global x for walking (corrected from x -=-3)

    # Ensure x and y are integers before applying to geometry
    x_int = int(x)
    y_int = int(y)

    # Use global x and y to set window position
    window.geometry(f"100x100+{x_int}+{y_int}")
    label.configure(image=frame)
    # Debug print: See what coordinates update is applying
    print(
        f"Update: Applying X: {x_int}, Y: {y_int} (check: {check}, event_number: {event_number})"
    )

    # Recursively call event, passing current state but not position
    window.after(1, event, cycle, check, event_number)


# Function to close the program
def close_program(event=None):
    window.destroy()


# Functions for dragging
def start_drag(event):
    global start_drag_x, start_drag_y
    # Store initial mouse position relative to the window
    start_drag_x = event.x
    start_drag_y = event.y


def do_drag(event):
    global x, y  # Need to modify global x and y

    # Calculate new absolute position of the window
    # window.winfo_x() and window.winfo_y() give the current window position on screen
    new_x = window.winfo_x() + (event.x - start_drag_x)
    new_y = window.winfo_y() + (event.y - start_drag_y)

    # Update global x and y with the new position (cast to int immediately)
    x = int(new_x)
    y = int(new_y)

    # Set the window geometry immediately during drag
    window.geometry(f"+{x}+{y}")
    # Debug print: See what coordinates do_drag is setting
    print(f"Drag: Setting X: {x}, Y: {y}")


window = tk.Tk()
# call buddy's action gif
idle = [
    tk.PhotoImage(file=impath + "idle.gif", format="gif -index %i" % (i))
    for i in range(5)
]  # idle gif
idle_to_sleep = [
    tk.PhotoImage(file=impath + "idle_to_sleep.gif", format="gif -index %i" % (i))
    for i in range(8)
]  # idle to sleep gif
sleep = [
    tk.PhotoImage(file=impath + "sleep.gif", format="gif -index %i" % (i))
    for i in range(3)
]  # sleep gif
sleep_to_idle = [
    tk.PhotoImage(file=impath + "sleep_to_idle.gif", format="gif -index %i" % (i))
    for i in range(8)
]  # sleep to idle gif
walk_positive = [
    tk.PhotoImage(file=impath + "walking_positive.gif", format="gif -index %i" % (i))
    for i in range(8)
]  # walk to left gif
walk_negative = [
    tk.PhotoImage(file=impath + "walking_negative.gif", format="gif -index %i" % (i))
    for i in range(8)
]  # walk to right gif

# window configuration
window.config(highlightbackground="black")
label = tk.Label(window, bd=0, bg="black")

# Bind Ctrl+P to close the program
window.bind("<Control-p>", close_program)

# Bind mouse events for dragging
label.bind("<Button-1>", start_drag)  # Left mouse button press
label.bind("<B1-Motion>", do_drag)  # Mouse motion while left button is held down

# Make the window always on top
window.attributes("-topmost", True)

# Remove window decorations and set transparency
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "black")
label.pack()

# Initial call to update, it will then recursively call event and update.
window.after(1, update, cycle, check, event_number)
window.mainloop()
