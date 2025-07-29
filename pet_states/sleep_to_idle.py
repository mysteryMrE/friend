from pet_state import PetState


class SleepToIdleState(PetState):
    def handle_event(self, event_number):
        if event_number == 14:
            from pet_states.idle import IdleState

            self._pet.set_state(IdleState(self._pet))
        # Stays in sleep for other sleep_num events
        pass

    def update_animation(self, cycle):
        return self._pet.gif_work_wrapper(cycle, self._pet.sleep_to_idle_frames, 1, 9)
