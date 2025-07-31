from abc import ABC, abstractmethod
import tkinter as tk


# TODO: not a clean thing to have abstract class without abstract methods, but it is to stop instantiation
class PetAnimation(ABC):
    def __init__(
        self,
        speed_x: int,
        speed_y: int,
        resource_name: str,
        resource_length: int,
        animation_speed: float,
        animation_repeat: int,
    ):
        self.cycle = 0
        self.imgpath = "D:\\Dokumentumok\\SCHOOL\\pets\\assets\\images\\"
        self.resource_name = resource_name
        self.resource_length = resource_length
        self.animation_speed = animation_speed
        self.animation_repeat = animation_repeat
        self.frames = self.make_frames()
        self.speed_x = speed_x
        self.speed_y = speed_y

    def make_frames(self):
        slow = round(1.0 / self.animation_speed)
        if slow < 1:
            slow = 1
        frames = [
            tk.PhotoImage(
                file=self.imgpath + self.resource_name, format="gif -index %i" % (i)
            )
            for i in range(self.resource_length)
            for _ in range(slow)
        ] * self.animation_repeat
        return frames

    def update_animation(self):
        if self.is_finished():
            return self.frames[-1], True, self.get_display_message()
        frame = self.frames[self.cycle % len(self.frames)]
        self.cycle += 1
        return frame, self.is_finished(), self.get_display_message()

    def is_finished(self):
        return self.cycle >= len(self.frames)

    def get_movement_delta(self):
        return self.speed_x, self.speed_y

    def get_display_message(self):
        return ""
