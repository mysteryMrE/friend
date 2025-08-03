from abc import ABC, abstractmethod
import tkinter as tk


# Global cache to keep image references alive
_image_cache = {}


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
        self.imgpath = "D:\\Dokumentumok\\SCHOOL\\IT_PROJECTS\\pets\\assets\\images\\"
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

        # Use cache key to avoid loading the same images multiple times
        cache_key = f"{self.resource_name}_{self.resource_length}_{slow}_{self.animation_repeat}"

        if cache_key in _image_cache:
            print(f"Using cached frames for {cache_key}")
            return _image_cache[cache_key]

        print(f"Loading new frames for {cache_key}")
        raw_frames = []
        for i in range(self.resource_length):
            try:
                # Check if individual frame is already cached
                frame_key = f"{self.resource_name}_{i}"
                if frame_key in _image_cache:
                    frame = _image_cache[frame_key]
                else:
                    # Load each frame individually and store it
                    frame = tk.PhotoImage(
                        file=self.imgpath + self.resource_name,
                        format="gif -index %i" % (i),
                    )
                    # Keep a reference in the global cache to prevent garbage collection
                    _image_cache[frame_key] = frame

                raw_frames.append(frame)
            except tk.TclError as e:
                # This helps with debugging if a frame is missing
                print(f"Error loading frame {i} from {self.resource_name}: {e}")

        # Create the final frame list with speed adjustment
        frames = []
        for frame in raw_frames:
            for _ in range(slow):
                frames.append(frame)

        final_frames = frames * self.animation_repeat
        _image_cache[cache_key] = final_frames
        return final_frames

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

    def cleanup(self):
        """Clean up resources when animation state changes"""
        # This method can be overridden by subclasses if needed
        pass

    @staticmethod
    def clear_image_cache():
        """Clear the global image cache if memory becomes an issue"""
        global _image_cache
        _image_cache.clear()
