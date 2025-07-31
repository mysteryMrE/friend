# window setup (mostly the same)
from pet import Pet
import tkinter as tk
from pet_animations.idle import IdleAnimation
from pet_animations.talk import TalkAnimation


window = tk.Tk()

# Use a Canvas for the speech bubble to allow drawing custom shapes
speech_bubble_canvas = tk.Canvas(
    window, width=300, height=100, bg="black", highlightthickness=0
)

# Create the pet object, passing necessary Tkinter elements
label = tk.Label(window, bd=0, bg="black")
pet = Pet(
    starting_state=IdleAnimation,
    window=window,
    label=label,
    message_label=speech_bubble_canvas,
    frequency=0.1,
    x=1400,
    y=150,
)

window.config(highlightbackground="black")
label.bind("<Control-Button-1>", pet.start_drag)
label.bind("<Control-B1-Motion>", pet.do_drag)
window.bind("<Control-p>", pet.close_program)
window.attributes("-topmost", True)
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "black")
label.place(x=150, y=150)  # Center the 100x100 cat image in the 400x400 window
speech_bubble_canvas.place(x=200, y=40, anchor="n")  # Position canvas above the cat


# Initial call to start the pet's behavior
pet.update_pet()  # Start the main loop via the pet object
window.mainloop()
