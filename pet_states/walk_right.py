from pet_state import PetState


class WalkRightState(PetState):
    def handle_event(self, event_number):
        if (
            event_number in self._pet.idle_events or event_number == 5
        ):  # Transition back to idle or idle-to-sleep
            from pet_states.idle import IdleState

            self._pet.set_state(
                IdleState(self._pet), called_from="WalkRightState.handle_event"
            )
        # Other conditions as needed
        pass

    def update_animation(self, cycle):
        # Using the correct GIF for right movement
        return self._pet.gif_work_wrapper(cycle, self._pet.walk_right_frames, 1, 9)

    def get_movement_delta(self):
        return 3, 0  # Move right
