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
        # Preload both directions into separate, independent lists
        self.left_bound_frames = self._load_frames("walking_left_transparent.gif")
        self.right_bound_frames = self._load_frames("walking_right_transparent.gif")
        # Set current frames based on start position
        self.frames = self.left_bound_frames if pet.x < 900 else self.right_bound_frames

    def _load_frames(self, resource_name: str):
        # Temporarily load frames for the given resource into a new list
        prev = self.resource_name
        self.resource_name = resource_name
        frames = list(self.make_frames())  # copy so lists don’t alias self.frames
        self.resource_name = prev
        return frames

    def is_finished(self):
        return (
            self.pet.x < -100
            or self.pet.y < -100
            or self.pet.x > 2000
            or self.pet.y > 1060
        )

    def get_movement_delta(self):
        self.calculate_delta()
        return super().get_movement_delta()

    def adjust_frames(self):
        new_frames = (
            self.left_bound_frames if self.pet.x < 900 else self.right_bound_frames
        )
        if self.frames is not new_frames:  # switch only if different list
            self.frames = new_frames
            self.cycle = 0
            self.resource_name = (
                "walking_left_transparent.gif"
                if self.pet.x < 900
                else "walking_right_transparent.gif"
            )
            print(f"Adjusting frames: {self.resource_name} (Pet X: {self.pet.x})")

    def calculate_delta(self):
        if self.pet.x < 900 and self.speed_x > 0:
            self.speed_x = -3
        elif self.pet.x >= 900 and self.speed_x < 0:
            self.speed_x = 3
        if self.pet.y < 400:
            self.speed_y = -3
        else:
            self.speed_y = 3
        self.adjust_frames()
