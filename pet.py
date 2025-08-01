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
        bed_label,
        frequency: int,
        x: int,
        y: int,
    ):
        self.window = window
        self.label = label  # Main canvas for drawing pet and bed
        self.message_label = message_label  # Speech bubble label
        self.bed_label = bed_label  # Not used in canvas approach
        self.pet_item = None  # Will store canvas item ID for pet image
        self.animation_order = {
            TalkAnimation: {
                "nexts": {
                    IdleAnimation: 0.7,
                    TalkAnimation: 0.3,
                }
            },
            IdleAnimation: {
                "nexts": {
                    WalkLeftAnimation: 0.3,
                    WalkRightAnimation: 0.3,
                    IdleToSleepAnimation: 0.2,
                    TalkAnimation: 10.2,
                }
            },
            IdleToSleepAnimation: {"nexts": {SleepAnimation: 1}},
            SleepAnimation: {"nexts": {SleepToIdleAnimation: 0.3, SleepAnimation: 0.7}},
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
        self.x = x
        self.y = y
        self.set_state(starting_state(), called_from="__init__")  # Set initial state

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
            # Create or update pet image on canvas (will be drawn over bed)
            if self.pet_item:
                self.label.itemconfig(self.pet_item, image=first_frame)
            else:
                self.pet_item = self.label.create_image(
                    0, 0, image=first_frame, anchor="nw"
                )
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

        # Update window position
        self.window.geometry(f"300x250+{int(self.x)}+{int(self.y)}")

        # Update pet image on canvas (transparent cat over bed)
        if self.pet_item:
            self.label.itemconfig(self.pet_item, image=frame)

        # Update speech bubble
        if message:
            self.message_label.configure(text=message)
            self.message_label.place(x=50, y=10)  # Above the pet, within window bounds
        else:
            self.message_label.place_forget()  # Hide when no message

        print(
            f"Update: X: {int(self.x)}, Y: {int(self.y)} (State: {type(self._current_state).__name__}))"
        )

        # Handle state transitions
        if finished_animation:
            new_animation_pool = self.animation_order[type(self._current_state)][
                "nexts"
            ]
            animations = list(new_animation_pool.keys())
            weights = list(new_animation_pool.values())
            new_state = random.choices(animations, weights=weights, k=1)[0]
            print(f"new state: {type(new_state)} and {new_state}")
            self.set_state(new_state(), called_from="update_pet")

        self.window.after(
            100, self.update_pet
        )  # Schedule next update    # Dragging functions (can remain mostly the same, just update self.x/self.y)

    def start_drag(self, event):
        self.start_drag_x = event.x
        self.start_drag_y = event.y

    def do_drag(self, event):
        # Calculate new position based on drag
        new_x = self.window.winfo_x() + (event.x - self.start_drag_x)
        new_y = self.window.winfo_y() + (event.y - self.start_drag_y)
        self.x = int(new_x)
        self.y = int(new_y)

        # Update window position (this moves both cat and bed together)
        self.window.geometry(f"200x200+{self.x}+{self.y}")
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
