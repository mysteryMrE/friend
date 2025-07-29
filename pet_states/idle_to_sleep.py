from pet_state import PetState


class IdleToSleepState(PetState):
    def handle_event(self, event_number):
        if event_number == 10:
            from pet_states.sleep import SleepState

            self._pet.set_state(SleepState(self._pet))
        pass

    def update_animation(self, cycle):
        return self._pet.gif_work_wrapper(cycle, self._pet.idle_to_sleep_frames, 10, 10)
