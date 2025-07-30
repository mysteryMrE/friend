from pet_animation import PetAnimation


class WalkLeftAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=-3,
            speed_y=0,
            gif_name="walking_left",
            gif_length=8,
            animation_speed=1,
            animation_repeat=3,
        )
