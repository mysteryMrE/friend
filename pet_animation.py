from abc import ABC, abstractmethod
import tkinter as tk


class PetAnimation(ABC):
    def __init__(self, ERROR):  # LETS USE PARAMETERS INSTED OF PROPERTIES
        self.cycle = 0
        self.imgpath = "D:\\Dokumentumok\\SCHOOL\\pets\\assets\\images\\"
        self.frames = [
            tk.PhotoImage(
                file=self.imgpath + self.gif_name + ".gif", format="gif -index %i" % (i)
            )
            for i in range(self.gif_length)
            for _ in range(self.animation_speed)
        ] * self.animation_repeat

    @property
    @abstractmethod
    def gif_length(self):
        pass

    @property
    @abstractmethod
    def gif_name(self):
        pass

    @property
    @abstractmethod
    def animation_speed(self):
        pass

    @property
    @abstractmethod
    def animation_repeat(self):
        pass

    @property
    @abstractmethod
    def speed_x(self):
        pass

    @property
    @abstractmethod
    def speed_y(self):
        pass

    @abstractmethod
    def update_animation(self):
        # Return the current frame and update cycle/event_number for animation
        pass

    def is_finished(self):
        return self.cycle >= len(self.frames)

    def get_movement_delta(self):
        return self.speed_x, self.speed_y
