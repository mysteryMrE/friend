from pet_animation import PetAnimation


class SleepToIdleAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            gif_name="sleep_to_idle",
            gif_length=8,
            animation_speed=1,
            animation_repeat=1,
        )
