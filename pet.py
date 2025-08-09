# pet.py
import threading
import tkinter as tk
import random
from hot import Hot
from pet_states.hide import HideAnimation
from pet_states.idle import IdleAnimation
from pet_states.idle_to_sleep import IdleToSleepAnimation
from pet_states.sleep import SleepAnimation
from pet_states.sleep_to_idle import SleepToIdleAnimation
from pet_states.talk import TalkAnimation
from pet_states.walk_left import WalkLeftAnimation
from pet_states.walk_right import WalkRightAnimation
from pet_states.listen import ListenAnimation
from pet_animation import PetAnimation
from animation_factory import AnimationFactory
from pet_states.lie_down import LieDownAnimation


class Pet:
    def __init__(
        self,
        starting_state: PetAnimation,
        pet_window,
        pet_canvas,
        bed_window,
        bed_canvas,
        message_window,
        speech_label,  # ADDED: Speech label is now a parameter
        frequency: int,
        x: int,
        y: int,
        access_key: str = None,
        custom_keyword_paths: list = None,
    ):
        self.starting_state = starting_state
        self.pet_window = pet_window
        self.pet_canvas = pet_canvas
        self.bed_window = bed_window
        self.bed_canvas = bed_canvas
        self.message_window = message_window
        self.speech_label = speech_label  # ADDED: Store the speech label
        self.pet_item = None
        self.current_pet_image = None
        self.bed_item = None
        self.first_run = True  # Flag to manage initial setup
        # TODO: screenshot, something wrong with the factory, talking sometimes is bad, usually if i move the pet??,
        self.animation_order = {
            LieDownAnimation: {"nexts": {IdleToSleepAnimation: 1}},
            HideAnimation: {"nexts": {IdleAnimation: 1}},
            ListenAnimation: {"nexts": {IdleAnimation: 100.0}},
            TalkAnimation: {"nexts": {IdleAnimation: 0.8, TalkAnimation: 0.2}},
            IdleAnimation: {
                "nexts": {
                    WalkLeftAnimation: 0.3,
                    WalkRightAnimation: 0.3,
                    IdleToSleepAnimation: 0.2,
                    TalkAnimation: 0.2,
                    HideAnimation: 0.1,  # Added HideAnimation
                    LieDownAnimation: 0.1,  # Added LieDownAnimation
                }
            },  # Corrected weights
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

        self.start_drag_x = 0
        self.start_drag_y = 0
        self.current_drag_window = None
        AnimationFactory.set_pet(self)
        self.frequency = frequency
        self._updating = False  # Flag to prevent recursive updates
        AnimationFactory.setup_listen()
        self.wait_for_callback = threading.Event()
        self.hot = Hot(
            mic_index=1,
            access_key=access_key,  # Access key can be set later if needed
            flag=self.wait_for_callback,
            custom_keyword_paths=custom_keyword_paths,
        )
        self.hot.start_listening()

    def set_state(self, new_state, called_from=None):
        print(
            f"Transitioning from {type(self._current_state).__name__} to {type(new_state).__name__} (state change called from {called_from})"
        )

        if hasattr(self._current_state, "cleanup"):
            print(f"Calling cleanup on {type(self._current_state).__name__}")
            self._current_state.cleanup()

        self._current_state = new_state

        if self._current_state:
            first_frame = self._current_state.update_animation()[0]
            self.current_pet_image = first_frame
            if self.pet_item:
                self.pet_canvas.itemconfig(self.pet_item, image=self.current_pet_image)
            else:
                self.pet_item = self.pet_canvas.create_image(
                    0, 0, image=self.current_pet_image, anchor="nw"
                )
            self.pet_canvas.update_idletasks()
            self.pet_window.update_idletasks()

    def update_pet(self):

        if self.wait_for_callback.is_set():
            self.listen_up()

        if self._updating:
            print("Warning: update_pet called while already updating, skipping...")
            return

        self._updating = True

        try:
            if self.first_run:
                initial_state = AnimationFactory.get_animation(self.starting_state)
                self.set_state(initial_state, called_from="first_update")
                self.first_run = False

            frame, finished_animation, message = self._current_state.update_animation()
            self.current_pet_image = frame

            delta_x, delta_y = self._current_state.get_movement_delta()
            self.x += delta_x
            self.y += delta_y

            self.pet_window.geometry(f"100x100+{int(self.x)}+{int(self.y)}")

            if self.pet_item:
                self.pet_canvas.itemconfig(self.pet_item, image=self.current_pet_image)
                self.pet_canvas.update_idletasks()

            if message:
                self.message_window.deiconify()
                self.speech_label.configure(
                    text=message
                )  # Corrected to use the stored label
                message_x = self.pet_window.winfo_x() + 50
                message_y = self.pet_window.winfo_y() - 50
                self.message_window.geometry(f"+{message_x}+{message_y}")
            else:
                self.message_window.withdraw()

            # print(
            #     f"Update: X: {int(self.x)}, Y: {int(self.y)} (State: {type(self._current_state).__name__}))"
            # )
            # TODO: what is pet_item
            # Periodic cleanup of old image reference

            if finished_animation:
                prev_anim_name = type(self._current_state).__name__
                new_animation_pool = self.animation_order[type(self._current_state)][
                    "nexts"
                ]
                animations = list(new_animation_pool.keys())
                weights = list(new_animation_pool.values())
                new_state_class = random.choices(animations, weights=weights, k=1)[0]
                new_state = AnimationFactory.get_animation(new_state_class)
                print(f"new state: {type(new_state)} and {new_state}")
                self.set_state(new_state, called_from="update_pet")
                if prev_anim_name == "ListenAnimation":
                    self.wait_for_callback.clear()

        except Exception as e:
            print(f"Error in update_pet: {e}")
        finally:
            self._updating = False
            # Schedule next update
            self.pet_window.after(100, self.update_pet)

    def bind_drag_events(self):
        self.bed_canvas.bind("<Button-1>", self.start_drag_bed)
        self.bed_canvas.bind("<B1-Motion>", self.do_drag_bed)
        self.pet_canvas.bind("<Button-1>", self.start_drag_pet)
        self.pet_canvas.bind("<B1-Motion>", self.do_drag_pet)
        self.pet_canvas.bind("<Button-3>", self.listen_up)
        self.bed_canvas.bind("<Double-Button-1>", self.tp)

    def maintain_stacking_order(self):
        """Keep pet above bed, both above other apps"""
        try:
            self.pet_window.lift(self.bed_window)
        except:
            pass

    def tp(self, event):
        """Teleport pet to bed location when double-clicking on bed"""
        print("Teleporting pet to bed")

        # Get bed window position (where the bed is)
        bed_x = self.bed_window.winfo_x()
        bed_y = self.bed_window.winfo_y()

        # Update pet's internal coordinates to match bed position
        self.x = bed_x
        self.y = bed_y - 20

        # Move pet window to bed location immediately
        self.pet_window.geometry(f"100x100+{int(self.x)}+{int(self.y)}")
        print(f"Pet teleported to bed at ({self.x}, {self.y})")

        self.pet_window.after(1, self.maintain_stacking_order)
        # Force update the display
        self.pet_window.update_idletasks()

    def okay_to_listen(self):
        if self._current_state and (
            isinstance(self._current_state, ListenAnimation)
            or isinstance(self._current_state, TalkAnimation)
        ):
            print("Already listening or talking, ignoring listen_up event")
            if isinstance(self._current_state, TalkAnimation):
                self.wait_for_callback.clear()
            return False
        return True

    def listen_up(self):
        if not self.okay_to_listen():
            return

        self.set_state(
            AnimationFactory.get_animation(ListenAnimation), called_from="listen_up"
        )
        print("Pet is now in listening state...")

    def start_drag_bed(self, event):
        self.start_drag_x = event.x
        self.start_drag_y = event.y
        self.current_drag_window = self.bed_window

    def do_drag_bed(self, event):
        if self.current_drag_window:
            new_x = self.current_drag_window.winfo_x() + (event.x - self.start_drag_x)
            new_y = self.current_drag_window.winfo_y() + (event.y - self.start_drag_y)
            self.current_drag_window.geometry(f"+{new_x}+{new_y}")

    def start_drag_pet(self, event):
        self.start_drag_x = event.x
        self.start_drag_y = event.y
        self.current_drag_window = self.pet_window

    def do_drag_pet(self, event):
        if self.current_drag_window:
            new_x = self.current_drag_window.winfo_x() + (event.x - self.start_drag_x)
            new_y = self.current_drag_window.winfo_y() + (event.y - self.start_drag_y)
            self.current_drag_window.geometry(f"+{new_x}+{new_y}")
            self.x = new_x
            self.y = new_y

    def close_program(self, event=None):
        # Clean up image references
        # Clear animation factory instances
        AnimationFactory.clear_instances()
        # Just destroy the windows, let the main window handle the rest
        try:
            self.pet_window.destroy()
        except:
            pass
        try:
            self.bed_window.destroy()
        except:
            pass
        try:
            self.message_window.destroy()
        except:
            pass
