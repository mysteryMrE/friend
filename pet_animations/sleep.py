from pet_animation import PetAnimation


class SleepAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="sleep.gif",
            resource_length=3,
            animation_speed=0.3,
            animation_repeat=2,
        )
