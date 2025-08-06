from pet_animation import PetAnimation


class IdleAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="idle_transparent.gif",
            resource_length=5,
            animation_speed=0.5,
            animation_repeat=4,
        )
