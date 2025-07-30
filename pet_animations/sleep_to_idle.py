# from pet_animations import PetState


# class SleepToIdleState(PetState):
#     def handle_event(self, event_number):
#         if event_number in self._pet.idle_events:
#             from pet_animations.idle import IdleState

#             self._pet.set_state(
#                 IdleState(self._pet), called_from="SleepToIdleState.handle_event"
#             )
#         # Stays in sleep for other sleep_num events
#         pass

#     def update_animation(self, cycle):
#         return self._pet.gif_work_wrapper(cycle, self._pet.sleep_to_idle_frames, 1, 4)
