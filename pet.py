import tkinter as tk
import random
from pet_animations.idle import IdleAnimation
from pet_animations.idle_to_sleep import IdleToSleepAnimation
from pet_animations.sleep import SleepAnimation
from pet_animations.sleep_to_idle import SleepToIdleAnimation
from pet_animations.walk_left import WalkLeftAnimation
from pet_animations.walk_right import WalkRightAnimation


class Pet:
    def __init__(self, window, label, frequency, x, y):
        self.window = window
        self.label = label

        self.animation_order = {
            IdleAnimation: {
                "nexts": {
                    WalkLeftAnimation: 0.4,
                    WalkRightAnimation: 0.4,
                    IdleToSleepAnimation: 0.2,
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
        self.set_state(IdleAnimation(), called_from="__init__")  # Set initial state

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

        frame, finished_animation = self._current_state.update_animation()

        # Get movement delta from the current state
        delta_x, delta_y = self._current_state.get_movement_delta()
        self.x += delta_x
        self.y += delta_y

        # Update window geometry and label image
        self.window.geometry(f"100x100+{int(self.x)}+{int(self.y)}")
        self.label.configure(image=frame)
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

    def close_program(self, event=None):
        self.window.destroy()
