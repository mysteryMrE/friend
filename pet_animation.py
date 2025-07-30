from abc import ABC
import tkinter as tk


# TODO: not a clean thing to have abstract class without abstract methods, but it is to stop instantiation
class PetAnimation(ABC):
    def __init__(
        self,
        speed_x: int,
        speed_y: int,
        gif_name: str,
        gif_length: int,
        animation_speed: float,
        animation_repeat: int,
    ):
        self.cycle = 0
        self.imgpath = "D:\\Dokumentumok\\SCHOOL\\pets\\assets\\images\\"
        self.gif_name = gif_name
        self.gif_length = gif_length
        self.animation_speed = animation_speed
        self.animation_repeat = animation_repeat
        slow = round(1.0 / self.animation_speed)
        if slow < 1:
            slow = 1
        self.frames = [
            tk.PhotoImage(
                file=self.imgpath + gif_name + ".gif", format="gif -index %i" % (i)
            )
            for i in range(gif_length)
            for _ in range(slow)
        ] * animation_repeat
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update_animation(self):
        if self.is_finished():
            return self.frames[-1], True
        frame = self.frames[self.cycle % len(self.frames)]
        self.cycle += 1
        return frame, self.is_finished()

    def is_finished(self):
        return self.cycle >= len(self.frames)

    def get_movement_delta(self):
        return self.speed_x, self.speed_y
