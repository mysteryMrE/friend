from pet_animation import PetAnimation


class IdleState(PetAnimation):
    @property
    def gif_length(self):
        return 5

    @property
    def gif_name(self):
        return "idle"

    @property
    def animation_speed(self):
        return 2  # Speed of the idle animation

    @property
    def animation_repeat(self):
        return 1

    @property
    def speed_x(self):
        return 0

    @property
    def speed_y(self):
        return 0

    def update_animation(self):
        # 'idle' is the list of frames for this state
        frame = self.frames[self.cycle % len(self.frames)]
        self.cycle += 1
        return frame, self.cycle
