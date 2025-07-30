# from pet_animations import PetState


# class SleepState(PetState):
#     def handle_event(self, event_number):
#         if event_number == 14:
#             from pet_animations.sleep_to_idle import SleepToIdleState

#             self._pet.set_state(
#                 SleepToIdleState(self._pet), called_from="SleepState.handle_event"
#             )
#         # Stays in sleep for other sleep_num events
#         pass

#     def update_animation(self, cycle):
#         return self._pet.gif_work_wrapper(cycle, self._pet.sleep_frames, 10, 15)

#     def get_movement_delta(self):
#         return 0, 0
