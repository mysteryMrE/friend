# window setup (mostly the same)
from pet import Pet
import tkinter as tk
from pet_animations.idle import IdleAnimation
from pet_animations.talk import TalkAnimation


window = tk.Tk()

message_label = tk.Label(window, text="", bg="black", fg="white", font=("Arial", 10))
# Create the pet object, passing necessary Tkinter elements
label = tk.Label(window, bd=0, bg="black")
pet = Pet(
    starting_state=IdleAnimation,
    window=window,
    label=label,
    message_label=message_label,
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
message_label.pack()
label.pack()


# Initial call to start the pet's behavior
pet.update_pet()  # Start the main loop via the pet object
window.mainloop()
