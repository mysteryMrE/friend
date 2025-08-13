from pet_animation import PetAnimation


class ComeBackAnimation(PetAnimation):
    def __init__(self, pet):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="idle_transparent.gif",
            resource_length=5,
            animation_speed=0.5,
            animation_repeat=1,
        )
        pet.x = pet.bed_window.winfo_x()
        pet.y = pet.bed_window.winfo_y() - 20
