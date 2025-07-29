from pet_state import PetState


class IdleState(PetState):
    def handle_event(self, event_number):
        if event_number == 5:
            from pet_states.idle_to_sleep import IdleToSleepState

            self._pet.set_state(IdleToSleepState(self._pet))
        elif (
            event_number in self._pet.walk_left_events
        ):  # Assuming these are defined in pet
            from pet_states.walk_left import WalkLeftState

            self._pet.set_state(WalkLeftState(self._pet))
        elif event_number in self._pet.walk_right_events:
            from pet_states.walk_right import WalkRightState

            self._pet.set_state(WalkRightState(self._pet))
        # No change needed for other idle_num events, stays in IdleState
        else:  # If event number is not handled, stay in current state (or default to idle)
            # This is where you might decide on fallback behavior
            pass

    def update_animation(self, cycle):
        # 'idle' is the list of frames for this state
        return self._pet.gif_work_wrapper(cycle, self._pet.idle_frames, 1, 9)
