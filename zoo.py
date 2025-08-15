# zoo.py
# Simple window setup with transparent pet on bed
import tkinter as tk
from pet import Pet
from pet_states.idle import IdleAnimation
from dotenv import load_dotenv
import os
import multiprocessing


# Load environment variables from .env file
load_dotenv()

PURCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
CUSTOM_KEYWORD_PATH = [os.getenv("KEYWORD_PATH")]


def main():
    # On Windows, multiprocessing-based libraries need freeze_support when
    # starting worker processes from spawned interpreters.
    multiprocessing.freeze_support()

    # Create main root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Bed window (use Toplevel)
    bed_window = tk.Toplevel(root)
    bed_window.config(bg="#7F007F")
    bed_window.attributes("-topmost", True)
    bed_window.overrideredirect(True)
    bed_window.wm_attributes("-transparentcolor", "#7F007F")
    bed_canvas = tk.Canvas(
        bed_window, width=100, height=100, bg="#7F007F", highlightthickness=0
    )
    bed_canvas.pack(fill="both", expand=True)

    bed_image = tk.PhotoImage(
        file="D:\\Dokumentumok\\SCHOOL\\IT_PROJECTS\\pets\\assets\\images\\bed.gif"
    )
    bed_item = bed_canvas.create_image(0, 0, image=bed_image, anchor="nw")

    # ball window
    ball_window = tk.Toplevel(root)
    ball_window.config(bg="#7F007F")
    ball_window.attributes("-topmost", True)
    ball_window.overrideredirect(True)
    ball_window.wm_attributes("-transparentcolor", "#7F007F")
    ball_canvas = tk.Canvas(
        ball_window, width=100, height=100, bg="#7F007F", highlightthickness=0
    )
    ball_canvas.pack(fill="both", expand=True)

    ball_image = tk.PhotoImage(
        file="D:\\Dokumentumok\\SCHOOL\\IT_PROJECTS\\pets\\assets\\images\\ball.gif"
    )
    ball_canvas.create_image(0, 0, image=ball_image, anchor="nw")

    ball_canvas.pack(fill="both", expand=True)

    ball_image = tk.PhotoImage(
        file="D:\\Dokumentumok\\SCHOOL\\IT_PROJECTS\\pets\\assets\\images\\ball.gif"
    )
    ball_canvas.create_image(0, 0, image=ball_image, anchor="nw")

    # Pet window (use Toplevel)
    pet_window = tk.Toplevel(root)
    pet_window.config(bg="#7F007F")
    pet_window.attributes("-topmost", True)
    pet_window.overrideredirect(True)
    pet_window.wm_attributes("-transparentcolor", "#7F007F")
    pet_canvas = tk.Canvas(
        pet_window, width=100, height=100, bg="#7F007F", highlightthickness=0
    )
    pet_canvas.pack(fill="both", expand=True)

    # Message window (use Toplevel)
    message_window = tk.Toplevel(root)
    message_window.overrideredirect(True)
    message_window.config(bg="#7F007F")
    message_window.attributes("-topmost", True)
    message_window.wm_attributes(
        "-transparentcolor", "#7F007F"
    )  # A better transparent color for the message
    speech_label = tk.Label(
        message_window,
        bg="white",
        fg="black",
        font=("Arial", 12),
        relief="solid",
        borderwidth=1,
    )
    speech_label.pack(fill="both", expand=True)
    message_window.withdraw()  # Initially hide the message window

    # Create the pet object
    pet = Pet(
        starting_state=IdleAnimation,  # Pass the class, not instance
        pet_window=pet_window,
        pet_canvas=pet_canvas,
        bed_window=bed_window,
        bed_canvas=bed_canvas,
        ball_window=ball_window,
        ball_canvas=ball_canvas,
        message_window=message_window,
        speech_label=speech_label,  # ADDED: Pass the speech label to the Pet object
        frequency=0.1,
        x=1400,
        y=150,
        access_key=PURCUPINE_ACCESS_KEY,  # Pass the access key
        custom_keyword_paths=CUSTOM_KEYWORD_PATH,  # Pass the custom keyword paths
    )

    pet.bind_drag_events()

    # Ensure the pet window has the close binding as well, for consistency
    pet_window.bind("<Control-p>", pet.close_program)
    bed_window.bind("<Control-p>", pet.close_program)
    ball_window.bind("<Control-p>", pet.close_program)

    # Close the application properly when windows are closed
    def on_closing():
        pet.close_program()
        root.destroy()

    bed_window.protocol("WM_DELETE_WINDOW", on_closing)
    pet_window.protocol("WM_DELETE_WINDOW", on_closing)
    message_window.protocol("WM_DELETE_WINDOW", on_closing)
    ball_window.protocol("WM_DELETE_WINDOW", on_closing)

    # root.bed_image = bed_image

    pet.update_pet()
    # pet_window.after(1, pet.update_pet)

    # Start the main Tkinter event loop on the root window
    root.mainloop()


if __name__ == "__main__":
    main()
