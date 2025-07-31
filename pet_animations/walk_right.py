from pet_animation import PetAnimation


class WalkRightAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=3,
            speed_y=0,
            resource_name="walking_right.gif",
            resource_length=8,
            animation_speed=1,
            animation_repeat=3,
        )
