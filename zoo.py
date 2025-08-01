# Simple window setup with transparent pet on bed
from pet import Pet
import tkinter as tk
from pet_animations.idle import IdleAnimation

window = tk.Tk()

# Create transparent background window
window.config(bg="#7F007F")
window.attributes("-topmost", True)
window.overrideredirect(True)
window.wm_attributes("-transparentcolor", "#7F007F")  # Make purple transparent

# Create main canvas that will hold both bed and cat
main_canvas = tk.Canvas(
    window, width=300, height=250, bg="#7F007F", highlightthickness=0
)

# Create speech bubble label (separate from canvas for easier text handling)
speech_label = tk.Label(
    window, bg="white", fg="black", font=("Arial", 12), relief="solid", borderwidth=1
)

# Load bed image
bed_image = tk.PhotoImage(
    file="D:\\Dokumentumok\\SCHOOL\\pets\\assets\\images\\bed.gif"
)

# Draw bed on canvas (this will be the background layer)
bed_item = main_canvas.create_image(0, 20, image=bed_image, anchor="nw")

# Create the pet object
pet = Pet(
    starting_state=IdleAnimation,
    window=window,
    label=main_canvas,  # Pass canvas for drawing pet
    message_label=speech_label,
    bed_label=None,  # No longer needed, bed is on canvas
    frequency=0.1,
    x=1400,
    y=150,
)

# Position the canvas and speech label
main_canvas.place(x=0, y=0)
# speech_label will be positioned dynamically when there's a message

# Bind drag events to canvas
main_canvas.bind("<Control-Button-1>", pet.start_drag)
main_canvas.bind("<Control-B1-Motion>", pet.do_drag)
window.bind("<Control-p>", pet.close_program)

# Keep reference to prevent garbage collection
window.bed_image = bed_image
main_canvas.bed_image = bed_image  # Also keep reference on canvas

# Initial call to start the pet's behavior
pet.update_pet()  # Start the main loop via the pet object
window.mainloop()
