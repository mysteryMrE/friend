from pet_animation import PetAnimation


class IdleToSleepAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            gif_name="idle_to_sleep",
            gif_length=8,
            animation_speed=1,
            animation_repeat=1,
        )
