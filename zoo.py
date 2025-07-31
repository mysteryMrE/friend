# window setup (mostly the same)
from pet import Pet
import tkinter as tk

window = tk.Tk()


# Create the pet object, passing necessary Tkinter elements
label = tk.Label(window, bd=0, bg="black")
pet = Pet(window, label, frequency=0.1, x=1400, y=150)

window.config(highlightbackground="black")
label.bind("<Control-Button-1>", pet.start_drag)
label.bind("<Control-B1-Motion>", pet.do_drag)
window.bind("<Control-p>", pet.close_program)
window.attributes("-topmost", True)
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "black")
label.pack()

# Initial call to start the pet's behavior
pet.update_pet()  # Start the main loop via the pet object
window.mainloop()
