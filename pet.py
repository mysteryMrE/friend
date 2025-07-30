import tkinter as tk
import random
from pet_animations.idle import IdleAnimation


class Pet:
    def __init__(self, window, label):
        self.window = window
        self.label = label

        # self.idle_to_sleep_
        # self.sleep_frames = [
        #     tk.PhotoImage(file=self.impath + "sleep.gif", format="gif -index %i" % (i))
        #     for i in range(3)
        #     for _ in range(4)
        # ] * 2
        # self.sleep_to_idle_frames = [
        #     tk.PhotoImage(
        #         file=self.impath + "sleep_to_idle.gif", format="gif -index %i" % (i)
        #     )
        #     for i in range(8)
        # ]

        # self.walk_left_frames = [
        #     tk.PhotoImage(
        #         file=self.impath + "walking_left.gif", format="gif -index %i" % (i)
        #     )
        #     for i in range(8)
        # ] * 2
        # self.walk_right_frames = [
        #     tk.PhotoImage(
        #         file=self.impath + "walking_right.gif", format="gif -index %i" % (i)
        #     )
        #     for i in range(8)
        # ] * 2

        # Define the event numbers associated with actions (can be properties or constants)
        self.idle_events = [1, 2, 3, 4]
        self.sleep_events = [10, 11, 12, 13, 15]
        self.walk_left_events = [6, 7]
        self.walk_right_events = [8, 9]

        self._current_state = None
        self.set_state(IdleAnimation(), called_from="__init__")  # Set initial state

        self.x = 1400  # Global x/y now belongs to the pet object
        self.y = 150
        self.event_number = random.randrange(1, 3, 1)  # Initial random event

        # Store mouse click position for dragging
        self.start_drag_x = 0
        self.start_drag_y = 0

    def set_state(self, new_state, called_from=None):
        print(
            f"Transitioning from {type(self._current_state).__name__} to {type(new_state).__name__} (state change called from {called_from})"
        )
        self._current_state = new_state

    def update_pet(self):
        # The main loop, less concerned with *how* to update, more with *what* to update

        # The state itself will decide if and how to transition
        frame, finished_animation = self._current_state.update_animation()

        if finished_animation:
            # json or enum
            # to be implemented
            pass

        # Get movement delta from the current state
        delta_x, delta_y = self._current_state.get_movement_delta()
        self.x += delta_x
        self.y += delta_y

        # Update window geometry and label image
        self.window.geometry(f"100x100+{int(self.x)}+{int(self.y)}")
        self.label.configure(image=frame)
        print(
            f"Update: X: {int(self.x)}, Y: {int(self.y)} (State: {type(self._current_state).__name__}, Event: {self.event_number})"
        )

        # Now, handle the next event based on the new event_number

        # Schedule the next update
        self.window.after(100, self.update_pet)  # Schedule next update directly

    # Dragging functions (can remain mostly the same, just update self.x/self.y)
    def start_drag(self, event):
        self.start_drag_x = event.x
        self.start_drag_y = event.y

    def do_drag(self, event):
        new_x = self.window.winfo_x() + (event.x - self.start_drag_x)
        new_y = self.window.winfo_y() + (event.y - self.start_drag_y)
        self.x = int(new_x)
        self.y = int(new_y)
        self.window.geometry(f"+{self.x}+{self.y}")
        print(f"Drag: Setting X: {self.x}, Y: {self.y}")

    def close_program(self, event=None):
        self.window.destroy()
