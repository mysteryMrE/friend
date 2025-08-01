import tkinter as tk
import random
from pet_animations.idle import IdleAnimation
from pet_animations.idle_to_sleep import IdleToSleepAnimation
from pet_animations.sleep import SleepAnimation
from pet_animations.sleep_to_idle import SleepToIdleAnimation
from pet_animations.talk import TalkAnimation
from pet_animations.walk_left import WalkLeftAnimation
from pet_animations.walk_right import WalkRightAnimation
from pet_animation import PetAnimation


class Pet:
    def __init__(
        self,
        starting_state: PetAnimation,
        window,
        label,
        message_label,
        frequency: int,
        x: int,
        y: int,
    ):
        self.window = window
        self.label = label
        self.message_label = message_label
        self.animation_order = {
            TalkAnimation: {
                "nexts": {
                    IdleAnimation: 0.5,
                    TalkAnimation: 0.5,
                }
            },
            IdleAnimation: {
                "nexts": {
                    WalkLeftAnimation: 0.2,
                    WalkRightAnimation: 0.2,
                    IdleToSleepAnimation: 0.2,
                    TalkAnimation: 100,
                }
            },
            IdleToSleepAnimation: {"nexts": {SleepAnimation: 1}},
            SleepAnimation: {"nexts": {SleepToIdleAnimation: 1}},
            SleepToIdleAnimation: {"nexts": {IdleAnimation: 1}},
            WalkLeftAnimation: {
                "nexts": {
                    IdleAnimation: 0.3,
                    WalkLeftAnimation: 0.2,
                    WalkRightAnimation: 0.5,
                }
            },
            WalkRightAnimation: {
                "nexts": {
                    IdleAnimation: 0.2,
                    WalkLeftAnimation: 0.3,
                    WalkRightAnimation: 0.5,
                }
            },
        }

        self._current_state = None
        self.set_state(starting_state(), called_from="__init__")  # Set initial state

        self.x = x
        self.y = y

        # Store mouse click position for dragging
        self.start_drag_x = 0
        self.start_drag_y = 0

        self.frequency = frequency

    def set_state(self, new_state, called_from=None):
        print(
            f"Transitioning from {type(self._current_state).__name__} to {type(new_state).__name__} (state change called from {called_from})"
        )

        # Clean up previous state if it has cleanup method
        if hasattr(self._current_state, "cleanup"):
            print(f"Calling cleanup on {type(self._current_state).__name__}")
            self._current_state.cleanup()

        self._current_state = new_state

        if self._current_state:
            first_frame = self._current_state.update_animation()[0]
            self.label.configure(image=first_frame)
            # Force an immediate update to prevent flickering
            self.label.update_idletasks()

    def update_pet(self):
        if not self._current_state:
            self.window.after(100, self.update_pet)
            return

        frame, finished_animation, message = self._current_state.update_animation()

        # Get movement delta from the current state
        delta_x, delta_y = self._current_state.get_movement_delta()
        self.x += delta_x
        self.y += delta_y

        # Update window geometry and label image
        self.window.config(bg="#7F007F")
        self.window.geometry(f"400x400+{int(self.x)}+{int(self.y)}")
        self.label.configure(image=frame)

        # Clear previous drawings and update the speech bubble
        self.message_label.delete("all")
        if message:
            # Create the speech bubble rectangle
            self.message_label.create_rectangle(
                10, 10, 290, 80, fill="white", outline="black", width=2
            )
            # Create the triangle pointing down
            self.message_label.create_polygon(
                140, 80, 160, 80, 150, 95, fill="white", outline="black", width=2
            )
            # Add the text to the canvas
            self.message_label.create_text(
                150, 45, text=message, font=("Arial", 12), fill="black", width=270
            )
        # if message == "":
        #     print("No message to display")

        #     # self.message_label.pack_forget()
        # else:

        #     #self.message_label.pack()
        print(
            f"Update: X: {int(self.x)}, Y: {int(self.y)} (State: {type(self._current_state).__name__}))"
        )

        # Now, handle the next event based on the new event_number

        if finished_animation:
            new_animation_pool = self.animation_order[type(self._current_state)][
                "nexts"
            ]
            animations = list(new_animation_pool.keys())
            weights = list(new_animation_pool.values())
            new_state = random.choices(animations, weights=weights, k=1)[0]
            print(f"new state: {type(new_state)} and {new_state}")
            self.set_state(new_state(), called_from="update_pet")

            # def transition_to_next():
            #     self.set_state(new_state(), called_from="delayed_transition")
            #     # TODO: THIS NEEDS TO BE HERE OR IT WILL FLICKER BUT WHYYYY??? ITS ALSO OK IF I DO THE SET_STATE CODE
            #     self.update_pet()
            # self.window.after(100, transition_to_next)
            # return  # Don't schedule regular update, transition will handle it

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

    # def _create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
    #     """Draw a rounded rectangle on a canvas."""
    #     # Draw the four corner arcs
    #     canvas.create_arc(
    #         x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, **kwargs
    #     )
    #     canvas.create_arc(
    #         x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, **kwargs
    #     )
    #     canvas.create_arc(
    #         x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, **kwargs
    #     )
    #     canvas.create_arc(
    #         x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, **kwargs
    #     )
    #     # Draw the four connecting lines
    #     canvas.create_line(x1 + radius, y1, x2 - radius, y1, **kwargs)
    #     canvas.create_line(x1 + radius, y2, x2 - radius, y2, **kwargs)
    #     canvas.create_line(x1, y1 + radius, x1, y2 - radius, **kwargs)
    #     canvas.create_line(x2, y1 + radius, x2, y2 - radius, **kwargs)
    #     # Draw the center rectangle to fill the color
    #     canvas.create_rectangle(
    #         x1 + radius, y1 + radius, x2 - radius, y2 - radius, **kwargs
    #     )

    def close_program(self, event=None):
        self.window.destroy()
