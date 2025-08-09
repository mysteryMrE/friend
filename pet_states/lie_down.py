from math import sqrt
from pet_animation import PetAnimation

window_width = 1920
window_height = 1080


class LieDownAnimation(PetAnimation):
    def __init__(self, pet):
        gif_name = (
            "walking_right_transparent.gif"
            if pet.x < pet.bed_window.winfo_x()
            else "walking_left_transparent.gif"
        )
        super().__init__(
            speed_x=3 if pet.x < pet.bed_window.winfo_x() else -3,
            speed_y=3 if pet.y < pet.bed_window.winfo_y() else -3,
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
        self.frames = (
            self.left_bound_frames
            if pet.x > self.pet.bed_window.winfo_x()
            else self.right_bound_frames
        )

    def _load_frames(self, resource_name: str):
        # Temporarily load frames for the given resource into a new list
        prev = self.resource_name
        self.resource_name = resource_name
        frames = list(self.make_frames())  # copy so lists don’t alias self.frames
        self.resource_name = prev
        return frames

    def is_finished(self):
        bed_x = self.pet.bed_window.winfo_x()
        bed_y = self.pet.bed_window.winfo_y()
        return self.pet.x == bed_x and self.pet.y == bed_y - 20

    def get_movement_delta(self):
        self.calculate_delta()
        return super().get_movement_delta()

    def adjust_frames(self, called_from=""):
        new_frames = (
            self.left_bound_frames
            if self.pet.x > self.pet.bed_window.winfo_x()
            else (
                self.right_bound_frames
                if self.pet.x < self.pet.bed_window.winfo_x()
                else None
            )
        )
        if (
            new_frames is not None and self.frames is not new_frames
        ):  # switch only if different list
            self.frames = new_frames
            self.cycle = 0
            self.resource_name = (
                "walking_left_transparent.gif"
                if self.speed_x < 0
                else "walking_right_transparent.gif"
            )
            print(
                f"Adjusting frames: {self.resource_name} (Pet X: {self.pet.x}) called from {called_from}"
            )

    def calculate_delta(self):
        bed_x = self.pet.bed_window.winfo_x()
        bed_y = self.pet.bed_window.winfo_y() - 20
        error_cap = 10
        if error_cap > sqrt((bed_x - self.pet.x) ** 2 + (bed_y - self.pet.y) ** 2):
            self.speed_x = 0
            self.speed_y = 0
            self.pet.x = bed_x
            self.pet.y = bed_y
        else:
            self.pet.x = (
                bed_x if abs(bed_x - self.pet.x) < error_cap // 2 else self.pet.x
            )
            self.pet.y = (
                bed_y if abs(bed_y - self.pet.y) < error_cap // 2 else self.pet.y
            )
            if self.pet.x < bed_x:
                self.speed_x = 3
            elif self.pet.x == bed_x:
                self.speed_x = 0
            else:
                self.speed_x = -3
            if self.pet.y < bed_y:
                self.speed_y = 3
            elif self.pet.y == bed_y:
                self.speed_y = 0
            else:
                self.speed_y = -3
        self.adjust_frames()
