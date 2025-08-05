from listerine import speech_to_text_english
from pet_animation import PetAnimation


class ListenAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="walking_left_transparent.gif",
            resource_length=8,
            animation_speed=1,
            animation_repeat=1,
        )

        self.message = None
        
        self.message = speech_to_text_english(2)
        


    def is_finished(self):
        print(f"Message: {self.message}")
        return self.message is not None
