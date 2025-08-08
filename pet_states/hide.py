from pet_animation import PetAnimation


class HideAnimation(PetAnimation):
    def __init__(self, pet):
        gif_name = (
            "walking_left_transparent.gif"
            if pet.x < 900
            else "walking_right_transparent.gif"
        )
        super().__init__(
            speed_x=-3 if pet.x < 900 else 3,
            speed_y=-3 if pet.y < 300 else 3,
            resource_name=gif_name,
            resource_length=8,
            animation_speed=1,
            animation_repeat=3,
        )
        self.pet = pet

    def is_finished(self):
        return (
            self.pet.x < -100
            or self.pet.y < -100
            or self.pet.x > 2000
            or self.pet.y > 2000
        )

    def get_movement_delta(self):
        if self.pet.x < 900 and self.speed_x > 0:
            self.resource_name = "walking_left_transparent.gif"
            self.frames = self.make_frames()
            self.speed_x = -3
        elif self.pet.x >= 900 and self.speed_x < 0:
            self.resource_name = "walking_right_transparent.gif"
            self.frames = self.make_frames()
            self.speed_x = 3
        if self.pet.y < 400:
            self.speed_y = -3
        else:
            self.speed_y = 3
        return super().get_movement_delta()
