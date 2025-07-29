from abc import ABC, abstractmethod


class PetState(ABC):
    def __init__(self, pet):
        self._pet = pet  # A reference back to the main Pet object (Context)

    @abstractmethod
    def handle_event(self, event_number):
        # Determine the next state based on the event_number
        pass

    @abstractmethod
    def update_animation(self, cycle):
        # Return the current frame and update cycle/event_number for animation
        pass

    def get_movement_delta(self):
        # Return (delta_x, delta_y) for this state
        return 0, 0

    def get_first_last_event_range(self):
        # Default range for events after current animation loop
        return 1, 15  # A common range, can be overridden by specific states
